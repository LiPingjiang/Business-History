"""Siemens Careers Adapter
Siemens 全球站使用 Avature ATS (jobs.siemens.com)。
该平台是SPA，岗位数据通过前端JS异步加载，无公开REST API。
本adapter尝试从SSR HTML中提取岗位数据。

注意：jobs.siemens.com.cn（中国站）使用不同的系统。
"""
from __future__ import annotations
from typing import List
import re
import json

from adapters.base import BaseAdapter
from models import Job
from config import CompanyConfig


class SiemensAdapter(BaseAdapter):
    """
    西门子招聘 (Avature ATS)。
    全球站 jobs.siemens.com 是SPA，需要浏览器渲染。
    中国站 jobs.siemens.com.cn 可能有独立API。
    """

    name = "siemens"

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        # 尝试中国站API
        china_apis = [
            "https://jobs.siemens.com.cn/api/position/list",
            "https://jobs.siemens.com.cn/siemens/position/queryPositionList",
            "https://jobs.siemens.com.cn/api/jobs/search",
        ]

        for api_url in china_apis:
            try:
                payload = {
                    "pageIndex": 1,
                    "pageSize": 50,
                    "recruitmentType": "SOCIALRECRUITMENT",
                    "keyword": "data",
                    "workCity": "北京",
                }
                resp = self.client.post(api_url, json=payload, headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                })
                if resp.status_code == 200 and "json" in resp.headers.get("content-type", ""):
                    data = resp.json()
                    jobs = self._parse_china_response(data, company)
                    if jobs:
                        return jobs
            except Exception:
                continue

        # 尝试全球站 Avature
        global_url = "https://jobs.siemens.com/careers?query=data&location=Beijing&pid=563156119869066&domain=siemens.com&sort_by=relevance"
        try:
            resp = self.client.get(global_url, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            })
            if resp.status_code == 200:
                jobs = self._parse_avature_html(resp.text, company)
                if jobs:
                    return jobs
        except Exception:
            pass

        raise RuntimeError(
            "Siemens (Avature ATS) SPA平台，中国站API返回404，"
            "全球站需要浏览器渲染加载岗位数据。"
        )

    def _parse_china_response(self, data: dict, company: CompanyConfig) -> List[Job]:
        """解析中国站API响应"""
        jobs = []
        records = data.get("data", {}).get("list", []) or data.get("data", {}).get("records", []) or []
        for item in records:
            if isinstance(item, dict):
                title = item.get("positionName", "") or item.get("name", "")
                loc = item.get("workCity", "") or item.get("city", "")
                job_id = str(item.get("id", "") or item.get("positionId", ""))
                dept = item.get("departmentName", "")
                jobs.append(Job(
                    title=title,
                    company=company.name,
                    location=loc,
                    job_id=job_id,
                    url=f"https://jobs.siemens.com.cn/siemens/position/detail/{job_id}" if job_id else "",
                    tags=[dept] if dept else [],
                    source_adapter=self.name,
                ))
        return jobs

    def _parse_avature_html(self, html: str, company: CompanyConfig) -> List[Job]:
        """尝试从Avature SSR HTML中提取岗位"""
        # Avature 有时在HTML中嵌入JSON数据
        patterns = [
            r'window\.__PRELOADED_STATE__\s*=\s*(\{.*?\});',
            r'"jobResults"\s*:\s*(\[.*?\])',
            r'data-ph-at-job-title-text="([^"]+)"',
        ]

        jobs = []
        # 尝试提取job title属性
        titles = re.findall(r'data-ph-at-job-title-text="([^"]+)"', html)
        links = re.findall(r'data-ph-at-job-title-url="([^"]+)"', html)

        for i, title in enumerate(titles):
            url = links[i] if i < len(links) else ""
            if not url.startswith("http"):
                url = f"https://jobs.siemens.com{url}"
            jobs.append(Job(
                title=title,
                company=company.name,
                url=url,
                source_adapter=self.name,
            ))

        return jobs

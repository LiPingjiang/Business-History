"""BMW/领悦 tupu360 Adapter
tupu360.com 是国内ATS平台，类似北森。
API路径需要探测。
"""
from __future__ import annotations
from typing import List

from adapters.base import BaseAdapter
from models import Job
from config import CompanyConfig


class BmwAdapter(BaseAdapter):
    """
    BMW中国招聘 (tupu360.com ATS)。
    尝试多种API路径。
    """

    name = "bmw"

    API_PATHS = [
        "/bmw/position/queryPositionList",
        "/bmw/zpPosition/queryPositionList",
        "/api/position/list",
        "/bmw/api/position/list",
    ]

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        base_host = "https://careersite.tupu360.com"

        for api_path in self.API_PATHS:
            api_url = f"{base_host}{api_path}"
            try:
                payload = {
                    "pageIndex": 1,
                    "pageSize": 50,
                    "recruitmentType": company.params.get("recruitmentType", "SOCIALRECRUITMENT"),
                    "keyword": "",
                    "workCity": "北京",
                }
                resp = self.client.post(api_url, json=payload, headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Referer": f"{base_host}/bmw/position/index",
                })
                if resp.status_code == 200 and "json" in resp.headers.get("content-type", ""):
                    data = resp.json()
                    jobs = self._parse_response(data, company)
                    if jobs:
                        return jobs
            except Exception:
                continue

        # 尝试GET方式
        try:
            resp = self.client.get(
                f"{base_host}/bmw/position/index",
                headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"},
            )
            if resp.status_code == 200:
                import re
                import json
                # 尝试从HTML中提取数据
                match = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});', resp.text, re.DOTALL)
                if match:
                    data = json.loads(match.group(1))
                    jobs = self._parse_response(data, company)
                    if jobs:
                        return jobs
        except Exception:
            pass

        raise RuntimeError(
            "BMW/领悦 (tupu360.com) API路径返回404，"
            "可能需要浏览器渲染或更新API路径。"
        )

    def _parse_response(self, data: dict, company: CompanyConfig) -> List[Job]:
        """解析响应"""
        jobs = []
        records = []
        if isinstance(data, dict):
            for key in ["data", "result", "content"]:
                val = data.get(key)
                if isinstance(val, list):
                    records = val
                    break
                if isinstance(val, dict):
                    for subkey in ["list", "records", "items"]:
                        subval = val.get(subkey)
                        if isinstance(subval, list):
                            records = subval
                            break
                    if records:
                        break

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
                    url=f"https://careersite.tupu360.com/bmw/position/detail/{job_id}" if job_id else "",
                    tags=[dept] if dept else [],
                    source_adapter=self.name,
                ))
        return jobs

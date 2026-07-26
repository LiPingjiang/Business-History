"""北森 zhiye.com Playwright Adapter — 覆盖SPA站点"""
from __future__ import annotations
from typing import List
import json
import re
import time

from adapters.playwright_base import PlaywrightAdapter
from models import Job
from config import CompanyConfig


class ZhiyePlaywrightAdapter(PlaywrightAdapter):
    """
    北森 zhiye.com 使用Playwright渲染SPA页面，
    拦截XHR请求获取岗位数据。
    """

    name = "zhiye_pw"

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        base_url = company.url.rstrip("/")
        page = self._new_page()
        jobs = []
        api_responses = []

        # 拦截API请求
        def handle_response(response):
            url = response.url
            if any(kw in url for kw in ["position", "recruit", "Position", "Recruit"]):
                try:
                    if "json" in response.headers.get("content-type", ""):
                        api_responses.append(response.json())
                except Exception:
                    pass

        page.on("response", handle_response)

        try:
            # 访问社招页面
            page.goto(f"{base_url}/Social", wait_until="networkidle", timeout=30000)
            time.sleep(2)

            # 如果有API响应，解析岗位
            for data in api_responses:
                records = self._extract_records(data)
                for item in records:
                    job = self._parse_job(item, company, base_url)
                    if job.title:
                        jobs.append(job)

            # 如果没有API响应，尝试从DOM提取
            if not jobs:
                jobs = self._extract_from_dom(page, company, base_url)

        finally:
            page.close()

        return jobs

    def _extract_records(self, data) -> list:
        """从各种JSON结构中提取岗位列表"""
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for key in ["data", "result", "content", "body"]:
                val = data.get(key)
                if isinstance(val, list) and len(val) > 0:
                    return val
                if isinstance(val, dict):
                    for subkey in ["list", "records", "items", "positions"]:
                        subval = val.get(subkey)
                        if isinstance(subval, list) and len(subval) > 0:
                            return subval
        return []

    def _parse_job(self, item: dict, company: CompanyConfig, base_url: str) -> Job:
        title = item.get("positionName", "") or item.get("name", "") or item.get("title", "")
        loc = item.get("workCity", "") or item.get("city", "") or item.get("location", "")
        job_id = str(item.get("id", "") or item.get("positionId", ""))
        dept = item.get("departmentName", "") or item.get("dept", "")
        return Job(
            title=title,
            company=company.name,
            location=loc,
            job_id=job_id,
            url=f"{base_url}/Social/position/{job_id}" if job_id else "",
            tags=[dept] if dept else [],
            source_adapter=self.name,
        )

    def _extract_from_dom(self, page, company: CompanyConfig, base_url: str) -> List[Job]:
        """从DOM中提取岗位信息"""
        jobs = []
        # 常见的岗位列表选择器
        selectors = [
            ".position-item", ".job-item", ".recruit-item",
            "[class*='position']", "[class*='job-list'] li",
            ".list-item", ".card-item",
        ]
        for selector in selectors:
            elements = page.query_selector_all(selector)
            if elements:
                for el in elements[:50]:
                    title_el = el.query_selector("h3, h4, .title, .name, [class*='title'], [class*='name']")
                    loc_el = el.query_selector("[class*='city'], [class*='location'], [class*='address']")
                    title = title_el.inner_text().strip() if title_el else ""
                    loc = loc_el.inner_text().strip() if loc_el else ""
                    if title:
                        jobs.append(Job(
                            title=title,
                            company=company.name,
                            location=loc,
                            source_adapter=self.name,
                        ))
                if jobs:
                    break
        return jobs

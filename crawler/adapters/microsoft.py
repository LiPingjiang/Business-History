"""Microsoft Careers Adapter
Microsoft 已迁移到 Eightfold.ai 平台 (apply.careers.microsoft.com)。
该平台是SPA，岗位数据通过前端JS异步加载。
本adapter尝试已知的Eightfold API路径。
"""
from __future__ import annotations
from typing import List

from adapters.base import BaseAdapter
from models import Job
from config import CompanyConfig


class MicrosoftAdapter(BaseAdapter):
    """
    Microsoft Careers (Eightfold.ai 平台)。
    已知API: POST https://apply.careers.microsoft.com/api/v1/jobs/search
    需要 _csrf token 和特定headers。
    """

    name = "microsoft"

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        import re

        # 第一步：访问主页获取 _csrf token
        main_url = "https://apply.careers.microsoft.com/careers"
        resp = self.client.get(main_url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        })

        csrf_token = ""
        csrf_match = re.search(r'name="_csrf"\s+content="([^"]+)"', resp.text)
        if csrf_match:
            csrf_token = csrf_match.group(1)

        # 第二步：尝试Eightfold搜索API
        api_urls = [
            "https://apply.careers.microsoft.com/api/v1/jobs/search",
            "https://apply.careers.microsoft.com/api/jobs",
            "https://apply.careers.microsoft.com/careers/api/jobs/search",
        ]

        for api_url in api_urls:
            try:
                payload = {
                    "query": "data engineer",
                    "location": "Beijing, China",
                    "page": 1,
                    "pageSize": 20,
                    "filters": {
                        "experience": ["Experienced"],
                    },
                }
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": main_url,
                }
                if csrf_token:
                    headers["X-CSRF-Token"] = csrf_token

                resp = self.client.post(api_url, json=payload, headers=headers)
                if resp.status_code == 200 and "json" in resp.headers.get("content-type", ""):
                    data = resp.json()
                    jobs = self._parse_response(data, company)
                    if jobs:
                        return jobs
            except Exception:
                continue

        # 如果API都失败，标记为需要浏览器
        raise RuntimeError(
            "Microsoft Careers (Eightfold.ai) SPA平台，"
            "需要浏览器渲染或找到正确的API endpoint。"
        )

    def _parse_response(self, data: dict, company: CompanyConfig) -> List[Job]:
        """解析Eightfold API响应"""
        jobs = []
        # Eightfold 常见响应格式
        positions = (
            data.get("positions", [])
            or data.get("jobs", [])
            or data.get("results", [])
            or data.get("data", {}).get("jobs", [])
        )

        for item in positions:
            if isinstance(item, dict):
                title = item.get("name", "") or item.get("title", "")
                loc = item.get("location", "") or item.get("locations", [""])[0] if item.get("locations") else ""
                job_id = str(item.get("id", "") or item.get("jobId", ""))
                posted = item.get("postedDate", "") or item.get("datePosted", "")

                jobs.append(Job(
                    title=title,
                    company=company.name,
                    location=loc if isinstance(loc, str) else str(loc),
                    job_id=job_id,
                    url=f"https://jobs.careers.microsoft.com/global/en/job/{job_id}" if job_id else "",
                    posted_date=posted,
                    source_adapter=self.name,
                ))
        return jobs

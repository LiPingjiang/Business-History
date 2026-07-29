"""Jibe (Google Cloud Talent Solution) Adapter — AMD, Schneider Electric 等"""
from __future__ import annotations
from typing import List

from adapters.base import BaseAdapter
from models import Job
from config import CompanyConfig


class JibeAdapter(BaseAdapter):
    """
    Jibe 招聘平台通用爬取器。
    API: GET {base_url}/api/jobs?page=1&location={location}&limit={limit}
    返回 JSON: {"jobs": [{"data": {"slug", "title", "city", "state", "country", ...}}]}
    """

    name = "jibe"

    def __init__(self):
        import httpx
        from config import REQUEST_TIMEOUT
        # Jibe API 对 Accept-Language: zh-CN 会过滤掉英文岗位，必须用 en-US
        self.client = httpx.Client(
            timeout=REQUEST_TIMEOUT,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            },
            follow_redirects=True,
        )

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        base_url = company.url.rstrip("/")
        location = company.params.get("location", "Beijing")
        limit = company.params.get("limit", 20)

        api_url = f"{base_url}/api/jobs"
        params = {"page": 1, "location": location, "limit": limit}

        resp = self.client.get(api_url, params=params)
        resp.raise_for_status()
        data = resp.json()

        jobs = []
        for item in data.get("jobs", []):
            d = item.get("data", {})
            title = d.get("title", "")
            city = d.get("city", "")
            state = d.get("state", "")
            country = d.get("country", "")
            loc = ", ".join(filter(None, [city, state, country]))
            slug = d.get("slug", "")
            req_id = d.get("req_id", slug)
            posted = d.get("posted_date", d.get("update_date", ""))
            job_url = f"{base_url}/careers-home/jobs/{slug}" if slug else ""

            jobs.append(Job(
                title=title,
                company=company.name,
                location=loc,
                job_id=req_id,
                url=job_url,
                posted_date=posted,
                source_adapter=self.name,
            ))

        return jobs

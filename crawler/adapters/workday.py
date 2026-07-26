"""Workday ATS Adapter — 覆盖18家企业"""
from __future__ import annotations
from typing import List

from adapters.base import BaseAdapter
from models import Job
from config import CompanyConfig


class WorkdayAdapter(BaseAdapter):
    """
    Workday 招聘系统通用爬取器。
    所有 *.myworkdayjobs.com 站点共享同一套 API 格式。
    API: POST {base_url}/wday/cxs/{tenant}/jobs
    """

    name = "workday"

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        url = company.url
        # 从URL提取tenant和site信息
        # 格式: https://{company}.wd{n}.myworkdayjobs.com/{site}
        parts = url.rstrip("/").split("/")
        site = parts[-1] if len(parts) > 3 else "jobs"
        host = parts[2]  # e.g. nvidia.wd5.myworkdayjobs.com
        tenant = host.split(".")[0]  # e.g. nvidia

        api_url = f"https://{host}/wday/cxs/{tenant}/{site}/jobs"

        location = company.params.get("location", "China")
        payload = {
            "appliedFacets": {},
            "limit": 20,
            "offset": 0,
            "searchText": f"{location} data",
        }

        resp = self.client.post(api_url, json=payload)
        resp.raise_for_status()
        data = resp.json()

        jobs = []
        for item in data.get("jobPostings", []):
            title = item.get("title", "")
            loc = item.get("locationsText", "")
            posted = item.get("postedOn", "")
            job_id = item.get("bulletFields", [""])[0] if item.get("bulletFields") else ""
            external_path = item.get("externalPath", "")
            job_url = f"https://{host}{external_path}" if external_path else ""

            jobs.append(Job(
                title=title,
                company=company.name,
                location=loc,
                job_id=job_id,
                url=job_url,
                posted_date=posted,
                source_adapter=self.name,
            ))

        return jobs

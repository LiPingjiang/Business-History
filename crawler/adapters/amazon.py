"""Amazon Jobs Adapter"""
from __future__ import annotations
from typing import List

from adapters.base import BaseAdapter
from models import Job
from config import CompanyConfig


class AmazonAdapter(BaseAdapter):
    """
    Amazon Jobs 公开 REST API。
    GET https://www.amazon.jobs/en/search.json?base_query=...&loc_query=...
    """

    name = "amazon"

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        params = {
            "base_query": company.params.get("base_query", "data engineer"),
            "loc_query": company.params.get("loc_query", "Beijing, China"),
            "result_limit": 50,
            "sort": "recent",
            "cache": "",
        }

        resp = self.client.get("https://www.amazon.jobs/en/search.json", params=params)
        resp.raise_for_status()
        data = resp.json()

        jobs = []
        for item in data.get("jobs", []):
            jobs.append(Job(
                title=item.get("title", ""),
                company=company.name,
                location=item.get("normalized_location", "") or item.get("location", ""),
                job_id=item.get("id_icims", "") or item.get("id", ""),
                url=f"https://www.amazon.jobs{item['job_path']}" if item.get("job_path") else "",
                posted_date=item.get("posted_date", ""),
                source_adapter=self.name,
            ))

        return jobs

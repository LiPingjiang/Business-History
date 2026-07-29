"""Phenom People Adapter — ABB 等"""
from __future__ import annotations
from typing import List

from adapters.base import BaseAdapter
from models import Job
from config import CompanyConfig


class PhenomAdapter(BaseAdapter):
    """
    Phenom People 招聘平台通用爬取器。
    API: POST {base_url}/widgets
    请求体包含搜索参数，返回 JSON: {"refineSearch": {"totalHits": N, "data": {"jobs": [...]}}}
    """

    name = "phenom"

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        base_url = company.url.rstrip("/")
        location = company.params.get("location", "Beijing")
        country_code = company.params.get("country_code", "cn")
        keyword = company.params.get("keyword", "")
        size = company.params.get("limit", 20)

        api_url = f"{base_url}/widgets"
        payload = {
            "lang": "en_global",
            "deviceType": "desktop",
            "country": "global",
            "pageName": "search-results",
            "ddoKey": "refineSearch",
            "sortBy": "",
            "subsidiary": "",
            "from": 0,
            "jobs": True,
            "counts": True,
            "all_fields": ["category", "country", "state", "city", "type", "experience", "subsidiary"],
            "size": size,
            "clearAll": False,
            "jdsource": "facets",
            "isSlider": False,
            "keyword": keyword,
            "location": location,
            "f_country": [country_code],
        }

        resp = self.client.post(api_url, json=payload)
        resp.raise_for_status()
        data = resp.json()

        refine = data.get("refineSearch", {})
        job_list = refine.get("data", {}).get("jobs", [])

        jobs = []
        for item in job_list:
            title = item.get("title", "")
            city = item.get("city", "")
            country = item.get("country", "")
            loc = ", ".join(filter(None, [city, country]))
            job_id = item.get("reqId", item.get("jobId", ""))
            posted = item.get("postedDate", "")
            slug = item.get("jobSeqNo", "")
            job_url = f"{base_url}/global/en/job/{slug}" if slug else ""

            jobs.append(Job(
                title=title,
                company=company.name,
                location=loc,
                job_id=str(job_id),
                url=job_url,
                posted_date=posted,
                source_adapter=self.name,
            ))

        return jobs

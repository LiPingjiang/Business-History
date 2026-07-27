"""SmartRecruiters ATS Adapter"""
from __future__ import annotations
from typing import List

from adapters.base import BaseAdapter
from models import Job
from config import CompanyConfig


class SmartRecruitersAdapter(BaseAdapter):
    """
    SmartRecruiters 公开 API:
    GET https://api.smartrecruiters.com/v1/companies/{company_id}/postings?q=...&country=cn&limit=100
    返回 JSON: {totalFound, content: [{id, name, location:{city,country}, ...}]}
    """

    name = "smartrecruiters"

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        company_id = company.params.get("company_id", "")
        query = company.params.get("query", "data")
        country = company.params.get("country", "cn")
        limit = company.params.get("limit", 100)

        url = f"https://api.smartrecruiters.com/v1/companies/{company_id}/postings"
        params = {"q": query, "country": country, "limit": limit, "offset": 0}

        all_jobs = []
        while True:
            resp = self.client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

            for item in data.get("content", []):
                loc = item.get("location", {})
                city = loc.get("city", "")
                country_name = loc.get("country", "")
                location_text = f"{city}, {country_name}" if city else country_name

                job_url = f"https://jobs.smartrecruiters.com/{company_id}/{item['id']}"

                all_jobs.append(Job(
                    title=item.get("name", ""),
                    company=company.name,
                    location=location_text,
                    job_id=str(item.get("id", "")),
                    url=job_url,
                    source_adapter=self.name,
                ))

            # Pagination
            total = data.get("totalFound", 0)
            params["offset"] += limit
            if params["offset"] >= total:
                break

        return all_jobs

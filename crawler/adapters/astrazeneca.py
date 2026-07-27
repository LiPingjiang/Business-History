"""AstraZeneca (TalentBrew ATS) Adapter"""
from __future__ import annotations
from typing import List
import re
import html as htmlmod

from adapters.base import BaseAdapter
from models import Job
from config import CompanyConfig


class AstraZenecaAdapter(BaseAdapter):
    """
    AstraZeneca 使用 TalentBrew ATS。
    API: GET https://careers.astrazeneca.com/search-jobs/results?...
    返回JSON，其中 results 字段是HTML片段，可解析岗位列表。
    """

    name = "astrazeneca"

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        keywords = company.params.get("keywords", "data")
        location = company.params.get("location", "Beijing, China")

        params = {
            "ActiveFacetID": "0",
            "CurrentPage": "1",
            "RecordsPerPage": "50",
            "Distance": "50",
            "RadiusUnitType": "0",
            "Keywords": keywords,
            "Location": location,
            "ShowRadius": "False",
            "IsPag498": "False",
            "CustomFacetName": "",
            "FacetTerm": "",
            "FacetType": "0",
            "SearchResultsModuleName": "Search Results",
            "SearchFiltersModuleName": "Search Filters",
            "SortCriteria": "0",
            "SortDirection": "0",
            "SearchType": "5",
            "PostalCode": "",
            "fc": "",
            "fl": "",
            "fcf": "",
            "afc": "",
            "afl": "",
            "afcf": "",
        }

        resp = self.client.get(
            "https://careers.astrazeneca.com/search-jobs/results",
            params=params,
        )
        resp.raise_for_status()
        data = resp.json()

        html_str = data.get("results", "")
        jobs = []

        # 解析HTML片段中的岗位
        # 格式: <a ... href="/job/location/title/7684/id" data-job-id="xxx" ...>
        #          <h2>Title</h2>
        #          <span class="job-location">Location</span>
        pattern = r'<a[^>]*href="(/job/[^"]+)"[^>]*data-job-id="(\d+)"[^>]*>.*?<h2>(.*?)</h2>.*?<span class="job-location">\s*(.*?)\s*</span>'
        matches = re.findall(pattern, html_str, re.DOTALL)

        for path, job_id, title, location_text in matches:
            title_clean = htmlmod.unescape(re.sub(r'<[^>]+>', '', title).strip())
            loc_clean = htmlmod.unescape(location_text.strip())
            url = f"https://careers.astrazeneca.com{path}"

            jobs.append(Job(
                title=title_clean,
                company=company.name,
                location=loc_clean,
                job_id=job_id,
                url=url,
                source_adapter=self.name,
            ))

        return jobs

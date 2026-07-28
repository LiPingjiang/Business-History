"""民生银行招聘 (career.cmbc.com.cn) Adapter
北森求贤平台，使用 form-urlencoded POST + SF_cookie 认证。
"""
from __future__ import annotations
from typing import List

from adapters.base import BaseAdapter
from models import Job
from config import CompanyConfig


class CmbcAdapter(BaseAdapter):
    """
    民生银行社招爬取器。
    API: POST https://career.cmbc.com.cn/portal/rest/careerrecruitment/search.view
    Content-Type: application/x-www-form-urlencoded
    需要先 GET 首页获取 SF_cookie_156 cookie。
    """

    name = "cmbc"
    BASE_URL = "https://career.cmbc.com.cn"
    SEARCH_URL = f"{BASE_URL}/portal/rest/careerrecruitment/search.view"

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        # Step 1: GET homepage to obtain session cookies (SF_cookie_156)
        self.client.get(self.BASE_URL)
        sf_cookie = self.client.cookies.get("SF_cookie_156", "")

        all_jobs = []
        page = 1
        max_pages = 30

        while page <= max_pages:
            form_data = (
                f"searchRecruitmentIds=social"
                f"&view=careerRecruitmentList"
                f"&pageNo={page}"
                f"&pageSize=20"
                f"&SF_cookie_156={sf_cookie}"
            )
            resp = self.client.post(
                self.SEARCH_URL,
                content=form_data,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                },
            )
            resp.raise_for_status()
            data = resp.json()
            if not data.get("success"):
                break

            items = data.get("data", {}).get("items", [])
            if not items:
                break

            for item in items:
                title = item.get("careerRecruitment_career_name", "")
                location = item.get("careerRecruitment_regions_name", "")
                dept = item.get("careerRecruitment_career_enterprise_name", "")
                job_family = item.get("careerRecruitment_career_jobFamily_name", "")
                publish_date = item.get("careerRecruitment_career_publishDate", "")[:10]
                job_id = item.get("id", "")
                job_url = f"{self.BASE_URL}/#/app/recruitmentview/{job_id}"

                all_jobs.append(Job(
                    title=title,
                    location=location,
                    url=job_url,
                    company=company.name,
                    tags=[dept, job_family, publish_date],
                ))

            page_count = data.get("data", {}).get("pageCount", 0)
            if page >= page_count:
                break
            page += 1

        return all_jobs

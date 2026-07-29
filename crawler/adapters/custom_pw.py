"""Custom Playwright adapter for央企 portals with unique SPA structures."""
from __future__ import annotations
from typing import List
import time

from adapters.playwright_base import PlaywrightAdapter
from models import Job
from config import CompanyConfig


class CustomPlaywrightAdapter(PlaywrightAdapter):
    """
    Generic Playwright adapter for custom央企 recruitment portals
    (中国石化 job.sinopec.com, 中国华能, 南方电网, 大唐).
    Intercepts XHR/fetch API responses and falls back to DOM extraction.
    """

    name = "custom_pw"

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        base_url = company.url.rstrip("/")
        page = self._new_page()
        jobs = []
        api_responses = []

        def handle_response(response):
            url = response.url
            keywords = ["position", "recruit", "job", "social", "list",
                        "Position", "Recruit", "Job", "Social", "List"]
            if any(kw in url for kw in keywords):
                try:
                    ct = response.headers.get("content-type", "")
                    if "json" in ct:
                        api_responses.append(response.json())
                except Exception:
                    pass

        page.on("response", handle_response)

        try:
            social_urls = [
                f"{base_url}/#/social/index",
                f"{base_url}/social",
                f"{base_url}/#/social",
                base_url,
            ]
            for url in social_urls:
                try:
                    page.goto(url, wait_until="networkidle", timeout=20000)
                    time.sleep(2)
                    if api_responses:
                        break
                except Exception:
                    continue

            for data in api_responses:
                records = self._extract_records(data)
                for item in records:
                    job = self._parse_job(item, company)
                    if job.title:
                        jobs.append(job)

            if not jobs:
                jobs = self._extract_from_dom(page, company)

        finally:
            page.close()

        return jobs

    def _extract_records(self, data) -> list:
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for key in ["data", "result", "content", "body", "rows", "records"]:
                val = data.get(key)
                if isinstance(val, list) and len(val) > 0:
                    return val
                if isinstance(val, dict):
                    for subkey in ["list", "records", "items", "rows",
                                   "positionList", "positions", "content"]:
                        subval = val.get(subkey)
                        if isinstance(subval, list) and len(subval) > 0:
                            return subval
                    for subkey in ["data"]:
                        subval = val.get(subkey)
                        if isinstance(subval, dict):
                            for k3 in ["list", "records", "rows"]:
                                v3 = subval.get(k3)
                                if isinstance(v3, list) and len(v3) > 0:
                                    return v3
        return []

    def _parse_job(self, item: dict, company: CompanyConfig) -> Job:
        title = (item.get("positionName", "") or item.get("name", "")
                 or item.get("title", "") or item.get("jobName", "")
                 or item.get("recruitTitle", ""))
        loc = (item.get("workCity", "") or item.get("city", "")
               or item.get("location", "") or item.get("workPlace", "")
               or item.get("workplace", ""))
        job_id = str(item.get("id", "") or item.get("positionId", "")
                     or item.get("jobId", ""))
        dept = (item.get("departmentName", "") or item.get("dept", "")
                or item.get("orgName", "") or item.get("companyName", ""))
        publish_date = (item.get("publishDate", "") or item.get("createTime", "")
                        or item.get("publishTime", ""))
        return Job(
            title=title,
            company=company.name,
            location=loc,
            job_id=job_id,
            posted_date=publish_date,
            tags=[dept] if dept else [],
            source_adapter=self.name,
        )

    def _extract_from_dom(self, page, company: CompanyConfig) -> List[Job]:
        jobs = []
        selectors = [
            ".position-item", ".job-item", ".recruit-item",
            "[class*='position']", "[class*='job'] li",
            ".list-item", ".el-table__row", "tr[class*='row']",
            ".card", ".item",
        ]
        for selector in selectors:
            try:
                elements = page.query_selector_all(selector)
            except Exception:
                continue
            if elements:
                for el in elements[:50]:
                    title_el = el.query_selector(
                        "h3, h4, .title, .name, [class*='title'], "
                        "[class*='name'], td:first-child, a"
                    )
                    loc_el = el.query_selector(
                        "[class*='city'], [class*='location'], "
                        "[class*='address'], [class*='place']"
                    )
                    title = title_el.inner_text().strip() if title_el else ""
                    loc = loc_el.inner_text().strip() if loc_el else ""
                    if title and len(title) > 2:
                        jobs.append(Job(
                            title=title,
                            company=company.name,
                            location=loc,
                            source_adapter=self.name,
                        ))
                if jobs:
                    break
        return jobs

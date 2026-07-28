"""Moka HR (app.mokahr.com) Adapter
从页面内嵌的 init-data hidden input 中提取职位列表，纯HTTP无需浏览器。
"""
from __future__ import annotations
from typing import List
import html as html_mod
import json

from adapters.base import BaseAdapter
from models import Job
from config import CompanyConfig


class MokahrAdapter(BaseAdapter):
    """
    Moka HR 招聘官网爬取器。
    职位数据嵌入在页面 <input id="init-data" type="hidden" value="..."> 中。
    URL格式: https://app.mokahr.com/social-recruitment/{org_id}/{site_id}
    """

    name = "mokahr"

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        url = company.url.rstrip("/")
        resp = self.client.get(url, headers={
            "Accept": "text/html",
        })
        resp.raise_for_status()
        text = resp.text

        # 从 hidden input 提取 JSON
        marker = 'id="init-data"'
        idx = text.find(marker)
        if idx < 0:
            raise ValueError("init-data input not found in page")

        val_start = text.find('value="', idx) + 7
        val_end = text.find('">', val_start)
        if val_start < 7 or val_end < 0:
            raise ValueError("Cannot parse init-data value")

        raw = html_mod.unescape(text[val_start:val_end])
        data = json.loads(raw)

        jobs = []
        for item in data.get("jobs", []):
            title = item.get("title", "")
            location = ""
            loc_info = item.get("location") or {}
            if isinstance(loc_info, dict):
                parts = [loc_info.get("country", ""), loc_info.get("address", "")]
                location = " ".join(p for p in parts if p)

            dept = ""
            dept_info = item.get("department") or {}
            if isinstance(dept_info, dict):
                dept = dept_info.get("name", "")

            job_url = f"{url}#/job/{item.get('id', '')}"

            jobs.append(Job(
                title=title,
                location=location,
                url=job_url,
                company=company.name,
                tags=[dept] if dept else [],
            ))

        return jobs

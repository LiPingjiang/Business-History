"""中信银行招聘 (job.citicbank.com) Adapter
使用其公开的 recruitportal API 获取社招岗位列表。
"""
from __future__ import annotations
from typing import List

from adapters.base import BaseAdapter
from models import Job
from config import CompanyConfig


class CiticbankAdapter(BaseAdapter):
    """
    中信银行社招爬取器。
    API: POST https://job.citicbank.com/recruitportal/portal/recruitQuery
    请求体: {RELEASENAME, recruitmentType, workAddr, deptCode, page}
    workAddr 使用省份代码列表，如 ['110000'] 表示北京。
    """

    name = "citicbank"
    BASE_URL = "https://job.citicbank.com/recruitportal/portal/recruitQuery"

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        work_addr = company.params.get("workAddr", [])
        keyword = company.params.get("keyword", "")
        all_jobs = []
        page = 1
        max_pages = 20  # 安全上限

        while page <= max_pages:
            payload = {
                "RELEASENAME": keyword,
                "recruitmentType": "01",  # 01=社招
                "workAddr": work_addr,
                "deptCode": [],
                "page": page,
            }
            resp = self.client.post(
                self.BASE_URL,
                json=payload,
                headers={"Content-Type": "application/json;charset=UTF-8"},
            )
            resp.raise_for_status()
            data = resp.json()
            rows = data.get("tableData", {}).get("rows", [])
            if not rows:
                break

            for row in rows:
                item = row.get("itemMap", {})
                title = item.get("RELEASENAME", "")
                location = item.get("WORKADDR", "")
                dept = item.get("CONTENT", "")  # 所属机构
                post_date = item.get("FBZWDATE", "")
                job_id = item.get("ID", "")
                job_url = f"https://job.citicbank.com/CustStyle/zpmhys/clubRecruit.html#/detail/{job_id}"

                all_jobs.append(Job(
                    title=title,
                    location=location,
                    url=job_url,
                    company=company.name,
                    tags=[dept, post_date] if dept else [post_date],
                ))

            # 每页固定15条，不足15条说明是最后一页
            if len(rows) < 15:
                break
            page += 1

        return all_jobs

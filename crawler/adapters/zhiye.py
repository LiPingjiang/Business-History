"""北森 zhiye.com Adapter — 覆盖7家企业
发现真实API: /api/Jobad/GetJobAdPageList (POST, JSON)
纯HTTP即可，不需要Playwright！
"""
from __future__ import annotations
from typing import List

from adapters.base import BaseAdapter
from models import Job
from config import CompanyConfig


class ZhiyeAdapter(BaseAdapter):
    """
    北森 zhiye.com 招聘系统爬取器。
    真实API: POST {base_url}/api/Jobad/GetJobAdPageList
    参数: {"pageIndex": 1, "pageSize": 50, "category": 1}
    category=1 表示社招
    """

    name = "zhiye"

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        base_url = company.url.rstrip("/")

        # 北森真实API
        api_url = f"{base_url}/api/Jobad/GetJobAdPageList"
        payload = {
            "pageIndex": 1,
            "pageSize": 50,
            # 不传category获取全部岗位（部分站点category=1返回空Data）
        }

        resp = self.client.post(api_url, json=payload, headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        })
        resp.raise_for_status()
        data = resp.json()

        jobs = []
        # 响应格式: {"Code": 200, "Count": N, "Data": [...]}
        records = data.get("Data", [])
        if not isinstance(records, list):
            records = []

        for item in records:
            if isinstance(item, dict):
                title = item.get("JobAdName", "") or item.get("positionName", "")
                loc_names = item.get("LocNames", [])
                loc = ", ".join(loc_names) if loc_names else ""
                job_id = item.get("Id", "") or str(item.get("JobAdId", ""))
                dept = item.get("Org", "") or ""

                # 过滤：只保留有标题的
                if title:
                    jobs.append(Job(
                        title=title,
                        company=company.name,
                        location=loc,
                        job_id=str(job_id),
                        url=f"{base_url}/Social/jobDetail/{job_id}" if job_id else "",
                        tags=[dept] if dept else [],
                        source_adapter=self.name,
                    ))

        return jobs

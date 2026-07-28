"""北森 zhiye.com Adapter — 支持分页
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
    参数: {"pageIndex": 1, "pageSize": 50}
    支持自动分页，最多10页（500条）防止无限循环。
    """

    name = "zhiye"
    MAX_PAGES = 20
    PAGE_SIZE = 20  # 部分站点（如北京银行）服务端强制cap到20，用20保证兼容

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        base_url = company.url.rstrip("/")
        # 去掉可能的 /Social 后缀
        if base_url.endswith("/Social"):
            base_url = base_url[:-7]

        api_url = f"{base_url}/api/Jobad/GetJobAdPageList"
        jobs = []

        # 北森API有两种分页模式：部分站点pageIndex从0开始，部分从1开始
        # 先尝试pageIndex=1，如果返回空Data但Count>0，则切换到pageIndex=0
        start_page = 1
        test_resp = self._try_fetch(api_url, 1)
        if test_resp and test_resp.get("Count", 0) > 0 and not test_resp.get("Data"):
            start_page = 0  # 0-based indexing

        page = start_page

        while page < start_page + self.MAX_PAGES:
            payload = {
                "pageIndex": page,
                "pageSize": self.PAGE_SIZE,
            }

            try:
                resp = self.client.post(api_url, json=payload, headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }, timeout=15)
                resp.raise_for_status()
                data = resp.json()
            except Exception:
                break

            records = data.get("Data", [])
            if not isinstance(records, list) or not records:
                break

            for item in records:
                if isinstance(item, dict):
                    title = item.get("JobAdName", "") or item.get("positionName", "")
                    loc_names = item.get("LocNames", [])
                    loc = ", ".join(loc_names) if loc_names else ""
                    job_id = item.get("Id", "") or str(item.get("JobAdId", ""))
                    dept = item.get("Org", "") or ""

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

            # 如果本页返回数量小于pageSize，说明已经是最后一页
            if len(records) < self.PAGE_SIZE:
                break
            page += 1

        return jobs

    def _try_fetch(self, api_url: str, page_index: int) -> dict | None:
        """尝试请求一页，返回JSON dict或None"""
        try:
            resp = self.client.post(api_url, json={
                "pageIndex": page_index,
                "pageSize": self.PAGE_SIZE,
            }, headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            }, timeout=10)
            if resp.status_code == 200 and "json" in resp.headers.get("content-type", ""):
                return resp.json()
        except Exception:
            pass
        return None

"""hotjob.cn JSON API Adapter — 适用于开放了JSON接口的hotjob企业"""
from __future__ import annotations
from typing import List
from adapters.base import BaseAdapter
from models import Job
from config import CompanyConfig


class HotjobJsonAdapter(BaseAdapter):
    """
    hotjob.cn JSON API adapter (无需Playwright/cookie)。
    适用于开放了 /wt/{code}/web/json/position/list 接口的企业。
    已验证: HTSC(华泰证券), xyzq(兴业证券), zts(中泰证券)
    
    config.params 需要:
      - su_id: 企业在hotjob.cn的代码 (如 HTSC, xyzq, zts)
    """

    name = "hotjob_json"

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        su_id = company.params.get("su_id", "")
        if not su_id:
            # 尝试从URL中提取
            # URL格式: https://www.hotjob.cn/wt/{su_id}/web/index
            parts = company.url.rstrip("/").split("/")
            for i, p in enumerate(parts):
                if p == "wt" and i + 1 < len(parts):
                    su_id = parts[i + 1]
                    break
            if not su_id:
                raise ValueError("su_id not found in params or URL")

        api_url = f"https://www.hotjob.cn/wt/{su_id}/web/json/position/list"
        jobs = []
        page = 1
        max_pages = 100  # safety limit

        while page <= max_pages:
            resp = self.client.get(
                api_url,
                params={
                    "recruitType": "2",
                    "pageNo": str(page),
                    "pageSize": "10",
                    "lanType": "1",
                },
            )
            resp.raise_for_status()
            data = resp.json()

            posts = data.get("postList", [])
            if not posts:
                break

            page_count = data.get("pageCount", 1)

            for item in posts:
                title = item.get("postName", "")
                location = item.get("workPlace", "")
                post_id = str(item.get("postId", ""))
                dept = item.get("deptOrgName", "")
                publish_date = item.get("publishDate", "")
                education = item.get("education", "")

                jobs.append(Job(
                    title=title,
                    company=company.name,
                    location=location,
                    job_id=post_id,
                    posted_date=publish_date,
                    tags=[t for t in [dept, education] if t],
                    source_adapter=self.name,
                ))

            if page >= page_count:
                break
            page += 1

        return jobs

"""浦发银行 (SPDB) Adapter — POST API直接获取岗位列表"""
from __future__ import annotations
from typing import List
import json
from datetime import datetime

from adapters.base import BaseAdapter
from models import Job
from config import CompanyConfig


class SPDBAdapter(BaseAdapter):
    """
    浦发银行招聘 API adapter.
    POST https://job.spdb.com.cn/socialJobJsonList
    返回全量岗位列表（无服务端城市过滤），客户端按address字段过滤北京。
    """

    name = "spdb"

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        jobs = []
        page = 1
        page_size = 50
        total = None

        while True:
            payload = {"pageNo": page, "pageSize": page_size}
            resp = self.client.post(
                "https://job.spdb.com.cn/socialJobJsonList",
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Referer": "https://job.spdb.com.cn/",
                },
            )
            data = resp.json()
            if total is None:
                total = data.get("totalRowCount", 0)

            rows = data.get("rows", [])
            if not rows:
                break

            for item in rows:
                address = item.get("address", "") or item.get("prmLocArea", "")
                title = item.get("positionName", "")
                dept = item.get("deptDescr", "")
                job_id = item.get("openningJobId", "")
                close_dt = item.get("closeDt", "")
                start_dt = item.get("desiredStartDt", "")

                # 解析更新时间
                updated = item.get("updatedDttm", {})
                publish_date = ""
                if isinstance(updated, dict) and updated.get("time"):
                    ts = updated["time"] / 1000
                    publish_date = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")

                job = Job(
                    title=f"{title} [{dept}]" if dept else title,
                    company=company.name,
                    location=address,
                    job_id=str(job_id),
                    url=f"https://job.spdb.com.cn/#/social/detail/{job_id}",
                    posted_date=publish_date,
                )
                jobs.append(job)

            # 浦发API忽略pageSize参数，固定返回10条
            actual_size = len(rows)
            if page * actual_size >= total:
                break
            page += 1

            # 安全上限
            if page > 100:
                break

        return jobs

"""hotjob.cn Adapter — 覆盖6家企业
注意：hotjob.cn/wecruit.hotjob.cn 是SPA应用（Vue/React），
API请求需要特定的cookie和防爬机制（acw_tc + 302循环）。
本adapter先获取页面cookie，然后尝试已知API路径。
"""
from __future__ import annotations
from typing import List
import re
import json

from adapters.base import BaseAdapter
from models import Job
from config import CompanyConfig


class HotjobAdapter(BaseAdapter):
    """
    hotjob.cn / wecruit.hotjob.cn 招聘系统爬取器。
    
    已知API路径（需要先获取session cookie）：
    - /wt/{su_id}/web/templet/position/recruitList (GET, 需cookie)
    - /wt/{su_id}/web/delivery/position/page (POST)
    - /{su_id}/pb/positionList.html (旧版)
    
    防爬机制：302循环设置acw_tc cookie，需要多次请求建立session。
    """

    name = "hotjob"

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        su_id = company.params.get("su_id", "")
        base_url = company.url.rstrip("/")

        # 第一步：访问主页建立session（获取acw_tc cookie）
        # hotjob使用302循环设置cookie，httpx的cookie jar会自动处理
        session_url = base_url
        if "wecruit" in base_url and "/pb/" in base_url:
            session_url = base_url
        elif "wecruit" not in base_url:
            session_url = f"https://{su_id}.hotjob.cn"

        try:
            self.client.get(session_url)
        except Exception:
            pass

        # 第二步：尝试各种API路径
        host = "wecruit.hotjob.cn" if "wecruit" in base_url else f"{su_id}.hotjob.cn"
        api_urls = [
            f"https://{host}/wt/{su_id}/web/templet/position/recruitList",
            f"https://{host}/wt/{su_id}/web/delivery/position/page",
            f"https://{host}/{su_id}/pb/positionList.html",
        ]

        for api_url in api_urls:
            try:
                # 尝试GET
                resp = self.client.get(
                    api_url,
                    params={
                        "SU_ID": su_id,
                        "pageNo": 1,
                        "pageSize": 50,
                        "recruitType": "SOCIAL",
                    },
                    headers={
                        "Accept": "application/json",
                        "X-Requested-With": "XMLHttpRequest",
                        "Referer": session_url,
                    },
                )
                if resp.status_code == 200 and "json" in resp.headers.get("content-type", ""):
                    data = resp.json()
                    jobs = self._parse_response(data, company)
                    if jobs:
                        return jobs
            except Exception:
                pass

            try:
                # 尝试POST
                resp = self.client.post(
                    api_url,
                    json={
                        "suId": su_id,
                        "pageNo": 1,
                        "pageSize": 50,
                        "recruitType": "SOCIAL",
                        "workCity": "北京",
                    },
                    headers={
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "Referer": session_url,
                    },
                )
                if resp.status_code == 200 and "json" in resp.headers.get("content-type", ""):
                    data = resp.json()
                    jobs = self._parse_response(data, company)
                    if jobs:
                        return jobs
            except Exception:
                pass

        # 第三步：尝试从SPA HTML中提取初始数据
        try:
            resp = self.client.get(session_url)
            if resp.status_code == 200:
                jobs = self._parse_from_html(resp.text, company)
                if jobs:
                    return jobs
        except Exception:
            pass

        raise RuntimeError(
            f"hotjob.cn SPA站点防爬机制（acw_tc cookie + 302循环），"
            f"纯HTTP无法获取岗位数据，需要浏览器渲染。su_id={su_id}"
        )

    def _parse_response(self, data: dict, company: CompanyConfig) -> List[Job]:
        """解析API响应"""
        records = []
        if isinstance(data, dict):
            for key in ["data", "result", "content", "body"]:
                val = data.get(key)
                if isinstance(val, list):
                    records = val
                    break
                if isinstance(val, dict):
                    for subkey in ["list", "records", "items", "positionList"]:
                        subval = val.get(subkey)
                        if isinstance(subval, list):
                            records = subval
                            break
                    if records:
                        break

        jobs = []
        for item in records:
            if isinstance(item, dict):
                title = item.get("positionName", "") or item.get("name", "")
                loc = item.get("workCity", "") or item.get("city", "")
                job_id = str(item.get("id", "") or item.get("positionId", ""))
                dept = item.get("departmentName", "") or item.get("dept", "")
                publish_date = item.get("publishDate", "") or item.get("createTime", "")

                jobs.append(Job(
                    title=title,
                    company=company.name,
                    location=loc,
                    job_id=job_id,
                    posted_date=publish_date,
                    tags=[dept] if dept else [],
                    source_adapter=self.name,
                ))
        return jobs

    def _parse_from_html(self, html: str, company: CompanyConfig) -> List[Job]:
        """尝试从HTML中提取初始数据"""
        patterns = [
            r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});',
            r'window\.positionData\s*=\s*(\{.*?\});',
        ]
        for pattern in patterns:
            match = re.search(pattern, html, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group(1))
                    return self._parse_response(data, company)
                except (json.JSONDecodeError, TypeError):
                    continue
        return []

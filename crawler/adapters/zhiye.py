"""北森 zhiye.com Adapter — 覆盖7家企业
注意：zhiye.com 是SPA应用，岗位数据通过前端JS渲染加载。
纯HTTP请求无法获取岗位列表，需要浏览器渲染。
本adapter使用页面HTML中嵌入的BSGlobal配置提取企业Key，
然后尝试北森已知的后端API路径。
"""
from __future__ import annotations
from typing import List
import re

from adapters.base import BaseAdapter
from models import Job
from config import CompanyConfig


class ZhiyeAdapter(BaseAdapter):
    """
    北森 zhiye.com 招聘系统爬取器。
    zhiye.com 是SPA，岗位列表通过前端异步加载。
    已知API路径：
    - /Social/recruitmentPosition/queryPage (POST, JSON)
    - /api/recruitmentPosition/queryPage
    - /Social/json/positions/{page}/{size}
    
    如果以上都返回HTML而非JSON，则回退到解析SSR页面中的数据。
    """

    name = "zhiye"

    # 北森已知的API路径列表
    API_PATHS = [
        "/Social/recruitmentPosition/queryPage",
        "/api/recruitmentPosition/queryPage",
        "/recruitmentPosition/queryPage",
    ]

    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        base_url = company.url.rstrip("/")

        # 第一步：访问主页获取cookie和BSGlobal配置
        main_resp = self.client.get(f"{base_url}/Social")
        main_resp.raise_for_status()

        # 提取BSGlobal中的Key
        key_match = re.search(r'"Key"\s*:\s*"([^"]+)"', main_resp.text)
        tenant_key = key_match.group(1) if key_match else ""

        # 第二步：尝试各种API路径
        jobs = []
        for api_path in self.API_PATHS:
            api_url = f"{base_url}{api_path}"
            payload = {
                "pageIndex": 1,
                "pageSize": 50,
                "recruitType": "SOCIAL",
                "keyword": "",
            }
            try:
                resp = self.client.post(
                    api_url,
                    json=payload,
                    headers={
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "X-Requested-With": "XMLHttpRequest",
                        "Referer": f"{base_url}/Social",
                    },
                )
                if resp.status_code == 200 and "application/json" in resp.headers.get("content-type", ""):
                    data = resp.json()
                    records = self._extract_records(data)
                    if records:
                        for item in records:
                            jobs.append(self._parse_job(item, company, base_url))
                        return jobs
            except Exception:
                continue

        # 第三步：如果API都失败，尝试从SSR HTML中提取岗位信息
        # zhiye.com 部分模板会在HTML中嵌入初始数据
        jobs = self._parse_from_html(main_resp.text, company, base_url)
        if jobs:
            return jobs

        # 标记为需要浏览器渲染
        raise RuntimeError(
            f"zhiye.com SPA站点需要浏览器渲染，纯HTTP无法获取岗位数据。"
            f" tenant_key={tenant_key}"
        )

    def _extract_records(self, data: dict) -> list:
        """从各种可能的JSON结构中提取岗位列表"""
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for key in ["data", "result", "content", "body"]:
                val = data.get(key)
                if isinstance(val, list):
                    return val
                if isinstance(val, dict):
                    for subkey in ["list", "records", "items", "positions"]:
                        subval = val.get(subkey)
                        if isinstance(subval, list):
                            return subval
        return []

    def _parse_job(self, item: dict, company: CompanyConfig, base_url: str) -> Job:
        """解析单个岗位"""
        title = item.get("positionName", "") or item.get("name", "") or item.get("title", "")
        loc = item.get("workCity", "") or item.get("city", "") or item.get("location", "")
        job_id = str(item.get("id", "") or item.get("positionId", ""))
        dept = item.get("departmentName", "") or item.get("dept", "")

        return Job(
            title=title,
            company=company.name,
            location=loc,
            job_id=job_id,
            url=f"{base_url}/Social/position/{job_id}" if job_id else "",
            tags=[dept] if dept else [],
            source_adapter=self.name,
        )

    def _parse_from_html(self, html: str, company: CompanyConfig, base_url: str) -> List[Job]:
        """尝试从HTML中提取岗位数据（部分模板会SSR渲染）"""
        # 尝试匹配 window.__INITIAL_STATE__ 或类似的数据注入
        patterns = [
            r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});',
            r'window\.positionList\s*=\s*(\[.*?\]);',
            r'"positions"\s*:\s*(\[.*?\])',
        ]
        import json
        for pattern in patterns:
            match = re.search(pattern, html, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group(1))
                    records = self._extract_records(data) if isinstance(data, dict) else data
                    if records:
                        return [self._parse_job(item, company, base_url) for item in records if isinstance(item, dict)]
                except (json.JSONDecodeError, TypeError):
                    continue
        return []

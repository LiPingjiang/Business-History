"""Adapter基类"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import httpx

from models import Job, CrawlResult
from config import CompanyConfig, REQUEST_TIMEOUT, REQUEST_HEADERS


class BaseAdapter(ABC):
    """所有adapter的基类"""

    name: str = "base"

    def __init__(self):
        self.client = httpx.Client(
            timeout=REQUEST_TIMEOUT,
            headers=REQUEST_HEADERS,
            follow_redirects=True,
        )

    def crawl(self, company: CompanyConfig) -> CrawlResult:
        """爬取单个企业，返回结果"""
        try:
            jobs = self.fetch_jobs(company)
            return CrawlResult(
                adapter_name=self.name,
                company=company.name,
                success=True,
                jobs=jobs,
            )
        except Exception as e:
            return CrawlResult(
                adapter_name=self.name,
                company=company.name,
                success=False,
                error=str(e),
            )

    @abstractmethod
    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        """子类实现：从企业招聘站抓取岗位列表"""
        ...

    def close(self):
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

"""数据模型"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import date
from typing import Optional
import json


@dataclass
class Job:
    """单个岗位"""
    title: str
    company: str
    location: str = ""
    job_id: str = ""
    url: str = ""
    posted_date: str = ""
    salary: str = ""
    experience: str = ""
    tags: list[str] = field(default_factory=list)
    source_adapter: str = ""
    crawled_date: str = field(default_factory=lambda: date.today().isoformat())

    @property
    def unique_key(self) -> str:
        """用于去重和diff对比的唯一键"""
        if self.job_id:
            return f"{self.company}::{self.job_id}"
        return f"{self.company}::{self.title}::{self.location}"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Job":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class CrawlResult:
    """单次爬取结果"""
    adapter_name: str
    company: str
    success: bool
    jobs: list[Job] = field(default_factory=list)
    error: str = ""
    crawled_at: str = field(default_factory=lambda: date.today().isoformat())

    def to_dict(self) -> dict:
        return {
            "adapter_name": self.adapter_name,
            "company": self.company,
            "success": self.success,
            "jobs": [j.to_dict() for j in self.jobs],
            "error": self.error,
            "crawled_at": self.crawled_at,
        }

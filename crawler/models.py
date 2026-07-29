"""数据模型"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import date
from typing import Optional
import json
import re


def parse_posted_days_ago(posted: str, crawled_date: str = "") -> int:
    """将 posted_date 文本解析为距今天数（数字越小越新）。
    
    支持格式：
    - "今天发布" / "today" → 0
    - "昨天" / "yesterday" → 1
    - "Posted 25 Days Ago" / "Posted 30+ Days Ago" → 25 / 30
    - "发布于 13 天前" → 13
    - "July 28, 2026" / "2026-07-28" → 计算与 crawled_date 的差值
    - "" (空) → -1 (未知)
    """
    if not posted or not posted.strip():
        return -1

    # "今天发布" / "today"
    if re.search(r'today|今天', posted, re.IGNORECASE):
        return 0

    # "yesterday" / "昨天"
    if re.search(r'yesterday|昨天', posted, re.IGNORECASE):
        return 1

    # "Posted X Days Ago" (English Workday style)
    m = re.search(r'(\d+)\+?\s*Days?\s*Ago', posted, re.IGNORECASE)
    if m:
        return int(m.group(1))

    # "发布于 X 天前" (Chinese style)
    m = re.search(r'(\d+)\s*天前', posted)
    if m:
        return int(m.group(1))

    # "30+" without "Days" keyword
    m = re.search(r'(\d+)\+', posted)
    if m:
        return int(m.group(1))

    # Absolute date: "July 28, 2026" or "2026-07-28"
    from datetime import datetime
    try:
        for fmt in ('%B %d, %Y', '%Y-%m-%d', '%b %d, %Y', '%d/%m/%Y'):
            try:
                abs_date = datetime.strptime(posted.strip(), fmt).date()
                ref = date.fromisoformat(crawled_date) if crawled_date else date.today()
                diff = (ref - abs_date).days
                return max(0, diff)
            except ValueError:
                continue
    except Exception:
        pass

    return -1  # unknown format


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

    @property
    def posted_days_ago(self) -> int:
        """发布距今天数（数字，用于排序）"""
        return parse_posted_days_ago(self.posted_date, self.crawled_date)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["posted_days_ago"] = self.posted_days_ago
        return d

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

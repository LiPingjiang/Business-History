"""输出模块：JSON存储 + Markdown diff报告"""
from __future__ import annotations
import json
from datetime import date
from pathlib import Path
from typing import List

from models import Job, CrawlResult
from config import DATA_DIR


def save_results(results: List[CrawlResult]) -> Path:
    """保存本次爬取结果到 data/{date}.json"""
    today = date.today().isoformat()
    output_file = DATA_DIR / f"{today}.json"

    all_jobs = []
    summary = {"date": today, "total_companies": 0, "success": 0, "failed": 0, "total_jobs": 0, "errors": []}

    for r in results:
        summary["total_companies"] += 1
        if r.success:
            summary["success"] += 1
            summary["total_jobs"] += len(r.jobs)
            all_jobs.extend([j.to_dict() for j in r.jobs])
        else:
            summary["failed"] += 1
            summary["errors"].append({"company": r.company, "error": r.error})

    output = {"summary": summary, "jobs": all_jobs}
    output_file.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_file


def load_previous_jobs() -> dict[str, dict]:
    """加载上一次的爬取结果，返回 {unique_key: job_dict}"""
    files = sorted(DATA_DIR.glob("*.json"))
    if len(files) < 2:
        return {}
    # 取倒数第二个文件（上一次）
    prev_file = files[-2]
    data = json.loads(prev_file.read_text(encoding="utf-8"))
    prev_jobs = {}
    for j in data.get("jobs", []):
        job = Job.from_dict(j)
        prev_jobs[job.unique_key] = j
    return prev_jobs


def generate_diff_report(results: List[CrawlResult]) -> str:
    """生成与上次对比的 Markdown diff 报告"""
    prev_jobs = load_previous_jobs()
    prev_keys = set(prev_jobs.keys())

    current_jobs: List[Job] = []
    for r in results:
        if r.success:
            current_jobs.extend(r.jobs)

    current_keys = {j.unique_key for j in current_jobs}

    new_keys = current_keys - prev_keys
    removed_keys = prev_keys - current_keys

    new_jobs = [j for j in current_jobs if j.unique_key in new_keys]
    today = date.today().isoformat()

    lines = [
        f"# 岗位变动报告 {today}",
        "",
        f"**新增岗位：{len(new_keys)}个 | 下架岗位：{len(removed_keys)}个 | 当前总计：{len(current_keys)}个**",
        "",
    ]

    if new_jobs:
        lines.append("## 🆕 新增岗位")
        lines.append("")
        lines.append("| 企业 | 岗位 | 地点 | 链接 |")
        lines.append("|------|------|------|------|")
        for j in sorted(new_jobs, key=lambda x: x.company):
            link = f"[投递]({j.url})" if j.url else "—"
            lines.append(f"| {j.company} | {j.title} | {j.location} | {link} |")
        lines.append("")

    if removed_keys:
        lines.append(f"## ❌ 下架岗位（{len(removed_keys)}个）")
        lines.append("")
        for key in sorted(removed_keys):
            prev = prev_jobs.get(key, {})
            lines.append(f"- {prev.get('company', '?')} — {prev.get('title', key)}")
        lines.append("")

    report = "\n".join(lines)

    # 保存报告
    report_file = DATA_DIR / f"diff_{today}.md"
    report_file.write_text(report, encoding="utf-8")

    return report

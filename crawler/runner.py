#!/usr/bin/env python3
"""
招聘岗位每日爬取 — 主调度器

用法:
    python runner.py              # 全量爬取所有企业
    python runner.py --diff       # 爬取并输出与上次的差异
    python runner.py --adapter workday  # 只跑某个adapter
    python runner.py --list       # 列出所有配置的企业
"""
from __future__ import annotations
import argparse
import sys
from datetime import date

from rich.console import Console
from rich.table import Table

from config import ALL_COMPANIES, CompanyConfig
from adapters import get_adapter, ADAPTER_REGISTRY
from models import CrawlResult
from output import save_results, generate_diff_report

console = Console()


def crawl_all(companies: list[CompanyConfig]) -> list[CrawlResult]:
    """爬取所有企业"""
    results = []
    adapters_cache = {}

    for i, company in enumerate(companies, 1):
        console.print(f"[{i}/{len(companies)}] {company.name} ({company.adapter})...", end=" ")

        # 复用adapter实例 (非Playwright); Playwright adapter每次新建
        if company.adapter not in adapters_cache:
            adapters_cache[company.adapter] = get_adapter(company.adapter)

        adapter = adapters_cache[company.adapter]

        # Playwright adapters: create fresh instance each time to avoid asyncio loop poisoning
        from adapters.playwright_base import PlaywrightAdapter
        if isinstance(adapter, PlaywrightAdapter):
            adapter = get_adapter(company.adapter)

        result = adapter.crawl(company)
        results.append(result)

        if result.success:
            console.print(f"[green]✓ {len(result.jobs)} jobs[/green]")
        else:
            console.print(f"[red]✗ {result.error[:60]}[/red]")

        # Cleanup Playwright adapter after each company
        if isinstance(adapter, PlaywrightAdapter):
            adapter.close()

    # 关闭所有adapter
    for adapter in adapters_cache.values():
        adapter.close()

    return results

def print_summary(results: list[CrawlResult]):
    """打印爬取摘要"""
    table = Table(title=f"爬取摘要 — {date.today().isoformat()}")
    table.add_column("企业", style="cyan")
    table.add_column("Adapter")
    table.add_column("状态")
    table.add_column("岗位数", justify="right")

    total_jobs = 0
    for r in results:
        status = "[green]✓[/green]" if r.success else f"[red]✗ {r.error[:30]}[/red]"
        count = str(len(r.jobs)) if r.success else "—"
        if r.success:
            total_jobs += len(r.jobs)
        table.add_row(r.company, r.adapter_name, status, count)

    console.print(table)
    console.print(f"\n[bold]总计: {len(results)}家企业, {sum(1 for r in results if r.success)}成功, "
                  f"{sum(1 for r in results if not r.success)}失败, {total_jobs}个岗位[/bold]")


def main():
    parser = argparse.ArgumentParser(description="招聘岗位每日爬取")
    parser.add_argument("--adapter", type=str, help="只运行指定adapter")
    parser.add_argument("--diff", action="store_true", help="输出与上次的差异报告")
    parser.add_argument("--list", action="store_true", help="列出所有配置的企业")
    args = parser.parse_args()

    if args.list:
        table = Table(title="配置的企业列表")
        table.add_column("#", justify="right")
        table.add_column("企业", style="cyan")
        table.add_column("Adapter")
        table.add_column("URL")
        for i, c in enumerate(ALL_COMPANIES, 1):
            table.add_row(str(i), c.name, c.adapter, c.url[:60])
        console.print(table)
        return

    # 过滤企业
    companies = ALL_COMPANIES
    if args.adapter:
        companies = [c for c in ALL_COMPANIES if c.adapter == args.adapter]
        if not companies:
            console.print(f"[red]No companies found for adapter: {args.adapter}[/red]")
            console.print(f"Available adapters: {list(ADAPTER_REGISTRY.keys())}")
            sys.exit(1)

    console.print(f"[bold]开始爬取 {len(companies)} 家企业...[/bold]\n")

    # 执行爬取
    results = crawl_all(companies)

    # 打印摘要
    print_summary(results)

    # 保存结果
    output_file = save_results(results)
    console.print(f"\n[green]结果已保存: {output_file}[/green]")

    # 生成diff报告
    if args.diff:
        report = generate_diff_report(results)
        console.print(f"\n[bold]===== Diff 报告 =====[/bold]\n")
        console.print(report)


if __name__ == "__main__":
    main()

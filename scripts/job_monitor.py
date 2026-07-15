#!/usr/bin/env python3
"""
北京数据研发/大数据研发岗位定期监控脚本

功能：
- 定期抓取各公司招聘页面，检查是否有新岗位
- 支持多种招聘平台（zhiye.com、hotjob.cn、官网等）
- 结果输出到 reports/ 目录
- 支持与上次结果对比，高亮新增岗位

使用方式：
    python3 scripts/job_monitor.py              # 检查所有目标
    python3 scripts/job_monitor.py --target央企  # 只检查央企
    python3 scripts/job_monitor.py --target外企  # 只检查外企
    python3 scripts/job_monitor.py --target科研  # 只检查科研单位

定时运行（crontab示例，每天早上9点执行）：
    0 9 * * * cd /path/to/Business-History && python3 scripts/job_monitor.py

依赖：
    pip install requests beautifulsoup4 lxml
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlencode

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("请先安装依赖: pip install requests beautifulsoup4 lxml")
    sys.exit(1)

# ============================================================
# 配置：监控目标
# ============================================================

TARGETS = {
    "央企": [
        {
            "name": "联通数科",
            "type": "zhiye",
            "url": "https://cudt.zhiye.com/Social",
            "keywords": ["大数据", "数据开发", "数据研发", "数据工程", "Spark", "Flink"],
            "location": "北京",
        },
        {
            "name": "联通数智",
            "type": "zhiye",
            "url": "https://cudataintelligence.zhiye.com/Social",
            "keywords": ["大数据", "数据", "平台研发", "数据开发"],
            "location": "北京",
        },
        {
            "name": "中国移动九天/数智事业部",
            "type": "hotjob",
            "url": "https://wecruit.hotjob.cn/SU60fa4d4e2f9d247b98de3fdc/pb/social.html",
            "keywords": ["大数据", "数据", "数据治理", "数据流通", "平台架构"],
            "location": "北京",
        },
        {
            "name": "中国移动主站",
            "type": "custom_api",
            "url": "https://job.10086.cn/personal/society/society_job_list.html",
            "keywords": ["大数据", "数据", "平台开发"],
            "location": "北京",
        },
        {
            "name": "中国联通社招",
            "type": "page_check",
            "url": "https://www.chinaunicom.com.cn/46/menu01/529/column06",
            "keywords": ["大数据", "数据", "软件研发"],
            "location": "北京",
        },
        {
            "name": "中国信通院",
            "type": "hotjob",
            "url": "https://www.hotjob.cn/wt/caict/web/index/webPosition210!getPostListByConditionShowPic",
            "keywords": ["大数据", "数据", "云计算", "人工智能"],
            "location": "北京",
        },
    ],
    "外企": [
        {
            "name": "领悦数字(BMW)",
            "type": "page_check",
            "url": "https://www.zhipin.com/gongsi/job/c95c0f437c854af103192NS_EA~~.html",
            "keywords": ["大数据", "数据", "Data Engineer", "数仓"],
            "location": "北京",
        },
        {
            "name": "微软(Microsoft)",
            "type": "workday",
            "url": "https://apply.careers.microsoft.com/careers",
            "search_params": {"location": "Beijing", "keyword": "data engineer"},
            "keywords": ["Data", "Engineer", "Scientist", "Big Data"],
            "location": "Beijing",
        },
        {
            "name": "亚马逊(Amazon)",
            "type": "amazon_jobs",
            "url": "https://www.amazon.jobs/en/search",
            "search_params": {"base_query": "Software Engineer", "loc_query": "China"},
            "keywords": ["Data", "Big Data", "data engineer"],
            "location": "Beijing",
        },
        {
            "name": "西门子(Siemens)",
            "type": "page_check",
            "url": "https://jobs.siemens.com.cn/siemens/position/index?recruitmentType=SOCIALRECRUITMENT&workCity=Beijing",
            "keywords": ["Data", "大数据", "AI", "Machine Learning"],
            "location": "Beijing",
        },
        {
            "name": "AMD",
            "type": "page_check",
            "url": "https://careers.amd.com/careers-home/jobs?location=Beijing",
            "keywords": ["Data", "大数据", "LLM", "compiler"],
            "location": "Beijing",
        },
    ],
    "科研": [
        {
            "name": "中科院信工所",
            "type": "page_check",
            "url": "https://www.iie.ac.cn/yjdw/rczp/",
            "keywords": ["大数据", "数据开发", "数据研发", "Spark", "Flink", "招聘"],
            "location": "北京",
        },
        {
            "name": "中科院计算所",
            "type": "page_check",
            "url": "http://ict.cas.cn/rczp/",
            "keywords": ["大数据", "数据", "软件", "计算"],
            "location": "北京",
        },
        {
            "name": "中科院计算机网络信息中心",
            "type": "page_check",
            "url": "https://www.cnic.cas.cn/rcdw/rczp/szyxz/",
            "keywords": ["大数据", "数据开发", "数据平台"],
            "location": "北京",
        },
        {
            "name": "中科院软件所",
            "type": "page_check",
            "url": "http://www.is.cas.cn/rcdw2016/rczp2016/",
            "keywords": ["大数据", "数据", "软件", "系统"],
            "location": "北京",
        },
        {
            "name": "国家数据发展研究院",
            "type": "page_check",
            "url": "https://www.nda.gov.cn/sjj/zwgk/tzgg/",
            "keywords": ["招聘", "社招", "数据"],
            "location": "北京",
        },
    ],
}

# ============================================================
# 工具函数
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REPORTS_DIR = PROJECT_ROOT / "scripts" / "reports"
CACHE_DIR = PROJECT_ROOT / "scripts" / ".cache"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


def ensure_dirs():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def get_page(url, timeout=15):
    """获取页面内容，返回 (status_code, text) 或 (error_code, error_msg)"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        return resp.status_code, resp.text
    except requests.exceptions.Timeout:
        return -1, "TIMEOUT"
    except requests.exceptions.ConnectionError as e:
        return -2, f"CONNECTION_ERROR: {e}"
    except Exception as e:
        return -3, f"ERROR: {e}"


def content_hash(text):
    """计算内容哈希，用于检测页面变化"""
    # 去除动态内容（时间戳、随机数等）
    cleaned = re.sub(r'\d{10,13}', '', text)  # 去除时间戳
    cleaned = re.sub(r'[a-f0-9]{32}', '', cleaned)  # 去除MD5
    return hashlib.md5(cleaned.encode()).hexdigest()


def load_cache(name):
    """加载上次的缓存结果"""
    safe_name = name.replace("/", "_").replace("\\", "_").replace(":", "_")
    cache_file = CACHE_DIR / f"{safe_name}.json"
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def save_cache(name, data):
    """保存本次结果到缓存"""
    safe_name = name.replace("/", "_").replace("\\", "_").replace(":", "_")
    cache_file = CACHE_DIR / f"{safe_name}.json"
    cache_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def extract_job_titles(html_text, keywords):
    """从HTML中提取包含关键词的岗位标题"""
    soup = BeautifulSoup(html_text, "lxml")
    jobs = []

    # 通用策略：查找包含关键词的链接和标题
    # 策略1: 查找所有链接文本
    for a_tag in soup.find_all("a"):
        text = a_tag.get_text(strip=True)
        if text and len(text) > 2 and len(text) < 100:
            if any(kw.lower() in text.lower() for kw in keywords):
                href = a_tag.get("href", "")
                jobs.append({"title": text, "link": href})

    # 策略2: 查找常见岗位容器
    for selector in [".job-name", ".position-name", ".job-title",
                     "[class*='job']", "[class*='position']", "[class*='post']"]:
        for el in soup.select(selector):
            text = el.get_text(strip=True)
            if text and len(text) > 2 and len(text) < 100:
                if any(kw.lower() in text.lower() for kw in keywords):
                    jobs.append({"title": text, "link": ""})

    # 去重
    seen = set()
    unique_jobs = []
    for job in jobs:
        if job["title"] not in seen:
            seen.add(job["title"])
            unique_jobs.append(job)

    return unique_jobs


# ============================================================
# 检查器
# ============================================================

def check_page(target):
    """通用页面检查：获取页面，提取岗位，对比缓存"""
    name = target["name"]
    url = target["url"]
    keywords = target["keywords"]

    status, text = get_page(url)

    result = {
        "name": name,
        "url": url,
        "check_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "ok" if status == 200 else "error",
        "status_code": status,
        "jobs_found": [],
        "new_jobs": [],
        "page_changed": False,
        "error": None,
    }

    if status != 200:
        result["status"] = "error"
        result["error"] = text if status < 0 else f"HTTP {status}"
        return result

    # 提取岗位
    jobs = extract_job_titles(text, keywords)
    result["jobs_found"] = jobs

    # 对比缓存
    cache = load_cache(name)
    current_hash = content_hash(text)

    if cache:
        old_hash = cache.get("page_hash", "")
        old_titles = set(j["title"] for j in cache.get("jobs_found", []))
        new_titles = set(j["title"] for j in jobs)

        result["page_changed"] = (current_hash != old_hash)
        result["new_jobs"] = [j for j in jobs if j["title"] not in old_titles]
    else:
        result["page_changed"] = True
        result["new_jobs"] = jobs  # 首次运行，所有都是新的

    # 保存缓存
    save_cache(name, {
        "page_hash": current_hash,
        "jobs_found": jobs,
        "check_time": result["check_time"],
    })

    return result


def check_zhiye(target):
    """北森招聘系统（zhiye.com）检查"""
    # zhiye.com 系统通常有 /Social 页面列出社招岗位
    return check_page(target)


def check_hotjob(target):
    """hotjob.cn 系统检查"""
    return check_page(target)


def check_target(target):
    """根据类型分发检查"""
    t = target.get("type", "page_check")
    if t == "zhiye":
        return check_zhiye(target)
    elif t == "hotjob":
        return check_hotjob(target)
    elif t in ("page_check", "custom_api", "workday", "amazon_jobs",
               "boss_search", "boss_company"):
        return check_page(target)
    else:
        return check_page(target)


# ============================================================
# 报告生成
# ============================================================

def generate_report(results, category=None):
    """生成Markdown报告"""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H%M%S")
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append(f"# 岗位监控报告")
    lines.append(f"")
    lines.append(f"> 检查时间：{date_str}")
    if category:
        lines.append(f"> 检查范围：{category}")
    lines.append(f"> 关注方向：北京 | 数据研发 / 大数据研发")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    # 汇总
    total = len(results)
    ok_count = sum(1 for r in results if r["status"] == "ok")
    error_count = total - ok_count
    changed_count = sum(1 for r in results if r.get("page_changed"))
    new_job_count = sum(len(r.get("new_jobs", [])) for r in results)

    lines.append(f"## 📊 汇总")
    lines.append(f"")
    lines.append(f"| 指标 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 检查目标数 | {total} |")
    lines.append(f"| 正常访问 | {ok_count} |")
    lines.append(f"| 访问异常 | {error_count} |")
    lines.append(f"| 页面有变化 | {changed_count} |")
    lines.append(f"| 新增岗位数 | {new_job_count} |")
    lines.append(f"")

    # 新增岗位（重点关注）
    if new_job_count > 0:
        lines.append(f"## 🆕 新增岗位")
        lines.append(f"")
        for r in results:
            if r.get("new_jobs"):
                lines.append(f"### {r['name']}")
                lines.append(f"")
                for job in r["new_jobs"]:
                    link_text = f" [链接]({job['link']})" if job.get("link") else ""
                    lines.append(f"- **{job['title']}**{link_text}")
                lines.append(f"")

    # 详细结果
    lines.append(f"## 📋 详细检查结果")
    lines.append(f"")
    lines.append(f"| 企业 | 状态 | 页面变化 | 匹配岗位数 | 新增 |")
    lines.append(f"|------|------|---------|-----------|------|")
    for r in results:
        status_icon = "✅" if r["status"] == "ok" else "❌"
        changed_icon = "🔄" if r.get("page_changed") else "—"
        job_count = len(r.get("jobs_found", []))
        new_count = len(r.get("new_jobs", []))
        new_text = f"**+{new_count}**" if new_count > 0 else "0"
        lines.append(f"| {r['name']} | {status_icon} | {changed_icon} | {job_count} | {new_text} |")
    lines.append(f"")

    # 错误详情
    errors = [r for r in results if r["status"] == "error"]
    if errors:
        lines.append(f"## ⚠️ 访问异常")
        lines.append(f"")
        for r in errors:
            lines.append(f"- **{r['name']}**: {r.get('error', 'Unknown error')}")
        lines.append(f"")

    # 保存报告
    report_name = f"monitor_{timestamp}.md"
    report_path = REPORTS_DIR / report_name
    report_path.write_text("\n".join(lines), encoding="utf-8")

    # 同时更新 latest 报告
    latest_path = REPORTS_DIR / "latest_report.md"
    latest_path.write_text("\n".join(lines), encoding="utf-8")

    return report_path, "\n".join(lines)


# ============================================================
# 主流程
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="北京数据研发岗位监控脚本")
    parser.add_argument("--target", choices=["央企", "外企", "科研", "all"],
                        default="all", help="检查目标类别")
    parser.add_argument("--dry-run", action="store_true",
                        help="仅显示将要检查的目标，不实际执行")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="显示详细输出")
    args = parser.parse_args()

    ensure_dirs()

    # 确定检查范围
    if args.target == "all":
        categories = list(TARGETS.keys())
    else:
        categories = [args.target]

    targets_to_check = []
    for cat in categories:
        for t in TARGETS.get(cat, []):
            t["_category"] = cat
            targets_to_check.append(t)

    if args.dry_run:
        print(f"将要检查 {len(targets_to_check)} 个目标：")
        for t in targets_to_check:
            print(f"  [{t['_category']}] {t['name']} - {t.get('url', 'N/A')}")
        return

    print(f"=" * 60)
    print(f"  北京数据研发岗位监控")
    print(f"  检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  检查范围: {', '.join(categories)}")
    print(f"  目标数量: {len(targets_to_check)}")
    print(f"=" * 60)
    print()

    results = []
    for i, target in enumerate(targets_to_check, 1):
        name = target["name"]
        print(f"[{i}/{len(targets_to_check)}] 检查: {name} ...", end=" ", flush=True)

        result = check_target(target)
        results.append(result)

        if result["status"] == "ok":
            new_count = len(result.get("new_jobs", []))
            job_count = len(result.get("jobs_found", []))
            if new_count > 0:
                print(f"✅ 匹配{job_count}个岗位, 🆕 新增{new_count}个!")
            else:
                changed = "🔄 页面有变化" if result.get("page_changed") else "无变化"
                print(f"✅ 匹配{job_count}个岗位, {changed}")
        else:
            print(f"❌ {result.get('error', 'Unknown error')}")

        if args.verbose and result.get("new_jobs"):
            for job in result["new_jobs"]:
                print(f"      🆕 {job['title']}")

        # 礼貌间隔，避免被封
        time.sleep(1.5)

    # 生成报告
    print()
    print("-" * 60)
    report_path, report_text = generate_report(results,
                                                category=args.target if args.target != "all" else None)
    print(f"📄 报告已保存: {report_path}")

    # 汇总
    new_total = sum(len(r.get("new_jobs", [])) for r in results)
    if new_total > 0:
        print(f"\n🎉 发现 {new_total} 个新增岗位！详见报告。")
    else:
        print(f"\n📭 本次检查未发现新增岗位。")


if __name__ == "__main__":
    main()

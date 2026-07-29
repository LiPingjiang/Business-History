"""Analyze all companies by data source type: third-party platform vs official website."""
from config import ALL_COMPANIES
from collections import Counter
import re

THIRD_PARTY_PLATFORMS = {
    "zhiye.com": "北森智聘(zhiye.com)",
    "workday": "Workday",
    "smartrecruiters": "SmartRecruiters",
    "hotjob": "前程无忧(51job/hotjob)",
    "mokahr": "Moka",
    "phenom": "Phenom",
    "jibe": "Jibe(Google)",
}

results = {"third_party": [], "official": []}

for c in ALL_COMPANIES:
    url = c.url
    platform = None
    for key, name in THIRD_PARTY_PLATFORMS.items():
        if key in url:
            platform = name
            break
    
    domain = ""
    m = re.search(r'://([^/]+)', url)
    if m:
        domain = m.group(1)
    
    entry = {
        "name": c.name,
        "adapter": c.adapter,
        "url": url,
        "domain": domain,
    }
    
    if platform:
        entry["platform"] = platform
        results["third_party"].append(entry)
    else:
        results["official"].append(entry)

print("=" * 70)
print(f"总计: {len(ALL_COMPANIES)} 个企业配置")
print("=" * 70)

print(f"\n【第三方招聘平台】{len(results['third_party'])} 家企业")
print("-" * 70)
platform_groups = {}
for e in results["third_party"]:
    platform_groups.setdefault(e["platform"], []).append(e)

for platform, companies in sorted(platform_groups.items(), key=lambda x: -len(x[1])):
    print(f"\n  {platform} ({len(companies)} 家):")
    for c in sorted(companies, key=lambda x: x["name"]):
        print(f"    {c['name']:<20} {c['domain']}")

print(f"\n\n【公司官网/自建站】{len(results['official'])} 家企业")
print("-" * 70)
for c in sorted(results["official"], key=lambda x: x["name"]):
    print(f"  {c['name']:<20} adapter={c['adapter']:<15} {c['domain']}")

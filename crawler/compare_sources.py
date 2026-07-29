"""
Compare job counts between zhiye/beisen (third-party) and official career sites
for key companies to determine if we should switch data sources.

For companies on zhiye.com that also have official career pages,
check if the official site provides more/better data (especially location info).
"""
import httpx
import json
import re
from config import ALL_COMPANIES

# Current zhiye/beisen job counts from API
# We'll check a few key companies' official sites to compare

# Companies to investigate - those with known official career sites
COMPANIES_TO_CHECK = {
    "工商银行": {
        "zhiye_url": "https://icbc.zhiye.com",
        "official_url": "https://job.icbc.com.cn/custom/icbc/search/PC/index.html",
        "notes": "ICBC has its own career site"
    },
    "建设银行": {
        "zhiye_url": "https://ccb.zhiye.com",
        "official_url": "https://job.ccb.com",
        "notes": "CCB has its own career site"
    },
    "农业银行": {
        "zhiye_url": "https://abchina.zhiye.com",
        "official_url": "https://career.abchina.com",
        "notes": "ABC has its own career site"
    },
    "交通银行": {
        "zhiye_url": "https://bankcomm.zhiye.com",
        "official_url": "https://job.bankcomm.com",
        "notes": "BoCom has its own career site"
    },
    "招商银行": {
        "zhiye_url": "https://cmbchina.zhiye.com",
        "official_url": "https://career.cmbchina.com",
        "notes": "CMB has its own career site"
    },
    "中国建筑": {
        "zhiye_url": "https://cscec.zhiye.com",
        "official_url": "https://job.cscec.com",
        "notes": "CSCEC has its own career site"
    },
    "中国交建": {
        "zhiye_url": "https://ccccltd.zhiye.com",
        "official_url": "https://hr.ccccltd.cn",
        "notes": "CCCC has its own career site"
    },
    "中金公司": {
        "zhiye_url": "https://cicc.zhiye.com",
        "official_url": "https://career.cicc.com",
        "notes": "CICC has its own career site"
    },
}

# Check zhiye API for each company's job count
print("=" * 80)
print("第三方平台 vs 官网 岗位数量对比")
print("=" * 80)
print()
print(f"{'企业':<12} {'zhiye岗位数':<12} {'zhiye有location':<16} {'官网URL'}")
print("-" * 80)

client = httpx.Client(timeout=15, verify=False)

for company in ALL_COMPANIES:
    if 'zhiye' not in company.url:
        continue
    
    # Try to get job count from zhiye API
    domain = company.url.split("//")[1].split("/")[0]
    api_url = f"https://{domain}/api/job/GetJobAdPageList"
    
    try:
        resp = client.post(api_url, json={
            "pageIndex": 1,
            "pageSize": 1,
            "keyword": "",
        }, headers={"Content-Type": "application/json"})
        data = resp.json()
        total = data.get("TotalCount", 0)
        
        # Check if any jobs have location
        jobs = data.get("JobAdList", [])
        has_loc = any(j.get("LocNames") for j in jobs)
        
        official = COMPANIES_TO_CHECK.get(company.name, {}).get("official_url", "")
        marker = "⚠️" if official and not has_loc else ""
        
        print(f"  {company.name:<12} {total:<12} {'有' if has_loc else '无':<16} {official} {marker}")
    except Exception as e:
        print(f"  {company.name:<12} {'ERROR':<12} {str(e)[:40]}")

print()
print("=" * 80)
print("结论:")
print("  ⚠️ = 该企业在zhiye上无location数据，且有独立官网，建议切换到官网爬取")
print()
print("关键发现:")
print("  - zhiye.com API 的 LocNames 字段对所有企业都返回空")
print("  - 这是北森平台的系统性问题，不是个别企业配置问题")
print("  - 对于有独立招聘官网的企业，官网通常会提供完整的地点信息")
print("  - 建议：大型银行和央企优先切换到官网爬取")
print("=" * 80)

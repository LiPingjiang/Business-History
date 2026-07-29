"""Analyze data source types and check if zhiye companies have official career sites."""
from config import ALL_COMPANIES
import httpx

# Companies currently on zhiye.com - check if they have official career pages
# that might provide better data (especially location info)
zhiye_companies = [c for c in ALL_COMPANIES if 'zhiye' in c.url]

# Known or suspected official career sites for zhiye companies
OFFICIAL_CAREER_SITES = {
    "中国交建": "https://hr.ccccltd.cn",
    "中金公司": "https://career.cicc.com",
    "招商局集团": "https://job.cmhk.com",
    "中国人民保险": "https://hr.picc.com.cn",
    "中国人寿": "https://job.chinalife.com.cn",
    "保利发展": "https://hr.polycn.com",
    "中国联通社招": "https://www.chinaunicom.com.cn/46/menu01/529/column06",
    "联通数科": "https://cudt.10010.com",
    "中科院自动化所": "http://www.ia.cas.cn/rczp/",
    "中国银河证券": "https://www.chinastock.com.cn",
    "中国建筑": "https://job.cscec.com",
    "中国核工业": "https://zhaopin.cnnc.com.cn",
    "中国航天科工": "https://zhaopin.casic.com.cn",
    "中国船舶": "https://zhaopin.cssc.net.cn",
    "中国能建": "https://zhaopin.ceec.net.cn",
    "中国太平保险": "https://job.cntaiping.com",
    "中国再保险": "https://www.chinare.com.cn",
    "中国银行": "https://campus.chinahr.com/pages/boc/",
    "工商银行": "https://job.icbc.com.cn",
    "建设银行": "https://job.ccb.com",
    "农业银行": "https://career.abchina.com",
    "交通银行": "https://job.bankcomm.com",
    "招商银行": "https://career.cmbchina.com",
    "邮储银行": "https://www.psbc.com/cn/grfw/rczp/",
    "北京银行": "https://bankofbeijing.zhiye.com",  # zhiye IS their official
    "光大证券": "https://www.ebscn.com",
    "国信证券": "https://www.guosen.com.cn",
    "中信建投证券": "https://www.csc108.com",
}

print("=" * 80)
print("数据来源分析：第三方平台 vs 公司官网")
print("=" * 80)

print(f"\n当前 zhiye.com 平台企业: {len(zhiye_companies)} 家")
print("\n注意: zhiye.com (北森智聘) 是第三方招聘SaaS平台")
print("      很多企业同时有自己的官方招聘网站")
print("      zhiye API 不返回地理位置信息(LocNames始终为空)")
print()

# Check which zhiye companies have known official sites
print("【zhiye企业 - 官网招聘页对照】")
print("-" * 80)
print(f"{'企业名':<16} {'zhiye域名':<35} {'已知官网招聘页'}")
print("-" * 80)

for c in sorted(zhiye_companies, key=lambda x: x.name):
    domain = c.url.split("//")[1].split("/")[0]
    official = OFFICIAL_CAREER_SITES.get(c.name, "")
    marker = "✓" if official else "?"
    print(f"  {marker} {c.name:<14} {domain:<33} {official}")

print()
print("=" * 80)
print("建议优先级:")
print("  1. zhiye.com 是这些企业的官方招聘入口(企业付费使用北森SaaS)")
print("     但API数据质量差(无location), 部分企业官网可能有更完整的数据")
print("  2. 对于有独立招聘官网的企业, 可以对比岗位数量差异")
print("  3. 差异大的企业应切换到官网爬取")
print("=" * 80)

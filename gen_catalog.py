#!/usr/bin/env python3
"""Generate COMPANY_CATALOG JS object from 企业黄页 directory structure + crawler config."""
import os
import sys
import json

sys.path.insert(0, "crawler")
from config import ALL_COMPANIES

# Get crawled company names
crawled_names = {c.name for c in ALL_COMPANIES}

# Name mapping: 企业黄页 filename → crawler config name (for matching)
NAME_MAP = {
    "英伟达": "NVIDIA", "英特尔": "Intel", "惠普": "HP",
    "万事达卡": "Mastercard", "壳牌": "Shell", "思科": "Cisco",
    "博通": "Broadcom", "亚马逊": "Amazon", "微软": "Microsoft",
    "西门子": "Siemens", "宝马": "BMW/领悦", "阿斯利康": "AstraZeneca",
    "辉瑞": "Pfizer", "红帽": "Red Hat", "戴尔": "Dell",
    "霍尼韦尔": "Honeywell",
    "施耐德电气": "Schneider Electric",
    "中国华电集团": "中国华电", "中国中车集团": "中国中车",
    "中国建筑集团": "中国建筑", "中国船舶集团": "中国船舶",
    "中国核工业集团": "中国核工业", "中国能源建设集团": "中国能建",
    "中国航天科工集团": "中国航天科工",
    "中国石油化工集团": "中国石化", "中国华能集团": "中国华能",
    "中国大唐集团": "中国大唐",
    "中国石油天然气集团": "中国石油", "中国海洋石油集团": "中国海油",
    "中国交通建设集团": "中国交建", "中国五矿集团": "中国五矿",
    "中国保利集团": "保利发展",
    "中国中化控股": "中化集团",
    "三星": "三星中国",
    "中国银河金融控股": "中国银河证券",
    "中国工商银行": "工商银行", "中国农业银行": "农业银行",
    "中国建设银行": "建设银行", "中国银行": "中国银行",
    "交通银行": "交通银行",
    "中国人民保险": "中国人民保险", "中国太平保险": "中国太平保险",
    "中国人寿": "中国人寿",
    "中国中信集团": "中信银行",
}

base = "企业黄页"
catalog = {}

for root, dirs, files in os.walk(base):
    dirs.sort()
    for f in sorted(files):
        if not f.endswith(".md"):
            continue
        if f in ("企业黄页总目录.md", "北京数据研发岗位核查汇总.md"):
            continue
        rel = os.path.relpath(os.path.join(root, f), base)
        parts = rel.replace(".md", "").split(os.sep)
        if len(parts) < 2:
            continue
        # Category: "外企/美国" → "外企 - 美国", "央企/能源电力" → "央企 - 能源电力"
        top = parts[0]
        sub = parts[1] if len(parts) == 3 else ""
        name = parts[-1]
        
        if top == "外企":
            cat_key = f"外企 - {sub}" if sub else "外企 - 其他"
        elif top == "央企":
            cat_key = f"央企 - {sub}" if sub else "央企 - 其他"
        else:
            cat_key = top
        
        # Check if this company is in the crawler config
        mapped_name = NAME_MAP.get(name, name)
        is_active = mapped_name in crawled_names
        
        entry = {"name": name, "active": is_active}
        if is_active and mapped_name != name:
            entry["crawlerName"] = mapped_name
        
        catalog.setdefault(cat_key, []).append(entry)

# Also add companies from crawler config that are NOT in 企业黄页
all_catalog_names = set()
for entries in catalog.values():
    for e in entries:
        all_catalog_names.add(e.get("crawlerName", e["name"]))

missing_from_catalog = crawled_names - all_catalog_names
# Add these under appropriate categories
extra_entries = {
    "银行": ["中信银行", "浦发银行", "民生银行", "华夏银行", "兴业银行",
             "招商银行", "邮储银行", "光大银行", "广发银行",
             "北京农商银行", "渤海银行", "恒丰银行", "北京银行",
             "上海银行", "长沙银行", "中信百信银行", "苏商银行"],
    "券商": ["中金公司", "华泰证券", "兴业证券", "中泰证券",
             "中信建投证券", "国信证券", "光大证券", "方正证券", "中金财富"],
    "研究机构": ["中科院自动化所", "智源研究院"],
    "央企 - 通信电子": ["联通数科", "联通数智", "中国联通社招",
                       "中国移动九天", "中国信通院"],
    "央企 - 其他": ["一汽大众", "招商局集团", "中国再保险",
                   "中国长城资产", "中国东方资产"],
    "外企 - 韩国": ["Samsung SEC"],
    "外企 - 美国": ["GE Aerospace"],
}

for cat, names in extra_entries.items():
    for n in names:
        if n in missing_from_catalog:
            existing_names = {e.get("crawlerName", e["name"]) for e in catalog.get(cat, [])}
            if n not in existing_names:
                catalog.setdefault(cat, []).append({"name": n, "active": True})
                missing_from_catalog.discard(n)

# Print remaining missing
if missing_from_catalog:
    print(f"// Still missing from catalog: {missing_from_catalog}", file=sys.stderr)

# Generate JS
print("const COMPANY_CATALOG = {")
for cat_key in sorted(catalog.keys()):
    entries = catalog[cat_key]
    print(f'  "{cat_key}": [')
    for e in sorted(entries, key=lambda x: x["name"]):
        parts = [f'name: "{e["name"]}"', f'active: {"true" if e["active"] else "false"}']
        if "crawlerName" in e:
            parts.append(f'crawlerName: "{e["crawlerName"]}"')
        print(f'    {{ {", ".join(parts)} }},')
    print("  ],")
print("}")
print(f"\n// Total: {sum(len(v) for v in catalog.values())} companies in {len(catalog)} categories")

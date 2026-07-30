#!/usr/bin/env python3
"""
fix_display_names.py
在 config.py 中为需要映射的企业添加 display_name 参数。
同时更新前端 Jobs.jsx 的 active 标记，使其与爬虫 active 列表对齐。
"""
import re
import sys

# 爬虫 name -> 前端 CATALOG display_name 映射
CRAWLER_TO_FRONTEND = {
    "NVIDIA": "英伟达",
    "Intel": "英特尔",
    "HP": "惠普",
    "Microsoft": "微软",
    "Amazon": "亚马逊",
    "Cisco": "思科",
    "Dell": "戴尔",
    "Broadcom": "博通",
    "Shell": "壳牌",
    "Siemens": "西门子",
    "Pfizer": "辉瑞",
    "AstraZeneca": "阿斯利康",
    "Mastercard": "万事达卡",
    "Schneider Electric": "施耐德电气",
    "Red Hat": "红帽",
    "Samsung SEC": "三星",
    "BMW/领悦": "宝马",
    "三星中国": "三星",
    "中国石油": "中国石油天然气集团",
    "中国石化": "中国石油化工集团",
    "中国海油": "中国海洋石油集团",
    "中国华能": "中国华能集团",
    "中国华电": "中国华电集团",
    "中国大唐": "中国大唐集团",
    "中国中车": "中国中车集团",
    "中国五矿": "中国五矿集团",
    "中国交建": "中国交通建设集团",
    "中国能建": "中国能源建设集团",
    "中国银河证券": "中国银河金融控股",
    "中化集团": "中国中化控股",
    "保利发展": "中国保利集团",
    "中国航天科工": "中国航天科工集团",
    "中国船舶": "中国船舶集团",
}

def patch_config(config_path):
    """在 CompanyConfig 构造调用中插入 display_name 参数"""
    with open(config_path, 'r') as f:
        content = f.read()

    changes = 0
    for crawler_name, display_name in CRAWLER_TO_FRONTEND.items():
        # Match: CompanyConfig("NVIDIA", ... ) patterns
        # We need to add display_name="英伟达" to those entries
        # Pattern: find the line with CompanyConfig("name", and add display_name
        escaped_name = re.escape(crawler_name)
        # Look for entries that don't already have display_name
        pattern = rf'(CompanyConfig\("{escaped_name}",\s*"[^"]+",\s*"[^"]+")'
        matches = list(re.finditer(pattern, content))
        if not matches:
            # Try alternate pattern for entries with source_type/official_url/status already set
            pattern2 = rf'(CompanyConfig\("{escaped_name}"[^)]*?)(\))'
            matches2 = list(re.finditer(pattern2, content))
            for m in matches2:
                if 'display_name' not in m.group(0):
                    # Add display_name before closing paren
                    old = m.group(0)
                    # Check if it ends with a trailing comma or not
                    inner = m.group(1).rstrip()
                    if inner.endswith(','):
                        new = f'{inner}\n                  display_name="{display_name}")'
                    else:
                        new = f'{inner},\n                  display_name="{display_name}")'
                    content = content.replace(old, new, 1)
                    changes += 1
        else:
            for m in matches:
                # Check if display_name already present in the full entry
                # Find the full entry (until closing paren)
                start = m.start()
                depth = 0
                end = start
                for i in range(start, len(content)):
                    if content[i] == '(':
                        depth += 1
                    elif content[i] == ')':
                        depth -= 1
                        if depth == 0:
                            end = i + 1
                            break
                full_entry = content[start:end]
                if 'display_name' not in full_entry:
                    # Insert display_name before the closing )
                    new_entry = full_entry[:-1].rstrip()
                    if new_entry.endswith(','):
                        new_entry += f'\n                  display_name="{display_name}")'
                    else:
                        new_entry += f',\n                  display_name="{display_name}")'
                    content = content[:start] + new_entry + content[end:]
                    changes += 1

    with open(config_path, 'w') as f:
        f.write(content)
    print(f"Patched {changes} entries in config.py with display_name")


def patch_frontend(jsx_path, active_names):
    """更新 Jobs.jsx 中的 active 标记"""
    with open(jsx_path, 'r') as f:
        content = f.read()

    # Build set of names that should be active
    active_set = set(active_names)

    changes = 0
    # Pattern: { name: "XXX", active: true/false }
    def replace_active(m):
        nonlocal changes
        name = m.group(1)
        current = m.group(2)
        should_be_active = name in active_set
        new_val = "true" if should_be_active else "false"
        if current != new_val:
            changes += 1
        return f'{{ name: "{name}", active: {new_val} }}'

    content = re.sub(
        r'\{ name: "([^"]+)", active: (true|false) \}',
        replace_active,
        content
    )

    with open(jsx_path, 'w') as f:
        f.write(content)
    print(f"Updated {changes} active flags in Jobs.jsx")


if __name__ == "__main__":
    import json

    config_path = sys.argv[1] if len(sys.argv) > 1 else "crawler/config.py"
    jsx_path = sys.argv[2] if len(sys.argv) > 2 else None
    jobs_json = sys.argv[3] if len(sys.argv) > 3 else None

    # Step 1: Patch config.py
    patch_config(config_path)

    # Step 2: If jsx_path provided, update active flags
    if jsx_path and jobs_json:
        # Load latest crawl data to determine which companies have data
        with open(jobs_json) as f:
            data = json.load(f)
        crawled_companies = set(j.get('company', '') for j in data['jobs'])

        # Build the full active set: crawled company names + their display_names
        active_frontend_names = set()
        for name in crawled_companies:
            active_frontend_names.add(name)
            if name in CRAWLER_TO_FRONTEND:
                active_frontend_names.add(CRAWLER_TO_FRONTEND[name])

        patch_frontend(jsx_path, active_frontend_names)

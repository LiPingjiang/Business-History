#!/usr/bin/env python3
"""Fix Workday URLs and suspend geo-blocked companies in config.py"""
import re

CONFIG_PATH = "config.py"
with open(CONFIG_PATH, "r") as f:
    content = f.read()

# Companies confirmed working (200) in WORKDAY_EXPANSION_2
working = {"Zoom", "Walmart", "Unilever", "Coca-Cola", "Roche", "Novartis", "Sanofi", "Medtronic", "Micron"}

# Fix Caterpillar URL: caterpillar.wd5 -> cat.wd5
content = content.replace("https://caterpillar.wd5.myworkdayjobs.com/CaterpillarCareers", "https://cat.wd5.myworkdayjobs.com/CaterpillarCareers")
print("Fixed Caterpillar URL")

# Fix VMware -> Broadcom
content = content.replace("https://vmware.wd1.myworkdayjobs.com/VMware", "https://broadcom.wd1.myworkdayjobs.com/External_Career")
print("Fixed VMware->Broadcom URL")

# Fix GM URL: gm.wd5 -> generalmotors.wd5
content = content.replace("https://gm.wd5.myworkdayjobs.com/Careers_GM", "https://generalmotors.wd5.myworkdayjobs.com/Careers_GM")
print("Fixed GM URL")

# Now add status="geo_blocked" to all non-working EXPANSION_2 entries
import config
geo_blocked_names = [c.name for c in config.WORKDAY_EXPANSION_2 if c.name not in working]
print(f"Geo-blocking {len(geo_blocked_names)} companies")

for name in geo_blocked_names:
    escaped = re.escape(name)
    pattern = r'(CompanyConfig\("' + escaped + r'",\s*"workday"[^)]*?display_name="[^"]*"\))'
    match = re.search(pattern, content)
    if match:
        old = match.group(1)
        if 'status=' not in old:
            new = old[:-1] + ', status="geo_blocked")'
            content = content.replace(old, new, 1)
        else:
            print(f"  Already has status: {name}")
    else:
        print(f"  WARN: not found: {name}")

with open(CONFIG_PATH, "w") as f:
    f.write(content)
print("Done!")

#!/usr/bin/env python3
"""
Fix Workday URLs in config.py:
1. Suspend geo-blocked companies (422 from China IP)
2. Fix known URL corrections (Caterpillar, VMware->Broadcom)
3. Keep working ones as-is
"""
import re

CONFIG_PATH = "/Users/pingjiangli/Code/Business-History/crawler/config.py"

# Companies confirmed working (200) from our batch test
WORKING = {
    "NVIDIA", "Intel", "HP", "Adobe", "3M", "GE Aerospace", "Pfizer",
    "Red Hat", "Visa", "Mastercard", "Samsung SEC", "Dell", "Shell",
    "Cisco", "Salesforce", "Broadcom", "Zoom", "Walmart", "Unilever",
    "Coca-Cola", "Roche", "Novartis", "Sanofi", "Medtronic", "Micron",
    "Meta",  # Meta uses metacareers not workday - will handle separately
}

# Companies returning 422 (geo-blocked) - suspend them
GEO_BLOCKED_422 = [
    "Datadog", "VMware", "Snowflake", "Fortinet", "Pure Storage",
    "Cloudflare", "MongoDB", "Elastic", "SAP", "Oracle", "IBM",
    "Starbucks", "IKEA", "P&G", "Adidas", "L'Oreal", "Nestle",
    "PepsiCo", "McDonald's", "H&M", "Eli Lilly", "Johnson & Johnson",
    "GSK", "Merck/MSD", "BMS", "Bayer", "Novo Nordisk",
    "BASF", "Honeywell", "Ford", "GM", "Emerson",
    "TotalEnergies", "ExxonMobil", "Volvo", "Philips",
    "Goldman Sachs", "Morgan Stanley", "JP Morgan", "BlackRock",
    "Deloitte", "EY", "PwC", "KPMG", "McKinsey", "BCG", "Bain",
    "Qualcomm", "Texas Instruments", "Applied Materials",
    "Western Digital", "LVMH", "Estee Lauder",
]

# URL fixes for companies that work but have wrong URL
URL_FIXES = {
    "Caterpillar": "https://cat.wd5.myworkdayjobs.com/CaterpillarCareers",
    # VMware is now under Broadcom
    "VMware": "https://broadcom.wd1.myworkdayjobs.com/External_Career",
}

# Companies to remove from geo-blocked list if they have alternative adapters
# (Meta uses metacareers.com not workday, keep as-is for now)

def main():
    with open(CONFIG_PATH, "r") as f:
        content = f.read()

    changes = 0

    # 1. Fix URL corrections
    for company, new_url in URL_FIXES.items():
        # Find the company config and update URL
        pattern = rf'(CompanyConfig\(\s*name="{re.escape(company)}"[^)]*?url=")[^"]*(")'
        match = re.search(pattern, content)
        if match:
            content = content[:match.start(1)] + match.group(1) + new_url + match.group(2) + content[match.end(2):]
            print(f"  Fixed URL: {company} -> {new_url}")
            changes += 1
        else:
            print(f"  WARNING: Could not find {company} to fix URL")

    # 2. Suspend geo-blocked companies
    for company in GEO_BLOCKED_422:
        # Find status="active" for this company and change to status="suspended"
        pattern = rf'(CompanyConfig\(\s*name="{re.escape(company)}"[^)]*?)status="active"'
        match = re.search(pattern, content)
        if match:
            content = content[:match.start()] + match.group(1) + 'status="geo_blocked"' + content[match.end():]
            print(f"  Suspended (geo_blocked): {company}")
            changes += 1
        else:
            # Maybe already not active
            pattern2 = rf'name="{re.escape(company)}"'
            if re.search(pattern2, content):
                print(f"  Skipped (not active): {company}")
            else:
                print(f"  WARNING: Not found: {company}")

    # 3. Also fix Meta - it doesn't use Workday anymore, uses metacareers.com
    # Mark as suspended since the workday URL doesn't work
    pattern = r'(CompanyConfig\(\s*name="Meta"[^)]*?)status="active"'
    match = re.search(pattern, content)
    if match:
        content = content[:match.start()] + match.group(1) + 'status="geo_blocked"' + content[match.end():]
        print(f"  Suspended (geo_blocked): Meta")
        changes += 1

    # Nike returns 404 (wrong tenant entirely)
    pattern = r'(CompanyConfig\(\s*name="Nike"[^)]*?)status="active"'
    match = re.search(pattern, content)
    if match:
        content = content[:match.start()] + match.group(1) + 'status="geo_blocked"' + content[match.end():]
        print(f"  Suspended (geo_blocked): Nike")
        changes += 1

    with open(CONFIG_PATH, "w") as f:
        f.write(content)

    print(f"\nTotal changes: {changes}")
    print("Done! Run `python3 -c 'import config; ...'` to verify.")


if __name__ == "__main__":
    main()

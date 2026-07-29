"""Discover ICBC official API endpoints for social recruitment jobs."""
import httpx
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
ctx.options |= 0x4  # Enable legacy renegotiation

c = httpx.Client(follow_redirects=True, verify=ctx, timeout=15)

base = "https://job.icbc.com.cn/icbc/trmo"

# Test post/qryPostType with different recruitTypes
print("=== ICBC post/qryPostType ===")
for rt in ["R00301", "R00302", "R00303", "R00304"]:
    r = c.post(f"{base}/post/qryPostType", json={"recruitType": rt}, 
               headers={"Content-Type": "application/json"}, timeout=10)
    data = r.json()
    items = data.get("data", {}).get("dataList", [])
    if items:
        print(f"  recruitType={rt}: {len(items)} post types")
        for i in items[:3]:
            print(f"    {i.get('postTypeId')} - {i.get('postName')}")

# Try to find the actual job listing endpoint
print("\n=== Testing other endpoints ===")
endpoints = [
    "/slide/list",
    "/news/list", 
    "/branchDynamic/list",
    "/specialTopic/list",
]

for ep in endpoints:
    try:
        r = c.post(f"{base}{ep}", json={"pageNum": 1, "pageSize": 5},
                   headers={"Content-Type": "application/json"}, timeout=10)
        data = r.json()
        if data.get("retCode") == "0":
            print(f"  {ep}: SUCCESS - {json.dumps(data, ensure_ascii=False)[:200]}")
        else:
            print(f"  {ep}: {data.get('retMsg', 'unknown')}")
    except Exception as e:
        print(f"  {ep}: ERROR - {e}")

# The ICBC site is a complex SPA - the announ endpoint needs specific params
# Let's try to find what params announ/qryAnnounList needs
print("\n=== Testing announ/qryAnnounList with various params ===")
param_combos = [
    {"pageNum": 1, "pageSize": 10, "recruitType": "R00301", "postTypeId": "D00001"},
    {"pageNum": 1, "pageSize": 10, "recruitType": "R00302", "postTypeId": ""},
    {"pageNum": "1", "pageSize": "10", "recruitType": "R00301"},
    {"pageNum": 1, "pageSize": 10},
]

for params in param_combos:
    r = c.post(f"{base}/announ/qryAnnounList", json=params,
               headers={"Content-Type": "application/json"}, timeout=10)
    data = r.json()
    if data.get("retCode") == "0":
        print(f"  params={params}: SUCCESS!")
        print(f"    data={json.dumps(data, ensure_ascii=False)[:300]}")
    else:
        print(f"  params={params}: {data.get('retMsg')}")

# Also check 交通银行
print("\n=== 交通银行 job.bankcomm.com ===")
r = c.get("https://job.bankcomm.com", timeout=10)
print(f"  Status: {r.status_code}, len={len(r.text)}")
# It's a Vue SPA, check for API paths in the JS
import re
scripts = re.findall(r'src="([^"]+\.js)"', r.text)
print(f"  JS files: {scripts}")

# Check 建设银行
print("\n=== 建设银行 job.ccb.com ===")
r = c.get("https://job.ccb.com", timeout=10)
print(f"  Status: {r.status_code}, len={len(r.text)}")
print(f"  Content: {r.text[:500]}")

# Check 农业银行
print("\n=== 农业银行 career.abchina.com ===")
r = c.get("https://career.abchina.com", timeout=10)
print(f"  Status: {r.status_code}, len={len(r.text)}")
print(f"  Content: {r.text[:500]}")

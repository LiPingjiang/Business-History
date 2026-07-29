"""Check official career websites for banks that left zhiye.com"""
import httpx

banks_to_check = [
    ("招商银行", "https://career.cmbchina.com"),
    ("交通银行", "https://job.bankcomm.com"),
    ("邮储银行", "https://www.psbc.com/cn/grfw/rczp/"),
    ("工商银行", "https://job.icbc.com.cn"),
    ("农业银行", "https://career.abchina.com"),
    ("建设银行", "https://job.ccb.com"),
    ("中国银行", "https://career.bankofchina.com"),
    ("广发银行", "https://www.cgbchina.com.cn/Channel/16000100"),
    ("北京农商银行", "https://www.bjrcb.com/nsh/rczp/index.html"),
    ("渤海银行", "https://www.cbhb.com.cn/bhbank/S101/renCaiZhaoPin"),
    ("恒丰银行", "https://www.hfbank.com.cn/gywm/rczp/index.shtml"),
]

# Also check央企 that were on zhiye_pw
soe_to_check = [
    ("中国建筑", "https://hr.cscec.com"),
    ("中国船舶", "https://www.cssc.net.cn/n7/index.html"),
    ("中国核工业", "https://hr.cnnc.com.cn"),
    ("中国能建", "https://hr.ceec.net.cn"),
    ("中国航天科工", "https://zhaopin.casic.cn"),
]

c = httpx.Client(follow_redirects=True, verify=False, timeout=15, headers={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
})

print("=" * 80)
print("银行官网招聘页面检查:")
print("=" * 80)
for name, url in banks_to_check:
    try:
        r = c.get(url, timeout=10)
        ok = r.status_code < 400 and len(r.text) > 500
        status = "OK" if ok else "FAIL"
        print(f"  {name:<10} {status:5} status={r.status_code} len={len(r.text):>6} url={str(r.url)[:60]}")
    except Exception as e:
        print(f"  {name:<10} ERROR {str(e)[:50]}")

print()
print("=" * 80)
print("央企官网招聘页面检查:")
print("=" * 80)
for name, url in soe_to_check:
    try:
        r = c.get(url, timeout=10)
        ok = r.status_code < 400 and len(r.text) > 500
        status = "OK" if ok else "FAIL"
        print(f"  {name:<10} {status:5} status={r.status_code} len={len(r.text):>6} url={str(r.url)[:60]}")
    except Exception as e:
        print(f"  {name:<10} ERROR {str(e)[:50]}")

# For banks that have official sites, check if they have API endpoints
print()
print("=" * 80)
print("尝试发现银行官网API:")
print("=" * 80)

# 招商银行 career site
try:
    r = c.get("https://career.cmbchina.com", timeout=10)
    print(f"  招商银行 career.cmbchina.com: status={r.status_code} url={str(r.url)[:80]}")
    if r.status_code < 400:
        import re
        apis = re.findall(r'(https?://[^\s"\'<>]+(?:api|job|position|recruit)[^\s"\'<>]*)', r.text[:5000])
        if apis:
            print(f"    Found APIs: {apis[:5]}")
except Exception as e:
    print(f"  招商银行 ERROR: {e}")

# 工商银行
try:
    r = c.get("https://job.icbc.com.cn", timeout=10)
    print(f"  工商银行 job.icbc.com.cn: status={r.status_code} url={str(r.url)[:80]}")
except Exception as e:
    print(f"  工商银行 ERROR: {e}")

# 建设银行
try:
    r = c.get("https://job.ccb.com", timeout=10)
    print(f"  建设银行 job.ccb.com: status={r.status_code} url={str(r.url)[:80]}")
except Exception as e:
    print(f"  建设银行 ERROR: {e}")

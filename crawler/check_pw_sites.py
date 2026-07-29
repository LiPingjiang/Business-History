"""Check which zhiye_pw sites are dead (404) vs alive, and identify the real problem."""
import httpx

c = httpx.Client(follow_redirects=True, verify=False, timeout=15)

# All zhiye_pw companies
zhiye_pw_urls = [
    ("招商银行", "https://cmbchina.zhiye.com/Social"),
    ("交通银行", "https://bankcomm.zhiye.com/Social"),
    ("邮储银行", "https://psbc.zhiye.com/Social"),
    ("工商银行", "https://icbc.zhiye.com/Social"),
    ("农业银行", "https://abchina.zhiye.com/Social"),
    ("建设银行", "https://ccb.zhiye.com/Social"),
    ("中国银行", "https://boc.zhiye.com/Social"),
    ("广发银行", "https://cgbchina.zhiye.com/Social"),
    ("北京农商银行", "https://bjrcb.zhiye.com/Social"),
    ("渤海银行", "https://cbhb.zhiye.com/Social"),
    ("恒丰银行", "https://hfbank.zhiye.com/Social"),
    ("中国建筑", "https://cscec.zhiye.com/Social"),
    ("中国船舶", "https://cssc.zhiye.com/Social"),
    ("中国核工业", "https://cnnc.zhiye.com/Social"),
    ("中国能建", "https://ceec.zhiye.com/Social"),
    ("中国航天科工", "https://casic.zhiye.com/Social"),
]

print("=" * 80)
print("zhiye_pw 企业站点状态检查")
print("=" * 80)
print(f"{'企业':<12} {'状态':<8} {'最终URL'}")
print("-" * 80)

dead_sites = []
alive_sites = []

for name, url in zhiye_pw_urls:
    try:
        r = c.get(url)
        final_url = str(r.url)
        if "404" in final_url or "Not Found" in r.text[:200]:
            status = "❌ 404"
            dead_sites.append(name)
        elif "info?message" in final_url or "暂停招聘" in r.text[:500]:
            status = "⚠️ 暂停"
            dead_sites.append(name)
        else:
            status = "✓ 正常"
            alive_sites.append(name)
        print(f"  {name:<12} {status:<8} {final_url[:60]}")
    except Exception as e:
        print(f"  {name:<12} ✗ ERROR  {str(e)[:50]}")
        dead_sites.append(name)

# Also check hotjob_pw sites
print("\n" + "=" * 80)
print("hotjob_pw 企业站点状态检查")
print("=" * 80)

hotjob_pw_urls = [
    ("中国移动九天", "https://wecruit.hotjob.cn/SU60fa4d4e2f9d247b98de3fdc/pb/social.html"),
    ("中国信通院", "https://wecruit.hotjob.cn/SU642fbf5fbef57c1e269fa798/pb/social.html"),
    ("中国华电", "https://chd.hotjob.cn"),
    ("中国中车", "https://crrc.hotjob.cn/SU64d47c466202cc36e27a52d4/pb/social.html"),
    ("一汽大众", "https://faw-vw.hotjob.cn"),
    ("中化集团", "https://sinochem.hotjob.cn"),
    ("华夏银行", "https://hxb.hotjob.cn/SU645b0d18bef57c0907e9fbc8/pb/social.html"),
    ("兴业银行", "https://job.cib.com.cn/portal/"),
    ("光大银行", "https://eoap.cebbank.com/uiap/wt/CEB/zpzh/social"),
]

for name, url in hotjob_pw_urls:
    try:
        r = c.get(url)
        final_url = str(r.url)
        ct = r.headers.get("content-type", "")
        has_content = len(r.text) > 500
        if r.status_code >= 400:
            status = f"❌ {r.status_code}"
            dead_sites.append(name)
        elif has_content:
            status = "✓ 正常"
            alive_sites.append(name)
        else:
            status = "? 空"
            dead_sites.append(name)
        print(f"  {name:<12} {status:<8} {final_url[:60]}")
    except Exception as e:
        print(f"  {name:<12} ✗ ERROR  {str(e)[:50]}")
        dead_sites.append(name)

# Also check custom_pw and other PW sites
print("\n" + "=" * 80)
print("custom_pw/其他 Playwright 企业站点状态检查")
print("=" * 80)

other_pw_urls = [
    ("Microsoft", "https://apply.careers.microsoft.com"),
    ("Siemens", "https://jobs.siemens.com.cn/siemens/position/index"),
    ("BMW/领悦", "https://careersite.tupu360.com/bmw/position/index"),
    ("中国石化", "https://job.sinopec.com"),
    ("中国华能", "https://zhaopin.chng.com.cn"),
    ("中国南方电网", "https://zhaopin.csg.cn"),
    ("中国大唐", "https://zhaopin.china-cdt.com"),
    ("中国石油", "https://zhaopin.cnpc.com.cn"),
    ("中国海油", "https://cnooc.zhaopin.com"),
]

for name, url in other_pw_urls:
    try:
        r = c.get(url)
        final_url = str(r.url)
        if r.status_code >= 400:
            status = f"❌ {r.status_code}"
        elif len(r.text) > 500:
            status = "✓ 正常"
        else:
            status = "? 空"
        print(f"  {name:<12} {status:<8} {final_url[:60]}")
    except Exception as e:
        print(f"  {name:<12} ✗ ERROR  {str(e)[:50]}")

print("\n" + "=" * 80)
print(f"总结: {len(dead_sites)} 个站点已失效, {len(alive_sites)} 个站点正常")
print(f"失效站点: {', '.join(dead_sites)}")
print("=" * 80)

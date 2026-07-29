#!/usr/bin/env python3
"""Test all央企 zhiye.com URLs to see which ones work with our zhiye adapter."""
import requests

zhiye_urls = [
    ("中国航发", "https://aecc.zhiye.com/"),
    ("鞍钢集团", "https://ansteel.zhiye.com/"),
    ("中国航空工业", "https://avic.zhiye.com/"),
    ("中国航天科工", "https://casic.zhiye.com/"),
    ("中国航天科技", "https://cast.zhiye.com/"),
    ("中国交建", "https://cccc.zhiye.com/"),
    ("中国电子", "https://cec.zhiye.com/"),
    ("中国节能", "https://cecep.zhiye.com/"),
    ("中国能建", "https://ceec.zhiye.com/"),
    ("中国电科", "https://cetc.zhiye.com/"),
    ("中国一重", "https://cfhi.zhiye.com/"),
    ("中国广核", "https://cgnpc.zhiye.com/"),
    ("中国诚通", "https://chengtong.zhiye.com/"),
    ("中国黄金", "https://chinagold.zhiye.com/"),
    ("中国铝业", "https://chinalco.zhiye.com/"),
    ("中国盐业", "https://chinasalt.zhiye.com/"),
    ("中国建材", "https://cnbm.zhiye.com/"),
    ("中国化学", "https://cncec.zhiye.com/"),
    ("中国核工业", "https://cnnc.zhiye.com/"),
    ("中国商飞", "https://comac.zhiye.com/"),
    ("中国远洋海运", "https://coscoshipping.zhiye.com/"),
    ("中国铁建", "https://crcc.zhiye.com/"),
    ("中国建筑", "https://cscec.zhiye.com/"),
    ("中国船舶", "https://cssc.zhiye.com/"),
    ("中国三峡", "https://ctg.zhiye.com/"),
    ("东风汽车", "https://dfmc.zhiye.com/"),
    ("东方电气", "https://dongfang.zhiye.com/"),
    ("中国一汽", "https://faw.zhiye.com/"),
    ("哈尔滨电气", "https://harbin-electric.zhiye.com/"),
    ("中国华录", "https://hualu.zhiye.com/"),
    ("中国冶金", "https://mcc.zhiye.com/"),
    ("中国五矿", "https://minmetals.zhiye.com/"),
    ("中国兵器", "https://norincogroup.zhiye.com/"),
    ("中国保利", "https://poly.zhiye.com/"),
    ("中国电建", "https://powerchina.zhiye.com/"),
    ("国家开发投资", "https://sdic.zhiye.com/"),
    ("中国储备粮", "https://sinograin.zhiye.com/"),
    ("中国机械", "https://sinomach.zhiye.com/"),
    ("中国南光", "https://csgc.zhiye.com/"),
]

print(f"Testing {len(zhiye_urls)} 央企 zhiye.com URLs...")
print()

works = []
fails = []

for name, url in zhiye_urls:
    base = url.rstrip("/")
    api_url = f"{base}/api/Jobad/GetJobAdPageList"
    try:
        # Try pageIndex=1 first
        r = requests.post(api_url, json={"pageIndex": 1, "pageSize": 20},
                         headers={"Content-Type": "application/json"}, timeout=10)
        if r.status_code == 200 and "json" in r.headers.get("content-type", ""):
            d = r.json()
            count = d.get("Count", 0)
            page_jobs = len(d.get("Data", []))
            if count > 0 and page_jobs == 0:
                # Try 0-based
                r2 = requests.post(api_url, json={"pageIndex": 0, "pageSize": 20},
                                  headers={"Content-Type": "application/json"}, timeout=10)
                if r2.status_code == 200:
                    d2 = r2.json()
                    page_jobs = len(d2.get("Data", []))
            if count > 0:
                print(f"✅ {name}: Count={count}, PageJobs={page_jobs} | {url}")
                works.append((name, url, count))
            else:
                print(f"⚠️  {name}: Count=0 (暂无岗位) | {url}")
                works.append((name, url, 0))
        else:
            print(f"❌ {name}: HTTP {r.status_code} or not JSON")
            fails.append((name, url))
    except Exception as e:
        print(f"❌ {name}: ERR {str(e)[:50]}")
        fails.append((name, url))

print(f"\n=== Summary ===")
print(f"✅ API可用: {len(works)} 家 (其中有岗位: {len([w for w in works if w[2]>0])})")
print(f"❌ API不可用: {len(fails)} 家")

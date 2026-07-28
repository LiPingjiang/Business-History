#!/usr/bin/env python3
"""Test which regional banks use zhiye.com (beisen) platform and have active positions."""
import requests

banks = [
    ("北京银行", "https://bankofbeijing.zhiye.com"),
    ("上海银行", "https://bosc.zhiye.com"),
    ("江苏银行", "https://jsbchina.zhiye.com"),
    ("宁波银行", "https://nbcb.zhiye.com"),
    ("平安银行", "https://pingan-bank.zhiye.com"),
    ("浙商银行", "https://czbank.zhiye.com"),
    ("徽商银行", "https://hsbank.zhiye.com"),
    ("长沙银行", "https://csbank.zhiye.com"),
    ("杭州银行", "https://hzbank.zhiye.com"),
    ("南京银行", "https://njcb.zhiye.com"),
    ("成都银行", "https://cdbank.zhiye.com"),
    ("郑州银行", "https://zzbank.zhiye.com"),
    ("青岛银行", "https://qdccb.zhiye.com"),
    ("贵阳银行", "https://gybank.zhiye.com"),
    ("西安银行", "https://xacbank.zhiye.com"),
    ("齐鲁银行", "https://qlbchina.zhiye.com"),
    ("重庆银行", "https://cqcbank.zhiye.com"),
    ("天津银行", "https://tccb.zhiye.com"),
]

# Also test research institutions
research = [
    ("中科院计算所", "https://ict.zhiye.com"),
    ("中科院软件所", "https://iscas.zhiye.com"),
    ("中科院信工所", "https://iie.zhiye.com"),
    ("中科院数学所", "https://amss.zhiye.com"),
    ("国家信息中心", "https://sic.zhiye.com"),
    ("中国电科", "https://cetc.zhiye.com"),
    ("航天科技", "https://casc.zhiye.com"),
    ("中国电子", "https://cec.zhiye.com"),
]

print("=== Banks ===")
for n, u in banks:
    try:
        r = requests.post(
            u + "/api/Jobad/GetJobAdPageList",
            json={"pageIndex": 1, "pageSize": 50},
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        if r.status_code == 200:
            try:
                d = r.json()
                cnt = d.get("Count", 0)
                page_jobs = len(d.get("Data", []))
                print(f"{n}: Count={cnt}, PageJobs={page_jobs}")
            except Exception:
                print(f"{n}: HTTP 200 but not JSON")
        else:
            print(f"{n}: HTTP {r.status_code}")
    except Exception as e:
        print(f"{n}: ERR {str(e)[:60]}")

print("\n=== Research Institutions ===")
for n, u in research:
    try:
        r = requests.post(
            u + "/api/Jobad/GetJobAdPageList",
            json={"pageIndex": 1, "pageSize": 50},
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        if r.status_code == 200:
            try:
                d = r.json()
                cnt = d.get("Count", 0)
                page_jobs = len(d.get("Data", []))
                print(f"{n}: Count={cnt}, PageJobs={page_jobs}")
            except Exception:
                print(f"{n}: HTTP 200 but not JSON")
        else:
            print(f"{n}: HTTP {r.status_code}")
    except Exception as e:
        print(f"{n}: ERR {str(e)[:60]}")

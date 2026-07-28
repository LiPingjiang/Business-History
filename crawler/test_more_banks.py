#!/usr/bin/env python3
"""Test more regional banks and research institutions for zhiye.com API availability."""
import requests

more_banks = [
    ("长沙银行", "https://cscb.zhiye.com"),
    ("成都银行", "https://cdbank.zhiye.com"),
    ("重庆银行", "https://cqcbank.zhiye.com"),
    ("齐鲁银行", "https://qlbchina.zhiye.com"),
    ("青岛银行", "https://qdccb.zhiye.com"),
    ("贵阳银行", "https://gybank.zhiye.com"),
    ("西安银行", "https://xacbank.zhiye.com"),
    ("郑州银行", "https://zzbank.zhiye.com"),
    ("徽商银行", "https://hsbank.zhiye.com"),
    ("厦门银行", "https://xmccb.zhiye.com"),
    ("兰州银行", "https://lzbank.zhiye.com"),
    ("苏州银行", "https://szbank.zhiye.com"),
    ("威海银行", "https://whccb.zhiye.com"),
    ("甘肃银行", "https://gsbank.zhiye.com"),
    ("盛京银行", "https://sjbank.zhiye.com"),
    ("哈尔滨银行", "https://hrbb.zhiye.com"),
    ("温州银行", "https://wzbank.zhiye.com"),
    ("中原银行", "https://zybank.zhiye.com"),
    ("晋商银行", "https://jsbank.zhiye.com"),
    ("九江银行", "https://jjccb.zhiye.com"),
    ("汉口银行", "https://hkbank.zhiye.com"),
    ("东莞银行", "https://dgbank.zhiye.com"),
    ("广州银行", "https://gzbank.zhiye.com"),
    ("锦州银行", "https://jzbank.zhiye.com"),
]

research_institutions = [
    ("中科院计算所", "https://ict.zhiye.com"),
    ("中科院软件所", "https://iscas.zhiye.com"),
    ("中科院信工所", "https://iie.zhiye.com"),
    ("中国电科", "https://cetc.zhiye.com"),
    ("航天科技", "https://casc.zhiye.com"),
    ("中国电子", "https://cec.zhiye.com"),
    ("国家电网", "https://sgcc.zhiye.com"),
    ("中国航发", "https://aecc.zhiye.com"),
    ("中国船舶", "https://cssc.zhiye.com"),
    ("中核集团", "https://cnnc.zhiye.com"),
    ("中国兵器", "https://norinco.zhiye.com"),
    ("中国航天科工", "https://casic.zhiye.com"),
    ("中国电信", "https://chinatelecom.zhiye.com"),
    ("国家开发银行", "https://cdb.zhiye.com"),
    ("中国进出口银行", "https://eximbank.zhiye.com"),
    ("中国农业发展银行", "https://adbc.zhiye.com"),
]

print("=== Regional Banks ===")
for n, u in more_banks:
    try:
        r = requests.post(
            u + "/api/Jobad/GetJobAdPageList",
            json={"pageIndex": 1, "pageSize": 20},
            headers={"Content-Type": "application/json"},
            timeout=8,
        )
        ct = r.headers.get("content-type", "")
        if "json" in ct:
            d = r.json()
            cnt = d.get("Count", 0)
            page_jobs = len(d.get("Data", []))
            print(f"✅ {n}: Count={cnt}, PageJobs={page_jobs} | {u}")
        else:
            print(f"❌ {n}: NO-JSON (HTML response)")
    except Exception as e:
        print(f"❌ {n}: ERR {str(e)[:50]}")

print("\n=== Research/SOE Institutions ===")
for n, u in research_institutions:
    try:
        r = requests.post(
            u + "/api/Jobad/GetJobAdPageList",
            json={"pageIndex": 1, "pageSize": 20},
            headers={"Content-Type": "application/json"},
            timeout=8,
        )
        ct = r.headers.get("content-type", "")
        if "json" in ct:
            d = r.json()
            cnt = d.get("Count", 0)
            page_jobs = len(d.get("Data", []))
            print(f"✅ {n}: Count={cnt}, PageJobs={page_jobs} | {u}")
        else:
            print(f"❌ {n}: NO-JSON (HTML response)")
    except Exception as e:
        print(f"❌ {n}: ERR {str(e)[:50]}")

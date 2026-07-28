#!/usr/bin/env python3
"""Get all 北京银行 jobs with pagination and filter for tech positions."""
import requests

all_jobs = []
page = 1
while True:
    r = requests.post(
        'https://bankofbeijing.zhiye.com/api/Jobad/GetJobAdPageList',
        json={'pageIndex': page, 'pageSize': 20},
        headers={'Content-Type': 'application/json'},
        timeout=10,
    )
    d = r.json()
    jobs = d.get('Data', [])
    if not jobs:
        break
    all_jobs.extend(jobs)
    page += 1

print(f"北京银行 Total: {len(all_jobs)} jobs")
tech_keywords = ['数据', '研发', '技术', '科技', 'IT', '系统', '开发', '软件', '信息', '架构', '运维', '安全', '算法', '测试', '网络']
tech = [j for j in all_jobs if any(k in j.get('JobAdName', '') for k in tech_keywords)]
print(f"Tech/Data jobs: {len(tech)}")
for j in tech:
    print(f"  {j.get('JobAdName', '')[:60]}")

# Now test 上海银行 with pagination
print("\n--- 上海银行 ---")
all_jobs2 = []
page = 1
while True:
    r = requests.post(
        'https://bosc.zhiye.com/api/Jobad/GetJobAdPageList',
        json={'pageIndex': page, 'pageSize': 50},
        headers={'Content-Type': 'application/json'},
        timeout=10,
    )
    d = r.json()
    jobs = d.get('Data', [])
    if not jobs:
        break
    all_jobs2.extend(jobs)
    page += 1

print(f"上海银行 Total: {len(all_jobs2)} jobs")
tech2 = [j for j in all_jobs2 if any(k in j.get('JobAdName', '') for k in tech_keywords)]
print(f"Tech/Data jobs: {len(tech2)}")
for j in tech2:
    print(f"  {j.get('JobAdName', '')[:60]}")

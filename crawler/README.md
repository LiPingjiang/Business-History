# 招聘岗位每日爬取系统

## 目录结构

```
crawler/
├── config.py          # 全局配置 + 企业列表
├── runner.py          # 主调度器（每日运行入口）
├── models.py          # 数据模型
├── output.py          # 输出：JSON存储 + Markdown diff报告
├── adapters/
│   ├── __init__.py
│   ├── base.py        # Adapter基类
│   ├── workday.py     # Workday平台（18家）
│   ├── zhiye.py       # 北森zhiye.com（7家）
│   ├── hotjob.py      # hotjob.cn（6家）
│   ├── oracle_hcm.py  # Oracle HCM Cloud（4家）
│   ├── eightfold.py   # Eightfold.ai（2家）
│   ├── amazon.py      # Amazon Jobs
│   ├── microsoft.py   # Microsoft Careers
│   ├── siemens.py     # Siemens China
│   └── bmw.py         # BMW/tupu360
├── data/              # 每日爬取结果存储
│   └── .gitkeep
└── requirements.txt
```

## 运行方式

```bash
cd crawler
pip install -r requirements.txt
python runner.py              # 全量爬取
python runner.py --diff       # 只输出与上次的差异
python runner.py --adapter workday  # 只跑某个adapter
```

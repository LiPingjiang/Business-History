"""全局配置 + 企业列表"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path

# 路径
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# 请求配置
REQUEST_TIMEOUT = 15
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Accept": "application/json, text/html, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

# 搜索关键词（用于过滤北京+数据/研发岗位）
LOCATION_KEYWORDS = ["北京", "Beijing", "beijing", "China"]
JOB_KEYWORDS = [
    "data", "大数据", "数据", "big data", "engineer", "研发", "开发",
    "backend", "后端", "Java", "Python", "Spark", "Flink", "Kafka",
    "AI", "agent", "智能体", "平台", "架构", "algorithm", "算法",
    "machine learning", "机器学习", "大模型", "LLM",
]


@dataclass
class CompanyConfig:
    """单个企业爬取配置"""
    name: str              # 企业名称
    adapter: str           # adapter名称
    url: str               # 招聘页面URL
    params: dict = field(default_factory=dict)  # adapter特定参数


# ============================================================
# Phase 1: 平台级 Adapter 企业列表
# ============================================================

WORKDAY_COMPANIES = [
    CompanyConfig("NVIDIA", "workday", "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite",
                  params={"location": "China"}),
    CompanyConfig("Intel", "workday", "https://intel.wd1.myworkdayjobs.com/External",
                  params={"location": "China"}),
    CompanyConfig("HP", "workday", "https://hp.wd5.myworkdayjobs.com/ExternalCareerSite",
                  params={"location": "China"}),
    CompanyConfig("Adobe", "workday", "https://adobe.wd5.myworkdayjobs.com/external_experienced",
                  params={"location": "China"}),
    CompanyConfig("3M", "workday", "https://3m.wd1.myworkdayjobs.com/Search",
                  params={"location": "China"}),
    CompanyConfig("GE Aerospace", "workday", "https://geaerospace.wd5.myworkdayjobs.com/GE_ExternalSite",
                  params={"location": "China"}),
    CompanyConfig("Pfizer", "workday", "https://pfizer.wd1.myworkdayjobs.com/PfizerCareers",
                  params={"location": "China"}),
    CompanyConfig("Red Hat", "workday", "https://redhat.wd5.myworkdayjobs.com/jobs",
                  params={"location": "China"}),
    CompanyConfig("Visa", "workday", "https://visa.wd5.myworkdayjobs.com/Visa",
                  params={"location": "China"}),
    CompanyConfig("Mastercard", "workday", "https://mastercard.wd1.myworkdayjobs.com/CorporateCareers",
                  params={"location": "China"}),
    CompanyConfig("Samsung SEC", "workday", "https://sec.wd3.myworkdayjobs.com/Samsung_Careers",
                  params={"location": "China"}),
]

ZHIYE_COMPANIES = [
    CompanyConfig("航天科工", "zhiye", "https://casic.zhiye.com",
                  params={"type": "social"}),
    CompanyConfig("三星中国", "zhiye", "https://dearsamsung.zhiye.com",
                  params={"type": "social"}),
    CompanyConfig("联通数科", "zhiye", "https://cudt.zhiye.com",
                  params={"type": "social"}),
    CompanyConfig("联通数智", "zhiye", "https://cudataintelligence.zhiye.com",
                  params={"type": "social"}),
    CompanyConfig("中科院自动化所", "zhiye", "https://casia.zhiye.com",
                  params={"type": "social"}),
]

HOTJOB_COMPANIES = [
    CompanyConfig("中国移动九天", "hotjob", "https://wecruit.hotjob.cn/SU60fa4d4e2f9d247b98de3fdc/pb/social.html",
                  params={"su_id": "SU60fa4d4e2f9d247b98de3fdc"}),
    CompanyConfig("中国信通院", "hotjob", "https://wecruit.hotjob.cn/SU642fbf5fbef57c1e269fa798/pb/social.html",
                  params={"su_id": "SU642fbf5fbef57c1e269fa798"}),
    CompanyConfig("中国华电", "hotjob", "https://chd.hotjob.cn",
                  params={"su_id": "chd"}),
    CompanyConfig("中国中车", "hotjob", "https://crrc.hotjob.cn/SU64d47c466202cc36e27a52d4/pb/social.html",
                  params={"su_id": "SU64d47c466202cc36e27a52d4"}),
    CompanyConfig("一汽大众", "hotjob", "https://faw-vw.hotjob.cn",
                  params={"su_id": "faw-vw"}),
    CompanyConfig("中化集团", "hotjob", "https://sinochem.hotjob.cn",
                  params={"su_id": "sinochem"}),
]

# ============================================================
# Phase 2: 高价值自建站
# ============================================================

CUSTOM_COMPANIES = [
    CompanyConfig("Amazon", "amazon", "https://www.amazon.jobs/en/search",
                  params={"base_query": "data engineer", "loc_query": "Beijing, China"}),
    CompanyConfig("Microsoft", "microsoft", "https://apply.careers.microsoft.com",
                  params={"location": "Beijing"}),
    CompanyConfig("Siemens", "siemens", "https://jobs.siemens.com.cn/siemens/position/index",
                  params={"recruitmentType": "SOCIALRECRUITMENT"}),
    CompanyConfig("BMW/领悦", "bmw", "https://careersite.tupu360.com/bmw/position/index",
                  params={"recruitmentType": "SOCIALRECRUITMENT"}),
]

# 汇总所有企业
ALL_COMPANIES = WORKDAY_COMPANIES + ZHIYE_COMPANIES + HOTJOB_COMPANIES + CUSTOM_COMPANIES

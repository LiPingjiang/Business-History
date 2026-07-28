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
    CompanyConfig("Dell", "workday", "https://dell.wd1.myworkdayjobs.com/External",
                  params={"location": "China"}),
    CompanyConfig("Shell", "workday", "https://shell.wd3.myworkdayjobs.com/ShellCareers",
                  params={"location": "China"}),
]

ZHIYE_COMPANIES = [
    # 航天科工 casic.zhiye.com 是旧版校招系统，无社招API，跳过
    # CompanyConfig("航天科工", "zhiye", "https://casic.zhiye.com", params={"type": "social"}),
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
    CompanyConfig("中国移动九天", "hotjob_pw", "https://wecruit.hotjob.cn/SU60fa4d4e2f9d247b98de3fdc/pb/social.html",
                  params={"su_id": "SU60fa4d4e2f9d247b98de3fdc"}),
    CompanyConfig("中国信通院", "hotjob_pw", "https://wecruit.hotjob.cn/SU642fbf5fbef57c1e269fa798/pb/social.html",
                  params={"su_id": "SU642fbf5fbef57c1e269fa798"}),
    CompanyConfig("中国华电", "hotjob_pw", "https://chd.hotjob.cn",
                  params={"su_id": "chd"}),
    CompanyConfig("中国中车", "hotjob_pw", "https://crrc.hotjob.cn/SU64d47c466202cc36e27a52d4/pb/social.html",
                  params={"su_id": "SU64d47c466202cc36e27a52d4"}),
    CompanyConfig("一汽大众", "hotjob_pw", "https://faw-vw.hotjob.cn",
                  params={"su_id": "faw-vw"}),
    CompanyConfig("中化集团", "hotjob_pw", "https://sinochem.hotjob.cn",
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
    CompanyConfig("AstraZeneca", "astrazeneca", "https://careers.astrazeneca.com/search-jobs",
                  params={"keywords": "data", "location": "Beijing, China"}),
]

# ============================================================
# Phase 3: SmartRecruiters 平台企业
# ============================================================

SMARTRECRUITERS_COMPANIES = [
    CompanyConfig("博世", "smartrecruiters", "https://jobs.bosch.com",
                  params={"company_id": "BoschGroup", "query": "data", "country": "cn"}),
]

# ============================================================
# Phase 4: 扩展 zhiye.com 央企 (45家)
# ============================================================

# 注：zhiye.com 新版API(/api/Jobad/GetJobAdPageList)仅3家可用: picc, cntaiping, chinalife
# 其余41家央企使用旧版北森Portal系统，API路径不同，暂不支持
ZHIYE_COMPANIES_EXTRA = [
    CompanyConfig("中国人民保险", "zhiye", "https://picc.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国太平保险", "zhiye", "https://cntaiping.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国人寿", "zhiye", "https://chinalife.zhiye.com", params={"type": "social"}),
]

# ============================================================
# Phase 5: 银行 + 事业单位/研究机构
# ============================================================

# 北京银行已在 ZHIYE_COMPANIES 中（bankofbeijing.zhiye.com）
BANK_COMPANIES = [
    CompanyConfig("银行C", "recruitportal", "https://internal://bank-c",
                  params={"workAddr": ["110000"]}),
]

# Mokahr 平台企业（银行+研究机构）
MOKAHR_COMPANIES = [
    CompanyConfig("智源研究院", "mokahr", "https://app.mokahr.com/social-recruitment/baai/42173"),
    CompanyConfig("中信百信银行", "mokahr", "https://app.mokahr.com/social-recruitment/aibank/46870"),
    CompanyConfig("苏商银行", "mokahr", "https://app.mokahr.com/social-recruitment/snb/45591"),
]

# 汇总所有企业
ZHIYE_RESEARCH_COMPANIES = [
    CompanyConfig("中科院自动化所", "zhiye", "https://casia.zhiye.com"),
    CompanyConfig("中金公司", "zhiye", "https://cicc.zhiye.com"),
    CompanyConfig("中国银河证券", "zhiye", "https://chinastock.zhiye.com"),
]

# 汇总所有企业
ALL_COMPANIES = WORKDAY_COMPANIES + ZHIYE_COMPANIES + HOTJOB_COMPANIES + CUSTOM_COMPANIES + SMARTRECRUITERS_COMPANIES + ZHIYE_COMPANIES_EXTRA + BANK_COMPANIES + MOKAHR_COMPANIES + ZHIYE_RESEARCH_COMPANIES

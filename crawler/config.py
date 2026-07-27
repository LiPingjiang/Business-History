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

ZHIYE_COMPANIES_EXTRA = [
    CompanyConfig("中国铁道建筑集团", "zhiye", "https://crcc.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国冶金科工集团", "zhiye", "https://mcc.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国能源建设集团", "zhiye", "https://ceec.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国交通建设集团", "zhiye", "https://cccc.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国建筑集团", "zhiye", "https://cscec.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国电力建设集团", "zhiye", "https://powerchina.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国建材集团", "zhiye", "https://cnbm.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国华录集团", "zhiye", "https://hualu.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国东方电气集团", "zhiye", "https://dongfang.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国商用飞机", "zhiye", "https://comac.zhiye.com", params={"type": "social"}),
    CompanyConfig("东风汽车集团", "zhiye", "https://dfmc.zhiye.com", params={"type": "social"}),
    CompanyConfig("哈尔滨电气集团", "zhiye", "https://harbin-electric.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国一重集团", "zhiye", "https://cfhi.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国第一汽车集团", "zhiye", "https://faw.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国机械工业集团", "zhiye", "https://sinomach.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国兵器装备集团", "zhiye", "https://csgc.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国航空发动机集团", "zhiye", "https://aecc.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国电子科技集团", "zhiye", "https://cetc.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国船舶集团", "zhiye", "https://cssc.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国兵器工业集团", "zhiye", "https://norincogroup.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国航空工业集团", "zhiye", "https://avic.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国航天科工集团", "zhiye", "https://casic.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国航天科技集团", "zhiye", "https://cast.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国五矿集团", "zhiye", "https://minmetals.zhiye.com", params={"type": "social"}),
    CompanyConfig("鞍钢集团", "zhiye", "https://ansteel.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国黄金集团", "zhiye", "https://chinagold.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国铝业集团", "zhiye", "https://chinalco.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国诚通控股", "zhiye", "https://chengtong.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国远洋海运集团", "zhiye", "https://coscoshipping.zhiye.com", params={"type": "social"}),
    CompanyConfig("国家开发投资集团", "zhiye", "https://sdic.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国保利集团", "zhiye", "https://poly.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国核工业集团", "zhiye", "https://cnnc.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国广核集团", "zhiye", "https://cgnpc.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国三峡集团", "zhiye", "https://ctg.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国节能环保集团", "zhiye", "https://cecep.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国化学工程集团", "zhiye", "https://cncec.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国中化控股", "zhiye", "https://sinochem.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国储备粮管理集团", "zhiye", "https://sinograin.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国盐业集团", "zhiye", "https://chinasalt.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国人民保险", "zhiye", "https://picc.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国太平保险", "zhiye", "https://cntaiping.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国人寿", "zhiye", "https://chinalife.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国银行", "zhiye", "https://boc.zhiye.com", params={"type": "social"}),
    CompanyConfig("中国电子信息产业集团", "zhiye", "https://cec.zhiye.com", params={"type": "social"}),
]

# 汇总所有企业
ALL_COMPANIES = WORKDAY_COMPANIES + ZHIYE_COMPANIES + HOTJOB_COMPANIES + CUSTOM_COMPANIES + SMARTRECRUITERS_COMPANIES + ZHIYE_COMPANIES_EXTRA

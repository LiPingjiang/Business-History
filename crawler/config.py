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
    CompanyConfig("浦发银行", "spdb", "https://job.spdb.com.cn"),
    CompanyConfig("民生银行", "cmbc", "https://career.cmbc.com.cn"),
    # 华夏银行 - 大易(wecruit)平台，需Playwright
    CompanyConfig("华夏银行", "hotjob_pw", "https://hxb.hotjob.cn/SU645b0d18bef57c0907e9fbc8/pb/social.html"),
    # 兴业银行 - 自建SPA，需Playwright
    CompanyConfig("兴业银行", "hotjob_pw", "https://job.cib.com.cn/portal/"),
    # 招商银行 - 北森新版Portal SPA，需Playwright
    CompanyConfig("招商银行", "zhiye_pw", "https://cmbchina.zhiye.com/Social"),
    # 交通银行 - 北森新版Portal SPA，需Playwright
    CompanyConfig("交通银行", "zhiye_pw", "https://bankcomm.zhiye.com/Social"),
    # 邮储银行 - 北森新版Portal SPA，需Playwright
    CompanyConfig("邮储银行", "zhiye_pw", "https://psbc.zhiye.com/Social"),
    # 工商银行 - 北森新版Portal SPA，需Playwright
    CompanyConfig("工商银行", "zhiye_pw", "https://icbc.zhiye.com/Social"),
    # 农业银行 - 北森新版Portal SPA，需Playwright
    CompanyConfig("农业银行", "zhiye_pw", "https://abchina.zhiye.com/Social"),
    # 建设银行 - 北森新版Portal SPA，需Playwright
    CompanyConfig("建设银行", "zhiye_pw", "https://ccb.zhiye.com/Social"),
    # 中国银行 - 北森新版Portal SPA，需Playwright
    CompanyConfig("中国银行", "zhiye_pw", "https://boc.zhiye.com/Social"),
    # 光大银行 - 瑞数WAF + React SPA，需Playwright
    CompanyConfig("光大银行", "hotjob_pw", "https://eoap.cebbank.com/uiap/wt/CEB/zpzh/social"),
    # 广发银行 - 北森新版Portal SPA，需Playwright
    CompanyConfig("广发银行", "zhiye_pw", "https://cgbchina.zhiye.com/Social"),
    # 北京农商银行 - 北森新版Portal SPA，需Playwright
    CompanyConfig("北京农商银行", "zhiye_pw", "https://bjrcb.zhiye.com/Social"),
    # 渤海银行 - 北森新版Portal SPA，需Playwright
    CompanyConfig("渤海银行", "zhiye_pw", "https://cbhb.zhiye.com/Social"),
    # 恒丰银行 - 北森新版Portal SPA，需Playwright
    CompanyConfig("恒丰银行", "zhiye_pw", "https://hfbank.zhiye.com/Social"),
    # 北京银行 - 北森API，纯HTTP分页
    CompanyConfig("北京银行", "zhiye", "https://bankofbeijing.zhiye.com"),
    # 上海银行 - 北森API，纯HTTP分页
    CompanyConfig("上海银行", "zhiye", "https://bosc.zhiye.com"),
    # 长沙银行 - 北森API，纯HTTP分页（0-based）
    CompanyConfig("长沙银行", "zhiye", "https://cscb.zhiye.com"),
]

# Mokahr 平台企业（银行+研究机构）
MOKAHR_COMPANIES = [
    CompanyConfig("智源研究院", "mokahr", "https://app.mokahr.com/social-recruitment/baai/42173"),
    CompanyConfig("中信百信银行", "mokahr", "https://app.mokahr.com/social-recruitment/aibank/46870"),
    CompanyConfig("苏商银行", "mokahr", "https://app.mokahr.com/social-recruitment/snb/45591"),
]

ZHIYE_RESEARCH_COMPANIES = [
    CompanyConfig("中科院自动化所", "zhiye", "https://casia.zhiye.com"),
    CompanyConfig("中金公司", "zhiye", "https://cicc.zhiye.com"),
    CompanyConfig("中国银河证券", "zhiye", "https://chinastock.zhiye.com"),
]


# ============================================================
# Phase 6: 央企扩展（zhiye_pw可复用 + 新发现平台）
# ============================================================

YANGQI_EXPANSION = [
    # zhiye.com 旧版Portal仍在线，可用zhiye_pw adapter
    CompanyConfig("中国建筑", "zhiye_pw", "https://cscec.zhiye.com"),
    CompanyConfig("中国船舶", "zhiye_pw", "https://cssc.zhiye.com"),
    CompanyConfig("中国核工业", "zhiye_pw", "https://cnnc.zhiye.com"),
    CompanyConfig("中国能建", "zhiye_pw", "https://ceec.zhiye.com"),
]

# ============================================================
# Phase 6b: 外企扩展（多平台适配）
# ============================================================

WORKDAY_EXPANSION = [
    # Workday 可用
    CompanyConfig("Cisco", "workday", "https://cisco.wd5.myworkdayjobs.com/Cisco_Careers",
                  params={"location": "China"}),
    CompanyConfig("Salesforce", "workday", "https://salesforce.wd12.myworkdayjobs.com/en/External_Career_Site",
                  params={"location": "China"}),
    CompanyConfig("Broadcom", "workday", "https://broadcom.wd1.myworkdayjobs.com/External_Career",
                  params={"location": "China"}),
    # Jibe 平台 (Google Cloud Talent Solution)
    CompanyConfig("AMD", "jibe", "https://careers.amd.com",
                  params={"location": "Beijing"}),
    CompanyConfig("Schneider Electric", "jibe", "https://careers.se.com",
                  params={"location": "Beijing"}),
    # Phenom People 平台
    CompanyConfig("ABB", "phenom", "https://careers.abb",
                  params={"location": "Beijing", "country_code": "cn"}),
    # 需要 Playwright（SPA/WAF）— 暂标记，后续实现
    # CompanyConfig("IBM", "ibm_playwright", "https://careers.ibm.com", params={"location": "Beijing"}),
    # CompanyConfig("Honeywell", "honeywell_playwright", "https://careers.honeywell.com", params={"location": "Beijing"}),
    # === Phase 7: 央企扩展 (beisen adapter) ===
    CompanyConfig("中国联通社招", "beisen", "https://chinaunicom.zhiye.com"),
    CompanyConfig("中国航天科工", "zhiye_pw", "https://casic.zhiye.com"),
    # === Phase 8: 央企扩展 (beisen + Playwright) ===
    CompanyConfig("招商局集团", "beisen", "https://cmhk.zhiye.com"),
    CompanyConfig("中国石化", "custom_pw", "https://job.sinopec.com"),
    CompanyConfig("中国华能", "custom_pw", "https://zhaopin.chng.com.cn"),
    CompanyConfig("中国南方电网", "custom_pw", "https://zhaopin.csg.cn"),
    CompanyConfig("中国大唐", "custom_pw", "https://zhaopin.china-cdt.com"),
    # === Phase 9: 三桶油 ===
    CompanyConfig("中国石油", "custom_pw", "https://zhaopin.cnpc.com.cn"),
    CompanyConfig("中国海油", "custom_pw", "https://cnooc.zhaopin.com"),


]

# VMware 已被 Broadcom 收购，岗位合并到 Broadcom Workday
# IBM: careers.ibm.com 有 AWS WAF challenge (202)，需 Playwright
# Honeywell: Oracle HCM SPA (ibqbjb.fa.ocs.oraclecloud.com)，需 Playwright

# ============================================================
# Phase 10: 券商扩展（hotjob_json + beisen）
# ============================================================

SECURITIES_COMPANIES = [
    # hotjob.cn JSON API (无需Playwright)
    CompanyConfig("华泰证券", "hotjob_json", "https://www.hotjob.cn/wt/HTSC/web/index", {"su_id": "HTSC"}),
    CompanyConfig("兴业证券", "hotjob_json", "https://www.hotjob.cn/wt/xyzq/web/index", {"su_id": "xyzq"}),
    CompanyConfig("中泰证券", "hotjob_json", "https://www.hotjob.cn/wt/zts/web/index", {"su_id": "zts"}),
    # beisen/zhiye.com
    CompanyConfig("中信建投证券", "beisen", "https://csc108.zhiye.com"),
    CompanyConfig("国信证券", "beisen", "https://guosen.zhiye.com"),
    CompanyConfig("光大证券", "beisen", "https://ebscn.zhiye.com"),
]

# 更新汇总
ALL_COMPANIES = WORKDAY_COMPANIES + ZHIYE_COMPANIES + HOTJOB_COMPANIES + CUSTOM_COMPANIES + SMARTRECRUITERS_COMPANIES + ZHIYE_COMPANIES_EXTRA + BANK_COMPANIES + MOKAHR_COMPANIES + ZHIYE_RESEARCH_COMPANIES + YANGQI_EXPANSION + WORKDAY_EXPANSION + SECURITIES_COMPANIES

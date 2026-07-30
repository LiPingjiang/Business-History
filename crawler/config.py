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
    source_type: str = ""  # "official" or "third_party:平台名"
    official_url: str = ""  # 企业官网招聘页面（用于对比/备用）
    status: str = "active"  # "active", "dead", "suspended"
    display_name: str = ""  # 前端展示名称（与 COMPANY_CATALOG 对齐）


# ============================================================
# Phase 1: 平台级 Adapter 企业列表
# ============================================================

WORKDAY_COMPANIES = [
    CompanyConfig("NVIDIA", "workday", "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite",
                  params={"location": "China"},
                  display_name="英伟达"),
    CompanyConfig("Intel", "workday", "https://intel.wd1.myworkdayjobs.com/External",
                  params={"location": "China"},
                  display_name="英特尔"),
    CompanyConfig("HP", "workday", "https://hp.wd5.myworkdayjobs.com/ExternalCareerSite",
                  params={"location": "China"},
                  display_name="惠普"),
    CompanyConfig("Adobe", "workday", "https://adobe.wd5.myworkdayjobs.com/external_experienced",
                  params={"location": "China"}),
    CompanyConfig("3M", "workday", "https://3m.wd1.myworkdayjobs.com/Search",
                  params={"location": "China"}),
    CompanyConfig("GE Aerospace", "workday", "https://geaerospace.wd5.myworkdayjobs.com/GE_ExternalSite",
                  params={"location": "China"}),
    CompanyConfig("Pfizer", "workday", "https://pfizer.wd1.myworkdayjobs.com/PfizerCareers",
                  params={"location": "China"},
                  display_name="辉瑞"),
    CompanyConfig("Red Hat", "workday", "https://redhat.wd5.myworkdayjobs.com/jobs",
                  params={"location": "China"},
                  display_name="红帽"),
    CompanyConfig("Visa", "workday", "https://visa.wd5.myworkdayjobs.com/Visa",
                  params={"location": "China"}),
    CompanyConfig("Mastercard", "workday", "https://mastercard.wd1.myworkdayjobs.com/CorporateCareers",
                  params={"location": "China"},
                  display_name="万事达卡"),
    CompanyConfig("Samsung SEC", "workday", "https://sec.wd3.myworkdayjobs.com/Samsung_Careers",
                  params={"location": "China"},
                  display_name="三星"),
    CompanyConfig("Dell", "workday", "https://dell.wd1.myworkdayjobs.com/External",
                  params={"location": "China"},
                  display_name="戴尔"),
    CompanyConfig("Shell", "workday", "https://shell.wd3.myworkdayjobs.com/ShellCareers",
                  params={"location": "China"},
                  display_name="壳牌"),
]

ZHIYE_COMPANIES = [
    # 航天科工 casic.zhiye.com 是旧版校招系统，无社招API，跳过
    # CompanyConfig("航天科工", "zhiye", "https://casic.zhiye.com", params={"type": "social"}),
    CompanyConfig("三星中国", "zhiye", "https://dearsamsung.zhiye.com",
                  params={"type": "social"},
                  display_name="三星"),
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
                  params={"su_id": "chd"},
                  display_name="中国华电集团"),
    CompanyConfig("中国中车", "hotjob_pw", "https://crrc.hotjob.cn/SU64d47c466202cc36e27a52d4/pb/social.html",
                  params={"su_id": "SU64d47c466202cc36e27a52d4"},
                  display_name="中国中车集团"),
    CompanyConfig("一汽大众", "hotjob_pw", "https://faw-vw.hotjob.cn",
                  params={"su_id": "faw-vw"}),
    CompanyConfig("中化集团", "hotjob_pw", "https://sinochem.hotjob.cn",
                  params={"su_id": "sinochem"},
                  display_name="中国中化控股"),
]

# ============================================================
# Phase 2: 高价值自建站
# ============================================================

CUSTOM_COMPANIES = [
    CompanyConfig("Amazon", "amazon", "https://www.amazon.jobs/en/search",
                  params={"base_query": "data engineer", "loc_query": "Beijing, China"},
                  display_name="亚马逊"),
    CompanyConfig("Microsoft", "microsoft", "https://apply.careers.microsoft.com",
                  params={"location": "Beijing"},
                  display_name="微软"),
    CompanyConfig("Siemens", "siemens", "https://jobs.siemens.com.cn/siemens/position/index",
                  params={"recruitmentType": "SOCIALRECRUITMENT"},
                  display_name="西门子"),
    CompanyConfig("BMW/领悦", "bmw", "https://careersite.tupu360.com/bmw/position/index",
                  params={"recruitmentType": "SOCIALRECRUITMENT"},
                  display_name="宝马"),
    CompanyConfig("AstraZeneca", "astrazeneca", "https://careers.astrazeneca.com/search-jobs",
                  params={"keywords": "data", "location": "Beijing, China"},
                  display_name="阿斯利康"),
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
    CompanyConfig("中信银行", "citicbank", "https://job.citicbank.com",
                  params={"workAddr": ["110000"]}),
    CompanyConfig("浦发银行", "spdb", "https://job.spdb.com.cn"),
    CompanyConfig("民生银行", "cmbc", "https://career.cmbc.com.cn"),
    # 华夏银行 - 大易(wecruit)平台，需Playwright
    CompanyConfig("华夏银行", "hotjob_pw", "https://hxb.hotjob.cn/SU645b0d18bef57c0907e9fbc8/pb/social.html"),
    # 兴业银行 - 自建SPA，需Playwright
    CompanyConfig("兴业银行", "hotjob_pw", "https://job.cib.com.cn/portal/"),
    # 招商银行 - zhiye.com已关闭(404)，官网career.cmbchina.com需Playwright
    CompanyConfig("招商银行", "zhiye_pw", "https://cmbchina.zhiye.com/Social",
                  official_url="https://career.cmbchina.com", status="dead"),
    # 交通银行 - zhiye.com已关闭(404)，官网job.bankcomm.com需Playwright+legacy SSL
    CompanyConfig("交通银行", "zhiye_pw", "https://bankcomm.zhiye.com/Social",
                  official_url="https://job.bankcomm.com", status="dead"),
    # 邮储银行 - zhiye.com已关闭(404)，官网psbc.com需Playwright
    CompanyConfig("邮储银行", "zhiye_pw", "https://psbc.zhiye.com/Social",
                  official_url="https://www.psbc.com/cn/grfw/rczp/", status="dead"),
    # 工商银行 - zhiye.com已关闭(404)，官网job.icbc.com.cn需Playwright+legacy SSL
    CompanyConfig("工商银行", "zhiye_pw", "https://icbc.zhiye.com/Social",
                  official_url="https://job.icbc.com.cn", status="dead"),
    # 农业银行 - zhiye.com已关闭(404)，官网career.abchina.com需Playwright+legacy SSL
    CompanyConfig("农业银行", "zhiye_pw", "https://abchina.zhiye.com/Social",
                  official_url="https://career.abchina.com", status="dead"),
    # 建设银行 - zhiye.com已关闭(404)，官网job.ccb.com有API(NHR104)需legacy SSL
    CompanyConfig("建设银行", "zhiye_pw", "https://ccb.zhiye.com/Social",
                  official_url="https://job.ccb.com", status="dead"),
    # 中国银行 - zhiye.com已关闭(404)，官网career.bankofchina.com需Playwright
    CompanyConfig("中国银行", "zhiye_pw", "https://boc.zhiye.com/Social",
                  official_url="https://career.bankofchina.com", status="dead"),
    # 光大银行 - 瑞数WAF + React SPA，需Playwright
    CompanyConfig("光大银行", "hotjob_pw", "https://eoap.cebbank.com/uiap/wt/CEB/zpzh/social"),
    # 广发银行 - zhiye.com已关闭(404)，官网cgbchina.com.cn返回500
    CompanyConfig("广发银行", "zhiye_pw", "https://cgbchina.zhiye.com/Social",
                  official_url="https://www.cgbchina.com.cn/Channel/16000100", status="dead"),
    # 北京农商银行 - zhiye.com已关闭(404)，官网bjrcb.com招聘页404
    CompanyConfig("北京农商银行", "zhiye_pw", "https://bjrcb.zhiye.com/Social",
                  official_url="https://www.bjrcb.com", status="dead"),
    # 渤海银行 - zhiye.com已关闭(404)，官网cbhb.com.cn可访问
    CompanyConfig("渤海银行", "zhiye_pw", "https://cbhb.zhiye.com/Social",
                  official_url="https://www.cbhb.com.cn/bhbank/S101/renCaiZhaoPin", status="dead"),
    # 恒丰银行 - zhiye.com已关闭(404)，官网hfbank.com.cn返回412(WAF)
    CompanyConfig("恒丰银行", "zhiye_pw", "https://hfbank.zhiye.com/Social",
                  official_url="https://www.hfbank.com.cn/gywm/rczp/index.shtml", status="dead"),
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
    CompanyConfig("中国银河证券", "zhiye", "https://chinastock.zhiye.com",
                  display_name="中国银河金融控股"),
]


# ============================================================
# Phase 6: 央企扩展（zhiye_pw可复用 + 新发现平台）
# ============================================================

YANGQI_EXPANSION = [
    # zhiye.com 旧版Portal API已失效(302→404)，需切换到官网或标记dead
    CompanyConfig("中国建筑", "zhiye_pw", "https://cscec.zhiye.com",
                  official_url="https://hr.cscec.com", status="dead"),
    CompanyConfig("中国船舶", "zhiye_pw", "https://cssc.zhiye.com",
                  official_url="https://www.cssc.net.cn", status="dead",
                  display_name="中国船舶集团"),
    CompanyConfig("中国核工业", "zhiye_pw", "https://cnnc.zhiye.com",
                  official_url="https://hr.cnnc.com.cn", status="dead"),
    CompanyConfig("中国能建", "zhiye_pw", "https://ceec.zhiye.com",
                  official_url="https://hr.ceec.net.cn", status="suspended",
                  display_name="中国能源建设集团"),
]

# ============================================================
# Phase 6b: 外企扩展（多平台适配）
# ============================================================

WORKDAY_EXPANSION = [
    # Workday 可用
    CompanyConfig("Cisco", "workday", "https://cisco.wd5.myworkdayjobs.com/Cisco_Careers",
                  params={"location": "China"},
                  display_name="思科"),
    CompanyConfig("Salesforce", "workday", "https://salesforce.wd12.myworkdayjobs.com/en/External_Career_Site",
                  params={"location": "China"}),
    CompanyConfig("Broadcom", "workday", "https://broadcom.wd1.myworkdayjobs.com/External_Career",
                  params={"location": "China"},
                  display_name="博通"),
    # Jibe 平台 (Google Cloud Talent Solution)
    CompanyConfig("AMD", "jibe", "https://careers.amd.com",
                  params={"location": "Beijing"}),
    CompanyConfig("Schneider Electric", "jibe", "https://careers.se.com",
                  params={"location": "Beijing"},
                  display_name="施耐德电气"),
    # Phenom People 平台
    CompanyConfig("ABB", "phenom", "https://careers.abb",
                  params={"location": "Beijing", "country_code": "cn"}),
    # 需要 Playwright（SPA/WAF）— 暂标记，后续实现
    # CompanyConfig("IBM", "ibm_playwright", "https://careers.ibm.com", params={"location": "Beijing"}),
    # CompanyConfig("Honeywell", "honeywell_playwright", "https://careers.honeywell.com", params={"location": "Beijing"}),
    # === Phase 7: 央企扩展 (beisen adapter) ===
    CompanyConfig("中国联通社招", "beisen", "https://chinaunicom.zhiye.com"),
    CompanyConfig("中国航天科工", "zhiye_pw", "https://casic.zhiye.com",
                  official_url="https://zhaopin.casic.cn", status="dead",
                  display_name="中国航天科工集团"),
    # === Phase 8: 央企扩展 (beisen + Playwright) ===
    CompanyConfig("招商局集团", "beisen", "https://cmhk.zhiye.com"),
    CompanyConfig("中国石化", "custom_pw", "https://job.sinopec.com",
                  display_name="中国石油化工集团"),
    CompanyConfig("中国华能", "custom_pw", "https://zhaopin.chng.com.cn",
                  display_name="中国华能集团"),
    CompanyConfig("中国南方电网", "custom_pw", "https://zhaopin.csg.cn"),
    CompanyConfig("中国大唐", "custom_pw", "https://zhaopin.china-cdt.com",
                  display_name="中国大唐集团"),
    # === Phase 9: 三桶油 ===
    CompanyConfig("中国石油", "custom_pw", "https://zhaopin.cnpc.com.cn",
                  display_name="中国石油天然气集团"),
    CompanyConfig("中国海油", "custom_pw", "https://cnooc.zhaopin.com",
                  display_name="中国海洋石油集团"),


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
    CompanyConfig("方正证券", "beisen", "https://foundersc.zhiye.com"),
    CompanyConfig("中金财富", "beisen", "https://ciccwm.zhiye.com"),
    # Phase 11: 国资控股扩展（beisen + hotjob_json）
    CompanyConfig("中国交建", "beisen", "https://ccccltd.zhiye.com",
                  display_name="中国交通建设集团"),
    CompanyConfig("保利发展", "beisen", "https://polycn.zhiye.com",
                  display_name="中国保利集团"),
    CompanyConfig("中国再保险", "beisen", "https://chinare.zhiye.com"),
    CompanyConfig("中国长城资产", "beisen", "https://gwamcc.zhiye.com"),
    CompanyConfig("中国东方资产", "beisen", "https://coamc.zhiye.com"),
    CompanyConfig("中国五矿", "hotjob_json", "https://www.hotjob.cn/wt/minmetals/web/index", {"su_id": "minmetals"},
                  display_name="中国五矿集团"),
]

# 更新汇总

# ============================================================
# Phase 12: Workday 批量扩展 (外企 + 咨询 + 金融)
# ============================================================

WORKDAY_EXPANSION_2 = [
    # --- Tech ---
    CompanyConfig("Meta", "workday", "https://meta.wd1.myworkdayjobs.com/Meta_Careers",
                  params={"location": "China"}, display_name="Meta", status="geo_blocked"),
    CompanyConfig("Zoom", "workday", "https://zoom.wd5.myworkdayjobs.com/Zoom",
                  params={"location": "China"}, display_name="Zoom"),
    CompanyConfig("VMware", "workday", "https://broadcom.wd1.myworkdayjobs.com/External_Career",
                  params={"location": "China"}, display_name="VMware", status="geo_blocked"),
    CompanyConfig("Datadog", "workday", "https://datadog.wd1.myworkdayjobs.com/Datadog",
                  params={"location": "China"}, display_name="Datadog", status="geo_blocked"),
    CompanyConfig("Snowflake", "workday", "https://snowflake.wd1.myworkdayjobs.com/en-US/Snowflake",
                  params={"location": "China"}, display_name="Snowflake", status="geo_blocked"),
    CompanyConfig("Fortinet", "workday", "https://fortinet.wd1.myworkdayjobs.com/Fortinet",
                  params={"location": "China"}, display_name="Fortinet", status="geo_blocked"),
    CompanyConfig("Pure Storage", "workday", "https://purestorage.wd1.myworkdayjobs.com/PureStorageExternalSite",
                  params={"location": "China"}, display_name="Pure Storage", status="geo_blocked"),
    CompanyConfig("Cloudflare", "workday", "https://cloudflare.wd1.myworkdayjobs.com/Cloudflare_Careers",
                  params={"location": "China"}, display_name="Cloudflare", status="geo_blocked"),
    CompanyConfig("MongoDB", "workday", "https://mongodb.wd1.myworkdayjobs.com/MongoDB_Careers",
                  params={"location": "China"}, display_name="MongoDB", status="geo_blocked"),
    CompanyConfig("Elastic", "workday", "https://elastic.wd1.myworkdayjobs.com/Elastic_Careers",
                  params={"location": "China"}, display_name="Elastic", status="geo_blocked"),
    CompanyConfig("SAP", "workday", "https://sap.wd1.myworkdayjobs.com/SAPCareers",
                  params={"location": "China"}, display_name="SAP", status="geo_blocked"),
    CompanyConfig("Oracle", "workday", "https://oracle.wd1.myworkdayjobs.com/Oracle_Careers",
                  params={"location": "China"}, display_name="甲骨文", status="geo_blocked"),
    CompanyConfig("IBM", "workday", "https://ibm.wd5.myworkdayjobs.com/IBM_Careers",
                  params={"location": "China"}, display_name="IBM", status="geo_blocked"),
    # --- Consumer / Retail ---
    CompanyConfig("Nike", "workday", "https://nike.wd1.myworkdayjobs.com/Nike_Careers",
                  params={"location": "China"}, display_name="耐克", status="geo_blocked"),
    CompanyConfig("Starbucks", "workday", "https://starbucks.wd1.myworkdayjobs.com/StarbucksCareers",
                  params={"location": "China"}, display_name="星巴克", status="geo_blocked"),
    CompanyConfig("IKEA", "workday", "https://ikea.wd3.myworkdayjobs.com/IKEA_Careers",
                  params={"location": "China"}, display_name="宜家", status="geo_blocked"),
    CompanyConfig("Walmart", "workday", "https://walmart.wd5.myworkdayjobs.com/WalmartExternal",
                  params={"location": "China"}, display_name="沃尔玛"),
    CompanyConfig("Unilever", "workday", "https://unilever.wd3.myworkdayjobs.com/Unilever_Experienced_Professionals",
                  params={"location": "China"}, display_name="联合利华"),
    CompanyConfig("P&G", "workday", "https://pg.wd1.myworkdayjobs.com/PGCareers",
                  params={"location": "China"}, display_name="宝洁", status="geo_blocked"),
    CompanyConfig("Adidas", "workday", "https://adidas.wd3.myworkdayjobs.com/adidas_Careers",
                  params={"location": "China"}, display_name="阿迪达斯", status="geo_blocked"),
    CompanyConfig("L'Oreal", "workday", "https://loreal.wd3.myworkdayjobs.com/en-US/LOreal_Careers",
                  params={"location": "China"}, display_name="欧莱雅", status="geo_blocked"),
    CompanyConfig("Nestle", "workday", "https://nestle.wd3.myworkdayjobs.com/en-US/Nestle_Careers",
                  params={"location": "China"}, display_name="雀巢", status="geo_blocked"),
    CompanyConfig("Coca-Cola", "workday", "https://coke.wd1.myworkdayjobs.com/coca-cola-careers",
                  params={"location": "China"}, display_name="可口可乐"),
    CompanyConfig("PepsiCo", "workday", "https://pepsico.wd1.myworkdayjobs.com/PepsiCo_Careers",
                  params={"location": "China"}, display_name="百事可乐", status="geo_blocked"),
    CompanyConfig("McDonald's", "workday", "https://mcdonalds.wd5.myworkdayjobs.com/McDonalds_Careers",
                  params={"location": "China"}, display_name="麦当劳", status="geo_blocked"),
    CompanyConfig("H&M", "workday", "https://hm.wd3.myworkdayjobs.com/HM_Careers",
                  params={"location": "China"}, display_name="H&M", status="geo_blocked"),
    # --- Pharma / Healthcare ---
    CompanyConfig("Roche", "workday", "https://roche.wd3.myworkdayjobs.com/roche-ext",
                  params={"location": "China"}, display_name="罗氏"),
    CompanyConfig("Novartis", "workday", "https://novartis.wd3.myworkdayjobs.com/Novartis_Careers",
                  params={"location": "China"}, display_name="诺华"),
    CompanyConfig("Eli Lilly", "workday", "https://lilly.wd5.myworkdayjobs.com/Lilly_Careers",
                  params={"location": "China"}, display_name="礼来", status="geo_blocked"),
    CompanyConfig("Johnson & Johnson", "workday", "https://jnj.wd5.myworkdayjobs.com/JNJ_Careers",
                  params={"location": "China"}, display_name="强生", status="geo_blocked"),
    CompanyConfig("Sanofi", "workday", "https://sanofi.wd3.myworkdayjobs.com/SanofiCareers",
                  params={"location": "China"}, display_name="赛诺菲"),
    CompanyConfig("GSK", "workday", "https://gsk.wd5.myworkdayjobs.com/GSK_Careers",
                  params={"location": "China"}, display_name="葛兰素史克", status="geo_blocked"),
    CompanyConfig("Merck/MSD", "workday", "https://merck.wd5.myworkdayjobs.com/External",
                  params={"location": "China"}, display_name="默沙东", status="geo_blocked"),
    CompanyConfig("BMS", "workday", "https://bms.wd5.myworkdayjobs.com/BMS_Careers",
                  params={"location": "China"}, display_name="百时美施贵宝", status="geo_blocked"),
    CompanyConfig("Bayer", "workday", "https://bayer.wd3.myworkdayjobs.com/BayerCareer",
                  params={"location": "China"}, display_name="拜耳", status="geo_blocked"),
    CompanyConfig("Novo Nordisk", "workday", "https://novonordisk.wd3.myworkdayjobs.com/en-US/NovoNordisk_Careers",
                  params={"location": "China"}, display_name="诺和诺德", status="geo_blocked"),
    CompanyConfig("Abbott", "workday", "https://abbott.wd5.myworkdayjobs.com/Abbott_Careers",
                  params={"location": "China"}, display_name="雅培", status="geo_blocked"),
    CompanyConfig("Medtronic", "workday", "https://medtronic.wd1.myworkdayjobs.com/MedtronicCareers",
                  params={"location": "China"}, display_name="美敦力"),
    # --- Industrial / Auto / Energy ---
    CompanyConfig("BASF", "workday", "https://basf.wd3.myworkdayjobs.com/BASF_Careers",
                  params={"location": "China"}, display_name="巴斯夫", status="geo_blocked"),
    CompanyConfig("Honeywell", "workday", "https://honeywell.wd5.myworkdayjobs.com/Honeywell_Careers",
                  params={"location": "China"}, display_name="霍尼韦尔", status="geo_blocked"),
    CompanyConfig("Caterpillar", "workday", "https://cat.wd5.myworkdayjobs.com/CaterpillarCareers",
                  params={"location": "China"}, display_name="卡特彼勒", status="geo_blocked"),
    CompanyConfig("Ford", "workday", "https://ford.wd1.myworkdayjobs.com/Ford_Careers",
                  params={"location": "China"}, display_name="福特汽车", status="geo_blocked"),
    CompanyConfig("GM", "workday", "https://generalmotors.wd5.myworkdayjobs.com/Careers_GM",
                  params={"location": "China"}, display_name="通用汽车", status="geo_blocked"),
    CompanyConfig("Emerson", "workday", "https://emerson.wd5.myworkdayjobs.com/Emerson_Careers",
                  params={"location": "China"}, display_name="艾默生", status="geo_blocked"),
    CompanyConfig("Chevron", "workday", "https://chevron.wd5.myworkdayjobs.com/Chevron_Careers",
                  params={"location": "China"}, display_name="雪佛龙", status="geo_blocked"),
    CompanyConfig("TotalEnergies", "workday", "https://totalenergies.wd3.myworkdayjobs.com/TotalEnergies_Careers",
                  params={"location": "China"}, display_name="道达尔能源", status="geo_blocked"),
    CompanyConfig("ExxonMobil", "workday", "https://exxonmobil.wd5.myworkdayjobs.com/ExxonMobil_Careers",
                  params={"location": "China"}, display_name="埃克森美孚", status="geo_blocked"),
    CompanyConfig("Volvo", "workday", "https://volvo.wd3.myworkdayjobs.com/Volvo_Careers",
                  params={"location": "China"}, display_name="沃尔沃", status="geo_blocked"),
    CompanyConfig("Philips", "workday", "https://philips.wd3.myworkdayjobs.com/Philips_Careers",
                  params={"location": "China"}, display_name="飞利浦", status="geo_blocked"),
    # --- Finance / Consulting ---
    CompanyConfig("Goldman Sachs", "workday", "https://gs.wd5.myworkdayjobs.com/GS_Careers",
                  params={"location": "China"}, display_name="高盛", status="geo_blocked"),
    CompanyConfig("Morgan Stanley", "workday", "https://morganstanley.wd5.myworkdayjobs.com/Morgan_Stanley_Careers",
                  params={"location": "China"}, display_name="摩根士丹利", status="geo_blocked"),
    CompanyConfig("JP Morgan", "workday", "https://jpmc.wd5.myworkdayjobs.com/JPMorgan_Careers",
                  params={"location": "China"}, display_name="摩根大通", status="geo_blocked"),
    CompanyConfig("BlackRock", "workday", "https://blackrock.wd1.myworkdayjobs.com/BlackRock_Careers",
                  params={"location": "China"}, display_name="贝莱德", status="geo_blocked"),
    CompanyConfig("Deloitte", "workday", "https://deloitte.wd1.myworkdayjobs.com/Deloitte_Careers",
                  params={"location": "China"}, display_name="德勤", status="geo_blocked"),
    CompanyConfig("EY", "workday", "https://ey.wd5.myworkdayjobs.com/EY_Careers",
                  params={"location": "China"}, display_name="安永", status="geo_blocked"),
    CompanyConfig("PwC", "workday", "https://pwc.wd3.myworkdayjobs.com/PwC_Careers",
                  params={"location": "China"}, display_name="普华永道", status="geo_blocked"),
    CompanyConfig("KPMG", "workday", "https://kpmg.wd3.myworkdayjobs.com/KPMG_Careers",
                  params={"location": "China"}, display_name="毕马威", status="geo_blocked"),
    CompanyConfig("McKinsey", "workday", "https://mckinsey.wd3.myworkdayjobs.com/McKinsey_Careers",
                  params={"location": "China"}, display_name="麦肯锡", status="geo_blocked"),
    CompanyConfig("BCG", "workday", "https://bcg.wd1.myworkdayjobs.com/BCG_Careers",
                  params={"location": "China"}, display_name="波士顿咨询", status="geo_blocked"),
    CompanyConfig("Bain", "workday", "https://bain.wd1.myworkdayjobs.com/Bain_Careers",
                  params={"location": "China"}, display_name="贝恩公司", status="geo_blocked"),
    # --- Semiconductor ---
    CompanyConfig("Qualcomm", "workday", "https://qualcomm.wd5.myworkdayjobs.com/External",
                  params={"location": "China"}, display_name="高通", status="geo_blocked"),
    CompanyConfig("Texas Instruments", "workday", "https://ti.wd1.myworkdayjobs.com/TI_Careers",
                  params={"location": "China"}, display_name="德州仪器", status="geo_blocked"),
    CompanyConfig("Applied Materials", "workday", "https://appliedmaterials.wd1.myworkdayjobs.com/External",
                  params={"location": "China"}, display_name="应用材料", status="geo_blocked"),
    CompanyConfig("Micron", "workday", "https://micron.wd1.myworkdayjobs.com/External",
                  params={"location": "China"}, display_name="美光科技"),
    CompanyConfig("Western Digital", "workday", "https://westerndigital.wd1.myworkdayjobs.com/WD_Careers",
                  params={"location": "China"}, display_name="西部数据", status="geo_blocked"),
    # --- Luxury / Fashion ---
    CompanyConfig("LVMH", "workday", "https://lvmh.wd3.myworkdayjobs.com/LVMH_Careers",
                  params={"location": "China"}, display_name="路威酩轩", status="geo_blocked"),
    CompanyConfig("Estee Lauder", "workday", "https://esteelauder.wd5.myworkdayjobs.com/EsteeLauder_Careers",
                  params={"location": "China"}, display_name="雅诗兰黛", status="geo_blocked"),
]

# ============================================================
# Phase 13: 央企/国企扩展 (zhiye.com / beisen)
# ============================================================

YANGQI_EXPANSION_2 = [
    CompanyConfig("中国航天科技集团", "zhiye", "https://casc.zhiye.com", display_name="中国航天科技集团"),
    CompanyConfig("中国电信", "zhiye", "https://chinatelecom.zhiye.com", display_name="中国电信"),
    CompanyConfig("中国铁塔", "zhiye", "https://chinatowercom.zhiye.com", display_name="中国铁塔"),
    CompanyConfig("中粮集团", "zhiye", "https://cofco.zhiye.com", display_name="中粮集团"),
    CompanyConfig("华润集团", "zhiye", "https://crg.zhiye.com", display_name="华润集团"),
    CompanyConfig("中国远洋海运", "zhiye", "https://cosco.zhiye.com", display_name="中国远洋海运集团"),
    CompanyConfig("中国宝武钢铁", "zhiye", "https://baowu.zhiye.com", display_name="中国宝武钢铁集团"),
    CompanyConfig("中国广核集团", "zhiye", "https://cgnpc.zhiye.com", display_name="中国广核集团"),
    CompanyConfig("中国节能环保", "zhiye", "https://cecep.zhiye.com", display_name="中国节能环保集团"),
    CompanyConfig("中国建材集团", "zhiye", "https://cnbm.zhiye.com", display_name="中国建材集团"),
    CompanyConfig("中国电子信息产业", "zhiye", "https://cec.zhiye.com", display_name="中国电子信息产业集团"),
    CompanyConfig("中国电子科技集团", "zhiye", "https://cetc.zhiye.com", display_name="中国电子科技集团"),
    CompanyConfig("中国兵器工业集团", "zhiye", "https://norinco.zhiye.com", display_name="中国兵器工业集团"),
    CompanyConfig("中国医药集团", "zhiye", "https://sinopharm.zhiye.com", display_name="中国医药集团"),
    CompanyConfig("鞍钢集团", "zhiye", "https://ansteel.zhiye.com", display_name="鞍钢集团"),
    CompanyConfig("国家电网", "custom_pw", "https://zhaopin.sgcc.com.cn", display_name="国家电网"),
    CompanyConfig("国家能源投资集团", "zhiye", "https://chnenergy.zhiye.com", display_name="国家能源投资集团"),
    CompanyConfig("中国三峡集团", "zhiye", "https://ctg.zhiye.com", display_name="中国三峡集团"),
]


YANGQI_EXPANSION_3 = [
    CompanyConfig("中国航空工业集团", "zhiye", "https://avic.zhiye.com", display_name="中国航空工业集团"),
    CompanyConfig("中国商用飞机", "zhiye", "https://comac.zhiye.com", display_name="中国商用飞机"),
    CompanyConfig("中国铁路工程集团", "zhiye", "https://crec.zhiye.com", display_name="中国铁路工程集团"),
    CompanyConfig("中国铁道建筑集团", "zhiye", "https://crcc.zhiye.com", display_name="中国铁道建筑集团"),
    CompanyConfig("中国铝业集团", "zhiye", "https://chalco.zhiye.com", display_name="中国铝业集团"),
    CompanyConfig("中国第一汽车集团", "zhiye", "https://faw.zhiye.com", display_name="中国第一汽车集团"),
    CompanyConfig("东风汽车集团", "zhiye", "https://dfmc.zhiye.com", display_name="东风汽车集团"),
    CompanyConfig("中国工商银行", "zhiye", "https://icbc.zhiye.com", display_name="中国工商银行"),
    CompanyConfig("中国农业银行", "zhiye", "https://abchina.zhiye.com", display_name="中国农业银行"),
    CompanyConfig("中国建设银行", "zhiye", "https://ccb.zhiye.com", display_name="中国建设银行"),
    CompanyConfig("中国南方航空", "zhiye", "https://csair.zhiye.com", display_name="中国南方航空"),
    CompanyConfig("中国东方航空", "zhiye", "https://ceair.zhiye.com", display_name="中国东方航空"),
    CompanyConfig("中国国航", "zhiye", "https://airchina.zhiye.com", display_name="中国国航"),
    CompanyConfig("中国一重集团", "zhiye", "https://cfhi.zhiye.com", display_name="中国一重集团"),
    CompanyConfig("中国东方电气集团", "zhiye", "https://dongfangelectric.zhiye.com", display_name="中国东方电气集团"),
    CompanyConfig("中国中信集团", "zhiye", "https://citic.zhiye.com", display_name="中国中信集团"),
    CompanyConfig("中国光大集团", "zhiye", "https://ebchina.zhiye.com", display_name="中国光大集团"),
    CompanyConfig("中国兵器装备集团", "zhiye", "https://csgc.zhiye.com", display_name="中国兵器装备集团"),
    CompanyConfig("中国农业发展银行", "zhiye", "https://adbc.zhiye.com", display_name="中国农业发展银行"),
    CompanyConfig("中国冶金科工集团", "zhiye", "https://mcc.zhiye.com", display_name="中国冶金科工集团"),
    CompanyConfig("中国化学工程集团", "zhiye", "https://cncec.zhiye.com", display_name="中国化学工程集团"),
    CompanyConfig("中国华录集团", "zhiye", "https://hualu.zhiye.com", display_name="中国华录集团"),
    CompanyConfig("中国国新控股", "zhiye", "https://crhc.zhiye.com", display_name="中国国新控股"),
    CompanyConfig("中国安能建设集团", "zhiye", "https://chinaan.zhiye.com", display_name="中国安能建设集团"),
    CompanyConfig("中国建设科技集团", "zhiye", "https://cadreg.zhiye.com", display_name="中国建设科技集团"),
    CompanyConfig("中国机械工业集团", "zhiye", "https://sinomach.zhiye.com", display_name="中国机械工业集团"),
    CompanyConfig("中国煤炭地质总局", "zhiye", "https://ccgc.zhiye.com", display_name="中国煤炭地质总局"),
    CompanyConfig("中国煤炭科工集团", "zhiye", "https://ccteg.zhiye.com", display_name="中国煤炭科工集团"),
    CompanyConfig("中国物流集团", "zhiye", "https://clg.zhiye.com", display_name="中国物流集团"),
    CompanyConfig("中国电力建设集团", "zhiye", "https://powerchina.zhiye.com", display_name="中国电力建设集团"),
    CompanyConfig("中国盐业集团", "zhiye", "https://chinasalt.zhiye.com", display_name="中国盐业集团"),
    CompanyConfig("中国矿产资源集团", "zhiye", "https://cmrg.zhiye.com", display_name="中国矿产资源集团"),
    CompanyConfig("中国移动", "zhiye", "https://chinamobile.zhiye.com", display_name="中国移动"),
    CompanyConfig("中国稀土集团", "zhiye", "https://creg.zhiye.com", display_name="中国稀土集团"),
    CompanyConfig("中国航空发动机集团", "zhiye", "https://aecc.zhiye.com", display_name="中国航空发动机集团"),
    CompanyConfig("中国航空油料集团", "zhiye", "https://cnaf.zhiye.com", display_name="中国航空油料集团"),
    CompanyConfig("中国融通资产管理集团", "zhiye", "https://rongtong.zhiye.com", display_name="中国融通资产管理集团"),
    CompanyConfig("中国诚通控股", "zhiye", "https://chengtong.zhiye.com", display_name="中国诚通控股"),
    CompanyConfig("中国进出口银行", "zhiye", "https://eximbank.zhiye.com", display_name="中国进出口银行"),
    CompanyConfig("中国储备粮管理集团", "zhiye", "https://sinograin.zhiye.com", display_name="中国储备粮管理集团"),
    CompanyConfig("中国黄金集团", "zhiye", "https://chinagold.zhiye.com", display_name="中国黄金集团"),
    CompanyConfig("中国中丝集团", "zhiye", "https://chinasilk.zhiye.com", display_name="中国中丝集团"),
]


WORKDAY_EXPANSION_3 = [
    # Accessible from China
    CompanyConfig("迪士尼", "workday", "https://disney.wd5.myworkdayjobs.com/disneycareer",
                  source_type="official:workday", display_name="迪士尼"),
    CompanyConfig("开云集团", "workday", "https://kering.wd3.myworkdayjobs.com/Kering",
                  source_type="official:workday", display_name="开云集团"),
    # Geo-blocked from China IP
    CompanyConfig("ASML", "workday", "https://asml.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="ASML"),
    CompanyConfig("Airbnb", "workday", "https://airbnb.wd5.myworkdayjobs.com/Airbnb",
                  source_type="official:workday", status="geo_blocked", display_name="Airbnb"),
    CompanyConfig("Canva", "workday", "https://canva.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="Canva"),
    CompanyConfig("GE医疗", "workday", "https://gehealthcare.wd5.myworkdayjobs.com/GEHealthCare",
                  source_type="official:workday", status="geo_blocked", display_name="GE医疗"),
    CompanyConfig("Inditex", "workday", "https://inditex.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="Inditex"),
    CompanyConfig("Juniper Networks", "workday", "https://juniper.wd1.myworkdayjobs.com/Juniper_Careers",
                  source_type="official:workday", status="geo_blocked", display_name="Juniper Networks"),
    CompanyConfig("KKR", "workday", "https://kkr.wd1.myworkdayjobs.com/KKR",
                  source_type="official:workday", status="geo_blocked", display_name="KKR"),
    CompanyConfig("Mobileye", "workday", "https://mobileye.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="Mobileye"),
    CompanyConfig("UPS", "workday", "https://ups.wd1.myworkdayjobs.com/UPSCareers",
                  source_type="official:workday", status="geo_blocked", display_name="UPS"),
    CompanyConfig("亿滋国际", "workday", "https://mondelezinternational.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="亿滋国际"),
    CompanyConfig("保时捷", "workday", "https://porsche.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="保时捷"),
    CompanyConfig("凯捷", "workday", "https://capgemini.wd3.myworkdayjobs.com/Global",
                  source_type="official:workday", status="geo_blocked", display_name="凯捷"),
    CompanyConfig("力拓", "workday", "https://riotinto.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="力拓"),
    CompanyConfig("勃林格殷格翰", "workday", "https://boehringeringelheim.wd3.myworkdayjobs.com/BoehringerExternalSite",
                  source_type="official:workday", status="geo_blocked", display_name="勃林格殷格翰"),
    CompanyConfig("博柏利", "workday", "https://burberry.wd3.myworkdayjobs.com/Burberry",
                  source_type="official:workday", status="geo_blocked", display_name="博柏利"),
    CompanyConfig("埃森哲", "workday", "https://accenture.wd3.myworkdayjobs.com/AccentureCareers",
                  source_type="official:workday", status="geo_blocked", display_name="埃森哲"),
    CompanyConfig("大众汽车", "workday", "https://volkswagen.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="大众汽车"),
    CompanyConfig("安捷伦", "workday", "https://agilent.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="安捷伦"),
    CompanyConfig("安进", "workday", "https://amgen.wd5.myworkdayjobs.com/Amgen",
                  source_type="official:workday", status="geo_blocked", display_name="安进"),
    CompanyConfig("安联保险", "workday", "https://allianz.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="安联保险"),
    CompanyConfig("宜家", "workday", "https://ikea.wd3.myworkdayjobs.com/Global",
                  source_type="official:workday", status="geo_blocked", display_name="宜家"),
    CompanyConfig("康宁", "workday", "https://corning.wd5.myworkdayjobs.com/Corning",
                  source_type="official:workday", status="geo_blocked", display_name="康宁"),
    CompanyConfig("康明斯", "workday", "https://cummins.wd5.myworkdayjobs.com/Cummins",
                  source_type="official:workday", status="geo_blocked", display_name="康明斯"),
    CompanyConfig("德意志银行", "workday", "https://deutschebank.wd5.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="德意志银行"),
    CompanyConfig("必和必拓", "workday", "https://bhp.wd1.myworkdayjobs.com/BHP_Careers",
                  source_type="official:workday", status="geo_blocked", display_name="必和必拓"),
    CompanyConfig("日产汽车", "workday", "https://nissan.wd5.myworkdayjobs.com/Nissan_Careers",
                  source_type="official:workday", status="geo_blocked", display_name="日产汽车"),
    CompanyConfig("本田汽车", "workday", "https://honda.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="本田汽车"),
    CompanyConfig("林德", "workday", "https://linde.wd5.myworkdayjobs.com/Linde",
                  source_type="official:workday", status="geo_blocked", display_name="林德"),
    CompanyConfig("标普全球", "workday", "https://spglobal.wd5.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="标普全球"),
    CompanyConfig("梅赛德斯-奔驰", "workday", "https://mercedesbenz.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="梅赛德斯-奔驰"),
    CompanyConfig("武田制药", "workday", "https://takeda.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="武田制药"),
    CompanyConfig("汇丰银行", "workday", "https://hsbc.wd3.myworkdayjobs.com/HSBC_Careers",
                  source_type="official:workday", status="geo_blocked", display_name="汇丰银行"),
    CompanyConfig("法国巴黎银行", "workday", "https://bnpparibas.wd3.myworkdayjobs.com/BNP_Paribas",
                  source_type="official:workday", status="geo_blocked", display_name="法国巴黎银行"),
    CompanyConfig("波士顿科学", "workday", "https://bostonscientific.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="波士顿科学"),
    CompanyConfig("渣打银行", "workday", "https://sc.wd3.myworkdayjobs.com/SCB",
                  source_type="official:workday", status="geo_blocked", display_name="渣打银行"),
    CompanyConfig("爱立信", "workday", "https://ericsson.wd3.myworkdayjobs.com/Ericsson_Careers",
                  source_type="official:workday", status="geo_blocked", display_name="爱立信"),
    CompanyConfig("现代汽车", "workday", "https://hyundai.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="现代汽车"),
    CompanyConfig("瑞银集团", "workday", "https://ubs.wd3.myworkdayjobs.com/UBS_Careers",
                  source_type="official:workday", status="geo_blocked", display_name="瑞银集团"),
    CompanyConfig("索尼", "workday", "https://sony.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="索尼"),
    CompanyConfig("美世", "workday", "https://mercer.wd5.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="美世"),
    CompanyConfig("美国运通", "workday", "https://americanexpress.wd5.myworkdayjobs.com/AmericanExpress",
                  source_type="official:workday", status="geo_blocked", display_name="美国运通"),
    CompanyConfig("联邦快递", "workday", "https://fedex.wd5.myworkdayjobs.com/FedEx_Careers",
                  source_type="official:workday", status="geo_blocked", display_name="联邦快递"),
    CompanyConfig("英国石油", "workday", "https://bp.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="英国石油"),
    CompanyConfig("诺基亚", "workday", "https://nokia.wd3.myworkdayjobs.com/Nokia_Careers",
                  source_type="official:workday", status="geo_blocked", display_name="诺基亚"),
    CompanyConfig("谷歌", "workday", "https://google.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="谷歌"),
    CompanyConfig("赛默飞世尔", "workday", "https://thermofisher.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="赛默飞世尔"),
    CompanyConfig("达能", "workday", "https://danone.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="达能"),
    CompanyConfig("采埃孚", "workday", "https://zf.wd3.myworkdayjobs.com/ZF_Careers",
                  source_type="official:workday", status="geo_blocked", display_name="采埃孚"),
    CompanyConfig("特斯拉", "workday", "https://tesla.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="特斯拉"),
    CompanyConfig("空客", "workday", "https://airbus.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="空客"),
    CompanyConfig("丰田汽车", "workday", "https://toyota.wd5.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="丰田汽车"),
    CompanyConfig("佳能", "workday", "https://canon.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="佳能"),
    CompanyConfig("圣戈班", "workday", "https://saintgobain.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="圣戈班"),
    CompanyConfig("奥迪", "workday", "https://audi.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="奥迪"),
    CompanyConfig("富士通", "workday", "https://fujitsu.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="富士通"),
    CompanyConfig("希捷", "workday", "https://seagate.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="希捷"),
    CompanyConfig("敦豪", "workday", "https://dhl.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="敦豪"),
    CompanyConfig("洲际酒店集团", "workday", "https://ihg.wd3.myworkdayjobs.com/IHG_Careers",
                  source_type="official:workday", status="geo_blocked", display_name="洲际酒店集团"),
    CompanyConfig("瓦克化学", "workday", "https://wacker.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="瓦克化学"),
    CompanyConfig("起亚汽车", "workday", "https://kia.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="起亚汽车"),
    CompanyConfig("达索系统", "workday", "https://3ds.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="达索系统"),
    CompanyConfig("迪卡侬", "workday", "https://decathlon.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="迪卡侬"),
    CompanyConfig("阿克苏诺贝尔", "workday", "https://akzonobel.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="阿克苏诺贝尔"),
    CompanyConfig("阿尔斯通", "workday", "https://alstom.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="阿尔斯通"),
    CompanyConfig("默克集团", "workday", "https://merckgroup.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="默克集团"),
    CompanyConfig("舍弗勒", "workday", "https://schaeffler.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="舍弗勒"),
    CompanyConfig("乐高", "workday", "https://lego.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="乐高"),
    CompanyConfig("大金工业", "workday", "https://daikin.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="大金工业"),
    CompanyConfig("大陆集团", "workday", "https://continental.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="大陆集团"),
    CompanyConfig("汉高", "workday", "https://henkel.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="汉高"),
    CompanyConfig("资生堂", "workday", "https://shiseido.wd1.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="资生堂"),
    CompanyConfig("费列罗", "workday", "https://ferrero.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="费列罗"),
    CompanyConfig("蒂森克虏伯", "workday", "https://thyssenkrupp.wd3.myworkdayjobs.com/External",
                  source_type="official:workday", status="geo_blocked", display_name="蒂森克虏伯"),
]


MISC_WAIQI_EXPANSION = [
    # Companies using other platforms - status suspended until adapter available
    CompanyConfig("Cockroach Labs", "custom_pw", "https://www.cockroachlabs.com/careers/", status="suspended", display_name="Cockroach Labs"),
    CompanyConfig("Confluent", "custom_pw", "https://careers.confluent.io/", status="suspended", display_name="Confluent"),
    CompanyConfig("Grab", "custom_pw", "https://grab.careers/", status="suspended", display_name="Grab"),
    CompanyConfig("LG新能源", "custom_pw", "https://careers.lgensol.com/", status="suspended", display_name="LG新能源"),
    CompanyConfig("LG集团", "custom_pw", "https://careers.lg.com/", status="suspended", display_name="LG集团"),
    CompanyConfig("Naver", "custom_pw", "https://recruit.navercorp.com/", status="suspended", display_name="Naver"),
    CompanyConfig("Rovio", "custom_pw", "https://www.rovio.com/careers/", status="suspended", display_name="Rovio"),
    CompanyConfig("SK On", "custom_pw", "https://skon.recruiter.co.kr/", status="suspended", display_name="SK On"),
    CompanyConfig("SKF", "custom_pw", "https://www.skf.com/group/careers", status="suspended", display_name="SKF"),
    CompanyConfig("SK海力士", "custom_pw", "https://recruit.skhynix.com/", status="suspended", display_name="SK海力士"),
    CompanyConfig("SK集团", "custom_pw", "https://www.skcareers.com/", status="suspended", display_name="SK集团"),
    CompanyConfig("Stellantis", "custom_pw", "https://careers.stellantis.com/", status="suspended", display_name="Stellantis"),
    CompanyConfig("Supercell", "custom_pw", "https://supercell.com/en/careers/", status="suspended", display_name="Supercell"),
    CompanyConfig("WPP", "custom_pw", "https://www.wpp.com/careers", status="suspended", display_name="WPP"),
    CompanyConfig("亚德诺", "custom_pw", "https://careers.analog.com/", status="suspended", display_name="亚德诺"),
    CompanyConfig("吉利德科学", "custom_pw", "https://www.gilead.com/careers", status="suspended", display_name="吉利德科学"),
    CompanyConfig("嘉能可", "custom_pw", "https://www.glencore.com/careers", status="suspended", display_name="嘉能可"),
    CompanyConfig("恒宝", "custom_pw", "https://www.gemalto.com/careers", status="suspended", display_name="恒宝"),
    CompanyConfig("新加坡政府投资公司", "custom_pw", "https://www.gic.com.sg/careers/", status="suspended", display_name="新加坡政府投资公司"),
    CompanyConfig("穆巴达拉投资公司", "custom_pw", "https://www.mubadala.com/en/careers", status="suspended", display_name="穆巴达拉投资公司"),
    CompanyConfig("苹果", "custom_pw", "https://jobs.apple.com/", status="suspended", display_name="苹果"),
    CompanyConfig("赛门铁克", "custom_pw", "https://www.broadcom.com/company/careers", status="suspended", display_name="赛门铁克"),
    CompanyConfig("赛门铁克_Veritas", "custom_pw", "https://www.veritas.com/company/careers", status="suspended", display_name="赛门铁克_Veritas"),
    CompanyConfig("巴西航空工业公司", "custom_pw", "https://embraer.com/global/en/careers", status="suspended", display_name="巴西航空工业公司"),
]


ZHIYE_WAIQI_EXPANSION = [
    CompanyConfig("三井住友银行", "zhiye", "https://smbc.zhiye.com", display_name="三井住友银行"),
    CompanyConfig("三井物产", "zhiye", "https://mitsui.zhiye.com", display_name="三井物产"),
    CompanyConfig("三星SDI", "zhiye", "https://samsungsdi.zhiye.com", display_name="三星SDI"),
    CompanyConfig("三菱商事", "zhiye", "https://mitsubishicorp.zhiye.com", display_name="三菱商事"),
    CompanyConfig("三菱日联银行", "zhiye", "https://mufg.zhiye.com", display_name="三菱日联银行"),
    CompanyConfig("三菱电机", "zhiye", "https://mitsubishielectric.zhiye.com", display_name="三菱电机"),
    CompanyConfig("世邦魏理仕", "zhiye", "https://cbre.zhiye.com", display_name="世邦魏理仕"),
    CompanyConfig("丰树集团", "zhiye", "https://mapletree.zhiye.com", display_name="丰树集团"),
    CompanyConfig("丸红", "zhiye", "https://marubeni.zhiye.com", display_name="丸红"),
    CompanyConfig("乐天集团", "zhiye", "https://rakuten.zhiye.com", display_name="乐天集团"),
    CompanyConfig("伊藤忠", "zhiye", "https://itochu.zhiye.com", display_name="伊藤忠"),
    CompanyConfig("住友商事", "zhiye", "https://sumitomocorp.zhiye.com", display_name="住友商事"),
    CompanyConfig("保诚集团", "zhiye", "https://prudential.zhiye.com", display_name="保诚集团"),
    CompanyConfig("倍耐力", "zhiye", "https://pirelli.zhiye.com", display_name="倍耐力"),
    CompanyConfig("凯德集团", "zhiye", "https://capitaland.zhiye.com", display_name="凯德集团"),
    CompanyConfig("凯雷投资集团", "zhiye", "https://carlyle.zhiye.com", display_name="凯雷投资集团"),
    CompanyConfig("卫材", "zhiye", "https://eisai.zhiye.com", display_name="卫材"),
    CompanyConfig("印孚瑟斯", "zhiye", "https://infosys.zhiye.com", display_name="印孚瑟斯"),
    CompanyConfig("历峰集团", "zhiye", "https://richemont.zhiye.com", display_name="历峰集团"),
    CompanyConfig("吉宝集团", "zhiye", "https://keppel.zhiye.com", display_name="吉宝集团"),
    CompanyConfig("喜力", "zhiye", "https://heineken.zhiye.com", display_name="喜力"),
    CompanyConfig("嘉士伯", "zhiye", "https://carlsberg.zhiye.com", display_name="嘉士伯"),
    CompanyConfig("埃尼集团", "zhiye", "https://eni.zhiye.com", display_name="埃尼集团"),
    CompanyConfig("培生", "zhiye", "https://pearson.zhiye.com", display_name="培生"),
    CompanyConfig("塔塔咨询", "zhiye", "https://tcs.zhiye.com", display_name="塔塔咨询"),
    CompanyConfig("夏普", "zhiye", "https://sharp.zhiye.com", display_name="夏普"),
    CompanyConfig("太古集团", "zhiye", "https://swire.zhiye.com", display_name="太古集团"),
    CompanyConfig("奥林巴斯", "zhiye", "https://olympus.zhiye.com", display_name="奥林巴斯"),
    CompanyConfig("威立雅", "zhiye", "https://veolia.zhiye.com", display_name="威立雅"),
    CompanyConfig("威达信", "zhiye", "https://mmc.zhiye.com", display_name="威达信"),
    CompanyConfig("安斯泰来", "zhiye", "https://astellas.zhiye.com", display_name="安斯泰来"),
    CompanyConfig("安盛集团", "zhiye", "https://axa.zhiye.com", display_name="安盛集团"),
    CompanyConfig("宏利金融", "zhiye", "https://manulife.zhiye.com", display_name="宏利金融"),
    CompanyConfig("富士胶片", "zhiye", "https://fujifilm.zhiye.com", display_name="富士胶片"),
    CompanyConfig("帝斯曼-芬美意", "zhiye", "https://dsm.zhiye.com", display_name="帝斯曼-芬美意"),
    CompanyConfig("庞巴迪", "zhiye", "https://bombardier.zhiye.com", display_name="庞巴迪"),
    CompanyConfig("忠利保险", "zhiye", "https://generali.zhiye.com", display_name="忠利保险"),
    CompanyConfig("意大利国家电力公司", "zhiye", "https://enel.zhiye.com", display_name="意大利国家电力公司"),
    CompanyConfig("戴德梁行", "zhiye", "https://cushwake.zhiye.com", display_name="戴德梁行"),
    CompanyConfig("斯堪尼亚", "zhiye", "https://scania.zhiye.com", display_name="斯堪尼亚"),
    CompanyConfig("斯沃琪集团", "zhiye", "https://swatch.zhiye.com", display_name="斯沃琪集团"),
    CompanyConfig("星展银行", "zhiye", "https://dbs.zhiye.com", display_name="星展银行"),
    CompanyConfig("曼恩", "zhiye", "https://man.zhiye.com", display_name="曼恩"),
    CompanyConfig("松下", "zhiye", "https://panasonic.zhiye.com", display_name="松下"),
    CompanyConfig("欧姆龙", "zhiye", "https://omron.zhiye.com", display_name="欧姆龙"),
    CompanyConfig("永明金融", "zhiye", "https://sunlife.zhiye.com", display_name="永明金融"),
    CompanyConfig("汉莎航空", "zhiye", "https://lufthansa.zhiye.com", display_name="汉莎航空"),
    CompanyConfig("沙特阿美", "zhiye", "https://aramco.zhiye.com", display_name="沙特阿美"),
    CompanyConfig("法国兴业银行", "zhiye", "https://societegenerale.zhiye.com", display_name="法国兴业银行"),
    CompanyConfig("法国电力集团", "zhiye", "https://edf.zhiye.com", display_name="法国电力集团"),
    CompanyConfig("泰雷兹", "zhiye", "https://thalesgroup.zhiye.com", display_name="泰雷兹"),
    CompanyConfig("派拓网络", "zhiye", "https://paloaltonetworks.zhiye.com", display_name="派拓网络"),
    CompanyConfig("浦项制铁", "zhiye", "https://posco.zhiye.com", display_name="浦项制铁"),
    CompanyConfig("液化空气集团", "zhiye", "https://airliquide.zhiye.com", display_name="液化空气集团"),
    CompanyConfig("淡水河谷", "zhiye", "https://vale.zhiye.com", display_name="淡水河谷"),
    CompanyConfig("淡马锡", "zhiye", "https://temasek.zhiye.com", display_name="淡马锡"),
    CompanyConfig("澳新银行", "zhiye", "https://anz.zhiye.com", display_name="澳新银行"),
    CompanyConfig("灵北制药", "zhiye", "https://lundbeck.zhiye.com", display_name="灵北制药"),
    CompanyConfig("爱马仕", "zhiye", "https://hermes.zhiye.com", display_name="爱马仕"),
    CompanyConfig("玛氏", "zhiye", "https://mars.zhiye.com", display_name="玛氏"),
    CompanyConfig("理光", "zhiye", "https://ricoh.zhiye.com", display_name="理光"),
    CompanyConfig("瑞士再保险", "zhiye", "https://swissre.zhiye.com", display_name="瑞士再保险"),
    CompanyConfig("瓦锡兰", "zhiye", "https://wartsila.zhiye.com", display_name="瓦锡兰"),
    CompanyConfig("科汉森", "zhiye", "https://chr-hansen.zhiye.com", display_name="科汉森"),
    CompanyConfig("第一三共", "zhiye", "https://daiichisankyo.zhiye.com", display_name="第一三共"),
    CompanyConfig("绫致时装", "zhiye", "https://bestseller.zhiye.com", display_name="绫致时装"),
    CompanyConfig("维布络", "zhiye", "https://wipro.zhiye.com", display_name="维布络"),
    CompanyConfig("维斯塔斯", "zhiye", "https://vestas.zhiye.com", display_name="维斯塔斯"),
    CompanyConfig("芬欧汇川", "zhiye", "https://upm.zhiye.com", display_name="芬欧汇川"),
    CompanyConfig("花旗银行", "zhiye", "https://citi.zhiye.com", display_name="花旗银行"),
    CompanyConfig("苏黎世保险", "zhiye", "https://zurich.zhiye.com", display_name="苏黎世保险"),
    CompanyConfig("荷兰国际集团", "zhiye", "https://ing.zhiye.com", display_name="荷兰国际集团"),
    CompanyConfig("西班牙电信", "zhiye", "https://telefonica.zhiye.com", display_name="西班牙电信"),
    CompanyConfig("诺维信", "zhiye", "https://novozymes.zhiye.com", display_name="诺维信"),
    CompanyConfig("贺利氏", "zhiye", "https://heraeus.zhiye.com", display_name="贺利氏"),
    CompanyConfig("赛峰集团", "zhiye", "https://safran.zhiye.com", display_name="赛峰集团"),
    CompanyConfig("路透社", "zhiye", "https://reuters.zhiye.com", display_name="路透社"),
    CompanyConfig("达飞海运", "zhiye", "https://cmacgm.zhiye.com", display_name="达飞海运"),
    CompanyConfig("通力电梯", "zhiye", "https://kone.zhiye.com", display_name="通力电梯"),
    CompanyConfig("通快", "zhiye", "https://trumpf.zhiye.com", display_name="通快"),
    CompanyConfig("里德爱思唯尔", "zhiye", "https://relx.zhiye.com", display_name="里德爱思唯尔"),
    CompanyConfig("野村证券", "zhiye", "https://nomura.zhiye.com", display_name="野村证券"),
    CompanyConfig("阿特拉斯·科普柯", "zhiye", "https://atlascopco.zhiye.com", display_name="阿特拉斯·科普柯"),
    CompanyConfig("陆逊梯卡", "zhiye", "https://essilorluxottica.zhiye.com", display_name="陆逊梯卡"),
    CompanyConfig("马士基", "zhiye", "https://maersk.zhiye.com", display_name="马士基"),
    CompanyConfig("鹏瑞利集团", "zhiye", "https://perennial.zhiye.com", display_name="鹏瑞利集团"),
    CompanyConfig("麦格理银行", "zhiye", "https://macquarie.zhiye.com", display_name="麦格理银行"),
    CompanyConfig("麦格纳", "zhiye", "https://magna.zhiye.com", display_name="麦格纳"),
]


ZHIYE_EXTRA_EXPANSION_2 = [
    # Japanese companies
    CompanyConfig("日本电产", "zhiye", "https://nidec.zhiye.com", display_name="日本电产"),
    CompanyConfig("村田制作所", "zhiye", "https://murata.zhiye.com", display_name="村田制作所"),
    CompanyConfig("京瓷", "zhiye", "https://kyocera.zhiye.com", display_name="京瓷"),
    CompanyConfig("东京电子", "zhiye", "https://tel.zhiye.com", display_name="东京电子"),
    CompanyConfig("瑞萨电子", "zhiye", "https://renesas.zhiye.com", display_name="瑞萨电子"),
    CompanyConfig("横河电机", "zhiye", "https://yokogawa.zhiye.com", display_name="横河电机"),
    CompanyConfig("住友电工", "zhiye", "https://sews.zhiye.com", display_name="住友电工"),
    CompanyConfig("日本烟草", "zhiye", "https://jti.zhiye.com", display_name="日本烟草"),
    CompanyConfig("三得利", "zhiye", "https://suntory.zhiye.com", display_name="三得利"),
    CompanyConfig("味之素", "zhiye", "https://ajinomoto.zhiye.com", display_name="味之素"),
    CompanyConfig("花王", "zhiye", "https://kao.zhiye.com", display_name="花王"),
    CompanyConfig("狮王", "zhiye", "https://lion.zhiye.com", display_name="狮王"),
    CompanyConfig("普利司通", "zhiye", "https://bridgestone.zhiye.com", display_name="普利司通"),
    CompanyConfig("电装", "zhiye", "https://denso.zhiye.com", display_name="电装"),
    CompanyConfig("爱信", "zhiye", "https://aisin.zhiye.com", display_name="爱信"),
    CompanyConfig("小松", "zhiye", "https://komatsu.zhiye.com", display_name="小松"),
    CompanyConfig("久保田", "zhiye", "https://kubota.zhiye.com", display_name="久保田"),
    CompanyConfig("三菱重工", "zhiye", "https://mhi.zhiye.com", display_name="三菱重工"),
    CompanyConfig("川崎重工", "zhiye", "https://khi.zhiye.com", display_name="川崎重工"),
    CompanyConfig("IHI", "zhiye", "https://ihi.zhiye.com", display_name="IHI"),
    CompanyConfig("日本邮船", "zhiye", "https://nyk.zhiye.com", display_name="日本邮船"),
    CompanyConfig("商船三井", "zhiye", "https://mol.zhiye.com", display_name="商船三井"),
    CompanyConfig("大和证券", "zhiye", "https://daiwa.zhiye.com", display_name="大和证券"),
    CompanyConfig("瑞穗银行", "zhiye", "https://mizuho.zhiye.com", display_name="瑞穗银行"),
    CompanyConfig("软银", "zhiye", "https://softbank.zhiye.com", display_name="软银"),
    CompanyConfig("NTT", "zhiye", "https://ntt.zhiye.com", display_name="NTT"),
    CompanyConfig("KDDI", "zhiye", "https://kddi.zhiye.com", display_name="KDDI"),
    # Korean companies
    CompanyConfig("现代重工", "zhiye", "https://hhi.zhiye.com", display_name="现代重工"),
    CompanyConfig("韩华", "zhiye", "https://hanwha.zhiye.com", display_name="韩华"),
    CompanyConfig("CJ集团", "zhiye", "https://cj.zhiye.com", display_name="CJ集团"),
    CompanyConfig("韩国电力", "zhiye", "https://kepco.zhiye.com", display_name="韩国电力"),
    # European companies
    CompanyConfig("斯凯孚", "zhiye", "https://skf.zhiye.com", display_name="斯凯孚"),
    CompanyConfig("阿法拉伐", "zhiye", "https://alfalaval.zhiye.com", display_name="阿法拉伐"),
    CompanyConfig("山特维克", "zhiye", "https://sandvik.zhiye.com", display_name="山特维克"),
    CompanyConfig("伊莱克斯", "zhiye", "https://electrolux.zhiye.com", display_name="伊莱克斯"),
    CompanyConfig("利乐", "zhiye", "https://tetrapak.zhiye.com", display_name="利乐"),
    CompanyConfig("雅高集团", "zhiye", "https://accor.zhiye.com", display_name="雅高集团"),
    CompanyConfig("米其林", "zhiye", "https://michelin.zhiye.com", display_name="米其林"),
    CompanyConfig("施维雅", "zhiye", "https://servier.zhiye.com", display_name="施维雅"),
    CompanyConfig("依视路", "zhiye", "https://essilor.zhiye.com", display_name="依视路"),
    CompanyConfig("安赛乐米塔尔", "zhiye", "https://arcelormittal.zhiye.com", display_name="安赛乐米塔尔"),
    CompanyConfig("帝亚吉欧", "zhiye", "https://diageo.zhiye.com", display_name="帝亚吉欧"),
    # American companies
    CompanyConfig("陶氏", "zhiye", "https://dow.zhiye.com", display_name="陶氏"),
    CompanyConfig("杜邦", "zhiye", "https://dupont.zhiye.com", display_name="杜邦"),
    CompanyConfig("江森自控", "zhiye", "https://johnsoncontrols.zhiye.com", display_name="江森自控"),
    CompanyConfig("伊顿", "zhiye", "https://eaton.zhiye.com", display_name="伊顿"),
    CompanyConfig("帕克汉尼汾", "zhiye", "https://parker.zhiye.com", display_name="帕克汉尼汾"),
    CompanyConfig("丹佛斯", "zhiye", "https://danfoss.zhiye.com", display_name="丹佛斯"),
    CompanyConfig("格兰富", "zhiye", "https://grundfos.zhiye.com", display_name="格兰富"),
    CompanyConfig("百威英博", "zhiye", "https://abinbev.zhiye.com", display_name="百威英博"),
    CompanyConfig("嘉吉", "zhiye", "https://cargill.zhiye.com", display_name="嘉吉"),
    CompanyConfig("ADM", "zhiye", "https://adm.zhiye.com", display_name="ADM"),
    CompanyConfig("邦吉", "zhiye", "https://bunge.zhiye.com", display_name="邦吉"),
    CompanyConfig("路易达孚", "zhiye", "https://ldc.zhiye.com", display_name="路易达孚"),
    CompanyConfig("益海嘉里", "zhiye", "https://yihaikerry.zhiye.com", display_name="益海嘉里"),
    CompanyConfig("好时", "zhiye", "https://hersheys.zhiye.com", display_name="好时"),
    CompanyConfig("高露洁", "zhiye", "https://colgate.zhiye.com", display_name="高露洁"),
    CompanyConfig("金佰利", "zhiye", "https://kimberlyclark.zhiye.com", display_name="金佰利"),
    CompanyConfig("利洁时", "zhiye", "https://reckitt.zhiye.com", display_name="利洁时"),
    CompanyConfig("科勒", "zhiye", "https://kohler.zhiye.com", display_name="科勒"),
    # Luxury brands
    CompanyConfig("香奈儿", "zhiye", "https://chanel.zhiye.com", display_name="香奈儿"),
    CompanyConfig("迪奥", "zhiye", "https://dior.zhiye.com", display_name="迪奥"),
    CompanyConfig("普拉达", "zhiye", "https://prada.zhiye.com", display_name="普拉达"),
    CompanyConfig("古驰", "zhiye", "https://gucci.zhiye.com", display_name="古驰"),
    CompanyConfig("范思哲", "zhiye", "https://versace.zhiye.com", display_name="范思哲"),
    CompanyConfig("卡地亚", "zhiye", "https://cartier.zhiye.com", display_name="卡地亚"),
    CompanyConfig("蒂芙尼", "zhiye", "https://tiffany.zhiye.com", display_name="蒂芙尼"),
    CompanyConfig("路易威登", "zhiye", "https://louisvuitton.zhiye.com", display_name="路易威登"),
    CompanyConfig("汉斯格雅", "zhiye", "https://hansgrohe.zhiye.com", display_name="汉斯格雅"),
    CompanyConfig("箭牌", "zhiye", "https://wrigley.zhiye.com", display_name="箭牌"),
    CompanyConfig("多美达", "zhiye", "https://dometic.zhiye.com", display_name="多美达"),
    # Consulting & Professional Services
    CompanyConfig("奥纬咨询", "zhiye", "https://oliverwyman.zhiye.com", display_name="奥纬咨询"),
    CompanyConfig("罗兰贝格", "zhiye", "https://rolandberger.zhiye.com", display_name="罗兰贝格"),
    CompanyConfig("科尔尼", "zhiye", "https://kearney.zhiye.com", display_name="科尔尼"),
    CompanyConfig("韦莱韬悦", "zhiye", "https://wtwco.zhiye.com", display_name="韦莱韬悦"),
    CompanyConfig("怡安", "zhiye", "https://aon.zhiye.com", display_name="怡安"),
    CompanyConfig("仲量联行", "zhiye", "https://jll.zhiye.com", display_name="仲量联行"),
    CompanyConfig("高力国际", "zhiye", "https://colliers.zhiye.com", display_name="高力国际"),
    CompanyConfig("第一太平戴维斯", "zhiye", "https://savills.zhiye.com", display_name="第一太平戴维斯"),
    # Semiconductor & Tech
    CompanyConfig("恩智浦", "zhiye", "https://nxp.zhiye.com", display_name="恩智浦"),
    CompanyConfig("意法半导体", "zhiye", "https://st.zhiye.com", display_name="意法半导体"),
    CompanyConfig("英飞凌", "zhiye", "https://infineon.zhiye.com", display_name="英飞凌"),
    CompanyConfig("安森美", "zhiye", "https://onsemi.zhiye.com", display_name="安森美"),
    CompanyConfig("新思科技", "zhiye", "https://synopsys.zhiye.com", display_name="新思科技"),
    CompanyConfig("楷登电子", "zhiye", "https://cadence.zhiye.com", display_name="楷登电子"),
    CompanyConfig("安谋科技", "zhiye", "https://arm.zhiye.com", display_name="安谋科技"),
    CompanyConfig("联发科", "zhiye", "https://mediatek.zhiye.com", display_name="联发科"),
    # Gaming & Tech
    CompanyConfig("育碧", "zhiye", "https://ubisoft.zhiye.com", display_name="育碧"),
    CompanyConfig("Unity", "zhiye", "https://unity.zhiye.com", display_name="Unity"),
    CompanyConfig("Riot Games", "zhiye", "https://riotgames.zhiye.com", display_name="Riot Games"),
    CompanyConfig("Epic Games", "zhiye", "https://epicgames.zhiye.com", display_name="Epic Games"),
    CompanyConfig("Databricks", "zhiye", "https://databricks.zhiye.com", display_name="Databricks"),
    CompanyConfig("ServiceNow", "zhiye", "https://servicenow.zhiye.com", display_name="ServiceNow"),
    CompanyConfig("Atlassian", "zhiye", "https://atlassian.zhiye.com", display_name="Atlassian"),
    CompanyConfig("Splunk", "zhiye", "https://splunk.zhiye.com", display_name="Splunk"),
    CompanyConfig("Okta", "zhiye", "https://okta.zhiye.com", display_name="Okta"),
    CompanyConfig("CrowdStrike", "zhiye", "https://crowdstrike.zhiye.com", display_name="CrowdStrike"),
    CompanyConfig("Zscaler", "zhiye", "https://zscaler.zhiye.com", display_name="Zscaler"),
    CompanyConfig("Twilio", "zhiye", "https://twilio.zhiye.com", display_name="Twilio"),
    CompanyConfig("GitLab", "zhiye", "https://gitlab.zhiye.com", display_name="GitLab"),
    CompanyConfig("HashiCorp", "zhiye", "https://hashicorp.zhiye.com", display_name="HashiCorp"),
    CompanyConfig("Stripe", "zhiye", "https://stripe.zhiye.com", display_name="Stripe"),
    CompanyConfig("Figma", "zhiye", "https://figma.zhiye.com", display_name="Figma"),
    CompanyConfig("Notion", "zhiye", "https://notion.zhiye.com", display_name="Notion"),
    CompanyConfig("Palantir", "zhiye", "https://palantir.zhiye.com", display_name="Palantir"),
]

ALL_COMPANIES = WORKDAY_COMPANIES + ZHIYE_COMPANIES + HOTJOB_COMPANIES + CUSTOM_COMPANIES + SMARTRECRUITERS_COMPANIES + ZHIYE_COMPANIES_EXTRA + BANK_COMPANIES + MOKAHR_COMPANIES + ZHIYE_RESEARCH_COMPANIES + YANGQI_EXPANSION + WORKDAY_EXPANSION + SECURITIES_COMPANIES + WORKDAY_EXPANSION_2 + YANGQI_EXPANSION_2 + YANGQI_EXPANSION_3 + WORKDAY_EXPANSION_3 + ZHIYE_WAIQI_EXPANSION + MISC_WAIQI_EXPANSION + ZHIYE_EXTRA_EXPANSION_2


# Auto-fill source_type based on URL patterns
_THIRD_PARTY_URL_PATTERNS = {
    'zhiye.com': 'third_party:北森智聘',
    'myworkdayjobs.com': 'third_party:Workday',
    'hotjob.cn': 'third_party:前程无忧',
    'mokahr.com': 'third_party:Moka',
    'smartrecruiters': 'third_party:SmartRecruiters',
    'jobs.lever.co': 'third_party:Lever',
}

for _c in ALL_COMPANIES:
    if not _c.source_type:
        _c.source_type = 'official'  # default
        for _pattern, _stype in _THIRD_PARTY_URL_PATTERNS.items():
            if _pattern in _c.url:
                _c.source_type = _stype
                break

#!/usr/bin/env python3
"""
expand_config.py - 批量添加新企业到 config.py
直接在初代机器上运行，追加到 config.py 末尾（ALL_COMPANIES 之前）
"""

NEW_WORKDAY = '''
# ============================================================
# Phase 12: Workday 批量扩展 (外企 + 咨询 + 金融)
# ============================================================

WORKDAY_EXPANSION_2 = [
    # --- Tech ---
    CompanyConfig("Meta", "workday", "https://meta.wd1.myworkdayjobs.com/Meta_Careers",
                  params={"location": "China"}, display_name="Meta"),
    CompanyConfig("Zoom", "workday", "https://zoom.wd5.myworkdayjobs.com/Zoom",
                  params={"location": "China"}, display_name="Zoom"),
    CompanyConfig("VMware", "workday", "https://vmware.wd1.myworkdayjobs.com/VMware",
                  params={"location": "China"}, display_name="VMware"),
    CompanyConfig("Datadog", "workday", "https://datadog.wd1.myworkdayjobs.com/Datadog",
                  params={"location": "China"}, display_name="Datadog"),
    CompanyConfig("Snowflake", "workday", "https://snowflake.wd1.myworkdayjobs.com/en-US/Snowflake",
                  params={"location": "China"}, display_name="Snowflake"),
    CompanyConfig("Fortinet", "workday", "https://fortinet.wd1.myworkdayjobs.com/Fortinet",
                  params={"location": "China"}, display_name="Fortinet"),
    CompanyConfig("Pure Storage", "workday", "https://purestorage.wd1.myworkdayjobs.com/PureStorageExternalSite",
                  params={"location": "China"}, display_name="Pure Storage"),
    CompanyConfig("Cloudflare", "workday", "https://cloudflare.wd1.myworkdayjobs.com/Cloudflare_Careers",
                  params={"location": "China"}, display_name="Cloudflare"),
    CompanyConfig("MongoDB", "workday", "https://mongodb.wd1.myworkdayjobs.com/MongoDB_Careers",
                  params={"location": "China"}, display_name="MongoDB"),
    CompanyConfig("Elastic", "workday", "https://elastic.wd1.myworkdayjobs.com/Elastic_Careers",
                  params={"location": "China"}, display_name="Elastic"),
    CompanyConfig("SAP", "workday", "https://sap.wd1.myworkdayjobs.com/SAPCareers",
                  params={"location": "China"}, display_name="SAP"),
    CompanyConfig("Oracle", "workday", "https://oracle.wd1.myworkdayjobs.com/Oracle_Careers",
                  params={"location": "China"}, display_name="甲骨文"),
    CompanyConfig("IBM", "workday", "https://ibm.wd5.myworkdayjobs.com/IBM_Careers",
                  params={"location": "China"}, display_name="IBM"),
    # --- Consumer / Retail ---
    CompanyConfig("Nike", "workday", "https://nike.wd1.myworkdayjobs.com/Nike_Careers",
                  params={"location": "China"}, display_name="耐克"),
    CompanyConfig("Starbucks", "workday", "https://starbucks.wd1.myworkdayjobs.com/StarbucksCareers",
                  params={"location": "China"}, display_name="星巴克"),
    CompanyConfig("IKEA", "workday", "https://ikea.wd3.myworkdayjobs.com/IKEA_Careers",
                  params={"location": "China"}, display_name="宜家"),
    CompanyConfig("Walmart", "workday", "https://walmart.wd5.myworkdayjobs.com/WalmartExternal",
                  params={"location": "China"}, display_name="沃尔玛"),
    CompanyConfig("Unilever", "workday", "https://unilever.wd3.myworkdayjobs.com/Unilever_Experienced_Professionals",
                  params={"location": "China"}, display_name="联合利华"),
    CompanyConfig("P&G", "workday", "https://pg.wd1.myworkdayjobs.com/PGCareers",
                  params={"location": "China"}, display_name="宝洁"),
    CompanyConfig("Adidas", "workday", "https://adidas.wd3.myworkdayjobs.com/adidas_Careers",
                  params={"location": "China"}, display_name="阿迪达斯"),
    CompanyConfig("L'Oreal", "workday", "https://loreal.wd3.myworkdayjobs.com/en-US/LOreal_Careers",
                  params={"location": "China"}, display_name="欧莱雅"),
    CompanyConfig("Nestle", "workday", "https://nestle.wd3.myworkdayjobs.com/en-US/Nestle_Careers",
                  params={"location": "China"}, display_name="雀巢"),
    CompanyConfig("Coca-Cola", "workday", "https://coke.wd1.myworkdayjobs.com/coca-cola-careers",
                  params={"location": "China"}, display_name="可口可乐"),
    CompanyConfig("PepsiCo", "workday", "https://pepsico.wd1.myworkdayjobs.com/PepsiCo_Careers",
                  params={"location": "China"}, display_name="百事可乐"),
    CompanyConfig("McDonald's", "workday", "https://mcdonalds.wd5.myworkdayjobs.com/McDonalds_Careers",
                  params={"location": "China"}, display_name="麦当劳"),
    CompanyConfig("H&M", "workday", "https://hm.wd3.myworkdayjobs.com/HM_Careers",
                  params={"location": "China"}, display_name="H&M"),
    # --- Pharma / Healthcare ---
    CompanyConfig("Roche", "workday", "https://roche.wd3.myworkdayjobs.com/roche-ext",
                  params={"location": "China"}, display_name="罗氏"),
    CompanyConfig("Novartis", "workday", "https://novartis.wd3.myworkdayjobs.com/Novartis_Careers",
                  params={"location": "China"}, display_name="诺华"),
    CompanyConfig("Eli Lilly", "workday", "https://lilly.wd5.myworkdayjobs.com/Lilly_Careers",
                  params={"location": "China"}, display_name="礼来"),
    CompanyConfig("Johnson & Johnson", "workday", "https://jnj.wd5.myworkdayjobs.com/JNJ_Careers",
                  params={"location": "China"}, display_name="强生"),
    CompanyConfig("Sanofi", "workday", "https://sanofi.wd3.myworkdayjobs.com/SanofiCareers",
                  params={"location": "China"}, display_name="赛诺菲"),
    CompanyConfig("GSK", "workday", "https://gsk.wd5.myworkdayjobs.com/GSK_Careers",
                  params={"location": "China"}, display_name="葛兰素史克"),
    CompanyConfig("Merck/MSD", "workday", "https://merck.wd5.myworkdayjobs.com/External",
                  params={"location": "China"}, display_name="默沙东"),
    CompanyConfig("BMS", "workday", "https://bms.wd5.myworkdayjobs.com/BMS_Careers",
                  params={"location": "China"}, display_name="百时美施贵宝"),
    CompanyConfig("Bayer", "workday", "https://bayer.wd3.myworkdayjobs.com/BayerCareer",
                  params={"location": "China"}, display_name="拜耳"),
    CompanyConfig("Novo Nordisk", "workday", "https://novonordisk.wd3.myworkdayjobs.com/en-US/NovoNordisk_Careers",
                  params={"location": "China"}, display_name="诺和诺德"),
    CompanyConfig("Abbott", "workday", "https://abbott.wd5.myworkdayjobs.com/Abbott_Careers",
                  params={"location": "China"}, display_name="雅培"),
    CompanyConfig("Medtronic", "workday", "https://medtronic.wd1.myworkdayjobs.com/MedtronicCareers",
                  params={"location": "China"}, display_name="美敦力"),
    # --- Industrial / Auto / Energy ---
    CompanyConfig("BASF", "workday", "https://basf.wd3.myworkdayjobs.com/BASF_Careers",
                  params={"location": "China"}, display_name="巴斯夫"),
    CompanyConfig("Honeywell", "workday", "https://honeywell.wd5.myworkdayjobs.com/Honeywell_Careers",
                  params={"location": "China"}, display_name="霍尼韦尔"),
    CompanyConfig("Caterpillar", "workday", "https://caterpillar.wd5.myworkdayjobs.com/CaterpillarCareers",
                  params={"location": "China"}, display_name="卡特彼勒"),
    CompanyConfig("Ford", "workday", "https://ford.wd1.myworkdayjobs.com/Ford_Careers",
                  params={"location": "China"}, display_name="福特汽车"),
    CompanyConfig("GM", "workday", "https://gm.wd5.myworkdayjobs.com/Careers_GM",
                  params={"location": "China"}, display_name="通用汽车"),
    CompanyConfig("Emerson", "workday", "https://emerson.wd5.myworkdayjobs.com/Emerson_Careers",
                  params={"location": "China"}, display_name="艾默生"),
    CompanyConfig("Chevron", "workday", "https://chevron.wd5.myworkdayjobs.com/Chevron_Careers",
                  params={"location": "China"}, display_name="雪佛龙"),
    CompanyConfig("TotalEnergies", "workday", "https://totalenergies.wd3.myworkdayjobs.com/TotalEnergies_Careers",
                  params={"location": "China"}, display_name="道达尔能源"),
    CompanyConfig("ExxonMobil", "workday", "https://exxonmobil.wd5.myworkdayjobs.com/ExxonMobil_Careers",
                  params={"location": "China"}, display_name="埃克森美孚"),
    CompanyConfig("Volvo", "workday", "https://volvo.wd3.myworkdayjobs.com/Volvo_Careers",
                  params={"location": "China"}, display_name="沃尔沃"),
    CompanyConfig("Philips", "workday", "https://philips.wd3.myworkdayjobs.com/Philips_Careers",
                  params={"location": "China"}, display_name="飞利浦"),
    # --- Finance / Consulting ---
    CompanyConfig("Goldman Sachs", "workday", "https://gs.wd5.myworkdayjobs.com/GS_Careers",
                  params={"location": "China"}, display_name="高盛"),
    CompanyConfig("Morgan Stanley", "workday", "https://morganstanley.wd5.myworkdayjobs.com/Morgan_Stanley_Careers",
                  params={"location": "China"}, display_name="摩根士丹利"),
    CompanyConfig("JP Morgan", "workday", "https://jpmc.wd5.myworkdayjobs.com/JPMorgan_Careers",
                  params={"location": "China"}, display_name="摩根大通"),
    CompanyConfig("BlackRock", "workday", "https://blackrock.wd1.myworkdayjobs.com/BlackRock_Careers",
                  params={"location": "China"}, display_name="贝莱德"),
    CompanyConfig("Deloitte", "workday", "https://deloitte.wd1.myworkdayjobs.com/Deloitte_Careers",
                  params={"location": "China"}, display_name="德勤"),
    CompanyConfig("EY", "workday", "https://ey.wd5.myworkdayjobs.com/EY_Careers",
                  params={"location": "China"}, display_name="安永"),
    CompanyConfig("PwC", "workday", "https://pwc.wd3.myworkdayjobs.com/PwC_Careers",
                  params={"location": "China"}, display_name="普华永道"),
    CompanyConfig("KPMG", "workday", "https://kpmg.wd3.myworkdayjobs.com/KPMG_Careers",
                  params={"location": "China"}, display_name="毕马威"),
    CompanyConfig("McKinsey", "workday", "https://mckinsey.wd3.myworkdayjobs.com/McKinsey_Careers",
                  params={"location": "China"}, display_name="麦肯锡"),
    CompanyConfig("BCG", "workday", "https://bcg.wd1.myworkdayjobs.com/BCG_Careers",
                  params={"location": "China"}, display_name="波士顿咨询"),
    CompanyConfig("Bain", "workday", "https://bain.wd1.myworkdayjobs.com/Bain_Careers",
                  params={"location": "China"}, display_name="贝恩公司"),
    # --- Semiconductor ---
    CompanyConfig("Qualcomm", "workday", "https://qualcomm.wd5.myworkdayjobs.com/External",
                  params={"location": "China"}, display_name="高通"),
    CompanyConfig("Texas Instruments", "workday", "https://ti.wd1.myworkdayjobs.com/TI_Careers",
                  params={"location": "China"}, display_name="德州仪器"),
    CompanyConfig("Applied Materials", "workday", "https://appliedmaterials.wd1.myworkdayjobs.com/External",
                  params={"location": "China"}, display_name="应用材料"),
    CompanyConfig("Micron", "workday", "https://micron.wd1.myworkdayjobs.com/External",
                  params={"location": "China"}, display_name="美光科技"),
    CompanyConfig("Western Digital", "workday", "https://westerndigital.wd1.myworkdayjobs.com/WD_Careers",
                  params={"location": "China"}, display_name="西部数据"),
    # --- Luxury / Fashion ---
    CompanyConfig("LVMH", "workday", "https://lvmh.wd3.myworkdayjobs.com/LVMH_Careers",
                  params={"location": "China"}, display_name="路威酩轩"),
    CompanyConfig("Estee Lauder", "workday", "https://esteelauder.wd5.myworkdayjobs.com/EsteeLauder_Careers",
                  params={"location": "China"}, display_name="雅诗兰黛"),
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
'''

NEW_ALL_COMPANIES_LINE = "ALL_COMPANIES = WORKDAY_COMPANIES + ZHIYE_COMPANIES + HOTJOB_COMPANIES + CUSTOM_COMPANIES + SMARTRECRUITERS_COMPANIES + ZHIYE_COMPANIES_EXTRA + BANK_COMPANIES + MOKAHR_COMPANIES + ZHIYE_RESEARCH_COMPANIES + YANGQI_EXPANSION + WORKDAY_EXPANSION + SECURITIES_COMPANIES + WORKDAY_EXPANSION_2 + YANGQI_EXPANSION_2"

import sys

config_path = sys.argv[1]

with open(config_path, 'r') as f:
    content = f.read()

# Insert new lists before ALL_COMPANIES line
old_all = "ALL_COMPANIES = WORKDAY_COMPANIES + ZHIYE_COMPANIES + HOTJOB_COMPANIES + CUSTOM_COMPANIES + SMARTRECRUITERS_COMPANIES + ZHIYE_COMPANIES_EXTRA + BANK_COMPANIES + MOKAHR_COMPANIES + ZHIYE_RESEARCH_COMPANIES + YANGQI_EXPANSION + WORKDAY_EXPANSION + SECURITIES_COMPANIES"

if old_all not in content:
    print("ERROR: Cannot find ALL_COMPANIES line to patch")
    sys.exit(1)

content = content.replace(old_all, NEW_WORKDAY + "\n\n" + NEW_ALL_COMPANIES_LINE)

with open(config_path, 'w') as f:
    f.write(content)

print("Done! Added WORKDAY_EXPANSION_2 + YANGQI_EXPANSION_2")

"""
Update config.py to:
1. Mark dead zhiye_pw bank sites with official URLs and 'uncrawlable' status
2. Add source_type annotations distinguishing official vs third-party
3. Add official_url field for companies where we know the real career site
"""
import re

# Read current config
with open('/Users/pingjiangli/Code/Business-History/crawler/config.py', 'r') as f:
    content = f.read()

# 1. Update CompanyConfig dataclass to add official_url and status fields
old_dataclass = '''@dataclass
class CompanyConfig:
    """单个企业爬取配置"""
    name: str              # 企业名称
    adapter: str           # adapter名称
    url: str               # 招聘页面URL
    params: dict = field(default_factory=dict)  # adapter特定参数
    source_type: str = ""  # "official" or "third_party:平台名"'''

new_dataclass = '''@dataclass
class CompanyConfig:
    """单个企业爬取配置"""
    name: str              # 企业名称
    adapter: str           # adapter名称
    url: str               # 招聘页面URL
    params: dict = field(default_factory=dict)  # adapter特定参数
    source_type: str = ""  # "official" or "third_party:平台名"
    official_url: str = ""  # 企业官网招聘页面（用于对比/备用）
    status: str = "active"  # "active", "dead", "suspended"'''

content = content.replace(old_dataclass, new_dataclass)

# 2. Update bank companies that are dead on zhiye.com with official URLs and status
bank_updates = {
    '    CompanyConfig("招商银行", "zhiye_pw", "https://cmbchina.zhiye.com/Social"),':
        '    CompanyConfig("招商银行", "zhiye_pw", "https://cmbchina.zhiye.com/Social",\n'
        '                  official_url="https://career.cmbchina.com", status="dead"),',
    
    '    CompanyConfig("交通银行", "zhiye_pw", "https://bankcomm.zhiye.com/Social"),':
        '    CompanyConfig("交通银行", "zhiye_pw", "https://bankcomm.zhiye.com/Social",\n'
        '                  official_url="https://job.bankcomm.com", status="dead"),',
    
    '    CompanyConfig("邮储银行", "zhiye_pw", "https://psbc.zhiye.com/Social"),':
        '    CompanyConfig("邮储银行", "zhiye_pw", "https://psbc.zhiye.com/Social",\n'
        '                  official_url="https://www.psbc.com/cn/grfw/rczp/", status="dead"),',
    
    '    CompanyConfig("工商银行", "zhiye_pw", "https://icbc.zhiye.com/Social"),':
        '    CompanyConfig("工商银行", "zhiye_pw", "https://icbc.zhiye.com/Social",\n'
        '                  official_url="https://job.icbc.com.cn", status="dead"),',
    
    '    CompanyConfig("农业银行", "zhiye_pw", "https://abchina.zhiye.com/Social"),':
        '    CompanyConfig("农业银行", "zhiye_pw", "https://abchina.zhiye.com/Social",\n'
        '                  official_url="https://career.abchina.com", status="dead"),',
    
    '    CompanyConfig("建设银行", "zhiye_pw", "https://ccb.zhiye.com/Social"),':
        '    CompanyConfig("建设银行", "zhiye_pw", "https://ccb.zhiye.com/Social",\n'
        '                  official_url="https://job.ccb.com", status="dead"),',
    
    '    CompanyConfig("中国银行", "zhiye_pw", "https://boc.zhiye.com/Social"),':
        '    CompanyConfig("中国银行", "zhiye_pw", "https://boc.zhiye.com/Social",\n'
        '                  official_url="https://career.bankofchina.com", status="dead"),',
    
    '    CompanyConfig("广发银行", "zhiye_pw", "https://cgbchina.zhiye.com/Social"),':
        '    CompanyConfig("广发银行", "zhiye_pw", "https://cgbchina.zhiye.com/Social",\n'
        '                  official_url="https://www.cgbchina.com.cn/Channel/16000100", status="dead"),',
    
    '    CompanyConfig("北京农商银行", "zhiye_pw", "https://bjrcb.zhiye.com/Social"),':
        '    CompanyConfig("北京农商银行", "zhiye_pw", "https://bjrcb.zhiye.com/Social",\n'
        '                  official_url="https://www.bjrcb.com", status="dead"),',
    
    '    CompanyConfig("渤海银行", "zhiye_pw", "https://cbhb.zhiye.com/Social"),':
        '    CompanyConfig("渤海银行", "zhiye_pw", "https://cbhb.zhiye.com/Social",\n'
        '                  official_url="https://www.cbhb.com.cn/bhbank/S101/renCaiZhaoPin", status="dead"),',
    
    '    CompanyConfig("恒丰银行", "zhiye_pw", "https://hfbank.zhiye.com/Social"),':
        '    CompanyConfig("恒丰银行", "zhiye_pw", "https://hfbank.zhiye.com/Social",\n'
        '                  official_url="https://www.hfbank.com.cn/gywm/rczp/index.shtml", status="dead"),',
}

for old, new in bank_updates.items():
    content = content.replace(old, new)

# 3. Update央企 zhiye_pw sites with status
yangqi_updates = {
    '    CompanyConfig("中国建筑", "zhiye_pw", "https://cscec.zhiye.com"),':
        '    CompanyConfig("中国建筑", "zhiye_pw", "https://cscec.zhiye.com",\n'
        '                  official_url="https://hr.cscec.com", status="dead"),',
    
    '    CompanyConfig("中国船舶", "zhiye_pw", "https://cssc.zhiye.com"),':
        '    CompanyConfig("中国船舶", "zhiye_pw", "https://cssc.zhiye.com",\n'
        '                  official_url="https://www.cssc.net.cn", status="dead"),',
    
    '    CompanyConfig("中国核工业", "zhiye_pw", "https://cnnc.zhiye.com"),':
        '    CompanyConfig("中国核工业", "zhiye_pw", "https://cnnc.zhiye.com",\n'
        '                  official_url="https://hr.cnnc.com.cn", status="dead"),',
    
    '    CompanyConfig("中国能建", "zhiye_pw", "https://ceec.zhiye.com"),':
        '    CompanyConfig("中国能建", "zhiye_pw", "https://ceec.zhiye.com",\n'
        '                  official_url="https://hr.ceec.net.cn", status="suspended"),',
    
    '    CompanyConfig("中国航天科工", "zhiye_pw", "https://casic.zhiye.com"),':
        '    CompanyConfig("中国航天科工", "zhiye_pw", "https://casic.zhiye.com",\n'
        '                  official_url="https://zhaopin.casic.cn", status="dead"),',
}

for old, new in yangqi_updates.items():
    content = content.replace(old, new)

# 4. Update comments for bank section
old_comment = "    # 招商银行 - 北森新版Portal SPA，需Playwright"
new_comment = "    # 招商银行 - zhiye.com已关闭(404)，官网career.cmbchina.com需Playwright"
content = content.replace(old_comment, new_comment)

old_comment2 = "    # 交通银行 - 北森新版Portal SPA，需Playwright"
new_comment2 = "    # 交通银行 - zhiye.com已关闭(404)，官网job.bankcomm.com需Playwright+legacy SSL"
content = content.replace(old_comment2, new_comment2)

old_comment3 = "    # 邮储银行 - 北森新版Portal SPA，需Playwright"
new_comment3 = "    # 邮储银行 - zhiye.com已关闭(404)，官网psbc.com需Playwright"
content = content.replace(old_comment3, new_comment3)

old_comment4 = "    # 工商银行 - 北森新版Portal SPA，需Playwright"
new_comment4 = "    # 工商银行 - zhiye.com已关闭(404)，官网job.icbc.com.cn需Playwright+legacy SSL"
content = content.replace(old_comment4, new_comment4)

old_comment5 = "    # 农业银行 - 北森新版Portal SPA，需Playwright"
new_comment5 = "    # 农业银行 - zhiye.com已关闭(404)，官网career.abchina.com需Playwright+legacy SSL"
content = content.replace(old_comment5, new_comment5)

old_comment6 = "    # 建设银行 - 北森新版Portal SPA，需Playwright"
new_comment6 = "    # 建设银行 - zhiye.com已关闭(404)，官网job.ccb.com有API(NHR104)需legacy SSL"
content = content.replace(old_comment6, new_comment6)

old_comment7 = "    # 中国银行 - 北森新版Portal SPA，需Playwright"
new_comment7 = "    # 中国银行 - zhiye.com已关闭(404)，官网career.bankofchina.com需Playwright"
content = content.replace(old_comment7, new_comment7)

old_comment8 = "    # 广发银行 - 北森新版Portal SPA，需Playwright"
new_comment8 = "    # 广发银行 - zhiye.com已关闭(404)，官网cgbchina.com.cn返回500"
content = content.replace(old_comment8, new_comment8)

old_comment9 = "    # 北京农商银行 - 北森新版Portal SPA，需Playwright"
new_comment9 = "    # 北京农商银行 - zhiye.com已关闭(404)，官网bjrcb.com招聘页404"
content = content.replace(old_comment9, new_comment9)

old_comment10 = "    # 渤海银行 - 北森新版Portal SPA，需Playwright"
new_comment10 = "    # 渤海银行 - zhiye.com已关闭(404)，官网cbhb.com.cn可访问"
content = content.replace(old_comment10, new_comment10)

old_comment11 = "    # 恒丰银行 - 北森新版Portal SPA，需Playwright"
new_comment11 = "    # 恒丰银行 - zhiye.com已关闭(404)，官网hfbank.com.cn返回412(WAF)"
content = content.replace(old_comment11, new_comment11)

# 5. Update yangqi comments
old_yq = "    # zhiye.com 旧版Portal仍在线，可用zhiye_pw adapter"
new_yq = "    # zhiye.com 旧版Portal API已失效(302→404)，需切换到官网或标记dead"
content = content.replace(old_yq, new_yq)

# Write updated config
with open('/Users/pingjiangli/Code/Business-History/crawler/config.py', 'w') as f:
    f.write(content)

print("config.py updated successfully!")
print("Changes:")
print("  - Added official_url and status fields to CompanyConfig")
print("  - Marked 11 dead zhiye_pw bank sites with official URLs")
print("  - Marked 5 dead/suspended zhiye_pw央企 sites with official URLs")
print("  - Updated comments to reflect current site status")

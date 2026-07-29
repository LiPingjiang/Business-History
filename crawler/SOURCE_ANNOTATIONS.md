# 数据来源标注说明 (SOURCE_ANNOTATIONS.md)

## 概述

本项目收录 **91家企业**，数据来源分为两类：

| 来源类型 | 企业数 | 说明 |
|---------|--------|------|
| 官网直接爬取 | 20家 | 直接从企业自建招聘系统获取，数据最准确 |
| 第三方平台爬取 | 71家 | 从招聘SaaS平台获取，可能与官网有差异 |

## 第三方平台分布

| 平台 | 企业数 | 说明 |
|------|--------|------|
| 北森智聘 (zhiye.com) | 41家 | 国内最大企业招聘SaaS，央企/银行/券商常用 |
| Workday | 16家 | 外企标配HR系统 |
| 前程无忧 (hotjob.cn) | 11家 | 央企/银行常用的招聘外包平台 |
| Moka | 3家 | 新兴招聘SaaS，研究机构/新型银行使用 |

## 官网 vs 第三方平台信息差异

### 已知差异情况

1. **北森智聘 (zhiye.com)**
   - 部分银行已从zhiye.com撤离（站点返回404），但官网仍有招聘
   - zhiye.com的岗位数据可能滞后于官网
   - LocNames字段经常为空，导致城市信息缺失

2. **Workday**
   - 外企官方ATS系统，数据与官网一致（Workday就是官网）
   - location字段准确

3. **前程无忧 (hotjob.cn)**
   - 部分企业在hotjob上的岗位是子集（只放部分岗位）
   - 更新频率可能低于官网

## 已失效站点（status=dead）

以下 **16家企业** 的zhiye.com站点已关闭（返回404或暂停），需要切换到官网爬取：

### 银行（11家）

| 企业 | 原爬取地址 | 官网招聘地址 | 官网状态 |
|------|-----------|-------------|---------|
| 招商银行 | cmbchina.zhiye.com | career.cmbchina.com | SPA，需Playwright |
| 交通银行 | bankcomm.zhiye.com | job.bankcomm.com | Vue SPA，需Playwright+legacy SSL |
| 邮储银行 | psbc.zhiye.com | psbc.com/cn/grfw/rczp/ | 页面404 |
| 工商银行 | icbc.zhiye.com | job.icbc.com.cn | SPA，API需session(NHR104)，需legacy SSL |
| 农业银行 | abchina.zhiye.com | career.abchina.com | SPA，需Playwright+legacy SSL |
| 建设银行 | ccb.zhiye.com | job.ccb.com | jQuery+API(NHR104)，需legacy SSL |
| 中国银行 | boc.zhiye.com | career.bankofchina.com | DNS解析失败 |
| 广发银行 | cgbchina.zhiye.com | cgbchina.com.cn | 返回500 |
| 北京农商银行 | bjrcb.zhiye.com | bjrcb.com | 招聘页404 |
| 渤海银行 | cbhb.zhiye.com | cbhb.com.cn | 可访问，需分析API |
| 恒丰银行 | hfbank.zhiye.com | hfbank.com.cn | WAF拦截(412) |

### 央企（5家）

| 企业 | 原爬取地址 | 官网招聘地址 | 官网状态 |
|------|-----------|-------------|---------|
| 中国建筑 | cscec.zhiye.com | hr.cscec.com | 可访问，需分析 |
| 中国船舶 | cssc.zhiye.com | cssc.net.cn | TLS错误 |
| 中国核工业 | cnnc.zhiye.com | hr.cnnc.com.cn | WAF拦截(412) |
| 中国能建 | ceec.zhiye.com | hr.ceec.net.cn | 超时 |
| 中国航天科工 | casic.zhiye.com | zhaopin.casic.cn | 连接重置 |

## 技术说明

### CompanyConfig 字段

```python
@dataclass
class CompanyConfig:
    name: str              # 企业名称
    adapter: str           # adapter名称
    url: str               # 当前爬取URL
    params: dict           # adapter特定参数
    source_type: str       # "official" or "third_party:平台名"
    official_url: str      # 企业官网招聘页面（用于对比/备用）
    status: str            # "active", "dead", "suspended"
```

### source_type 自动推断规则

```python
_THIRD_PARTY_URL_PATTERNS = {
    'zhiye.com': 'third_party:北森智聘',
    'myworkdayjobs.com': 'third_party:Workday',
    'hotjob.cn': 'third_party:前程无忧',
    'mokahr.com': 'third_party:Moka',
    'smartrecruiters': 'third_party:SmartRecruiters',
}
```

### 建议优先级

对于差距大的企业，优先从官网获取信息：
1. 官网有可用API → 写专用adapter
2. 官网是SPA但可用Playwright → 用Playwright adapter
3. 官网有WAF/反爬 → 保留第三方平台数据，标注来源
4. 官网完全不可访问 → 标记为uncrawlable，保留历史数据

## 更新日志

- 2026-07-29: 初始标注，发现16家zhiye.com站点已失效，添加official_url字段

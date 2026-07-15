# 岗位监控脚本

定期检查目标公司招聘页面，发现新增的数据研发/大数据研发岗位。

## 快速开始

```bash
# 安装依赖
pip install requests beautifulsoup4 lxml

# 检查所有目标
python3 scripts/job_monitor.py

# 只检查央企
python3 scripts/job_monitor.py --target 央企

# 只检查外企
python3 scripts/job_monitor.py --target 外企

# 只检查科研单位
python3 scripts/job_monitor.py --target 科研

# 预览模式（不实际请求）
python3 scripts/job_monitor.py --dry-run

# 详细输出
python3 scripts/job_monitor.py -v
```

## 监控目标

### 央企（6个）
| 企业 | 平台 | URL |
|------|------|-----|
| 联通数科 | zhiye.com | cudt.zhiye.com |
| 联通数智 | zhiye.com | cudataintelligence.zhiye.com |
| 中国移动九天 | hotjob.cn | wecruit.hotjob.cn |
| 中国移动主站 | 官网 | job.10086.cn |
| 中国联通社招 | 官网 | chinaunicom.com.cn |
| 中国信通院 | hotjob.cn | hotjob.cn/wt/caict |

### 外企（5个）
| 企业 | 平台 | URL |
|------|------|-----|
| 领悦数字(BMW) | BOSS直聘 | zhipin.com |
| 微软 | Workday | careers.microsoft.com |
| 亚马逊 | Amazon Jobs | amazon.jobs |
| 西门子 | 官网 | jobs.siemens.com.cn |
| AMD | 官网 | careers.amd.com |

### 科研单位（5个）
| 企业 | 平台 | URL |
|------|------|-----|
| 中科院信工所 | BOSS直聘 | zhipin.com |
| 中科院计算所 | 官网 | ict.cas.cn |
| 中科院网络信息中心 | 官网 | cnic.cas.cn |
| 中科院软件所 | 官网 | is.cas.cn |
| 国家数据发展研究院 | 官网 | nda.gov.cn |

## 定时运行

### macOS (launchd)

创建 `~/Library/LaunchAgents/com.business-history.job-monitor.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.business-history.job-monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/lipingjiang/Codes/Business-History/scripts/job_monitor.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/job-monitor.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/job-monitor-error.log</string>
</dict>
</plist>
```

加载：
```bash
launchctl load ~/Library/LaunchAgents/com.business-history.job-monitor.plist
```

### crontab

```bash
# 每天早上9点运行
0 9 * * * cd /Users/lipingjiang/Codes/Business-History && python3 scripts/job_monitor.py >> /tmp/job-monitor.log 2>&1
```

## 输出

- `scripts/reports/latest_report.md` — 最新一次报告
- `scripts/reports/monitor_YYYY-MM-DD_HHMMSS.md` — 历史报告
- `scripts/.cache/` — 缓存数据（用于对比新增岗位）

## 工作原理

1. 访问各公司招聘页面
2. 解析HTML，提取包含关键词（大数据、数据开发、Spark、Flink等）的岗位标题
3. 与上次缓存对比，识别新增岗位
4. 生成Markdown报告

## 局限性

- BOSS直聘、猎聘等平台有反爬机制，脚本只能做基础页面检查
- 部分网站（如中国石化）需要登录才能查看岗位
- 动态渲染页面（SPA）可能无法通过简单HTTP请求获取完整内容
- 建议配合浏览器手动检查BOSS直聘等平台

## 扩展

如需更强的抓取能力，可考虑：
- 使用 Playwright/Selenium 处理动态页面
- 接入 BOSS直聘/猎聘 的 RSS 或邮件订阅
- 使用企业微信/钉钉 webhook 推送新岗位通知

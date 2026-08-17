#!/bin/bash
# 每日招聘岗位爬取脚本
cd /Users/pingjiangli/Code/Business-History/crawler
LOG_DIR=/Users/pingjiangli/Code/Business-History/crawler/logs
mkdir -p $LOG_DIR
DATE=$(date +%Y-%m-%d)
LOG_FILE=$LOG_DIR/$DATE.log

echo "[$(date)] Starting daily crawl..." >> $LOG_FILE

# 全量爬取
/usr/local/bin/python3 runner.py --diff >> $LOG_FILE 2>&1

# git push结果
cd /Users/pingjiangli/Code/Business-History
git add crawler/data/ >> $LOG_FILE 2>&1
git commit -m "data: daily crawl $DATE" >> $LOG_FILE 2>&1
git push origin main >> $LOG_FILE 2>&1

# 同步数据到腾讯云
echo "[$(date)] Syncing to cloud..." >> $LOG_FILE
/Users/pingjiangli/Code/Business-History/crawler/sync_to_cloud.sh >> $LOG_FILE 2>&1

echo "[$(date)] Daily crawl completed." >> $LOG_FILE

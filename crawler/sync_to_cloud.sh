#!/bin/bash
# 每日爬虫完成后，将数据同步到腾讯云
# 由 daily_crawl.sh 调用，或单独执行

DATA_DIR="$HOME/Code/Business-History/crawler/data"
REMOTE="root@49.232.173.252"
REMOTE_DIR="/opt/jobs-data"

TODAY=$(date +%Y-%m-%d)

# 同步今天的 JSON 数据
if [ -f "$DATA_DIR/$TODAY.json" ]; then
  scp "$DATA_DIR/$TODAY.json" "$REMOTE:$REMOTE_DIR/"
  echo "[sync] Uploaded $TODAY.json"
fi

# 同步今天的 diff
if [ -f "$DATA_DIR/diff_$TODAY.md" ]; then
  scp "$DATA_DIR/diff_$TODAY.md" "$REMOTE:$REMOTE_DIR/"
  echo "[sync] Uploaded diff_$TODAY.md"
fi

echo "[sync] Done at $(date)"

"""Analyze source_type breakdown and identify official vs third-party sources."""
import sys
sys.path.insert(0, '.')
from config import ALL_COMPANIES

third = [c for c in ALL_COMPANIES if "third_party" in c.source_type]
official = [c for c in ALL_COMPANIES if c.source_type == "official"]

print(f"总企业数: {len(ALL_COMPANIES)}")
print(f"官网直接爬取: {len(official)}")
print(f"第三方平台爬取: {len(third)}")
print()

print("=== 第三方平台企业 ===")
for c in sorted(third, key=lambda x: x.source_type):
    print(f"  {c.name:<14} adapter={c.adapter:<12} source={c.source_type}")

print()
print("=== 官网直接爬取企业 ===")
for c in sorted(official, key=lambda x: x.adapter):
    print(f"  {c.name:<14} adapter={c.adapter:<12} url={c.url[:50]}")

# Check which companies have official websites that differ from their crawl URL
print()
print("=== 需要对比官网 vs 第三方平台信息的企业 ===")
print("(这些企业目前从第三方平台爬取，需要检查官网是否有独立招聘页面)")
for c in third:
    print(f"  {c.name}: 当前爬取={c.url[:60]}")

"""
Fix dead zhiye_pw sites:
1. Banks that left zhiye.com (404) - these need to be switched to zhiye HTTP adapter 
   (which uses the API endpoint that might still work) or marked as uncrawlable
2. Sites that are "暂停招聘" - mark as suspended
3. Working zhiye_pw sites (中国建筑, 中国船舶, 中国核工业, 中国航天科工) - keep as-is but 
   they need the zhiye HTTP API since Playwright isn't finding XHR responses

Strategy: 
- For zhiye_pw sites that return 404 on /Social, try the zhiye HTTP API directly
- If the API works, switch them from zhiye_pw to zhiye adapter
- If the API also fails, mark them as uncrawlable
"""
import sys
sys.path.insert(0, '/Users/pingjiangli/Code/Business-History/crawler')

from config import ALL_COMPANIES
import httpx

c = httpx.Client(follow_redirects=True, verify=False, timeout=15)

# All zhiye_pw companies
zhiye_pw = [x for x in ALL_COMPANIES if x.adapter == "zhiye_pw"]

print("=" * 80)
print("zhiye_pw 企业 → 尝试切换到 zhiye HTTP API")
print("=" * 80)

can_switch_to_http = []
truly_dead = []
suspended = []

for company in zhiye_pw:
    base_url = company.url.rstrip("/")
    if base_url.endswith("/Social"):
        base_url = base_url[:-7]
    
    api_url = f"{base_url}/api/Jobad/GetJobAdPageList"
    
    try:
        resp = c.post(api_url, json={"pageIndex": 1, "pageSize": 5}, 
                     headers={"Content-Type": "application/json", "Accept": "application/json"},
                     timeout=10)
        
        if resp.status_code == 200:
            try:
                data = resp.json()
                if isinstance(data, dict) and data.get("Data"):
                    count = data.get("Count", len(data.get("Data", [])))
                    print(f"  ✓ {company.name:<12} API可用! {count} jobs → 切换到 zhiye adapter")
                    can_switch_to_http.append((company.name, count))
                elif isinstance(data, list) and len(data) > 0:
                    print(f"  ✓ {company.name:<12} API可用! {len(data)} jobs → 切换到 zhiye adapter")
                    can_switch_to_http.append((company.name, len(data)))
                else:
                    # API returns empty or unexpected format
                    print(f"  ⚠️ {company.name:<12} API返回空数据 → 可能已暂停招聘")
                    suspended.append(company.name)
            except Exception:
                print(f"  ❌ {company.name:<12} API返回非JSON → 站点已关闭")
                truly_dead.append(company.name)
        elif resp.status_code == 302:
            # Redirect to info/404 page
            print(f"  ❌ {company.name:<12} API重定向(302) → 站点已关闭或暂停")
            truly_dead.append(company.name)
        else:
            print(f"  ❌ {company.name:<12} API返回 {resp.status_code} → 不可用")
            truly_dead.append(company.name)
    except Exception as e:
        print(f"  ✗ {company.name:<12} Error: {str(e)[:50]}")
        truly_dead.append(company.name)

print(f"\n{'='*80}")
print(f"结果:")
print(f"  可切换到HTTP API: {len(can_switch_to_http)} 家 → {[x[0] for x in can_switch_to_http]}")
print(f"  已暂停招聘: {len(suspended)} 家 → {suspended}")
print(f"  完全不可用: {len(truly_dead)} 家 → {truly_dead}")
print(f"{'='*80}")

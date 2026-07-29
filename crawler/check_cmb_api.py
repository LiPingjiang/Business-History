"""Check CMB official career site API endpoints by extracting from JS bundle."""
import httpx
import re

c = httpx.Client(follow_redirects=True, verify=False, timeout=15)
r = c.get('https://career.cmbchina.com/static/js/main.0cff8bce.js')
body = r.text

# Find API endpoints
apis = re.findall(r'["\'](/api/[^"\']+)["\']', body)
print("Found API endpoints:")
for a in sorted(set(apis))[:30]:
    print(f"  {a}")

# Also look for fetch/axios patterns
fetches = re.findall(r'(?:fetch|axios|get|post)\s*\(\s*["\']([^"\']+)["\']', body)
print("\nFetch/axios URLs:")
for f in sorted(set(fetches))[:20]:
    print(f"  {f}")

# Look for recruitment/job related patterns
job_patterns = re.findall(r'["\']([^"\']*(?:recruit|job|position|career|社招|岗位)[^"\']*)["\']', body, re.IGNORECASE)
print("\nJob-related strings:")
for p in sorted(set(job_patterns))[:30]:
    if len(p) < 100:
        print(f"  {p}")

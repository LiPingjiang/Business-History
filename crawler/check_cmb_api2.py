"""Check CMB official career site - find the actual API by looking for socialRecruitmentWebsite config."""
import httpx
import re

c = httpx.Client(follow_redirects=True, verify=False, timeout=15)
r = c.get('https://career.cmbchina.com/static/js/main.0cff8bce.js')
body = r.text

# Find the socialRecruitmentWebsite config
patterns = [
    r'socialRecruitmentWebsite\s*:\s*["\']([^"\']+)["\']',
    r'campusRecruitmentWebsite\s*:\s*["\']([^"\']+)["\']',
    r'(https?://[^"\']+recruit[^"\']*)',
    r'(https?://[^"\']+career[^"\']*)',
    r'baseURL\s*:\s*["\']([^"\']+)["\']',
    r'(https?://[^"\']*cmbchina[^"\']*)',
]

for pat in patterns:
    matches = re.findall(pat, body)
    if matches:
        print(f"Pattern: {pat[:50]}")
        for m in sorted(set(matches))[:10]:
            print(f"  {m}")
        print()

# Look for route patterns
routes = re.findall(r'path\s*:\s*["\']([^"\']+)["\']', body)
print("Routes:")
for r in sorted(set(routes))[:20]:
    print(f"  {r}")

# Look for API base or gateway patterns
gw = re.findall(r'["\']([^"\']*(?:gateway|api|service)[^"\']*)["\']', body)
print("\nGateway/API/Service strings:")
for g in sorted(set(gw))[:20]:
    if 5 < len(g) < 100:
        print(f"  {g}")

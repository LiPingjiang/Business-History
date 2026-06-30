#!/usr/bin/env python3
"""
企业招聘网站爬虫脚本
==================
实际爬取各企业招聘网站的北京研发/技术岗位数据

可爬取的网站（API 确认可用）：
1. Amazon Jobs API (amazon.jobs/en/search.json)
2. NVIDIA Workday API (nvidia.wd5.myworkdayjobs.com)
3. Microsoft Careers (通过浏览器自动化 catdesk browser-action)

无法直接爬取的网站：
- BOSS直聘/猎聘（反爬机制）
- 中国移动/电信/联通/工行等央企（JavaScript SPA，需浏览器渲染）
- Apple/Google/Meta（API 需认证或不可公开访问）
"""
import json
import ssl
import time
import urllib.request
import subprocess
import os
from datetime import datetime

OUTPUT_DIR = "/mnt/openclaw/catdesk/home/workspace/bh/爬取结果"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# SSL context that skips verification (for corporate proxy environments)
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
}

WORKDAY_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}


def http_get_json(url, headers=None):
    """GET request returning JSON."""
    req = urllib.request.Request(url, headers=headers or HEADERS)
    resp = urllib.request.urlopen(req, timeout=15, context=CTX)
    return json.loads(resp.read())


def http_post_json(url, body, headers=None):
    """POST request returning JSON."""
    data = json.dumps(body).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers or WORKDAY_HEADERS)
    resp = urllib.request.urlopen(req, timeout=15, context=CTX)
    return json.loads(resp.read())


def catdesk_evaluate(script):
    """Run JavaScript in browser via catdesk and return result."""
    cmd = ['catdesk', 'browser-action', json.dumps({"action": "evaluate", "script": script})]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    try:
        data = json.loads(result.stdout)
        return data.get('data', {}).get('result', '')
    except:
        return ''


def catdesk_navigate(url):
    """Navigate browser to URL."""
    cmd = ['catdesk', 'browser-action', json.dumps({
        "action": "navigate", "url": url, "waitUntil": "networkidle"
    })]
    subprocess.run(cmd, capture_output=True, text=True, timeout=30)


# ============================================================
# 1. Amazon Jobs API Crawler
# ============================================================
def crawl_amazon():
    """Crawl Amazon Jobs API for Beijing positions."""
    print("\n{'='*60}")
    print("1. Crawling Amazon Jobs API...")
    print("="*60)
    
    all_jobs = []
    seen_ids = set()
    
    # Amazon returns the same results regardless of query when city=Beijing
    # So we just get all Beijing jobs in one request
    url = "https://amazon.jobs/en/search.json?city=Beijing&count=50&page=1"
    try:
        data = http_get_json(url)
        total = data.get('hits', 0)
        jobs = data.get('jobs', [])
        print(f"  Total hits: {total}, Returned: {len(jobs)}")
        
        for j in jobs:
            if j.get('city') != 'Beijing':
                continue
            job_id = j.get('id', '')
            if job_id in seen_ids:
                continue
            seen_ids.add(job_id)
            
            title = j.get('title', '?')
            category = j.get('job_category', '?')
            desc = j.get('description_short', '')
            
            # Filter for R&D/tech roles
            tech_keywords = ['software', 'engineer', 'data', 'AI', 'developer', 
                           'research', 'scientist', 'architect', 'technical',
                           'machine learning', 'cloud', 'infrastructure']
            is_tech = any(kw.lower() in (title + category + desc).lower() for kw in tech_keywords)
            
            all_jobs.append({
                'company': 'Amazon',
                'title': title,
                'location': 'Beijing, China',
                'category': category,
                'url': f"https://amazon.jobs/en/jobs/{job_id}/",
                'is_tech': is_tech,
                'posted_date': j.get('posted_date', ''),
            })
            tag = " [TECH]" if is_tech else ""
            print(f"  - {title}{tag} | {category}")
        
        print(f"\n  Total Beijing jobs: {len(all_jobs)}")
        print(f"  Tech/R&D jobs: {sum(1 for j in all_jobs if j['is_tech'])}")
    except Exception as e:
        print(f"  ERROR: {e}")
    
    return all_jobs


# ============================================================
# 2. NVIDIA Workday API Crawler
# ============================================================
def crawl_nvidia():
    """Crawl NVIDIA Workday API for China/Beijing positions."""
    print("\n" + "="*60)
    print("2. Crawling NVIDIA Workday API...")
    print("="*60)
    
    all_china_jobs = []
    offset = 0
    limit = 20
    total = None
    
    url = "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs"
    
    while True:
        body = {'search': '', 'limit': limit, 'offset': offset}
        try:
            data = http_post_json(url, body)
        except Exception as e:
            print(f"  Error at offset {offset}: {e}")
            break
        
        if total is None:
            total = data.get('total', 0)
            print(f"  Total global jobs: {total}")
        
        jobs = data.get('jobPostings', [])
        if not jobs:
            break
        
        for j in jobs:
            loc = j.get('locationsText', '')
            if any(city in loc for city in ['China', 'Beijing', 'Shanghai', 'Shenzhen']):
                title = j.get('title', '?')
                path = j.get('externalPath', '')
                job_url = f"https://nvidia.wd5.myworkdayjobs.com{path}"
                
                # Filter for R&D/tech roles
                tech_keywords = ['software', 'engineer', 'data', 'AI', 'developer',
                               'research', 'scientist', 'architect', 'technical',
                               'machine learning', 'deep learning', 'CUDA', 'GPU',
                               'system', 'algorithm', 'circuit', 'verification', 'design']
                non_tech_keywords = ['manager', 'marketing', 'business development',
                                   'account manager', 'operations', 'sourcing', 'program manager']
                is_tech = any(kw.lower() in title.lower() for kw in tech_keywords) and \
                          not any(kw.lower() in title.lower() for kw in non_tech_keywords)
                
                all_china_jobs.append({
                    'company': 'NVIDIA',
                    'title': title,
                    'location': loc,
                    'url': job_url,
                    'is_tech': is_tech,
                    'posted_on': j.get('postedOn', ''),
                })
                
                tag = " [TECH]" if is_tech else ""
                print(f"  - {title}{tag} | {loc}")
        
        offset += limit
        if offset >= total:
            break
        if offset % 200 == 0:
            print(f"  Progress: {offset}/{total}...")
        time.sleep(0.3)
    
    # Filter for Beijing only
    beijing_jobs = [j for j in all_china_jobs if 'Beijing' in j['location']]
    print(f"\n  Total China jobs: {len(all_china_jobs)}")
    print(f"  Beijing jobs: {len(beijing_jobs)}")
    print(f"  Tech/R&D jobs in Beijing: {sum(1 for j in beijing_jobs if j['is_tech'])}")
    
    return all_china_jobs


# ============================================================
# 3. Microsoft Careers Browser Crawler
# ============================================================
def crawl_microsoft():
    """Crawl Microsoft Careers using browser automation."""
    print("\n" + "="*60)
    print("3. Crawling Microsoft Careers (browser)...")
    print("="*60)
    
    all_jobs = []
    
    # Navigate to Microsoft Careers search
    catdesk_navigate("https://apply.careers.microsoft.com/careers?lc=Beijing&kw=software&start=0&sort_by=timestamp")
    time.sleep(3)
    
    # Extract job data using evaluate
    script = """(function(){
        var jobs = [];
        var links = document.querySelectorAll('a[href*="careers/job"]');
        links.forEach(function(l) {
            var txt = l.textContent.trim();
            if (txt.length < 10) return;
            // Parse: TitleLocationPosted X ago
            var parts = txt.split(/Posted\s+/);
            var titleLoc = parts[0];
            var posted = parts[1] ? parts[1].trim() : '';
            
            // Try to separate title from location
            var locMatch = titleLoc.match(/(China|India|United States|United Kingdom|Germany|Netherlands|France|Japan|Korea|Brazil|Canada|Australia|Singapore|Ireland|Israel|Sweden|Finland|Denmark|Norway|Poland|Italy|Spain|Mexico|Costa Rica)/);
            var title = titleLoc;
            var location = '';
            if (locMatch) {
                var idx = titleLoc.indexOf(locMatch[1]);
                title = titleLoc.substring(0, idx).trim();
                location = titleLoc.substring(idx).trim();
            }
            
            var isChina = location.indexOf('China') >= 0 || location.indexOf('Beijing') >= 0;
            jobs.push({
                title: title,
                location: location,
                posted: posted,
                url: l.href,
                is_china: isChina
            });
        });
        return JSON.stringify(jobs);
    })()"""
    
    result = catdesk_evaluate(script)
    try:
        jobs = json.loads(result) if isinstance(result, str) else result
        print(f"  Total jobs on page: {len(jobs)}")
        
        china_jobs = [j for j in jobs if j.get('is_china')]
        print(f"  China jobs: {len(china_jobs)}")
        
        for j in jobs:
            title = j.get('title', '?')
            loc = j.get('location', '?')
            is_china = j.get('is_china', False)
            
            # Filter for R&D/tech roles
            tech_keywords = ['software', 'engineer', 'data', 'AI', 'developer',
                           'research', 'scientist', 'architect', 'technical',
                           'machine learning', 'cloud', 'solution']
            is_tech = any(kw.lower() in title.lower() for kw in tech_keywords)
            
            all_jobs.append({
                'company': 'Microsoft',
                'title': title,
                'location': loc,
                'url': j.get('url', ''),
                'is_tech': is_tech,
                'is_china': is_china,
                'posted': j.get('posted', ''),
            })
            
            tag = " [TECH]" if is_tech else ""
            china_tag = " [CHINA]" if is_china else ""
            print(f"  - {title}{tag}{china_tag} | {loc}")
        
        print(f"\n  Total jobs: {len(all_jobs)}")
        print(f"  China jobs: {len(china_jobs)}")
        print(f"  Tech jobs: {sum(1 for j in all_jobs if j['is_tech'])}")
    except Exception as e:
        print(f"  Parse error: {e}")
        print(f"  Raw result: {result[:500]}")
    
    return all_jobs


# ============================================================
# 4. Additional Workday-based Crawlers
# ============================================================
def crawl_workday(company, tenant, site, wd_server="wd5"):
    """Generic Workday API crawler."""
    print(f"\n  Trying {company} ({tenant}.{wd_server}.myworkdayjobs.com/{site})...")
    url = f"https://{tenant}.{wd_server}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs"
    
    try:
        data = http_post_json(url, {'search': '', 'limit': 5, 'offset': 0})
        total = data.get('total', 0)
        jobs = data.get('jobPostings', [])
        if jobs:
            print(f"    ✓ Site found! Total jobs: {total}")
            return True, total
        else:
            print(f"    No jobs returned")
            return False, 0
    except Exception as e:
        print(f"    ✗ Failed: {e}")
        return False, 0


def try_more_companies():
    """Try to discover more Workday-based company career sites."""
    print("\n" + "="*60)
    print("4. Discovering more Workday career sites...")
    print("="*60)
    
    # Known and guessed Workday tenants
    companies = [
        ("Sony", "sony", "SonyCareers", "wd5"),
        ("Sony", "sony", "External", "wd5"),
        ("Samsung", "samsung", "SamsungCareers", "wd1"),
        ("Samsung", "samsung", "External", "wd5"),
        ("Siemens", "siemens", "Siemens_Careers", "wd3"),
        ("Siemens", "siemens", "External", "wd3"),
        ("Cisco", "cisco", "External", "wd5"),
        ("Cisco", "cisco", "CiscoCareers", "wd3"),
        ("Qualcomm", "qualcomm", "External", "wd5"),
        ("AMD", "amd", "External", "wd5"),
        ("VMware", "vmware", "external", "wd1"),
        ("Dell", "dell", "DellCareers", "wd1"),
        ("Dell", "dell", "External", "wd5"),
        ("Intel", "intel", "External", "wd5"),
        ("Intel", "intel", "IntelCareers", "wd5"),
        ("Oracle", "oracle", "External", "wd3"),
        ("SAP", "sap", "SAP_Careers", "wd3"),
        ("SAP", "sap", "External", "wd3"),
        ("Tesla", "tesla", "Tesla", "wd5"),
        ("Google", "google", "External", "wd5"),
        ("Apple", "apple", "External", "wd3"),
    ]
    
    found = []
    for name, tenant, site, wd in companies:
        ok, total = crawl_workday(name, tenant, site, wd)
        if ok:
            found.append((name, tenant, site, wd, total))
        time.sleep(0.3)
    
    print(f"\n  Found {len(found)} working Workday sites:")
    for name, tenant, site, wd, total in found:
        print(f"    - {name}: {tenant}.{wd}.myworkdayjobs.com/{site} ({total} jobs)")
    
    return found


# ============================================================
# Main
# ============================================================
def main():
    print("="*60)
    print(f"企业招聘网站爬虫脚本")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    results = {}
    
    # 1. Amazon
    results['amazon'] = crawl_amazon()
    
    # 2. NVIDIA
    results['nvidia'] = crawl_nvidia()
    
    # 3. Microsoft (browser)
    results['microsoft'] = crawl_microsoft()
    
    # 4. Try more companies
    found_sites = try_more_companies()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for company, jobs in results.items():
        beijing = [j for j in jobs if 'Beijing' in j.get('location', '') or j.get('is_china')]
        tech = [j for j in beijing if j.get('is_tech')]
        print(f"  {company}: {len(jobs)} total, {len(beijing)} Beijing, {len(tech)} tech/R&D")
    
    # Save results
    output_file = os.path.join(OUTPUT_DIR, f"crawl_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'crawl_time': datetime.now().isoformat(),
            'results': results,
            'found_workday_sites': [(name, tenant, site, wd, total) for name, tenant, site, wd, total in found_sites],
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    
    # Also save a clean summary for each company
    for company, jobs in results.items():
        if not jobs:
            continue
        beijing_jobs = [j for j in jobs if 'Beijing' in j.get('location', '') or 
                       (company == 'microsoft' and j.get('is_china'))]
        if beijing_jobs:
            summary_file = os.path.join(OUTPUT_DIR, f"{company}_beijing_jobs.json")
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(beijing_jobs, f, ensure_ascii=False, indent=2)
            print(f"  {company} Beijing jobs saved to: {summary_file}")


if __name__ == "__main__":
    main()

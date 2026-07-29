"""Beisen (北森) zhiye.com new portal adapter - uses POST /api/Jobad/GetJobAdPageList"""
import httpx
from models import Job, CrawlResult
from config import CompanyConfig


class BeisenAdapter:
    def close(self):
        pass

    """Adapter for beisen new-portal zhiye.com sites (e.g. chinaunicom.zhiye.com)"""

    def crawl(self, company: CompanyConfig) -> CrawlResult:
        base_url = company.url.rstrip('/')
        api_url = f"{base_url}/api/Jobad/GetJobAdPageList"
        headers = {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": base_url,
        }
        jobs = []
        page = 0
        try:
            while True:
                resp = httpx.post(api_url, json={"PageIndex": page, "PageSize": 50}, headers=headers, timeout=15)
                resp.raise_for_status()
                data = resp.json()
                if data.get("Code") != 200:
                    return CrawlResult(company=company.name, success=False, jobs=[], error=f"API error: {data.get('Message')}")
                items = data.get("Data", [])
                if not items:
                    break
                for item in items:
                    loc_names = item.get("LocNames") or []
                    location = ", ".join(loc_names) if loc_names else ""
                    jobs.append(Job(
                        title=item.get("JobAdName", ""),
                        location=location,
                        url=f"{base_url}/Social/SocialDetail/{item.get('Id', '')}",
                        company=company.name,
                        source_adapter="beisen",
                    ))
                if len(items) < 50:
                    break
                page += 1
                if page > 20:
                    break
            return CrawlResult(adapter_name="beisen", company=company.name, success=True, jobs=jobs)
        except Exception as e:
            return CrawlResult(adapter_name="beisen", company=company.name, success=False, jobs=jobs, error=str(e))

from adapters.base import BaseAdapter
from adapters.workday import WorkdayAdapter
from adapters.zhiye import ZhiyeAdapter
from adapters.hotjob import HotjobAdapter
from adapters.amazon import AmazonAdapter
from adapters.microsoft import MicrosoftAdapter
from adapters.siemens import SiemensAdapter
from adapters.bmw import BmwAdapter
from adapters.astrazeneca import AstraZenecaAdapter
from adapters.smartrecruiters import SmartRecruitersAdapter
from adapters.mokahr import MokahrAdapter
from adapters.recruitportal import RecruitPortalAdapter
from adapters.spdb import SPDBAdapter
from adapters.cmbc import CmbcAdapter
from adapters.jibe import JibeAdapter
from adapters.phenom import PhenomAdapter
from adapters.beisen import BeisenAdapter
from adapters.custom_pw import CustomPlaywrightAdapter

# Playwright adapters (lazy import to avoid hard dependency)
try:
    from adapters.zhiye_pw import ZhiyePlaywrightAdapter
    from adapters.hotjob_pw import HotjobPlaywrightAdapter
    _HAS_PLAYWRIGHT = True
except ImportError:
    _HAS_PLAYWRIGHT = False

ADAPTER_REGISTRY: dict[str, type[BaseAdapter]] = {
    "workday": WorkdayAdapter,
    "zhiye": ZhiyeAdapter,
    "hotjob": HotjobAdapter,
    "amazon": AmazonAdapter,
    "microsoft": MicrosoftAdapter,
    "siemens": SiemensAdapter,
    "bmw": BmwAdapter,
    "astrazeneca": AstraZenecaAdapter,
    "smartrecruiters": SmartRecruitersAdapter,
    "mokahr": MokahrAdapter,
    "recruitportal": RecruitPortalAdapter,
    "spdb": SPDBAdapter,
    "cmbc": CmbcAdapter,
    "jibe": JibeAdapter,
    "phenom": PhenomAdapter,
    "beisen": BeisenAdapter,
}

if _HAS_PLAYWRIGHT:
    ADAPTER_REGISTRY["zhiye_pw"] = ZhiyePlaywrightAdapter
    ADAPTER_REGISTRY["hotjob_pw"] = HotjobPlaywrightAdapter
    ADAPTER_REGISTRY["custom_pw"] = CustomPlaywrightAdapter


def get_adapter(name: str) -> BaseAdapter:
    """根据名称获取adapter实例"""
    cls = ADAPTER_REGISTRY.get(name)
    if cls is None:
        raise ValueError(f"Unknown adapter: {name}")
    return cls()

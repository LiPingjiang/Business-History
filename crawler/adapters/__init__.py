from adapters.base import BaseAdapter
from adapters.workday import WorkdayAdapter
from adapters.zhiye import ZhiyeAdapter
from adapters.hotjob import HotjobAdapter
from adapters.amazon import AmazonAdapter
from adapters.microsoft import MicrosoftAdapter
from adapters.siemens import SiemensAdapter
from adapters.bmw import BmwAdapter

ADAPTER_REGISTRY: dict[str, type[BaseAdapter]] = {
    "workday": WorkdayAdapter,
    "zhiye": ZhiyeAdapter,
    "hotjob": HotjobAdapter,
    "amazon": AmazonAdapter,
    "microsoft": MicrosoftAdapter,
    "siemens": SiemensAdapter,
    "bmw": BmwAdapter,
}


def get_adapter(name: str) -> BaseAdapter:
    """根据名称获取adapter实例"""
    cls = ADAPTER_REGISTRY.get(name)
    if cls is None:
        raise ValueError(f"Unknown adapter: {name}")
    return cls()

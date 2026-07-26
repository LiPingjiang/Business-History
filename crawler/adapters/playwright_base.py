"""Playwright浏览器渲染基类 — 用于SPA站点"""
from __future__ import annotations
from abc import abstractmethod
from typing import List
import json
import re

from playwright.sync_api import sync_playwright, Page, Browser

from adapters.base import BaseAdapter
from models import Job
from config import CompanyConfig


class PlaywrightAdapter(BaseAdapter):
    """需要浏览器渲染的adapter基类"""

    name = "playwright_base"

    def __init__(self):
        super().__init__()
        self._playwright = None
        self._browser: Browser | None = None

    def _get_browser(self) -> Browser:
        if self._browser is None:
            self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.launch(headless=True)
        return self._browser

    def _new_page(self) -> Page:
        browser = self._get_browser()
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )
        return context.new_page()

    def close(self):
        super().close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

    @abstractmethod
    def fetch_jobs(self, company: CompanyConfig) -> List[Job]:
        ...

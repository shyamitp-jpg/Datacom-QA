import pytest
from playwright.sync_api import sync_playwright
from pages.bugs_form_page import BugsFormPage
import os
from datetime import datetime

headless = os.getenv("HEADLESS", "0") == "1"

os.makedirs("pytest_tests/screenshots_pytest", exist_ok=True)

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=["--start-maximized"])
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def form(page):
    return BugsFormPage(page)

def pytest_exception_interact(node, call, report):
    if report.failed and "page" in node.funcargs:
        page = node.funcargs["page"]
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"pytest_tests/screenshots_pytest/FAIL_{node.name}_{ts}.png"
        page.screenshot(path=path, full_page=True)
        print(f"PYTEST PROOF → {path}")
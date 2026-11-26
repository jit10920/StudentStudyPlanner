"""End-to-end browser tests (Selenium + headless Chrome) against a live server."""
import importlib
import threading

import pytest

selenium = pytest.importorskip("selenium")
from selenium import webdriver  # noqa: E402
from selenium.common.exceptions import WebDriverException  # noqa: E402
from selenium.webdriver.common.by import By  # noqa: E402
from werkzeug.serving import make_server  # noqa: E402

import database  # noqa: E402


@pytest.fixture
def live_server(monkeypatch, tmp_path):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "e2e.db")
    module = importlib.reload(importlib.import_module("app"))
    server = make_server("127.0.0.1", 0, module.app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()


@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    for flag in ("--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--window-size=1280,900"):
        options.add_argument(flag)
    try:
        driver = webdriver.Chrome(options=options)
    except WebDriverException as error:
        pytest.skip(f"Chrome/driver unavailable: {error.msg[:80]}")
    driver.implicitly_wait(3)
    yield driver
    driver.quit()


def add_course(browser, base, name, code):
    browser.get(f"{base}/courses")
    browser.find_element(By.NAME, "course_name").send_keys(name)
    browser.find_element(By.NAME, "course_code").send_keys(code)
    browser.find_element(By.CSS_SELECTOR, "form[method=post] .btn-primary").click()


def test_add_course_appears_in_list(live_server, browser):
    add_course(browser, live_server, "Data Communication", "CSE3203")

    assert "Data Communication" in browser.page_source
    assert "Course added successfully" in browser.page_source


def test_add_task_then_complete_updates_progress(live_server, browser):
    add_course(browser, live_server, "Data Communication", "CSE3203")

    browser.get(f"{live_server}/tasks")
    browser.find_element(By.NAME, "title").send_keys("Finish lab report")
    browser.find_element(By.CSS_SELECTOR, "form[method=post] .btn-primary").click()
    assert "Finish lab report" in browser.page_source

    browser.find_element(By.CSS_SELECTOR, "form[action*='/tasks/complete/'] button").click()
    assert "Task marked as completed" in browser.page_source

    browser.get(f"{live_server}/progress")
    assert browser.find_element(By.ID, "overall-percent").text == "100%"


def test_activity_page_shows_observer_log(live_server, browser):
    browser.get(f"{live_server}/tasks")
    browser.find_element(By.NAME, "title").send_keys("Observe me")
    browser.find_element(By.CSS_SELECTOR, "form[method=post] .btn-primary").click()

    browser.get(f"{live_server}/activity")

    assert "Task added: Observe me" in browser.page_source


def test_navigation_reaches_deadlines(live_server, browser):
    browser.get(live_server)
    browser.find_element(By.LINK_TEXT, "Deadlines").click()

    assert "Deadline Management" in browser.page_source

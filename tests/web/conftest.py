import os
import time

import requests
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver

import pytest

from litres_project.helpers.helper_api import api_put_wishlist, check_status_code, api_put_cart_add
from litres_project.models.book_model import Book
from litres_project.utils import attach
from litres_project.utils.logging import book_attaching
from litres_project.utils.resource import load_data_json_value
from tests.web.config import USE_SELENOID, DEFAULT_SELENOID_URL, DEFAULT_BROWSER_VERSION, DEFAULT_BROWSER_NAME, BASE_URL
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name",
        action="store",
        default="chrome",
        help="Укажите браузер: chrome или firefox"
    )
    parser.addoption(
        "--browser_version",
        action="store",
        default="128.0",
        help="Укажите версию браузера"  # chrome 128.0, 127.0, firefox 124.0, 125.0
    )
    parser.addoption(
        "--selenoid_url",
        action="store",
        default="selenoid.autotests.cloud",
        help="URL Selenoid"
    )


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function")
def setup_browser(request):
    # Определяем, используется ли Selenoid
    print(f" Selenoid: {USE_SELENOID}")
    video_url = ""

    if USE_SELENOID:
        browser_name = request.config.getoption('--browser_name')
        browser_version = request.config.getoption('--browser_version')
        selenoid_url = request.config.getoption('--selenoid_url')
        print(f"Установленные параметры: {selenoid_url}: {browser_name}:{browser_version}")
        browser_name = browser_name if browser_name != "" else DEFAULT_BROWSER_NAME
        browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION
        selenoid_url = selenoid_url if selenoid_url != "" else DEFAULT_SELENOID_URL

        options = FirefoxOptions() if browser_name.lower() == "firefox" else Options()

        selenoid_capabilities = {
            "browserName": browser_name,
            "browserVersion": browser_version,
            "selenoid:options": {
                "enableLog": True,
                "enableVNC": True,
                "enableVideo": True,
                "screenResolution": "1280x1080"
            },
            "goog:loggingPrefs": {"browser": "ALL"},
        }

        if browser_name.lower() == "firefox":
            selenoid_capabilities["moz:firefoxOptions"] = {
                "log": {"level": "trace"},
                "prefs": {
                    "devtools.console.stdout.content": True,
                    "browser.console.showInPanel": True,
                    "dom.ipc.processCount": 8
                }
            }

        options.capabilities.update(selenoid_capabilities)

        selenoid_login = os.getenv("SELENOID_LOGIN")
        selenoid_pass = os.getenv("SELENOID_PASS")

        print(options.to_capabilities())
        driver = webdriver.Remote(
            command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub",
            options=options
        )

        video_url = selenoid_url
    else:
        print(f"Браузер: {DEFAULT_BROWSER_NAME}")
        options = FirefoxOptions() if DEFAULT_BROWSER_NAME.lower() == "firefox" else Options()
        if DEFAULT_BROWSER_NAME.lower() == "firefox":
            options.set_preference("devtools.console.stdout.content", True)
            options.set_preference("browser.console.showInPanel", True)
        driver = webdriver.Firefox(options=options) if DEFAULT_BROWSER_NAME.lower() == "firefox" else webdriver.Chrome(
            options=options)
    browser.config.driver = driver
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.timeout = 5
    browser.config.base_url = BASE_URL
    yield browser
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser, video_url)
    driver.quit()


@pytest.fixture(params=load_data_json_value('search.json'))
def search_data(request):
    return request.param


@pytest.fixture(scope="function")
def api_session():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def api_session_add_wishlist(api_session):
    book1 = Book(id='66924193')
    book2 = Book(id='65841173')
    book_attaching(book1, "Book1")
    book_attaching(book2, "Book2")
    response1 = api_put_wishlist(api_session, book1.id)
    check_status_code(response1, 204)
    time.sleep(20)  # Добавлено специально, чтобы избежать блокировки
    response2 = api_put_wishlist(api_session, book2.id)
    check_status_code(response2, 204)
    yield api_session, book1, book2


@pytest.fixture(scope="function")
def api_session_add_cart(api_session):
    book1 = Book(id='66924193')
    book2 = Book(id='65841173')
    book_attaching(book1, "Book1")
    book_attaching(book2, "Book2")
    response1 = api_put_cart_add(api_session, book1.id)
    check_status_code(response1, 200)
    time.sleep(20)  # Добавлено специально, чтобы избежать блокировки
    response2 = api_put_cart_add(api_session, book2.id)
    check_status_code(response2, 200)
    yield api_session, book1, book2


@pytest.fixture(scope="function")
def api_session():
    session = requests.Session()
    yield session
    session.close()

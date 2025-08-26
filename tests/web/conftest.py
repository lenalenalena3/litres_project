import os
import time
from pathlib import Path

import allure
import allure_commons
import requests
from dotenv import load_dotenv
from selene import browser, support
from selenium import webdriver

import pytest

from litres_project.helpers.helper_api import APIHelper
from litres_project.models.book_model import Book
from litres_project.utils import attach
from litres_project.utils.logging import book_attaching
from litres_project.utils.resource import load_data_json_value, abs_path_from_project
from tests.web import config


def pytest_addoption(parser):
    parser.addoption(
        "--context",
        default=None,
        help="Укажите файл настроек: selenoid, local_web"
    )


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture
def context(request):
    return request.config.getoption("--context") or 'local_web'


@pytest.fixture(scope='function', autouse=True)
def web_management(request, context):
    settings = config.get_settings(context)
    options = config.driver_options(settings, context)
    if context == 'selenoid':
        selenoid_url = settings.SELENOID_URL

        credentials_path = abs_path_from_project('.env.selenoid_credentials')
        print(f"Загружаем credentials из: {credentials_path}")
        if not Path(credentials_path).exists():
            raise FileNotFoundError(f"Файл .env.credentials не найден: {credentials_path}")
        load_dotenv(dotenv_path=credentials_path)
        selenoid_login = os.getenv("SELENOID_LOGIN")
        selenoid_pass = os.getenv("SELENOID_PASS")
        if not all([selenoid_login, selenoid_pass]):
            raise ValueError("SELENOID_LOGIN и SELENOID_PASS не установлены")

        driver = webdriver.Remote(
            command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub",
            options=options
        )
    if context == 'local_web':
        if settings.BROWSER_NAME.lower() == "firefox":
            driver = webdriver.Firefox(options=options)
        else:
            driver = webdriver.Chrome(options=options)

    browser.config.driver = driver
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.timeout = settings.TIMEOUT
    browser.config.base_url = settings.BASE_URL
    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )
    yield browser
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    if context == 'selenoid':
        video_url = selenoid_url
        attach.add_video(browser, video_url)
    with allure.step("Закрыть браузер"):
        browser.quit()


@pytest.fixture(params=load_data_json_value('search.json'))
def search_data(request):
    return request.param


@pytest.fixture(scope="function")
def api_session(request):
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture
def helper_api(context):
    settings = config.get_settings(context)
    helper = APIHelper()
    helper.set_base_url_api(settings.BASE_URL_API)
    return helper


@pytest.fixture(scope="function")
def api_session_add_wishlist(api_session, helper_api):
    book1 = Book(id='66924193')
    book2 = Book(id='65841173')
    book_attaching(book1, "Book1")
    book_attaching(book2, "Book2")

    response_book1 = helper_api.api_put_wishlist(api_session, book1.id)
    helper_api.check_status_code(response_book1, 204)
    time.sleep(20)  # Добавлено специально, чтобы избежать блокировки
    response_book2 = helper_api.api_put_wishlist(api_session, book2.id)
    helper_api.check_status_code(response_book2, 204)
    yield api_session, book1, book2


@pytest.fixture(scope="function")
def api_session_add_cart(api_session, helper_api):
    book1 = Book(id='66924193')
    book2 = Book(id='65841173')
    book_attaching(book1, "Book1")
    book_attaching(book2, "Book2")

    response_book1 = helper_api.api_put_cart_add(api_session, book1.id)
    helper_api.check_status_code(response_book1, 200)
    time.sleep(20)  # Добавлено специально, чтобы избежать блокировки
    response_book2 = helper_api.api_put_cart_add(api_session, book2.id)
    helper_api.check_status_code(response_book2, 200)
    yield api_session, book1, book2

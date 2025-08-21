import os
import time
from pathlib import Path

import pytest
import requests
from dotenv import load_dotenv

from litres_project.helpers.helper_api import APIHelper
from litres_project.models.book_model import Book
from litres_project.utils.logging import book_attaching
from litres_project.utils.resource import abs_path_from_project


def pytest_addoption(parser):
    parser.addoption(
        "--context",
        default='api',
        help="Укажите файл настроек: api"
    )


@pytest.fixture
def context(request):
    return request.config.getoption("--context") or 'api'


@pytest.fixture
def helper_api(context):
    helper = APIHelper()
    env_filename = f'.env.{context}'
    url_api_path = abs_path_from_project(env_filename)
    if not Path(url_api_path).exists():
        raise FileNotFoundError(f"Файл .env.{context} не найден: {url_api_path}")
    load_dotenv(dotenv_path=url_api_path)
    helper.set_base_url_api(os.getenv("BASE_URL_API"))
    return helper

@pytest.fixture(scope="function")
def api_session():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def api_session_add_wishlist(api_session, helper_api):
    book = Book(id='65841173')
    book_attaching(book, "Book")
    helper_api.set_base_url_api(os.getenv("BASE_URL_API"))
    helper_api.api_put_wishlist(api_session, book.id)
    yield api_session, book
    api_session.close()


@pytest.fixture(scope="function")
def api_session_add_cart(api_session, helper_api):
    book = Book(id='65841173')
    book_attaching(book, "Book")
    helper_api.set_base_url_api(os.getenv("BASE_URL_API"))
    helper_api.api_put_cart_add(api_session, book.id)
    yield api_session, book
    api_session.close()


@pytest.fixture(autouse=True)
def delay_between_tests():
    yield
    time.sleep(30)  # Добавлено специально, чтобы избежать блокировки

import time

import pytest
import requests
from dotenv import load_dotenv

from litres_project.helpers.helper_api import api_put_wishlist, api_put_cart_add
from litres_project.models.book_model import Book
from litres_project.utils.logging import book_attaching


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function")
def api_session():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def api_session_add_wishlist(api_session):
    book = Book(id='65841173')
    book_attaching(book, "Book")
    api_put_wishlist(api_session, book.id)
    yield api_session, book
    api_session.close()


@pytest.fixture(scope="function")
def api_session_add_cart(api_session):
    book = Book(id='65841173')
    book_attaching(book, "Book")
    api_put_cart_add(api_session, book.id)
    yield api_session, book
    api_session.close()


@pytest.fixture(autouse=True)
def delay_between_tests():
    yield
    time.sleep(30)  # Добавлено специально, чтобы избежать блокировки

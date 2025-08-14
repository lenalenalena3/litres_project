import allure
from allure_commons._allure import step
from allure_commons.types import Severity
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have

from litres_project.pages.application_mobile import app_mobile
from litres_project.utils.resource import load_data_json


@allure.epic("MOBILE")
@allure.feature("Личный кабинет")
@allure.story("Список избранных книг")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression")
@allure.title("Личный кабинет: Добавление в избранное")
@allure.description("Найти по поиску книгу -> Добавить книгу в избранное -> Проверить список избранных книг")
def test_add_favorite(open_app):
    with step('Найти по поиску книгу'):
        text = "Красная корова"
        app_mobile.search_page_mobile.search(text)
    with step('Добавить первую книгу в избранные'):
        index = 0
        book = app_mobile.search_page_mobile.add_favorite(index)
    with step('Открыть список избранных книг'):
        app_mobile.favorite_page_mobile.open_favorite()
    with step('Проверить, что в списке есть книга {text}'):
        app_mobile.favorite_page_mobile.should_favorite_by_name(1, [book.name])


@allure.epic("MOBILE")
@allure.feature("Книжная страница")
@allure.story("Работоспособность кнопок")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression")
@allure.title("Книжная страница: Просмотр оглавления")
@allure.description("Найти по поиску книгу -> Открыть книгу -> Проверить оглавление")
def test_open_contents(open_app):
    with step('Найти по поиску книгу'):
        text = "Красная корова"
        app_mobile.search_page_mobile.search(text)
    with step('Открыть книгу'):
        index = 0
        app_mobile.search_page_mobile.open_book(index)
    with step('Проверить оглавление'):
        list_book = load_data_json('contents_mobile.json')
        contents = list_book['contents']
        app_mobile.book_page_mobile.should_contents(contents)

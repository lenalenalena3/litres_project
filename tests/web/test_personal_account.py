import allure
import pytest
from allure_commons.types import Severity

from litres_project.pages.application import app


@allure.epic("Пользовательские взаимодействия")
@allure.feature("Личный кабинет")
@allure.story("Список 'Отложено'")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression")
@allure.title("Личный кабинет: Добавление книги в список 'Отложено'")
@allure.description(
    "Открыть страницу -> Найти нужный товар -> добавить товар в избранное -> проверить страницу избранное")
def test_add_favorites(setup_browser):
    app.menu_page.open_main_page()
    text = "Красная корова Барвицкая"
    app.menu_page.search_text(text)
    index_book = 0
    book = app.list_results_page.add_favorite(index_book)
    app.menu_page.open_my_books()
    app.favorite_page.open_favorite()
    app.favorite_page.should_favorite_result_name(1, [book.name])

@pytest.mark.skip(reason="Тест не доделан")
@allure.epic("Пользовательские взаимодействия")
@allure.feature("Личный кабинет")
@allure.story("Список 'Отложено'")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression")
@allure.title("Личный кабинет: Удаление книги из списка 'Отложено'")
@allure.description(
    "Открыть страницу -> Открыть избранное -> удалить товар из избранного -> проверить страницу избранное")
def test_del_favorites(setup_browser):
    app.menu_page.open_main_page()
    text = "Красная корова Барвицкая"
    app.menu_page.search_text(text)
    index_book = 0
    book = app.list_results_page.add_favorite(index_book)
    app.menu_page.open_my_books()
    app.favorite_page.open_favorite()
    app.favorite_page.should_favorite_result_name(1, [book.name])


@pytest.mark.skip(reason="Тест не доделан")
@allure.epic("Пользовательские взаимодействия")
@allure.feature("Личный кабинет")
@allure.story("Корзина")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("smoke", "regression")
@allure.title("Личный кабинет: Добавление книги в корзину")
@allure.description(
    "Открыть страницу -> Найти нужный товар -> добавить товар в корзину -> проверить корзину")
def test_add_cart(setup_browser):
    app.menu_page.open_main_page()
    text = "Красная корова Барвицкая"
    app.menu_page.search_text(text)
    index_book = 0
    app.list_results_page.open_info_book(index_book)
    app.menu_page.open_cart()
    with allure.step("Проверить содержимое корзины"):
        pass



@pytest.mark.skip(reason="Тест не доделан")
@allure.epic("Пользовательские взаимодействия")
@allure.feature("Личный кабинет")
@allure.story("Корзина")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("smoke", "regression")
@allure.title("Личный кабинет: Удаление книги из корзины")
@allure.description(
    "Открыть страницу -> Открыть корзину -> удалить товар из корзины -> проверить корзину")
def test_del_cart(setup_browser):
    app.menu_page.open_main_page()
    text = "Красная корова Барвицкая"
    app.menu_page.search_text(text)
    index_book = 0
    book = app.list_results_page.add_favorite(index_book)
    app.menu_page.open_my_books()
    app.favorite_page.open_favorite()
    app.favorite_page.should_favorite_result_name(1, [book.name])


import allure
from allure_commons.types import Severity

from litres_project.pages.application import app

text = "Красная корова Барвицкая"


@allure.epic("WEB")
@allure.feature("Личный кабинет")
@allure.story("Список 'Отложено'")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression")
@allure.title("Личный кабинет: Добавление книги в список 'Отложено'")
@allure.description(
    "Открыть главную страницу -> Проверить, что список 'Отложено' пуст -> Найти по поиску книгу -> Добавить книгу в список 'Отложено' -> Проверить список 'Отложено'")
def test_add_wishlist(setup_browser):
    with allure.step("Открыть главную страницу"):
        app.menu_page.open_main_page()
    with allure.step("Проверить, что список 'Отложено' пуст"):
        app.menu_page.open_my_books()
        app.favorite_page.open_favorite()
        app.favorite_page.should_count_result(0)
    with allure.step("Найти по поиску книгу"):
        app.menu_page.search_text(text)
    with allure.step("Добавить книгу в список 'Отложено'"):
        index_book = 0
        book = app.search_page.add_favorite(index_book)
    with allure.step("Проверить список 'Отложено'"):
        app.menu_page.open_my_books()
        app.favorite_page.open_favorite()
        app.favorite_page.should_favorite_result_name(1, [book.name])


@allure.epic("WEB")
@allure.feature("Личный кабинет")
@allure.story("Список 'Отложено'")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression")
@allure.title("Личный кабинет: Удаление книги из списка 'Отложено'")
@allure.description(
    "Предусловие: в списке 'Отложено' есть две книги. "
    "Открыть главную страницу -> Открыть список 'Отложено' -> Проверить список 'Отложено' -> Удалить одну книгу -> Проверить список 'Отложено'")
def test_del_wishlist(setup_browser, api_session_add_wishlist):
    with allure.step("Открыть главную страницу"):
        api_session, book, book_del = api_session_add_wishlist
        app.menu_page.open_main_page()
        app.menu_page.refresh_cookies(api_session)
    with allure.step("Открыть список 'Отложено'"):
        app.menu_page.open_my_books()
        app.favorite_page.open_favorite()
    with allure.step("Проверить список 'Отложено'"):
        list_book = []
        list_book.append(book_del.id)
        list_book.append(book.id)
        app.favorite_page.should_favorite_result_id(2, list_book)
    with allure.step("Удалить одну книгу"):
        index_book = 0
        app.favorite_page.del_favorite(index_book)
    with allure.step("Проверить список 'Отложено'"):
        app.favorite_page.should_favorite_result_id(1, [book.id])

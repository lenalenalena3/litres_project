import allure
from allure_commons.types import Severity

from litres_project.helpers.helper_api import api_put_add_favorite, api_delete_del_favorite, api_request
from litres_project.models.book_model import Book
from litres_project.pages.application import app
from litres_project.utils.logging import book_attaching
from tests.api.config import BASE_URL_API


@allure.epic("Пользовательские взаимодействия")
@allure.feature("Личный кабинет")
@allure.story("Список 'Отложено'")
@allure.link("https://www.litres.ru/", name="litres")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression", "api")
@allure.title("API: Личный кабинет: Добавление в список 'Отложено' нескольких книг")
@allure.description("Добавить в список 'Отложено'  -> проверить список 'Отложено'")
def test_api_put_add_favorite(setup_browser, api_session):
    with allure.step("Добавление в избранное нескольких товаров (API)"):
        book1 = Book(id='66924193')
        book2 = Book(id='65841173')
        book_attaching(book1, "Book1")
        book_attaching(book2, "Book2")
        api_put_add_favorite(api_session, book1.id)
        api_put_add_favorite(api_session, book2.id)
    with allure.step("Проверить список избранного в интерфейсе"):
        app.menu_page.open_main_page()
        app.menu_page.refresh_cookies(api_session)
        app.menu_page.open_my_books()
        app.favorite_page.open_favorite()
        list_book = []
        list_book.append(book2.id)
        list_book.append(book1.id)
        app.favorite_page.should_favorite_result_id(2, list_book)


@allure.epic("Пользовательские взаимодействия")
@allure.feature("Личный кабинет")
@allure.story("Список 'Отложено'")
@allure.link("https://www.litres.ru/", name="litres")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression", "api")
@allure.title("API: Личный кабинет: Удаление из списка 'Отложено' только одной книги из нескольких")
@allure.description("Удалить из списка 'Отложено' только 1 товар -> проверить список 'Отложено'")
def test_api_delete_favorite(setup_browser, api_session_add_favorite):
    with allure.step("Удаление из избранного товара (API)"):
        api_session, book, book_del = api_session_add_favorite
        api_delete_del_favorite(api_session, book_del.id)
        book_attaching(book_del, "Book_del")
    with allure.step("Проверить список избранного в интерфейсе"):
        app.menu_page.open_main_page()
        app.menu_page.refresh_cookies(api_session)
        app.menu_page.open_my_books()
        app.favorite_page.open_favorite()
        list_book = []
        list_book.append(book.id)
        app.favorite_page.should_favorite_result_id(1, list_book)

@allure.epic("Пользовательские взаимодействия")
@allure.feature("Личный кабинет")
@allure.story("Список 'Отложено'")
@allure.link("https://www.litres.ru/", name="litres")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression", "api")
@allure.title("API: Личный кабинет: Удаление из списка 'Отложено' несуществующей книги")
@allure.description("Удалить из списка 'Отложено' несуществующий товар -> проверить статус ошибки 404")
def test_api_delete_non_existent(api_session):
    with allure.step("Удаление из избранного несуществующего товара (API)"):
        id_book='12345678'
        endpoint = f"/foundation/api/wishlist/arts/{id_book}"
        response = api_request(session=api_session, base_api_url=BASE_URL_API, endpoint=endpoint, method="DELETE")
        assert response.status_code == 404


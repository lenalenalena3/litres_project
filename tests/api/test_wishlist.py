import allure
from allure_commons.types import Severity

from litres_project.helpers.helper_api import api_put_wishlist, check_status_code, api_delete_wishlist
from litres_project.models.book_model import Book
from litres_project.utils.logging import book_attaching


@allure.epic("API")
@allure.feature("Личный кабинет")
@allure.story("Список 'Отложено'")
@allure.link("https://www.litres.ru/", name="litres")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression", "api")
@allure.title("API: PUT_wishlist: Добавление в список 'Отложено'")
@allure.description(
    "Отправить запрос PUT_wishlist -> "
    "В полученном ответе:"
    " - проверить, что статус код = 204")
def test_api_put_wishlist(api_session):
    with allure.step("Отправить запрос PUT_wishlist"):
        id_book = '65841173'
        book = Book(id=id_book)
        book_attaching(book, "Book")
        response = api_put_wishlist(api_session, book.id)
    with allure.step("Проверить ответ"):
        check_status_code(response, 204)


@allure.epic("API")
@allure.feature("Личный кабинет")
@allure.story("Список 'Отложено'")
@allure.link("https://www.litres.ru/", name="litres")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression", "api")
@allure.title("API: DELETE_wishlist: Удаление из списка 'Отложено'")
@allure.description(
    "Отправить запрос DELETE_wishlist -> "
    "В полученном ответе:"
    " - проверить, что статус код = 204")
def test_api_delete_wishlist(api_session_add_wishlist):
    with allure.step("Отправить запрос DELETE_wishlist"):
        api_session, id_book_del = api_session_add_wishlist
        book_attaching(id_book_del, "Book_del")
        response = api_delete_wishlist(api_session, id_book_del.id)
    with allure.step("Проверить ответ"):
        check_status_code(response, 204)


@allure.epic("API")
@allure.feature("Личный кабинет")
@allure.story("Список 'Отложено'")
@allure.link("https://www.litres.ru/", name="litres")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression", "api")
@allure.title("API: DELETE_wishlist: Удаление из списка 'Отложено' несуществующей книги")
@allure.description(
    "Отправить запрос DELETE_wishlist с несуществующим id-> "
    "В полученном ответе: проверить, что статус код = 404")
def test_api_delete_wishlist_non_existent(api_session):
    with allure.step("Отправить запрос DELETE_wishlist"):
        id_book = '12345678'
        book = Book(id=id_book)
        response = api_delete_wishlist(api_session, book.id)
    with allure.step("Проверить ответ"):
        check_status_code(response, 404)

import allure
from allure_commons.types import Severity

from litres_project.models.book_model import Book
from litres_project.utils.logging import book_attaching


@allure.epic("API")
@allure.feature("Личный кабинет")
@allure.story("Список 'Отложено'")
class TestWishlist:

    @allure.link("https://www.litres.ru/", name="litres")
    @allure.severity(Severity.NORMAL)
    @allure.label("owner", "Tinkalyuk")
    @allure.tag("regression", "api")
    @allure.title("Личный кабинет: Добавление в список 'Отложено'")
    @allure.description(
        "1. Отправить запрос PUT_wishlist \n"
        "2. Проверить ответ: \n "
        " - проверить, что статус код = 204")
    def test_api_put_wishlist(self, api_session, helper_api):
        with allure.step("Отправить запрос PUT_wishlist"):
            id_book = '65841173'
            book = Book(id=id_book)
            book_attaching(book, "Book")
            response = helper_api.api_put_wishlist(api_session, book.id)
        with allure.step("Проверить ответ"):
            helper_api.check_status_code(response, 204)

    @allure.link("https://www.litres.ru/", name="litres")
    @allure.severity(Severity.NORMAL)
    @allure.label("owner", "Tinkalyuk")
    @allure.tag("regression", "api")
    @allure.title("Личный кабинет: Удаление из списка 'Отложено'")
    @allure.description(
        "1. Отправить запрос DELETE_wishlist \n"
        "2. Проверить ответ: \n"
        " - проверить, что статус код = 204")
    def test_api_delete_wishlist(self, api_session_add_wishlist, helper_api):
        with allure.step("Отправить запрос DELETE_wishlist"):
            api_session, id_book_del = api_session_add_wishlist
            book_attaching(id_book_del, "Book_del")
            response = helper_api.api_delete_wishlist(api_session, id_book_del.id)
        with allure.step("Проверить ответ"):
            helper_api.check_status_code(response, 204)

    @allure.link("https://www.litres.ru/", name="litres")
    @allure.severity(Severity.NORMAL)
    @allure.label("owner", "Tinkalyuk")
    @allure.tag("regression", "api")
    @allure.title("Личный кабинет: Удаление из списка 'Отложено' несуществующей книги")
    @allure.description(
        "1. Отправить запрос DELETE_wishlist с несуществующим id \n"
        "2. Проверить ответ: \n"
        " - проверить, что статус код = 404")
    def test_api_delete_wishlist_non_existent(self, api_session, helper_api):
        with allure.step("Отправить запрос DELETE_wishlist"):
            id_book = '12345678'
            book = Book(id=id_book)
            response = helper_api.api_delete_wishlist(api_session, book.id)
        with allure.step("Проверить ответ"):
            helper_api.check_status_code(response, 404)

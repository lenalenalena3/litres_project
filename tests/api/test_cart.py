import allure
from allure_commons.types import Severity

from litres_project.models.book_model import Book


@allure.epic("API")
@allure.feature("Личный кабинет")
@allure.story("Корзина")
class TestCart:

    @allure.severity(Severity.CRITICAL)
    @allure.label("owner", "Tinkalyuk")
    @allure.tag("regression", "api")
    @allure.title("API: PUT_cart_add: Личный кабинет: Добавление в корзину")
    @allure.description(
        "1. Отправить запрос PUT_add_cart \n"
        "2. Проверить ответ:\n"
        " - проверить, что статус код = 200,\n"
        " - сверить с схемой put_add_cart.json,\n"
        " - проверить, что в ответе есть добавленный id")
    def test_api_put_cart_add(self, api_session, helper_api):
        with allure.step("Отправить запрос PUT_cart_add"):
            id_book = '65841173'
            book = Book(id=id_book)
            response = helper_api.api_put_cart_add(api_session, book.id)
        with allure.step("Проверить ответ"):
            helper_api.check_status_code(response, 200)
            helper_api.validate_schema(response, 'put_add_cart.json')
            json_data = response.json()
            field = "added_art_ids"
            with allure.step(f"Проверить в response: {field} == [{id_book}]"):
                assert json_data['payload']['data'][field] == [int(id_book)], \
                    f"Ожидалось {id_book}, получено {json_data['payload']['data'][field]}"

    @allure.severity(Severity.CRITICAL)
    @allure.label("owner", "Tinkalyuk")
    @allure.tag("regression", "api")
    @allure.title("API: PUT_cart_remove: Личный кабинет: Удаление из корзины")
    @allure.description(
        "1. Отправить запрос PUT_cart_remove \n "
        "2. Проверить ответ:\n"
        " - проверить, что статус код = 204")
    def test_api_put_cart_remove(self, api_session_add_cart, helper_api):
        session, book = api_session_add_cart
        with allure.step("Отправить запрос PUT_cart_remove"):
            response = helper_api.api_put_cart_remove(session, book.id)
        with allure.step("Проверить ответ"):
            helper_api.check_status_code(response, 204)

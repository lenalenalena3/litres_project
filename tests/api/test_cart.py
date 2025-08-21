import allure
from allure_commons.types import Severity

from litres_project.models.book_model import Book


@allure.epic("API")
@allure.feature("Личный кабинет")
@allure.story("Корзина")
@allure.link("https://www.litres.ru/", name="litres")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression", "api")
@allure.title("Личный кабинет: Добавление в корзину")
@allure.description(
    "Отправить запрос PUT_add_cart -> "
    "В полученном ответе:"
    " - проверить, что статус код = 200,"
    " - сверить с схемой put_add_cart.json,"
    " - проверить, что в ответе есть добавленный id")
def test_api_put_cart_add(api_session, helper_api):
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


@allure.epic("API")
@allure.feature("Личный кабинет")
@allure.story("Корзина")
@allure.link("https://www.litres.ru/", name="litres")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression", "api")
@allure.title("Личный кабинет: Удаление из корзины")
@allure.description(
    "Отправить запрос PUT_add_cart -> "
    "В полученном ответе:"
    " - проверить, что статус код = 204,"
    " - проверить, что в ответе есть добавленный id")
def test_api_put_cart_remove(api_session_add_cart, helper_api):
    with allure.step("Отправить запрос PUT_cart_remove"):
        api_session, book = api_session_add_cart
        response = helper_api.api_put_cart_remove(api_session, book.id)
    with allure.step("Проверить ответ"):
        helper_api.check_status_code(response, 204)

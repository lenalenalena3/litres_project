import allure
from allure_commons.types import Severity
from litres_project.pages.application import app


@allure.epic("WEB")
@allure.feature("Личный кабинет")
@allure.story("Корзина")
class TestCart:
    @allure.severity(Severity.CRITICAL)
    @allure.label("owner", "Tinkalyuk")
    @allure.tag("smoke", "regression")
    @allure.title("Личный кабинет: Добавление книги в корзину")
    @allure.description(
        "1. Открыть главную страницу \n"
        "2. Проверить, что корзина пустая \n"
        "3. Найти по поиску книгу \n"
        "4. Добавить книгу в корзину \n"
        "5. Проверить корзину")
    def test_add_cart(self, web_management):
        with allure.step("Открыть главную страницу"):
            app.menu_page.open_main_page()
        with allure.step("Проверить, что корзина пустая"):
            app.menu_page.open_cart()
            app.cart_page.should_count_result(0)
        with allure.step("Найти по поиску книгу"):
            text_search = "Красная корова Барвицкая"
            app.menu_page.search_text(text_search)
        with allure.step("Добавить книгу в корзину"):
            index_book = 0
            book = app.search_page.open_info_book(index_book)
            app.menu_page.switch_tab()
            app.book_page.add_to_cart()
        with allure.step("Проверить корзину"):
            app.menu_page.open_cart()
            app.cart_page.should_cart_result_name(1, [book.name])

    @allure.severity(Severity.CRITICAL)
    @allure.label("owner", "Tinkalyuk")
    @allure.tag("smoke", "regression")
    @allure.title("Личный кабинет: Удаление книги из корзины")
    @allure.description(
        "Предусловие: в 'Корзине' есть две книги. \n"
        "1. Открыть главную страницу \n"
        "2. Открыть корзину \n"
        "3. Проверить корзину \n"
        "4. Удалить одну книгу \n "
        "5. Проверить корзину")
    def test_del_cart(self, web_management, api_session_add_cart):
        with allure.step("Открыть главную страницу"):
            api_session, book_del, book = api_session_add_cart
            app.menu_page.open_main_page()
            app.menu_page.refresh_cookies(api_session)
        with allure.step("Открыть корзину"):
            app.menu_page.open_cart()
        with allure.step("Проверить корзину"):
            list_book = []
            list_book.append(book_del.id)
            list_book.append(book.id)
            app.cart_page.should_cart_result_id(2, list_book)
        with allure.step("Удалить одну книгу"):
            index_book = 0
            app.cart_page.del_cart(index_book)
        with allure.step("Проверить корзину"):
            app.cart_page.should_cart_result_id(1, [book.id])

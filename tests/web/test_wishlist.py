import allure
from allure_commons.types import Severity
from litres_project.pages.application import app
from litres_project.utils.cookie_utils import refresh_cookies


@allure.epic("WEB")
@allure.feature("Личный кабинет")
@allure.story("Список 'Отложено'")
class TestWishlist:
    @allure.severity(Severity.NORMAL)
    @allure.label("owner", "Tinkalyuk")
    @allure.tag("regression")
    @allure.title("WEB: Личный кабинет: Добавление книги в список 'Отложено'")
    @allure.description(
        "1. Открыть главную страницу \n"
        "2. Проверить, что список 'Отложено' пуст \n"
        "3. Найти по поиску книгу \n"
        "4. Добавить книгу в список 'Отложено' \n"
        "5. Проверить список 'Отложено'")
    def test_add_wishlist(self, web_management):
        with allure.step("Открыть главную страницу"):
            app.menu_page.open_main_page()
        with allure.step("Проверить, что список 'Отложено' пуст"):
            app.menu_page.open_my_books()
            app.favorite_page.open_favorite()
            app.favorite_page.should_count_result(0)
        with allure.step("Найти по поиску книгу"):
            text_search = "Красная корова Барвицкая"
            app.menu_page.search_text(text_search)
        with allure.step("Добавить книгу в список 'Отложено'"):
            index_book = 0
            book = app.search_page.add_favorite(index_book)
        with allure.step("Проверить список 'Отложено'"):
            app.menu_page.open_my_books()
            app.favorite_page.open_favorite()
            app.favorite_page.should_favorite_by_name(1, [book])

    @allure.severity(Severity.NORMAL)
    @allure.label("owner", "Tinkalyuk")
    @allure.tag("regression")
    @allure.title("WEB: Личный кабинет: Удаление книги из списка 'Отложено'")
    @allure.description(
        "Предусловие: в списке 'Отложено' есть две книги.\n"
        "1. Открыть главную страницу \n"
        "2. Открыть список 'Отложено' \n"
        "3. Проверить список 'Отложено' \n"
        "4. Удалить одну книгу \n"
        "5. Проверить список 'Отложено'")
    def test_del_wishlist(self, web_management, api_session_add_wishlist):
        with allure.step("Открыть главную страницу"):
            session, book, book_del = api_session_add_wishlist
            app.menu_page.open_main_page()
            refresh_cookies(session)
        with allure.step("Открыть список 'Отложено'"):
            app.menu_page.open_my_books()
            app.favorite_page.open_favorite()
        with allure.step("Проверить список 'Отложено'"):
            list_book = []
            list_book.append(book_del)
            list_book.append(book)
            app.favorite_page.should_favorite_by_id(2, list_book)
        with allure.step("Удалить одну книгу"):
            index_book = 0
            app.favorite_page.del_favorite(index_book)
        with allure.step("Проверить список 'Отложено'"):
            app.favorite_page.should_favorite_by_id(1, [book])

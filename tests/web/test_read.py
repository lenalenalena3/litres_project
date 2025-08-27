import allure
from allure_commons.types import Severity
from litres_project.pages.application import app
from litres_project.utils.resource import load_data_json


@allure.epic("WEB")
@allure.feature("Книжная страница")
@allure.story("Работоспособность кнопок")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression")
@allure.title("WEB: Книжная страница: Просмотр оглавления")
@allure.description(
    "1. Открыть главную страницу \n"
    "2. Найти по поиску книгу \n"
    "3. Открыть книгу \n"
    "4. Проверить оглавление")
def test_view_contents(web_management):
    with allure.step("Открыть главную страницу"):
        app.menu_page.open_main_page()
    with allure.step("Найти по поиску книгу"):
        text_search = "Алиса в стране чудес Льюис Кэрролл перевод Нина Демурова"
        app.menu_page.search_text(text_search)
    with allure.step("Открыть книгу"):
        index_book = 0
        app.search_page.open_info_book(index_book)
        app.menu_page.switch_tab()
    with allure.step("Проверить оглавление"):
        list_book = load_data_json('contents.json')
        contents = list_book['contents']
        app.book_page.should_contents(contents)

import allure
from allure_commons.types import Severity
from litres_project.pages.application import app


@allure.epic("WEB")
@allure.feature("Интерфейс")
@allure.story("Работа с поиском")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("smoke", "regression")
@allure.title("WEB: Главное меню: Проверка поиска")
@allure.description(
    "1. Открыть главную страницу \n"
    "2. Найти по поиску книгу \n"
    "3. Проверить результат поиска")
def test_search(web_management, search_data):
    with allure.step("Открыть главную страницу"):
        text_search = search_data['name']
        app.menu_page.open_main_page()
    with allure.step("Найти по поиску книгу"):
        app.menu_page.search_text(text_search)
    with allure.step("Проверить результат поиска"):
        app.search_page.should_search_result_name(text_search)

import allure
from allure_commons.types import Severity

from litres_project.pages.application import app


@allure.epic("WEB")
@allure.feature("Интерфейс")
@allure.story("Работа с поиском")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("smoke", "regression")
@allure.title("Главное меню: Проверка поиска")
@allure.description("Открыть главную страницу -> Найти по поиску книгу -> Проверить результат поиска")
def test_search(setup_browser, search_data):
    with allure.step("Открыть главную страницу"):
        text = search_data['name']
        app.menu_page.open_main_page()
    with allure.step("Найти по поиску книгу"):
        app.menu_page.search_text(text)
    with allure.step("Проверить результат поиска"):
        app.search_page.should_search_result_name(text)

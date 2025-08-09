import allure
from allure_commons.types import Severity

from litres_project.pages.application import app


@allure.epic("Пользовательские взаимодействия")
@allure.feature("Работа с поиском")
@allure.story("Успешный поиск существующего товара")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("smoke", "regression")
@allure.title("Главное меню: Проверка поиска")
@allure.description("Открыть страницу -> Найти по поиску книгу -> Проверить результат поиска")
def test_search(setup_browser, search_data):
    text = search_data['name']
    app.menu_page.open_main_page()
    app.menu_page.search_text(text)
    app.menu_page.should_search_result_name(text)

import allure
from allure_commons.types import Severity

from litres_project.pages.application import app


@allure.epic("Интерфейс")
@allure.feature("Навигация по сайту")
@allure.story("Главное меню")
@allure.link("https://www.litres.ru/", name="litres")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("smoke", "regression")
@allure.title("Главное меню: Проверка названий верхнего меню")
@allure.description("Открыть страницу -> проверить меню")
def test_should_menu(setup_browser):
    app.menu_page.open_main_page()
    app.menu_page.should_horizontal_menu()
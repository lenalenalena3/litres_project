import allure
from allure_commons.types import Severity
from litres_project.pages.application import app


@allure.epic("WEB")
@allure.feature("Интерфейс")
@allure.story("Главное меню")
@allure.link("https://www.litres.ru/", name="litres")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("smoke", "regression")
@allure.title("Главное меню: Проверка названий верхнего меню")
@allure.description("Открыть главную страницу -> Проверить верхнее меню")
def test_should_menu(web_management):
    with allure.step("Открыть главную страницу"):
        app.menu_page.open_main_page()
    with allure.step("Проверить верхнее меню"):
        app.menu_page.should_horizontal_menu()

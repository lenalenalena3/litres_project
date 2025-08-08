import allure
import pytest
from allure_commons.types import Severity

from litres_project.pages.application import app


@pytest.mark.skip(reason="Тест не доделан")
@allure.epic("Пользовательские взаимодействия")
@allure.feature("Книжная страница")
@allure.story("Работоспособность кнопок")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression")
@allure.title("Книжная страница: просмотр оглавления")
@allure.description("Открыть страницу -> поиск необходимой книги -> открыть книгу -> просмотреть оглавление")
def view_contents(setup_browser):
    app.menu_page.open_main_page()
    text = "Красная корова"
    app.menu_page.search_text(text)
    index_book = 0
    app.list_results_page.open_info_book(index_book)
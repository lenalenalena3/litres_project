import allure
from allure_commons.types import Severity

from litres_project.helpers.helper import verify_response_text
from litres_project.helpers.helper_api import api_get_suggestions



@allure.epic("Интерфейс")
@allure.feature("Навигация по сайту")
@allure.story("Проверка подсказок")
@allure.link("https://www.litres.ru/", name="litres")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression", "api")
@allure.title("API: Главное меню: Проверка подсказок для строки поиска")
@allure.description("Открытие страницы -> проверка подсказки для поля поиска")
def test_api_get_suggestions(api_session):
    text = 'сказки'
    response = api_get_suggestions(api_session, text)
    assert verify_response_text(response.json(), text) == True

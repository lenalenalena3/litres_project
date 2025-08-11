import allure
from allure_commons.types import Severity

from litres_project.helpers.helper import verify_response_text
from litres_project.helpers.helper_api import api_request, check_status_code, validate_schema


@allure.epic("API")
@allure.feature("Интерфейс")
@allure.story("Проверка подсказок")
@allure.link("https://www.litres.ru/", name="litres")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression", "api")
@allure.title("Главное меню: Проверка подсказок для строки поиска")
@allure.description(
    "Отправить запрос GET_suggestions -> "
    "В полученном ответе:"
    " - проверить статус код, "
    " - сверить с схемой get_list_suggestions.json,"
    " - проверить, что в каждой строки ответа содержится передаваемый текст")
def test_api_get_suggestions(api_session):
    with allure.step("Отправить запрос GET_suggestions"):
        text = 'сказки'
        endpoint = f"/search/suggestions"
        params = {'q': text}
        response = api_request(session=api_session, endpoint=endpoint, method="GET", params=params)
    with allure.step("Проверить ответ"):
        check_status_code(response, 200)
        validate_schema(response, 'get_list_suggestions.json')
        assert verify_response_text(response.json(), text) == True

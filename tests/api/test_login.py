import allure
from allure_commons.types import Severity


@allure.epic("API")
@allure.feature("Личный кабинет")
@allure.story("Авторизация")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression", "api")
@allure.title("API: POST_login_available: Авторизация: доступность логина: логин занят")
@allure.description(
    "1. Отправить запрос POST_login_available: \n "
    " - сверить с схемой запрос post_login_available_request.json,\n"
    " - отправить запрос post_login_available_request.json\n"
    "2. Проверить ответ:\n"
    " - проверить статус код,\n"
    " - сверить с схемой post_login-available.json,\n"
    " - проверить, что в строке ответа содержится available=false")
def test_api_post_login_available_false(api_session, helper_api):
    with allure.step("Отправить запрос POST login-available"):
        endpoint = f"/auth/login-available"
        payload = {"login": "lena7lena7lena7@icloud.com"}
        helper_api.validate_schema(payload, 'post_login_available_request.json')
        response = helper_api.request(session=api_session, endpoint=endpoint, method="POST", payload=payload)
    with allure.step("Проверить ответ"):
        helper_api.check_status_code(response, 200)
        helper_api.validate_schema(response, 'post_login_available.json')
        json_data = response.json()
        field = "available"
        with allure.step(f"Проверить в response: {field} = False"):
            assert json_data['payload']['data'][field] == False


@allure.epic("API")
@allure.feature("Личный кабинет")
@allure.story("Авторизация")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression", "api")
@allure.title("API: POST_login_available: Авторизация: доступность логина: логин свободен")
@allure.description(
    "1. Отправить запрос POST_login_available: \n "
    " - сверить с схемой запрос post_login_available_request.json,\n"
    " - отправить запрос post_login_available_request.json\n"
    "2. Проверить ответ:\n"
    " - проверить статус код,\n"
    " - сверить с схемой post_login-available.json,\n"
    " - проверить, что в строке ответа содержится available=true")
def test_api_post_login_available_true(api_session, helper_api):
    with allure.step("Отправить запрос POST login-available"):
        endpoint = f"/auth/login-available"
        payload = {"login": "1234567@icloud.com"}
        helper_api.validate_schema(payload, 'post_login_available_request.json')
        response = helper_api.request(session=api_session, endpoint=endpoint, method="POST", payload=payload)
    with allure.step("Проверить ответ"):
        helper_api.check_status_code(response, 200)
        helper_api.validate_schema(response, 'post_login_available.json')
        json_data = response.json()
        field = "available"
        with allure.step(f"Проверить в response: {field} = True"):
            assert json_data['payload']['data'][field] == True

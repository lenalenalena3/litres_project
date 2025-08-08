import json
import allure

from litres_project.utils import resource
from litres_project.utils.logging import response_logging, response_attaching
from jsonschema import validate

from tests.api.config import BASE_URL_API


@allure.step("api_request")
def api_request(session, base_api_url, endpoint, method, data=None, params=None):
    url = f"{base_api_url}{endpoint}"
    method = method.upper()
    if method == "POST":
        response = session.post(url, data=data, params=params)
    if method == "GET":
        response = session.get(url, params=params)
    if method == "PUT":
        response = session.put(url, data=data, params=params)
    if method == "DELETE":
        response = session.delete(url)
    response_logging(response)
    response_attaching(response)
    return response


@allure.step("GET: Получить список подсказок для {text} через API")
def api_get_suggestions(session, text):
    endpoint = f"/foundation/api/search/suggestions"
    params = {'q': text}
    response = api_request(session=session, base_api_url=BASE_URL_API, endpoint=endpoint, method="GET", params=params)
    assert response.status_code == 200
    with open(resource.path_schema("get_list_suggestions.json")) as file:
        schema = json.load(file)
        validate(response.json(), schema=schema)
    return response


@allure.step("PUT: добавить в избранное через API")
def api_put_add_favorite(session, id_book):
    endpoint = f"/foundation/api/wishlist/arts/{id_book}"
    response = api_request(session=session, base_api_url=BASE_URL_API, endpoint=endpoint, method="PUT")
    assert response.status_code == 204


@allure.step("DELETE: удалить из избранного через API")
def api_delete_del_favorite(session, id_book):
    endpoint = f"/foundation/api/wishlist/arts/{id_book}"
    response = api_request(session=session, base_api_url=BASE_URL_API, endpoint=endpoint, method="DELETE")
    assert response.status_code == 204

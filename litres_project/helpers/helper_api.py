import json
import allure

from litres_project.utils import resource
from litres_project.utils.logging import response_logging, response_attaching
from jsonschema import validate

class APIHelper:
    def __init__(self):
        self.settings = None

    def set_settings(self, settings):
        self.settings = settings

    @allure.step("api_request")
    def api_request(self, session, endpoint, method, payload=None, params=None):
        url = f"{self.settings.BASE_URL_API}{endpoint}"
        method = method.upper()
        headers = {"Content-Type": "application/json"}
        data = json.dumps(payload)
        if method == "POST":
            response = session.post(url, data=data, params=params, headers=headers)
        elif method == "GET":
            response = session.get(url, params=params)
        elif method == "PUT":
            response = session.put(url, data=data, params=params, headers=headers)
        elif method == "DELETE":
            response = session.delete(url, data=data, params=params)
        else:
            raise ValueError(f"Неподдерживаемый HTTP метод: {method}")
        response_logging(response)
        response_attaching(response)
        return response


    @allure.step("Сверить со схемой")
    def validate_schema(self, response, name_schema):
        with open(resource.path_schema(name_schema)) as file:
            schema = json.load(file)
            validate(response.json(), schema=schema)


    @allure.step("Проверить: response.status_code == {status_code}")
    def check_status_code(self,response, status_code):
        assert response.status_code == status_code, (
            f"Ожидалось status_code == {status_code}, получено {response.status_code}")


    @allure.step("PUT: wishlist для {id_book}")
    def api_put_wishlist(self, session, id_book):
        endpoint = f"/wishlist/arts/{id_book}"
        response = self.api_request(session=session, endpoint=endpoint, method="PUT")
        return response


    @allure.step("DELETE: wishlist для {id_book}")
    def api_delete_wishlist(self,session, id_book):
        endpoint = f"/wishlist/arts/{id_book}"
        response = self.api_request(session=session, endpoint=endpoint, method="DELETE")
        return response


    @allure.step("PUT: cart add для {id_book}")
    def api_put_cart_add(self,session, id_book):
        endpoint = f"/cart/arts/add"
        payload = {"art_ids": [id_book]}
        response = self.api_request(session=session, endpoint=endpoint, method="PUT", payload=payload)
        return response


    @allure.step("PUT: cart remove для {id_book}")
    def api_put_cart_remove(self,session, id_book):
        endpoint = f"/cart/arts/remove"
        payload = {"art_ids": [id_book]}
        response = self.api_request(session=session, endpoint=endpoint, method="PUT", payload=payload)
        return response


    # @allure.step("GET: status")
    # def api_get_status(self,session, field, count):
    #     endpoint = f"/users/me/arts/stats"
    #     response = self.api_request(session=session, endpoint=endpoint, method="GET")
    #     self.check_status_code(response, 200)
    #     self.validate_schema(response, 'get_status.json')
    #     json_data = response.json()
    #     with allure.step(f"Проверить в response: {field} == {count}"):
    #         assert json_data['payload']['data'][field] == count, \
    #             f"Ожидалось {count}, получено {json_data['payload']['data'][field]}"
    #
    #
    # @allure.step("POST: folders для {name_folders}")
    # def api_post_folders(self, session, name_folders):
    #     endpoint = "/users/me/folders"
    #     response = self.api_request(session=session, endpoint=endpoint, method="POST")
    #     self.check_status_code(response, 204)

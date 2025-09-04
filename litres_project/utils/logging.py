import logging
import json
import allure
from allure_commons.types import AttachmentType


def response_logging(response):
    logging.info("Request: " + response.request.url)
    if response.request.body:
        logging.info("INFO Request body: " + response.request.body)
    logging.info("Request headers: " + str(response.request.headers))
    logging.info("Response code " + str(response.status_code))
    logging.info("Response: " + response.text)


def response_attaching(response):
    allure.attach(
        body=response.request.url,
        name="Request url",
        attachment_type=AttachmentType.TEXT,
    )

    if response.request.body:
        allure.attach(
            body=json.dumps(response.request.body, indent=4, ensure_ascii=True),
            name="Request body",
            attachment_type=AttachmentType.JSON,
            extension="json",
        )
    try:
        json_data = response.json()
        allure.attach(
            body=json.dumps(json_data, indent=4, ensure_ascii=False),
            name="Response Json",
            attachment_type=AttachmentType.JSON,
            extension="json"
        )
    except json.JSONDecodeError:
        # Если JSON невалидный, сохраняем сырой ответ
        allure.attach(
            body=response.text or str(response.content),
            name="Response TEXT",
            attachment_type=AttachmentType.TEXT,
            extension="txt"
        )


def book_attaching(book, name_file: str = "Book"):
    allure.attach(
        body=str(book),
        name=name_file,
        attachment_type=allure.attachment_type.TEXT,
        extension=".txt"
    )


def current_url_attaching(current_url):
    allure.attach(
        body=current_url,
        name="Page URL",
        attachment_type=allure.attachment_type.TEXT,
        extension=".txt"
    )


def info_attaching(info, name_file: str = "info"):
    allure.attach(
        body=str(info),
        name=name_file,
        attachment_type=allure.attachment_type.TEXT,
        extension=".txt"
    )

import os

import allure
import requests
from selene import browser

def info_attaching(info, name_file: str = "info"):
    allure.attach(
        body=str(info),
        name=name_file,
        attachment_type=allure.attachment_type.TEXT
    )

def add_screenshot():
    png = browser.driver.get_screenshot_as_png()
    allure.attach(body=png, name='screenshot', attachment_type=allure.attachment_type.PNG)


def add_xml():
    xml = browser.driver.page_source
    allure.attach(body=xml, name='xml', attachment_type=allure.attachment_type.XML)


def add_bstack_video(session_id):
    bstack_session = requests.get(
        f'https://api.browserstack.com/app-automate/sessions/{session_id}.json',
        auth=(os.getenv('USER_NAME'), os.getenv('ACCESS_KEY')),
    ).json()
    print(bstack_session)
    video_url = bstack_session['automation_session']['video_url']

    allure.attach(
        '<html><body>'
        '<video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4">'
        '</video>'
        '</body></html>',
        name='video recording',
        attachment_type=allure.attachment_type.HTML,
    )

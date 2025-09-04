import allure
from selene import browser


def cookie_attaching(cookies_browser):
    try:
        cookies = {cookie['name']: cookie['value'] for cookie in cookies_browser}
        cookies_str = "\n".join([f"{name}: {value}" for name, value in cookies.items()])

        allure.attach(
            body=cookies_str,
            name="Session Cookies",
            attachment_type=allure.attachment_type.TEXT,
            extension=".txt"
        )
    except Exception as e:
        allure.attach(
            body=f"Failed to get cookies: {str(e)}",
            name="Cookies Error",
            attachment_type=allure.attachment_type.TEXT
        )

@allure.step("Обновить cookies")
def refresh_cookies(session):
    with allure.step(f"Session Cookies old"):
        cookie_attaching(browser.driver.get_cookies())
    browser.driver.delete_all_cookies()
    for name, value in session.cookies.get_dict().items():
        browser.driver.add_cookie({
            'name': name,
            'value': value,
            'domain': 'litres.ru',
            'path': '/',
            'secure': True
        })
    browser.driver.refresh()
    with allure.step(f"Session Cookies new"):
        cookie_attaching(browser.driver.get_cookies())
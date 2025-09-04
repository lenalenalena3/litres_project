import allure
from selene import browser
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait


#Проверить, есть ли более одной вкладки
def tab_more_one():
    try:
        WebDriverWait(browser.driver, 5).until(
            lambda d: len(d.window_handles) > 1
        )
        return True
    except TimeoutException:
        return False


@allure.step("Переключиться на новую вкладку")
def switch_tab():
    if tab_more_one():
        current_handles = browser.driver.window_handles
        browser.driver.switch_to.window(current_handles[-1])
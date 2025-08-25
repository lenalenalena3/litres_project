import allure
import pytest
import allure_commons
from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from dotenv import load_dotenv
from selene import browser, support, be

from appium import webdriver

from litres_project.utils import attach_mobile
from tests.mobile import config
from tests.mobile.config import get_settings


def pytest_addoption(parser):
    parser.addoption(
        "--context",
        default=None,
        help="Укажите файл настроек: local_emulator, bstack"
    )


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture
def context(request):
    return request.config.getoption("--context") or 'local_emulator'


@pytest.fixture(scope='function', autouse=True)
def mobile_management(request, context):
    settings = get_settings(context)
    options = config.driver_options(settings, context=context)
    browser.config.driver = webdriver.Remote(options.get_capability('remote_url'), options=options)
    browser.config.timeout = settings.TIMEOUT
    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )
    yield

    attach_mobile.add_screenshot()
    attach_mobile.add_xml()
    session_id = browser.driver.session_id

    with allure.step('tear down app session with id: ' + session_id):
        browser.quit()

    if context == 'bstack':
        attach_mobile.add_bstack_video(session_id)


@pytest.fixture(scope='function')
def open_app(mobile_management):
    with step('Выбираем язык для приложения'):
        browser.element((AppiumBy.ID, 'ru.litres.android:id/choosebutton')).should(be.clickable).click()
    with step('Закрываем окно о подписке'):
        browser.element((AppiumBy.ID, 'ru.litres.android:id/circleButtonSubscriptionPaywallClose')).should(
            be.clickable).click()

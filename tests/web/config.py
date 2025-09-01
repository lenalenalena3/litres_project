from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

from litres_project.utils.resource import abs_path_from_project
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options


class WebSettings(BaseSettings):
    BROWSER_NAME: str
    TIMEOUT: int
    BASE_URL: str
    BASE_URL_API: str

    def __init__(self, **kwargs):
        # Вывод информации перед загрузкой настроек
        env_file = self.model_config.get('env_file', '.env')
        abs_env_path = abs_path_from_project(env_file)
        print(f"\n[Конфигурация] Загружаем настройки из файла: {abs_env_path}")
        kwargs['_env_file'] = abs_env_path
        kwargs['_env_file_encoding'] = 'utf-8'
        super().__init__(**kwargs)

    model_config = SettingsConfigDict(
        env_file_encoding='utf-8',
        extra='ignore'
    )


class SelenoidSettings(WebSettings):
    BROWSER_VERSION: str
    SELENOID_URL: str
    model_config = SettingsConfigDict(
        env_file='.env.selenoid',
        env_file_encoding='utf-8',
        extra='ignore'
    )


class LocalSettings(WebSettings):
    model_config = SettingsConfigDict(
        env_file='.env.local_web',
        env_file_encoding='utf-8',
        extra='ignore'
    )


def get_settings(context: Literal["local_web", "selenoid"]) -> WebSettings:
    if context == "local_web":
        return LocalSettings()
    elif context == "selenoid":
        return SelenoidSettings()
    else:
        raise ValueError(f"Unknown context: {context}")


def driver_options(settings, context):
    if context == 'selenoid':
        options = FirefoxOptions() if settings.BROWSER_NAME.lower() == "firefox" else Options()
        selenoid_capabilities = {
            "browserName": settings.BROWSER_NAME,
            "browserVersion": settings.BROWSER_VERSION,
            "selenoid:options": {
                "enableLog": True,
                "enableVNC": True,
                "enableVideo": True,
                "screenResolution": "1280x1080"
            },
            "goog:loggingPrefs": {"browser": "ALL"},
        }
        if settings.BROWSER_NAME.lower() == "firefox":
            selenoid_capabilities["moz:firefoxOptions"] = {
                "log": {"level": "trace"},
                "prefs": {
                    "devtools.console.stdout.content": True,
                    "browser.console.showInPanel": True,
                    "dom.ipc.processCount": 8
                }
            }
        options.capabilities.update(selenoid_capabilities)
        print(options.to_capabilities())

    elif context == 'local_web':
        options = FirefoxOptions() if settings.BROWSER_NAME.lower() == "firefox" else Options()
        if settings.BROWSER_NAME.lower() == "firefox":
            options.set_preference("devtools.console.stdout.content", True)
            options.set_preference("browser.console.showInPanel", True)
    else:
        raise ValueError(f"Неизвестный контекст: {context}")
    return options

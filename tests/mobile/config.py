import os
from pathlib import Path

from appium.options.android import UiAutomator2Options
from typing import Literal
from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from litres_project.utils.resource import abs_path_from_project


class BaseAppSettings(BaseSettings):
    REMOTE_URL: str
    APP_ACTIVITY: str
    DEVICE_NAME: str
    UDID: str

    def __init__(self, **kwargs):
        # Вывод информации перед загрузкой настроек
        env_file = self.model_config.get('env_file', '.env')
        abs_env_path = abs_path_from_project(env_file)
        print(f"\n[Конфигурация] Загружаем настройки из файла: {abs_env_path}")
        print(f"[Конфигурация] Файл существует: {Path(abs_env_path).absolute().exists()}")
        kwargs['_env_file'] = abs_env_path
        kwargs['_env_file_encoding'] = 'utf-8'
        super().__init__(**kwargs)
        print("[Конфигурация] Настройки успешно загружены\n")

    model_config = SettingsConfigDict(
        env_file_encoding='utf-8',
        extra='ignore'
    )


class LocalEmulatorSettings(BaseAppSettings):
    APP: str

    @field_validator("APP")
    @classmethod
    def validate_app_file(cls, v: str) -> str:
        if not v.lower().endswith('.apk'):
            raise ValueError("Приложение должно быть в формате .apk")

        full_path = abs_path_from_project(v)
        if not Path(full_path).exists():
            raise ValueError(f"Файла APK не найдено: {full_path}")

        return full_path

    model_config = SettingsConfigDict(
        env_file='.env.local_emulator',
        env_file_encoding='utf-8',
        extra='ignore'
    )

class BrowserStackSettings(BaseAppSettings):
    APP: str
    PLATFORM_NAME: str
    PLATFORM_VERSION: str
    model_config = SettingsConfigDict(
        env_file='.env.bstack',
        env_file_encoding='utf-8',
        extra='ignore'
    )


def get_settings(context: Literal["local_emulator", "bstack"]) -> BaseAppSettings:
    if context == "local_emulator":
        return LocalEmulatorSettings()
    elif context == "bstack":
        return BrowserStackSettings()
    else:
        raise ValueError(f"Unknown context: {context}")


def driver_options(context: Literal["local_emulator", "bstack"]) -> UiAutomator2Options:
    settings = get_settings(context)
    options = UiAutomator2Options()

    options.set_capability('remote_url', settings.REMOTE_URL)
    options.set_capability('deviceName', settings.DEVICE_NAME)
    options.set_capability('udid', settings.UDID)
    options.set_capability('appActivity', settings.APP_ACTIVITY)

    if context in ("local_emulator", "local_real"):
        options.set_capability('app', abs_path_from_project(settings.APP))

    if context == 'bstack':
        credentials_path = abs_path_from_project('.env.credentials')
        print(f"Загружаем credentials из: {credentials_path}")
        if not Path(credentials_path).exists():
            raise FileNotFoundError(f"Файл .env.credentials не найден: {credentials_path}")
        load_dotenv(dotenv_path=credentials_path)
        bstack_userName = os.getenv('USER_NAME')
        bstack_accessKey = os.getenv('ACCESS_KEY')

        options.set_capability('platformName', settings.PLATFORM_NAME)
        options.set_capability('platformVersion', settings.PLATFORM_VERSION)
        options.set_capability('app', settings.APP)

        options.set_capability(
            'bstack:options', {
                'projectName': 'Wikipedia project',
                'buildName': 'browserstack-build-1',
                'sessionName': 'BStack test',
                'userName': bstack_userName,
                'accessKey': bstack_accessKey,
            },
        )

    return options

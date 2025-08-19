import os

USE_SELENOID = False
SELENOID_URL = os.getenv('SELENOID_URL', 'selenoid.autotests.cloud')
BROWSER_NAME = os.getenv('BROWSER_NAME', 'chrome')
BROWSER_VERSION = os.getenv('BROWSER_VERSION', '128.0')
TIMEOUT = os.getenv('TIMEOUT', '5')
BASE_URL = os.getenv('BASE_URL', 'https://www.litres.ru')


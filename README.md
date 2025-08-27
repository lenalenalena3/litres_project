# litres_project

<img src="images/litres_web.jpg" alt="Image litres_web" width="625"><img src="images/litres_mobile.jpg" alt="litres_mobile" width="200">

## Дипломный проект

Реализован во время обучения в Школе инженеров по автоматизации тестирования <a target="_blank" href="https://qa.guru">
qa.guru</a>

### Используемые технологии

<p  align="center">
    <code><img width="5%" title="PyCharm" src="images/pycharm.png"></code>
    <code><img width="5%" title="Python" src="images/python.png"></code>
    <code><img width="5%" title="Pytest" src="images/pytest.png"></code>
    <code><img width="5%" title="Requests" src="images/requests.png"></code>
    <code><img width="5%" title="Selene" src="images/selene.png"></code>
    <code><img width="5%" title="Selenium" src="images/selenium.png"></code>
    <code><img width="5%" title="Selenoid" src="images/selenoid.png"></code>
    <code><img width="5%" title="Appium" src="images/appium.png"></code>
    <code><img width="5%" title="Android Studio" src="images/android_studio.png"></code>
    <code><img width="5%" title="Browserstack" src="images/browserstack.png"></code>
    <code><img width="5%" title="Jenkins" src="images/jenkins.png"></code>
    <code><img width="5%" title="Allure Report" src="images/allure_report.png"></code>
    <code><img width="5%" title="Allure TestOps" src="images/allure_testops.png"></code>
    <code><img width="5%" title="Jira" src="images/jira.png"></code>
    <code><img width="5%" title="Telegram" src="images/tg.png"></code>
</p>


<!-- Тест кейсы -->
WEB:

* ✅ WEB: Главное меню: Проверка названий верхнего меню
* ✅ WEB: Главное меню: Проверка поиска
* ✅ WEB: Книжная страница: Просмотр оглавления
* ✅ WEB: Личный кабинет: Добавление книги в список 'Отложено'
* ✅ WEB: Личный кабинет: Удаление книги из списка 'Отложено'
* ✅ WEB: Личный кабинет: Добавление книги в корзину
* ✅ WEB: Личный кабинет: Удаление книги из корзины


API:

* ✅ API: GET_suggestions: Главное меню: Проверка подсказок для строки поиска
* ✅ API: PUT_wishlist: Личный кабинет: Добавление в список 'Отложено'
* ✅ API: DELETE_wishlist: Личный кабинет: Удаление из списка 'Отложено'
* ✅ API: DELETE_wishlist: Личный кабинет: Удаление из списка 'Отложено' несуществующей книги
* ✅ API: PUT_cart_add: Личный кабинет: Добавление в корзину
* ✅ API: PUT_cart_remove: Личный кабинет: Удаление из корзины
* ✅ API: POST_login_available: Авторизация: доступность логина: логин свободен
* ✅ API: POST_login_available: Авторизация: доступность логина: логин занят

Mobile:

* ✅ MOBILE: Личный кабинет: Добавление в избранное
* ✅ MOBILE: Главная страница: Проверка добавления/снятия признака 'Прочитана'
* ✅ MOBILE: Книжная страница: Просмотр оглавления


<!-- Jenkins -->

### <img width="3%" title="Jenkins" src="images/jenkins.png"> Запуск проекта в Jenkins
### [Задача в jenkins для WEB тестов](https://jenkins.autotests.cloud/job/guru20_homework22_web/)
Для запуска можно менять параметры:
![This is an image](images/jenkins_web.jpg)
### [Задача в jenkins для API тестов](https://jenkins.autotests.cloud/job/guru20_homework22_api/)
### [Задача в jenkins для Mobile тестов](https://jenkins.autotests.cloud/job/guru20_homework22_mob/)



<!-- Allure report -->

### <img width="3%" title="Allure Report" src="images/allure_report.png"> Allure report
WEB:
![This is an image](images/allure_web.jpg)
API:
![This is an image](images/allure_api.jpg)
Mobile:
![This is an image](images/allure_mobile.jpg)
<!-- Allure TestOps -->

### <img width="3%" title="Allure TestOps" src="images/allure_testops.png"> Интеграция с Allure TestOps
##### В Allure TestOps загружены тест-кейсы из Jenkins, а также добавлены ручные тесты
![This is an image](images/tests_allure_testops.jpg)
![This is an image](images/dashboards_allure_testops.jpg)

<!-- Jira -->

### <img width="3%" title="Jira" src="images/jira.png"> Интеграция с Jira

![This is an image](images/jira.jpg)

<!-- Telegram -->

### <img width="3%" title="Telegram" src="images/tg.png"> Оповещения в Telegram

##### После выполнения тестов, в Telegram bot приходит сообщение с графиком и информацией о тестовом прогоне.
<img src="images/bot_web_result.jpg" alt="This is an image" width="400">
<img src="images/bot_api_result.jpg" alt="This is an image" width="400">
<img src="images/bot_mobile_result.jpg" alt="This is an image" width="400">


## Видео запуска тестов
### <img src="images/selenoid.png" width="25" height="25" alt="Jenkins"/></a> Видео запуска WEB-теста в Selenoid
<p align="center">
<img title="Книжная страница: Просмотр оглавления" src="images/test_web.gif">
</p>

### <img src="images/browserstack.png" width="25" height="25" alt="Jenkins"/></a> Видео запуска MOBILE-теста в Browserstack
<p align="center">
<img title="Книжная страница: Просмотр оглавления" src="images/test_mobile.gif">
</p>




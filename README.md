# litres_project

litres_project

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
UI:

* ✅ Главное меню: Проверка названий верхнего меню
* ✅ Главное меню: Проверка поиска
* ✅ Книжная страница: Просмотр оглавления
* ✅ Личный кабинет: Добавление книги в список 'Отложено'
* ✅ Личный кабинет: Удаление книги из списка 'Отложено'
* ✅ Личный кабинет: Добавление книги в корзину
* ✅ Личный кабинет: Удаление книги из корзины


API:

* ✅ Главное меню: Проверка подсказок для строки поиска
* ✅ Личный кабинет: Добавление в список 'Отложено'
* ✅ Личный кабинет: Удаление из списка 'Отложено'
* ✅ Личный кабинет: Удаление из списка 'Отложено' несуществующей книги
* ✅ Личный кабинет: Добавление в корзину
* ✅ Личный кабинет: Удаление из корзины

Mobile:

* ✅ Личный кабинет: Добавление в избранное
* ✅ Главная страница: Проверка добавления/снятия признака 'Прочитана'
* ✅ Книжная страница: Просмотр оглавления


<!-- Jenkins -->

### <img width="3%" title="Jenkins" src="images/jenkins.png"> Запуск проекта в Jenkins
### [Задача в jenkins для UI тестов](https://jenkins.autotests.cloud/job/guru20_homework22_web/)
### [Задача в jenkins для API тестов](https://jenkins.autotests.cloud/job/guru20_homework22_api/)
### [Задача в jenkins для Mobile тестов](https://jenkins.autotests.cloud/job/guru20_homework22_mob/)



<!-- Allure report -->

### <img width="3%" title="Allure Report" src="images/allure_report.png"> Allure report
UI:
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
### <img src="images/selenoid.png" width="25" height="25" alt="Jenkins"/></a> Видео запуска UI-тестов в Selenoid
<p align="Книжная страница: Просмотр оглавления" src="images/test_web.mp4">
</p>

### <img src="images/browserstack.png" width="25" height="25" alt="Jenkins"/></a> Видео запуска MOBILE-тестов в Browserstack
<p align="Книжная страница: Просмотр оглавления" src="images/test_mobile.mp4">
</p>




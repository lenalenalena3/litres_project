import allure
from allure_commons._allure import step
from allure_commons.types import Severity
from litres_project.pages.application_mobile import app_mobile
from litres_project.utils.resource import load_data_json

text = "Красная корова"


@allure.epic("MOBILE")
@allure.feature("Личный кабинет")
@allure.story("Список избранных книг")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression")
@allure.title("MOBILE: Личный кабинет: Добавление в избранное")
@allure.description(
    "1. Найти по поиску книгу \n"
    "2. Добавить книгу в список избранных \n"
    "3. Открыть список избранных книг\n"
    "4. Проверить список избранных книг")
def test_add_favorite(open_app):
    with step('Найти по поиску книгу'):
        app_mobile.search_page_mobile.search(text)
    with step('Добавить книгу в список избранных'):
        index = 0
        book = app_mobile.search_page_mobile.add_favorite(index)
    with step('Открыть список избранных книг'):
        app_mobile.favorite_page_mobile.open_favorite()
    with step(f'Проверить, что в списке есть книга {text}'):
        app_mobile.favorite_page_mobile.should_favorite_by_name(1, [book.name])


@allure.epic("MOBILE")
@allure.feature("Книжная страница")
@allure.story("Работоспособность кнопок")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression")
@allure.title("MOBILE: Книжная страница: Просмотр оглавления")
@allure.description(
    "1. Найти по поиску книгу \n"
    "2. Открыть книгу \n"
    "3. Проверить оглавление")
def test_open_contents(open_app):
    with step('Найти по поиску книгу'):
        app_mobile.search_page_mobile.search(text)
    with step('Открыть книгу'):
        index = 0
        app_mobile.search_page_mobile.open_book(index)
    with step('Проверить оглавление'):
        list_book = load_data_json('contents_red_cow.json')
        contents = list_book['contents']
        app_mobile.book_page_mobile.should_contents(contents)


@allure.epic("MOBILE")
@allure.feature("Главная страница")
@allure.story("Работоспособность кнопок")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Tinkalyuk")
@allure.tag("regression")
@allure.title("MOBILE: Главная страница: Проверка признака прочитана/не прочитана")
@allure.description(
    "1. Найти по поиску книгу \n"
    "2. Отметить книгу прочитанной \n"
    "3. Проверить появление признака 'Прочитана' \n"
    "4. Отметить книгу непрочитанной \n"
    "5. Проверить скрытие признака 'Прочитана'")
def test_mark_read(open_app):
    with step('Найти по поиску книгу'):
        app_mobile.search_page_mobile.search(text)
    with step('Отметить книгу прочитанной'):
        index = 0
        app_mobile.search_page_mobile.mark_read(index)
    with step('Проверить, что книга прочитана'):
        assert app_mobile.search_page_mobile.check_mark_read(index, visible=True) == True
    with step('Отметить книгу не прочитанной'):
        app_mobile.search_page_mobile.mark_read(index)
    with step('Проверить, что книга не прочитана'):
        assert app_mobile.search_page_mobile.check_mark_read(index, visible=False) == True

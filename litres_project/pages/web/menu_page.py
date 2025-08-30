import allure
from selene import browser, have, be, query
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from pytest_check import check

from litres_project.utils.logging import info_attaching, current_url_attaching, cookie_attaching


class MenuPage:
    def __init__(self):
        self._menu = browser.element('#lowerMenuWrap')
        self._menu_elements = self._menu.all('[data-testid*="lowerMenu__item"][aria-hidden="false"]')
        self._menu_dop = self._menu.element('[data-testid*="lower-menu__more-button"] > a')
        self._menu_dop_elements = self._menu.all('[data-testid*="lowerMenu_moreItem"] > div')
        self._search = browser.element('//form[@action="/search/"]')
        self._search_input = self._search.element('.//input')
        self._search_elements = browser.all('[data-testid="search__content--wrapper"] > div')
        self._cart = browser.element('[data-testid="tab-basket"] > a')
        self._my_books = browser.element('[data-testid="tab-myBooks"] > a')

    def add_favorite(self, index):
        self._search_elements.element(index).element('./a').should(be.visible).get(query.attribute('aria-label'))

    @allure.step("Открыть главную страницу")
    def open_main_page(self):
        browser.open('/')
        current_url_attaching(browser.driver.current_url)

    @allure.step("На главной странице в верхнем меню кликнуть на кнопку 'Мои книги'")
    def open_my_books(self):
        self._my_books.should(be.visible).click()

    @allure.step("На главной странице в верхнем меню кликнуть на кнопку 'Корзина'")
    def open_cart(self):
        self._cart.should(be.visible).click()

    @allure.step("Проверить главное меню")
    def should_horizontal_menu(self):
        list_menu = ['Подписка за 0 ₽',
                     'Промокод',
                     'Новинки',
                     'Популярное',
                     'Подборки',
                     'Аудиокниги',
                     'Эксклюзивы',
                     'Черновики',
                     'Лекции',
                     'Комиксы и вебтуны',
                     'Журнал',
                     'Сертификаты',
                     'Партнёрская программа',
                     'Стать автором',
                     'Детская литература',
                     'Фанфики',
                     'Литрес Абонемент',
                     'Подкасты',
                     'Корпоративная библиотека',
                     'Литрес Чтец',
                     'Издать свою книгу',
                     'Мобильные приложения']
        list_menu_discounts = ['Подписка за 0 ₽',
                               'Промокод',
                               'Новинки',
                               'Популярное',
                               'Подборки',
                               'Аудиокниги',
                               'Эксклюзивы',
                               'Черновики',
                               'Скидки',
                               'Комиксы и вебтуны',
                               'Журнал',
                               'Сертификаты',
                               'Партнёрская программа',
                               'Стать автором',
                               'Детская литература',
                               'Фанфики',
                               'Литрес Абонемент',
                               'Лекции',
                               'Подкасты',
                               'Корпоративная библиотека',
                               'Литрес Чтец',
                               'Издать свою книгу',
                               'Мобильные приложения']

        actual_menu_texts = [element.get(query.text) for element in self._menu_elements]
        if 'Скидки' in actual_menu_texts:
            actual_list_menu = list_menu_discounts
        else:
            actual_list_menu = list_menu
        count_visible = len(self._menu_elements)
        count_hidden = len(actual_list_menu) - count_visible
        with allure.step("Проверить видимое меню {count_visible}"):
            actual_list_menu_visible = actual_list_menu[:count_visible]
            info_attaching(actual_list_menu_visible)
            with check:
                self._menu_elements.should(have.exact_texts(actual_list_menu_visible))
        with allure.step("Проверить скрытое меню {count_hidden}"):
            actual_list_menu_hidden = actual_list_menu[-count_hidden:]
            info_attaching(actual_list_menu_hidden)
            self._menu_dop.should(be.visible).click()
            with check:
                self._menu_dop_elements.should(have.exact_texts(actual_list_menu_hidden))

    @allure.step("На главной странице в строку поиска ввести {text}")
    def search_text(self, text):
        self._search_input.should(be.visible).type(text).press_enter()

    @allure.step("Обновить cookies")
    def refresh_cookies(self, session):
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

    def tab_more_one(self):
        try:
            WebDriverWait(browser.driver, 5).until(
                lambda d: len(d.window_handles) > 1
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Переключиться на новую вкладку")
    def switch_tab(self):
        if self.tab_more_one():
            current_handles = browser.driver.window_handles
            browser.driver.switch_to.window(current_handles[-1])

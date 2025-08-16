import allure
from selene import browser, query, be
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from litres_project.helpers.helper import extract_book_id
from litres_project.models.book_model import Book
from litres_project.utils.logging import info_attaching


class SearchPage:
    def __init__(self):
        self._search_list_elements = browser.all('[data-testid="search__content--wrapper"] > div')

    def get_field_text_book(self, index, field):
        return self._search_list_elements.element(index).element(f'[data-testid*="{field}"').should(
            be.visible).get(query.text)

    def get_name_book(self, index):
        return self.get_field_text_book(index, 'title')

    def get_id_book(self, index):
        href = self._search_list_elements.element(index).element(f'[data-testid="art__title"').should(be.visible).get(query.attribute('href'))
        return extract_book_id(href)

    def get_info_book(self, index):
        book = Book()
        book.name = self.get_name_book(index)
        book.author = self.get_field_text_book(index, 'authorName')
        book.price = self.get_field_text_book(index, 'finalPrice')
        book.id = self.get_id_book(index)
        info_attaching(book, "Book")
        return book

    def check_not_favorite(self, index):
        return self._search_list_elements.element(index).element('.//button').should(be.visible).get(
            query.attribute('aria-label')) == "Отложить"

    @allure.step("Добавить в избранное товар с индексом {index}")
    def add_favorite(self, index):
        if self.check_not_favorite(index):
            self._search_list_elements.element(index).element('.//button').should(be.visible).click()
        return self.get_info_book(index)

    @allure.step("Открыть товар с индексом {index}")
    def open_info_book(self, index):
        self._search_list_elements.element(index).element('[data-testid="art__title"]').should(be.visible).click()
        return self.get_info_book(index)

    def get_count_result(self):
        try:
            WebDriverWait(self, 10).until(
                lambda _: self._search_list_elements.__len__() > 0
            )
            return self._search_list_elements.__len__()
        except TimeoutException:
            return 0

    @allure.step("Проверить результат поиска")
    def should_search_result_name(self, text):
        with allure.step("Проверить, что количество строк > 0"):
            actual_count = self.get_count_result()
            assert actual_count > 0
        with allure.step("Проверить, подходит ли название первого найденного элемента"):
            assert self.get_name_book(0) == text

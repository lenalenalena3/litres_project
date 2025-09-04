import allure
from selene import browser, query, be
from selenium.webdriver.support.wait import WebDriverWait

from litres_project.helpers.helper import extract_book_id
from litres_project.models.book_model import Book
from litres_project.utils.logging import info_attaching


class SearchPage:
    def __init__(self):
        self._list_search = browser.all('[data-testid="search__content--wrapper"] > div')

    def get_book_field_text(self, index, field):
        return self._list_search.element(index).element(f'[data-testid*="{field}"').should(
            be.visible).get(query.text)

    def get_book_name(self, index):
        return self.get_book_field_text(index, 'title')

    def get_book_info(self, index):
        book = Book()
        book.name = self.get_book_name(index)
        book.author = self.get_book_field_text(index, 'authorName')
        book.price = self.get_book_field_text(index, 'finalPrice')
        book.id = extract_book_id(
            self._list_search.element(index).element(f'[data-testid="art__title"').should(be.visible).get(
                query.attribute('href')))
        info_attaching(book, "Book")
        return book

    @allure.step("Добавить в избранное товар с индексом {index}")
    def add_favorite(self, index):
        self._list_search.element(index).element('.//button').should(be.clickable).click()
        return self.get_book_info(index)

    @allure.step("Открыть товар с индексом {index}")
    def open_info_book(self, index):
        self._list_search.element(index).element('[data-testid="art__title"]').should(be.clickable).click()
        return self.get_book_info(index)

    @allure.step("Проверить результат поиска")
    def should_search_by_name(self, text):
        with allure.step("Проверить, что количество строк > 0"):
            try:
                WebDriverWait(self, 10).until(
                    lambda _: len(self._list_search) > 0
                )
            finally:
                actual_count = len(self._list_search)
            assert actual_count > 0, f"В результате поиска нет данных"

        with allure.step("Проверить, подходит ли название первого найденного элемента"):
            assert self.get_book_name(0) == text

import allure
from selene import browser, be, query
from selenium.webdriver.support.wait import WebDriverWait

from litres_project.helpers.helper import extract_book_id
from litres_project.models.book_model import Book
from litres_project.utils.logging import info_attaching


class FavoritePage:
    def __init__(self):
        self._favorite_list_elements = browser.all('[data-testid="art__wrapper"]')
        self._favorite = browser.element('//*[@data-testid="icon_wishlist"]/parent::*')
        self._favorite_count = self._favorite.element(
            './following-sibling::span[@data-testid="navigation__tabItem__counter"]')
        self._context_menu = browser.element('[data-testid="overlay__container"]')
        self._del_favorite_context_menu = self._context_menu.element('[data-testid="icon_favorites"]')

    def get_field_book(self, index, field):
        return self._favorite_list_elements.element(index).element(f'[data-testid*="{field}"').should(
            be.visible).get(query.text)

    def get_name_book(self, index):
        return self.get_field_book(index, 'title')

    def get_id_book(self, index):
        href = self._favorite_list_elements.element(index).element(f'[data-testid*="title"').should(
            be.visible).get(query.attribute('href'))
        return extract_book_id(href)

    def get_info_book(self, index):
        book = Book()
        book.name = self.get_name_book(index)
        book.author = self.get_field_book(index, 'authorName')
        book.price = self.get_field_book(index, 'finalPrice')
        book.id = self.get_id_book(index)
        info_attaching(book, "Book")
        return book

    @allure.step("На странице 'Мои книги' выбрать вкладку 'Отложено'")
    def open_favorite(self):
        self._favorite.should(be.visible).click()

    @allure.step("На странице 'Мои книги' для книги {index} нажать на пункт меню 'Убрать из отложенного'")
    def del_favorite(self, index):
        self._favorite_list_elements.element(index).element('[aria-label="Меню"]').should(
            be.visible).click()
        self._del_favorite_context_menu.should(
            be.visible).click()
        return self.get_info_book(index)

    @allure.step("На странице 'Мои книги' проверить: количество книг ={count_book}")
    def should_count_result(self, count_book):
        try:
            WebDriverWait(self, 10).until(
                lambda _: len(self._favorite_list_elements) == count_book
            )
        finally:
            actual_count = len(self._favorite_list_elements)
        assert actual_count == count_book, f"Несовпадение: {actual_count} != {count_book}"

    @allure.step("На странице 'Мои книги' проверить список книг по названию")
    def should_favorite_result_name(self, count_book, list_book):
        self.should_count_result(count_book)
        with (allure.step("Проверить названия книг")):
            for i in range(len(list_book)):
                assert self.get_name_book(i) == list_book[i], \
                    f"Несовпадение в элементе {i}: '{self.get_name_book(i)}' != '{list_book[i]}'"

    @allure.step("На странице 'Мои книги' проверить список книг по id")
    def should_favorite_result_id(self, count_book, list_book):
        self.should_count_result(count_book)
        with (allure.step("Проверить id книг")):
            for i in range(len(list_book)):
                self.get_info_book(i)
                assert self.get_id_book(i) == list_book[i], \
                    f"Несовпадение в элементе {i}: {self.get_id_book(i)} != {list_book[i]}"

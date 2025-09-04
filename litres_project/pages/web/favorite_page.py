import allure
from selene import browser, be, query
from selenium.webdriver.support.wait import WebDriverWait

from litres_project.helpers.helper import extract_book_id
from litres_project.models.book_model import Book
from litres_project.utils.logging import info_attaching


class FavoritePage:
    def __init__(self):
        self._list_favorites = browser.all('[data-testid="art__wrapper"]')
        self._favorite = browser.element('//*[@data-testid="icon_wishlist"]/parent::*')
        self._context_menu = browser.element('[data-testid="overlay__container"]')
        self._del_favorite_context_menu = self._context_menu.element('[data-testid="icon_favorites"]')

    def get_book_field(self, index, field):
        return self._list_favorites.element(index).element(f'[data-testid*="{field}"').should(
            be.visible).get(query.text)

    def get_book_info(self, index):
        book = Book()
        book.name = self.get_book_field(index, 'title')
        book.author = self.get_book_field(index, 'authorName')
        book.price = self.get_book_field(index, 'finalPrice')
        book.id = extract_book_id(self._list_favorites.element(index).element(f'[data-testid*="title"').should(
            be.visible).get(query.attribute('href')))
        info_attaching(book, "Book")
        return book

    @allure.step("На странице 'Мои книги' выбрать вкладку 'Отложено'")
    def open_favorite(self):
        self._favorite.should(be.clickable).click()

    @allure.step("На странице 'Мои книги' для книги {index} нажать на пункт меню 'Убрать из отложенного'")
    def delete_book_from_favorite(self, index):
        book = self.get_book_info(index)
        self._list_favorites.element(index).element('[aria-label="Меню"]').should(
            be.clickable).click()
        self._del_favorite_context_menu.should(
            be.clickable).click()
        return book

    @allure.step("На странице 'Мои книги' проверить: количество книг ={count_book}")
    def check_books_count(self, count_book):
        try:
            WebDriverWait(self, 10).until(
                lambda _: len(self._list_favorites) == count_book
            )
        finally:
            actual_count = len(self._list_favorites)
        assert actual_count == count_book, f"Несовпадение: {actual_count} != {count_book}"

    @allure.step("На странице 'Мои книги' проверить список книг по названию")
    def should_favorite_by_name(self, count_book, list_book):
        self.check_books_count(count_book)
        with (allure.step("Проверить названия книг")):
            for i in range(len(list_book)):
                actual_book = self.get_book_info(i)
                expected_book = list_book[i]
                assert actual_book.equals_by_name(expected_book), \
                    f"Несовпадение в элементе {i}: {actual_book.name} != {expected_book.name}"

    @allure.step("На странице 'Мои книги' проверить список книг по id")
    def should_favorite_by_id(self, count_book, list_book):
        self.check_books_count(count_book)
        with (allure.step("Проверить id книг")):
            for i in range(len(list_book)):
                actual_book = self.get_book_info(i)
                expected_book = list_book[i]
                assert actual_book.equals_by_id(expected_book), \
                    f"Несовпадение в элементе {i}: {actual_book.id} != {expected_book.id}"

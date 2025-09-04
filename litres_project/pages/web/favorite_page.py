import allure
from selene import browser, be, query
from selenium.webdriver.support.wait import WebDriverWait

from litres_project.helpers.helper import extract_book_id
from litres_project.models.book_model import Book, BookAttribute
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
            WebDriverWait(browser.driver, 10).until(
                lambda _: len(self._list_favorites) == count_book
            )
        finally:
            actual_count = len(self._list_favorites)
        assert actual_count == count_book, f"Несовпадение: {actual_count} != {count_book}"

    @allure.step("На странице 'Мои книги' проверить список книг")
    def should_have_books(self, count_book, list_book, attribute_name: BookAttribute):
        self.check_books_count(count_book)

        with allure.step(f"Проверить книги по {attribute_name}"):
            for i, expected_book in enumerate(list_book):
                actual_book = self.get_book_info(i)

                with allure.step(f"Проверить {attribute_name} книги {i}"):
                    assert actual_book.equals_by_attribute(expected_book, attribute_name.value), \
                        f"Несовпадение {attribute_name.value} в элементе {i}: " \
                        f"{getattr(actual_book, attribute_name.value)} != {getattr(expected_book, attribute_name.value)}"

import allure
from selene import browser, be, query
from selenium.webdriver.support.wait import WebDriverWait

from litres_project.helpers.helper import extract_book_id
from litres_project.models.book_model import Book
from litres_project.utils.logging import info_attaching


class CartPage:
    def __init__(self):
        self._list_cart = browser.all('[data-testid*="cart__listItem"]')
        self._cart_favorite_context_menu = browser.element('//*[@data-testid="cart__modalDeleteArt"]//button')

    def get_field_book(self, index, field):
        return self._list_cart.element(index).element(f'[data-testid*="cart__{field}"]').should(
            be.visible).get(query.text)

    def get_info_book(self, index):
        book = Book()
        book.name = self.get_field_book(index, 'bookCardTitle')
        book.author = self.get_field_book(index, 'bookCardAuthor')
        book.price = self.get_field_book(index, 'bookCardDiscount')
        book.id = extract_book_id(
            self._list_cart.element(index).element(f'[data-testid*="cart__bookCardTitle"]> a').should(
                be.visible).get(query.attribute('href')))
        info_attaching(book, "Book")
        return book

    @allure.step("На странице 'Корзина' проверить количество товаров")
    def should_count_result(self, count_book):
        try:
            WebDriverWait(self, 10).until(
                lambda _: len(self._list_cart) == count_book
            )
        finally:
            actual_count = len(self._list_cart)
        assert actual_count == count_book, \
            f"Несовпадение: {actual_count} != {count_book}"

    @allure.step("На странице 'Корзина' проверить список книг по id")
    def should_cart_by_id(self, count_book, list_book):
        self.should_count_result(count_book)
        with (allure.step("Проверить id книг")):
            for i in range(len(list_book)):
                actual_book = self.get_info_book(i)
                expected_book = list_book[i]
                assert actual_book.equals_by_id(expected_book), \
                    f"Несовпадение в элементе {i}: {actual_book.id} != {expected_book.id}"

    @allure.step("На странице 'Корзина' проверить список книг по названию")
    def should_cart_by_name(self, count_book, list_book):
        self.should_count_result(count_book)
        with (allure.step("Проверить названия книг")):
            for i in range(len(list_book)):
                actual_book = self.get_info_book(i)
                expected_book = list_book[i]
                assert actual_book.equals_by_name(expected_book), \
                    f"Несовпадение в элементе {i}: {actual_book.name} != {expected_book.name}"

    @allure.step("На странице 'Корзина' для книги {index} нажать на кнопку 'Удалить'")
    def del_cart(self, index):
        book = self.get_info_book(index)
        self._list_cart.element(index).element('[data-testid="cart__listDeleteButton"]').should(
            be.clickable).click()
        self._cart_favorite_context_menu.should(be.clickable).click()
        return book

import allure
from selene import browser, be, query
from selenium.webdriver.support.wait import WebDriverWait

from litres_project.helpers.helper import extract_book_id
from litres_project.models.book_model import Book, BookAttribute
from litres_project.utils.logging import info_attaching


class CartPage:
    def __init__(self):
        self._list_cart = browser.all('[data-testid*="cart__listItem"]')
        self._cart_favorite_context_menu = browser.element('//*[@data-testid="cart__modalDeleteArt"]//button')

    def get_book_field(self, index, field):
        return self._list_cart.element(index).element(f'[data-testid*="cart__{field}"]').should(
            be.visible).get(query.text)

    def get_book_info(self, index):
        book = Book()
        book.name = self.get_book_field(index, 'bookCardTitle')
        book.author = self.get_book_field(index, 'bookCardAuthor')
        book.price = self.get_book_field(index, 'bookCardDiscount')
        book.id = extract_book_id(
            self._list_cart.element(index).element(f'[data-testid*="cart__bookCardTitle"]> a').should(
                be.visible).get(query.attribute('href')))
        info_attaching(book, "Book")
        return book

    @allure.step("На странице 'Корзина' проверить количество книг")
    def check_books_count(self, count_book):
        try:
            WebDriverWait(browser.driver, 10).until(
                lambda _: len(self._list_cart) == count_book
            )
        finally:
            actual_count = len(self._list_cart)
        assert actual_count == count_book, \
            f"Несовпадение: {actual_count} != {count_book}"

    @allure.step("На странице 'Корзина' проверить список книг")
    def should_have_books(self, count_book, list_book, attribute_name: BookAttribute):
        self.check_books_count(count_book)

        with allure.step(f"Проверить книги в корзине по {attribute_name}"):
            for i, expected_book in enumerate(list_book):
                actual_book = self.get_book_info(i)

                with allure.step(f"Проверить {attribute_name} книги {i}"):
                    assert actual_book.equals_by_attribute(expected_book, attribute_name.value), \
                        f"Несовпадение {attribute_name.value} в элементе {i}: " \
                        f"{getattr(actual_book, attribute_name.value)} != {getattr(expected_book, attribute_name.value)}"

    @allure.step("На странице 'Корзина' для книги {index} нажать на кнопку 'Удалить'")
    def delete_book_from_cart(self, index):
        book = self.get_book_info(index)
        self._list_cart.element(index).element('[data-testid="cart__listDeleteButton"]').should(
            be.clickable).click()
        self._cart_favorite_context_menu.should(be.clickable).click()
        return book

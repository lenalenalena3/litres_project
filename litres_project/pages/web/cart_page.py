import allure
from selene import browser, be, query
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from litres_project.helpers.helper import extract_book_id
from litres_project.models.book_model import Book
from litres_project.utils.logging import info_attaching


class CartPage:
    def __init__(self):
        self._cart_result_elements = browser.all(
            '//div[contains(@class, "Cart-module")][contains(@class, "content")]//div[contains(@data-testid,"cart__listItem")]')

    def get_name_book(self, index):
        return self._cart_result_elements.element(index).element(
            './/*[@data-testid="cart__bookCardTitle--wrapper"]').should(
            be.visible).get(query.text)

    def get_author_book(self, index):
        return self._cart_result_elements.element(index).element(
            './/*[@data-testid="cart__bookCardAuthor--wrapper"]').should(
            be.visible).get(query.text)

    def get_price_book(self, index):
        return self._cart_result_elements.element(index).element(
            './/*[@data-testid="cart__bookCardDiscount--wrapper"]').should(
            be.visible).get(query.text)

    def get_id_book(self, index):
        href = self._cart_result_elements.element(index).element(
            './/*[@data-testid="cart__bookCardTitle--wrapper"]/a').should(
            be.visible).get(
            query.attribute('href'))
        return extract_book_id(href)

    def get_info_book(self, index):
        book = Book()
        book.name = self.get_name_book(index)
        book.author = self.get_author_book(index)
        book.price = self.get_price_book(index)
        book.id = self.get_id_book(index)
        info_attaching(book, "Book")
        return book

    def get_count_result(self):
        try:
            WebDriverWait(self, 10).until(
                lambda _: self._cart_result_elements.__len__() > 0
            )
            return self._cart_result_elements.__len__()
        except TimeoutException:
            return 0

    @allure.step("На странице 'Корзина' проверить количество товаров")
    def should_count_result(self, count_book):
        actual_count = self.get_count_result()
        assert actual_count == count_book, \
            f"Несовпадение: {actual_count} != {count_book}"

    @allure.step("На странице 'Корзина' проверить список книг по id")
    def should_cart_result_id(self, count_book, list_book):
        self.should_count_result(count_book)
        with (allure.step("Проверить id книг")):
            for i in range(len(list_book)):
                assert self.get_id_book(i) == list_book[i], \
                    f"Несовпадение в элементе {i}: {self.get_id_book(i)} != {list_book[i]}"

    @allure.step("На странице 'Корзина' проверить список книг по названию")
    def should_cart_result_name(self, count_book, list_book):
        self.should_count_result(count_book)
        with (allure.step("Проверить названия книг")):
            for i in range(len(list_book)):
                assert self.get_name_book(i) == list_book[i], \
                    f"Несовпадение в элементе {i}: '{self.get_name_book(i)}' != '{list_book[i]}'"

    @allure.step("На странице 'Корзина' для книги {index} нажать на кнопку 'Удалить'")
    def del_favorite(self, index):
        self._cart_result_elements.element(index).element('.//button[@data-testid="cart__listDeleteButton"]').should(
            be.visible).click()
        browser.element("//div[@data-testid='cart__modalDeleteArt']//div[text()='Удалить']").should(be.visible).click()
        return self.get_info_book(index)

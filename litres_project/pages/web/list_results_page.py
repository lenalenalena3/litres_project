import allure
from selene import browser, query, be

from litres_project.models.book_model import Book
from litres_project.utils.logging import info_attaching


class ListResultsPage:
    def __init__(self):
        self._search_result_elements = browser.all('//*[@data-testid="search__content--wrapper"]/div')

    def get_name_book(self, index):
        return self._search_result_elements.element(index).element('.//a[@data-testid="art__title"]').should(
            be.visible).get(query.text)

    def get_author_book(self, index):
        return self._search_result_elements.element(index).element('.//a[@data-testid="art__authorName"]').should(
            be.visible).get(query.text)

    def get_price_book(self, index):
        return self._search_result_elements.element(index).element('.//div[@data-testid="art__finalPrice"]').should(
            be.visible).get(query.text)

    def get_id_book(self, index):
        return self._search_result_elements.element(index).element('.//a[@data-testid="art__title"]').should(
            be.visible).get(query.attribute("href"))

    def get_info_book(self, index):
        book = Book()
        book.name = self.get_name_book(index)
        book.author = self.get_author_book(index)
        book.price = self.get_price_book(index)
        book.id = self.get_id_book(index)
        info_attaching(book, "Book")
        return book

    def check_not_favorite(self, index):
        return self._search_result_elements.element(index).element('.//button').should(be.visible).get(
            query.attribute('aria-label')) == "Отложить"

    @allure.step("Добавить в избранное товар с индексом {index}")
    def add_favorite(self, index):
        if self.check_not_favorite(index):
            self._search_result_elements.element(index).element('.//button').should(be.visible).click()
        return self.get_info_book(index)

    @allure.step("Открыть товар с индексом {index}")
    def open_info_book(self, index):
        self._search_result_elements.element(index).element('.//a[@data-testid="art__title"]').click()
        return self.get_info_book(index)

import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, be, query

from litres_project.models.book_model import Book
from litres_project.utils.attach_mobile import info_attaching


class SearchPageMobile:
    def __init__(self):
        self._search_button = browser.element((AppiumBy.ID, 'ru.litres.android:id/nav_search'))
        self._search_input = browser.element((AppiumBy.ID, 'ru.litres.android:id/et_search_query'))
        self._results_books = browser.all((AppiumBy.XPATH,
                                           '//android.view.ViewGroup[@resource-id="ru.litres.android:id/clArtLayout"]'))

    @allure.step("В поисковой строке ввести {text}")
    def search(self, text):
        self._search_button.should(be.visible).click()
        text = "Красная корова"
        self._search_input.should(be.visible).send_keys(text)
        browser.driver.press_keycode(66)

    def open_book(self, index_book):
        self._results_books.element(index=index_book).click()

    def add_favorite(self, index_book):
        book = Book()
        self._results_books.element(index=index_book).element((AppiumBy.XPATH,'//android.widget.ImageView[@resource-id="ru.litres.android:id/imageViewFavorite"]')).should(
            be.visible).click()
        book.name = self._results_books.element(index=index_book).element(
            (AppiumBy.XPATH, './/android.widget.TextView[@resource-id="ru.litres.android:id/textViewBookName"]')).get(
            query.text)
        book.author = self._results_books.element(index=index_book).element(
            (AppiumBy.XPATH, './/android.widget.TextView[@resource-id="ru.litres.android:id/textViewAuthor"]')).get(
            query.text)
        info_attaching(book, "Book")
        return book

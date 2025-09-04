import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, be, query
from selenium.common import NoSuchElementException, TimeoutException
from litres_project.models.book_model import Book
from litres_project.utils.attach_mobile import info_attaching


class SearchPageMobile:
    def __init__(self):
        self._search_button = browser.element((AppiumBy.ID, 'ru.litres.android:id/nav_search'))
        self._search_input = browser.element((AppiumBy.ID, 'ru.litres.android:id/et_search_query'))
        self._list_books = browser.all((AppiumBy.XPATH,
                                        '//android.view.ViewGroup[@resource-id="ru.litres.android:id/clArtLayout"]'))
        self._mark_read_button = browser.all(
            (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="android:id/title"]')).element(index=1)

    @allure.step("В поисковой строке ввести {text}")
    def search(self, text):
        self._search_button.should(be.clickable).click()
        self._search_input.should(be.visible).send_keys(text)
        browser.driver.press_keycode(66)

    def get_book_info(self, index_book):
        book = Book()
        book.name = self.get_book_field_text(index_book, 'textViewBookName')
        book.author = self.get_book_field_text(index_book, 'textViewAuthor')
        info_attaching(book, "Book")
        return book

    @allure.step("Открыть книгу с индексом {index_book} ")
    def open_book(self, index_book):
        self.get_book_info(index_book)
        self._list_books.element(index=index_book).click()

    def get_book_field_text(self, index_book, field):
        return self._list_books.element(index=index_book).element(
            (AppiumBy.XPATH, f'.//android.widget.TextView[@resource-id="ru.litres.android:id/{field}"]')).get(
            query.text)

    @allure.step("Добавить в избранное книгу с индексом {index_book} ")
    def add_favorite(self, index_book):
        self._list_books.element(index=index_book).element((AppiumBy.XPATH,
                                                            './/android.widget.ImageView[@resource-id="ru.litres.android:id/imageViewFavorite"]')).should(
            be.clickable).click()
        return self.get_book_info(index_book)

    @allure.step("Пометить книгу с индексом {index_book} как прочитанную")
    def mark_read(self, index_book):
        self.get_book_info(index_book)
        self._list_books.element(index=index_book).element(
            (AppiumBy.XPATH,
             './/android.widget.ImageView[@resource-id="ru.litres.android:id/imageTripleDots"]')).should(
            be.clickable).click()
        self._mark_read_button.should(be.clickable).click()

    @allure.step("Для книги {index_book} проверить признак 'прочитана' = {visible}")
    def check_mark_read(self, index_book, visible):
        timeout = 5
        mark_read_element = './/android.widget.TextView[@resource-id="ru.litres.android:id/textViewRead"]'
        try:
            if visible:
                self._list_books.element(index=index_book).element((AppiumBy.XPATH, mark_read_element)).with_(
                    timeout=timeout).should(be.visible)
            else:
                self._list_books.element(index=index_book).element((AppiumBy.XPATH, mark_read_element)).with_(
                    timeout=timeout).should(be.not_.visible)
            return True
        except (NoSuchElementException, TimeoutException):
            return False

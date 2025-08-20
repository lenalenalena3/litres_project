import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, be, query
from selenium.webdriver.support.wait import WebDriverWait


class FavoritePageMobile:
    def __init__(self):
        self._my_books_button = browser.element((AppiumBy.ID, 'ru.litres.android:id/nav_my_audiobooks'))
        self._favorite_button = browser.element((AppiumBy.XPATH,
                                                 '//android.widget.TextView[@resource-id="ru.litres.android:id/textViewBookSectionTitle" and @text="Favorites"]'))
        self._list_favorites = browser.all(
            (AppiumBy.XPATH, '//android.view.ViewGroup[@resource-id="ru.litres.android:id/clArtLayout"]'))

    @allure.step("Открыть список избранных книг")
    def open_favorite(self):
        self._my_books_button.should(be.visible).click()
        self._favorite_button.should(be.visible).click()

    @allure.step("Проверить количество книг в избранном")
    def should_count_result(self, count_book):
        try:
            WebDriverWait(self, 10).until(
                lambda _: len(self._list_favorites) == count_book
            )
        finally:
            actual_count = len(self._list_favorites)

        assert actual_count == count_book, f"Несовпадение количества книг в избранном: {actual_count} != {count_book}"
        return actual_count

    def get_name_book(self, index):
        return self._list_favorites.element(index).element(
            (AppiumBy.XPATH, '//android.widget.TextView[@resource-id,"ru.litres.android:id/textViewBookName"]')).should(
            be.visible).get(query.text)

    @allure.step("Проверить список книг в избранном по названию")
    def should_favorite_by_name(self, count_book, list_book):
        self.should_count_result(count_book)
        with (allure.step("Проверить названия книг")):
            for i in range(len(list_book)):
                assert self.get_name_book(i) == list_book[i], \
                    f"Несовпадение в элементе {i}: '{self.get_name_book(i)}' != '{list_book[i]}'"

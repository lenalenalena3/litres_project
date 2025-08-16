import allure
from selene import browser, be, query


class BookPage:
    def __init__(self):
        self._add_to_cart_button = browser.element('button[data-testid="book__addToCartButton"]')

        self._modal_windows_close = browser.element('//div[@id="dialogDesc"]//parent::div//div[@data-testid="icon_close"]')
        self._contents = browser.element(
            '//div[@data-testid="book__infoAboutBook--wrapper"]//button[@aria-haspopup="dialog"]')
        self._list_contents = browser.all('//div[contains(@class,"bookTableContent")][@role="list"]/div')

    def modal_window_visible(self):
        try:
            self._modal_windows_close.with_(timeout=10).should(be.visible)
            return True
        except:
            return False

    @allure.step("Нажать на кнопку 'Добавить в корзину'")
    def add_to_cart(self):
        self._add_to_cart_button.should(be.visible).click()
        if self.modal_window_visible():
            self._modal_windows_close.click()

    @allure.step("Проверить оглавление")
    def should_contents(self, list_book):
        self._contents.should(be.visible).click()
        count_list_actual = len(self._list_contents)
        count_list_expected = len(list_book)
        assert count_list_actual == count_list_expected, \
            f"Несовпадение количества строк: в интерфейсе {count_list_actual} != в файле {count_list_expected}"
        for i in range(count_list_actual):
            element_text = self._list_contents.element(i).get(query.text)
            assert element_text == list_book[i], \
                f"Несовпадение в элементе {i}: {element_text} != {list_book[i]}"

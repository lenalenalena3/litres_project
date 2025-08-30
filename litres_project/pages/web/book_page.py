import allure
from selene import browser, be, query


class BookPage:
    def __init__(self):
        self._add_to_cart_button = browser.element('button[data-testid="book__addToCartButton"]')
        self._modal_windows_action = browser.element('//*[@id="dialogDesc"]/parent::div')
        self._modal_windows_action_close = self._modal_windows_action.element('[data-testid="icon_close"]')
        self._contents = browser.element('[data-testid="book__infoAboutBook--wrapper"] button[aria-haspopup="dialog"]')
        self._list_contents = browser.all('[class*="bookTableContent"][role="list"] > div')

    def modal_window_visible(self):
        try:
            self._modal_windows_action.with_(timeout=10).should(be.visible)
            return True
        except AssertionError:
            return False

    @allure.step("Нажать на кнопку 'Добавить в корзину'")
    def add_to_cart(self):
        self._add_to_cart_button.should(be.clickable).click()
        if self.modal_window_visible():
            self._modal_windows_action_close.should(be.clickable).click()
            self._modal_windows_action.with_(timeout=5).should(be.not_.visible)

    @allure.step("Проверить оглавление")
    def should_contents(self, list_book):
        self._contents.should(be.clickable).click()
        count_list_actual = len(self._list_contents)
        count_list_expected = len(list_book)
        assert count_list_actual == count_list_expected, \
            f"Несовпадение количества строк: в интерфейсе {count_list_actual} != в файле {count_list_expected}"
        for i in range(count_list_actual):
            element_text = self._list_contents.element(i).get(query.text)
            assert element_text == list_book[i], \
                f"Несовпадение в элементе {i}: {element_text} != {list_book[i]}"

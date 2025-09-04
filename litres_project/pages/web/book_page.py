import allure
from selene import browser, be, query


class BookPage:
    def __init__(self):
        self._add_to_cart_button = browser.element('button[data-testid="book__addToCartButton"]')
        self._modal_windows_action = browser.element('//*[@id="dialogDesc"]/parent::div')
        self._modal_windows_action_close = self._modal_windows_action.element('[data-testid="icon_close"]')
        self._contents = browser.element('[data-testid="book__infoAboutBook--wrapper"] button[aria-haspopup="dialog"]')
        self._actual_content = browser.all('[class*="bookTableContent"][role="list"] > div')

    def is_modal_window_visible(self):
        try:
            self._modal_windows_action.with_(timeout=10).should(be.visible)
            return True
        except AssertionError:
            return False

    @allure.step("Нажать на кнопку 'Добавить в корзину'")
    def add_to_cart(self):
        self._add_to_cart_button.should(be.clickable).click()
        if self.is_modal_window_visible():
            self._modal_windows_action_close.should(be.clickable).click()
            self._modal_windows_action.with_(timeout=5).should(be.not_.visible)

    @allure.step("Проверить оглавление")
    def should_have_contents(self, expected_content):
        self._contents.should(be.clickable).click()
        actual_elements_count = len(self._actual_content)
        expected_elements_count = len(expected_content)
        assert actual_elements_count == expected_elements_count, \
            f"Несовпадение количества строк: в интерфейсе {actual_elements_count} != в файле {expected_elements_count}"
        for i in range(actual_elements_count):
            element_text = self._actual_content.element(i).get(query.text)
            assert element_text == expected_content[i], \
                f"Несовпадение в элементе {i}: {element_text} != {expected_content[i]}"

import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, be, query


class BookPageMobile:
    def __init__(self):
        self._open_contents_button = browser.element((AppiumBy.ID, 'ru.litres.android:id/textViewChaptersRowRoot'))
        self._list_contents = browser.all(
            (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="ru.litres.android:id/toc_title"]'))

    @allure.step("Проверить оглавление")
    def should_contents(self, list_book):
        browser.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                    'new UiScrollable(new UiSelector().scrollable(true))'
                                    '.scrollIntoView(new UiSelector().resourceId("ru.litres.android:id/textViewChaptersRowRoot"))')
        self._open_contents_button.should(be.clickable).click()
        count_list_actual = len(self._list_contents)
        count_list_expected = len(list_book)
        assert count_list_actual == count_list_expected, f"Несовпадение количества строк: в интерфейсе {count_list_actual} != в файле {count_list_expected}"
        for i in range(count_list_actual):
            element_text = self._list_contents.element(i).get(query.text)
            assert element_text == list_book[i], f"Несовпадение в элементе {i}: {element_text} != {list_book[i]}"

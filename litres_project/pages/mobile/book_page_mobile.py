import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, be, query


class BookPageMobile:
    def __init__(self):
        self._open_contents_button = browser.element((AppiumBy.ID, 'ru.litres.android:id/textViewChaptersRowRoot'))
        self._actual_content = browser.all(
            (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="ru.litres.android:id/toc_title"]'))

    @allure.step("Проверить оглавление")
    def should_have_contents(self, expected_content):
        browser.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                    'new UiScrollable(new UiSelector().scrollable(true))'
                                    '.scrollIntoView(new UiSelector().resourceId("ru.litres.android:id/textViewChaptersRowRoot"))')
        self._open_contents_button.should(be.clickable).click()
        actual_elements_count = len(self._actual_content)
        expected_elements_count = len(expected_content)
        assert actual_elements_count == expected_elements_count, f"Несовпадение количества строк: в интерфейсе {actual_elements_count} != в файле {expected_elements_count}"
        for i in range(actual_elements_count):
            element_text = self._actual_content.element(i).get(query.text)
            assert element_text == expected_content[
                i], f"Несовпадение в элементе {i}: {element_text} != {expected_content[i]}"

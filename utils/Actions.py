from selenium.common.exceptions import (ElementNotVisibleException, NoSuchElementException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import allure
from allure_commons.types import AttachmentType


class Actions:
    def wait(self, browser, time, how, what):
        try:
            WebDriverWait(browser, time).until(EC.visibility_of_element_located((how, what)))
        except TimeoutException:
            return False
        except ElementNotVisibleException:
            return False
        except NoSuchElementException:
            return False
        return True

    def clickable(self, browser, time, how, what):
        try:
            WebDriverWait(browser, time).until(EC.element_to_be_clickable((how, what)))
        except TimeoutException:
            return False
        except WebDriverException:
            return False
        except NoSuchElementException:
            return False
        except ElementNotVisibleException:
            return False
        return True

    def click(self, browser, obj):
        ActionChains(browser).click(obj).perform()

    def right_click(self, browser, obj):
        ActionChains(browser).context_click(obj).perform()

    def assert_wait(self, browser, time, how, what, message):
        self.wait(browser, time, how, what)
        if self.wait(browser, time, how, what) == False:
            allure.attach(browser.get_screenshot_as_png(), name="Failed step screenshot",
                          attachment_type=AttachmentType.PNG)
            assert False, f'{message}'

    def assert_clickable(self, browser, time, how, what, message):
        self.clickable(browser, time, how, what)
        if self.clickable(browser, time, how, what) == False:
            allure.attach(browser.get_screenshot_as_png(), name="Failed step screenshot",
                          attachment_type=AttachmentType.PNG)
            assert False, f'{message}'

    def scroll_to_element(self, browser, element):
        browser.execute_script("arguments[0].scrollIntoView();", element)

    def scroll_element_to_page_center(self, browser, element):
        browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def move_to_element(self, browser, element):
        ActionChains(browser).move_to_element(element).perform()

    def drag_and_drop(self, browser, el1, el2):
        ActionChains(browser).drag_and_drop(el1, el2).perform()

    def move_by_offset(self, browser, el, x, y):
        ActionChains(browser).move_to_element_with_offset(el, x, y).perform()

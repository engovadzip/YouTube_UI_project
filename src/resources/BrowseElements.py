from resources import Actions
from selenium.webdriver.common.keys import Keys

action = Actions.Actions()

class BrowseElements:
    def element(self, browser, how, what, element):
        action.assert_wait(browser, 5, how, what, f'Элемент {element} не найден.')
        el = browser.find_element(how, what)

        return el

    def elements(self, browser, how, what, elements):
        action.assert_wait(browser, 5, how, what, f'Элементы {elements} не найдены.')
        els = browser.find_elements(how, what)

        return els
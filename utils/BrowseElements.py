from utils import Actions

action = Actions.Actions()

class BrowseElements:
    def element(self, browser, how, what, element):
        action.assert_wait(browser, 5, how, what, f'Element "{element}" is not found.')
        el = browser.find_element(how, what)

        return el

    def elements(self, browser, how, what, elements):
        action.assert_wait(browser, 5, how, what, f'Elements "{elements}" are not found.')
        els = browser.find_elements(how, what)

        return els

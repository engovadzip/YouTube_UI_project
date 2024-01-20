from selenium.webdriver.common.by import By
from random import randint
from utils import Actions, BrowseElements

action = Actions.Actions()
browse = BrowseElements.BrowseElements()


class Locators:
    # Кнопка "Войти"
    LOGIN_XP = (By.XPATH, '//div[@id="buttons"]/ytd-button-renderer')

    # Строка поиска
    SEARCH_STRING_XP = (By.XPATH, '//input[@id="search"]')

    # Строка поиска
    SEARCH_BUTTON_XP = (By.XPATH, '//button[@id="search-icon-legacy"]')

    # Название видео в результатах поиска
    SEARCHED_VIDEO_TITLE_XP = (
    By.XPATH, '//yt-formatted-string[@class="style-scope ytd-video-renderer" and @aria-label]')


locator = Locators()


class Actions:
    def search_video(self, browser, search):
        search_string = browse.element(browser, *locator.SEARCH_STRING_XP, 'Search string')
        search_string.send_keys(f'{search}')

        search_button = browse.element(browser, *locator.SEARCH_BUTTON_XP, '"Search" button')
        search_button.click()

    def check_results(self, browser, search, component):
        search_results = browse.elements(browser, *locator.SEARCHED_VIDEO_TITLE_XP, f'{component}')
        correct_results = [el for el in search_results if search.lower() in el.text.lower()]

        assert len(correct_results) > 0, \
            (f'There are no "{search}" video among first {len(correct_results)} search results. '
             f'Try to use other keywords.')

    def collect_results(self, browser, search, component):
        self.check_results(browser, search, component)
        search_results = browse.elements(browser, *locator.SEARCHED_VIDEO_TITLE_XP, f'{component}')
        correct_results = [el for el in search_results if search.lower() in el.text.lower()]

        return correct_results

    def random_result(self, results):
        n = len(results)
        i = randint(0, n - 1)

        return results[i]

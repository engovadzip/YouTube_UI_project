from resources import Actions, BrowseElements
from selenium.webdriver.common.by import By

action = Actions.Actions()
browse = BrowseElements.BrowseElements()

class Locators:
    VIDEO_TITLE_XP = (By.XPATH, '//yt-formatted-string[@class="style-scope ytd-watch-metadata" and @force-default-style]')

locator = Locators()

class Actions:
    def open_searched_video(self, browser, video):
        searched_video_title = video.text
        action.scroll_to_element(browser, video)
        action.click(browser, video)

        action.assert_wait(browser, 5, *locator.VIDEO_TITLE_XP, f'Произошла ошибка при открытии видео "{searched_video_title}".')

        opened_video_title = browse.element(browser, *locator.VIDEO_TITLE_XP, 'Один из результатов поиска').text
        assert searched_video_title == opened_video_title, f'Названия найденного и открытого видео отличаются. Найденное видео: "{searched_video_title}", а открытое: "{opened_video_title}".'
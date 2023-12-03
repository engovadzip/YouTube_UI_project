from resources import Actions, BrowseElements
from selenium.webdriver.common.by import By
import time

action = Actions.Actions()
browse = BrowseElements.BrowseElements()

class Locators:
    VIDEO_TITLE_XP = (By.XPATH, '//yt-formatted-string[@class="style-scope ytd-watch-metadata" and @force-default-style]')

    VIDEO_WINDOW_CSS = (By.CSS_SELECTOR, '#player')

    YT_SHORTS_WINDOW_CSS = (By.CSS_SELECTOR, '[class="short-video-container style-scope ytd-reel-video-renderer"]')

    CURRENT_TIMELINE_CSS = (By.CSS_SELECTOR, '.ytp-left-controls div[class="ytp-time-display notranslate"] span .ytp-time-current')

    VIDEO_DURATION_CSS = (By.CSS_SELECTOR, '.ytp-left-controls div[class="ytp-time-display notranslate"] span .ytp-time-duration')

locator = Locators()

class Actions:
    def video_is_not_yt_shorts(self, browser):
        action.wait(browser, 1, *locator.YT_SHORTS_WINDOW_CSS)
        assert action.wait(browser, 1, *locator.YT_SHORTS_WINDOW_CSS) == False, 'Открытое видео является YouTube Shorts. Дальнейшее тестирование невозможно.'

    def duration_in_seconds(self, el):
        duration = list(map(int, el.split(':')))
        duration[-2] = duration[-2] * 60
        if len(duration) == 3:
            duration[-3] = duration[-3] * 3600
        duration = sum(duration)
        return duration

    def open_video(self, browser, video):
        video_title = video.text
        action.scroll_element_to_page_center(browser, video)
        action.click(browser, video)

        self.video_is_not_yt_shorts(browser)
        action.assert_wait(browser, 5, *locator.VIDEO_TITLE_XP, f'Произошла ошибка при открытии видео "{video_title}".')

        opened_video_title = browse.element(browser, *locator.VIDEO_TITLE_XP, 'Один из результатов поиска').text
        assert video_title == opened_video_title, f'Названия найденного и открытого видео отличаются. Найденное видео: "{video_title}", а открытое: "{opened_video_title}".'

    def check_video_playback(self, browser):
        self.video_is_not_yt_shorts(browser)
        video_window = browse.element(browser, *locator.VIDEO_WINDOW_CSS, 'Окно воспроизведения видео')
        action.move_to_element(browser, video_window)

        timeline_before = browse.element(browser, *locator.CURRENT_TIMELINE_CSS, 'Время воспроизведения')
        action.move_to_element(browser, timeline_before)

        timeline_before = browse.element(browser, *locator.CURRENT_TIMELINE_CSS, 'Время воспроизведения').text
        time.sleep(2)
        timeline_after = browse.element(browser, *locator.CURRENT_TIMELINE_CSS, 'Время воспроизведения').text

        assert timeline_before != timeline_after, f'Ошибка при воспроизведении видео. При открытии, видео было на "{timeline_before}", а через две секунды на "{timeline_after}".'
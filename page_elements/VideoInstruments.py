from utils import Actions, BrowseElements
from selenium.webdriver.common.by import By
import time

action = Actions.Actions()
browse = BrowseElements.BrowseElements()


class Locators:
    # Название видео под проигрывателем видео
    VIDEO_TITLE_XP = (
    By.XPATH, '//yt-formatted-string[@class="style-scope ytd-watch-metadata" and @force-default-style]')

    # Окно проигрывателя
    VIDEO_WINDOW_CSS = (By.CSS_SELECTOR, '#player')

    # Окно проигрывателя YouTube Shorts
    YT_SHORTS_WINDOW_CSS = (By.CSS_SELECTOR, '[class="short-video-container style-scope ytd-reel-video-renderer"]')

    # Текущее время воспроизведения видео (в проигрывателе)
    CURRENT_TIMELINE_CSS = (
    By.CSS_SELECTOR, '.ytp-left-controls div[class="ytp-time-display notranslate"] span .ytp-time-current')

    # Длительность видео (в проигрывателе)
    VIDEO_DURATION_CSS = (
    By.CSS_SELECTOR, '.ytp-left-controls div[class="ytp-time-display notranslate"] span .ytp-time-duration')

    # Шкала воспроизведения
    VIDEO_SCALE_CSS = (By.CSS_SELECTOR, '#player .ytp-chrome-bottom .ytp-progress-bar-container')


locator = Locators()


class Actions:
    def video_is_not_yt_shorts(self, browser):
        action.wait(browser, 0.5, *locator.YT_SHORTS_WINDOW_CSS)
        assert action.wait(browser, 0.5, *locator.YT_SHORTS_WINDOW_CSS) == False, \
            'An opened video is YouTube Shorts.'

    def duration_in_seconds(self, el):
        duration = list(map(int, el.split(':')))
        duration[-2] = duration[-2] * 60
        if len(duration) == 3:
            duration[-3] = duration[-3] * 3600
        duration = sum(duration)
        return duration

    def move_mouse_to_player(self, browser):
        self.video_is_not_yt_shorts(browser)
        video_window = browse.element(browser, *locator.VIDEO_WINDOW_CSS, 'Video player')
        action.move_to_element(browser, video_window)

    def open_video(self, browser, video):
        video_title = video.text
        action.scroll_element_to_page_center(browser, video)
        action.click(browser, video)

        self.video_is_not_yt_shorts(browser)
        action.assert_wait(browser, 5, *locator.VIDEO_TITLE_XP,
                           f'An error occurred when opening the video "{video_title}".')

        opened_video_title = browse.element(browser, *locator.VIDEO_TITLE_XP, 'One of the search results').text
        assert video_title == opened_video_title, \
            (f'The titles of the found and opened videos are different. '
             f'Found video: "{video_title}", opened video: "{opened_video_title}".')

    def check_video_playback(self, browser):
        self.move_mouse_to_player(browser)

        timeline_before = browse.element(browser, *locator.CURRENT_TIMELINE_CSS, 'Playback time')
        action.move_to_element(browser, timeline_before)

        timeline_before = browse.element(browser, *locator.CURRENT_TIMELINE_CSS, 'Playback time').text
        time.sleep(1)
        timeline_after = browse.element(browser, *locator.CURRENT_TIMELINE_CSS, 'Playback time').text

        video_duration = browse.element(browser, *locator.CURRENT_TIMELINE_CSS, 'Video duration').text
        if video_duration in ['0:00', '0:01']:
            pass
        else:
            assert timeline_before != timeline_after, \
                (f'Video playback error. '
                 f'When opening, the video was on {timeline_before} and one second later is on {timeline_after}.')

    def move_mouse_to_video_part(self, browser, element, part):
        timeline_before = browse.element(browser, *locator.CURRENT_TIMELINE_CSS, 'Playback time').text
        pixels = float(element.value_of_css_property('width').rstrip('px'))
        part = float(part)

        checked_part = (pixels * part) - (pixels * 0.5)

        timeline = action.move_by_offset(browser, element, checked_part, 0)
        action.click(browser, timeline)
        timeline_after = browse.element(browser, *locator.CURRENT_TIMELINE_CSS, 'Playback time').text

        after_sec = self.duration_in_seconds(timeline_after)

        duration = browse.element(browser, *locator.VIDEO_DURATION_CSS, 'Video duration').text
        duration_sec = self.duration_in_seconds(duration)

        if 0 <= duration_sec <= 2:
            pass

        elif part == 1:
            assert duration_sec - 5 <= after_sec <= duration_sec, \
                (f'An error occurred while rewinding the video to the end. '
                 f'The timeline after rewind is {timeline_after} and video duration is {duration}.')

        else:
            assert timeline_before != timeline_after, \
                (f'Video playback error. '
                 f'When opening, the video was on {timeline_before} and one second later on {timeline_after}.')

            timeline_sec = self.duration_in_seconds(timeline_after)

            final_part = timeline_sec / duration_sec
            final_part = round(final_part, 2)

            assert final_part - 0.01 <= part <= final_part + 0.01, \
                f'The {part} part of the video was transmitted to the test and the rewind was to {final_part} part.'

    def check_video_scale(self, browser, part):
        action.assert_wait(browser, 5, *locator.VIDEO_SCALE_CSS,
                           f'An error occurred while loading the video playback scale.')

        video_scale = browse.element(browser, *locator.VIDEO_SCALE_CSS, 'Video playback scale')

        action.move_to_element(browser, video_scale)

        self.move_mouse_to_video_part(browser, video_scale, part)
        if part != 1:
            self.check_video_playback(browser)

from utils import Actions
from page_elements import SearchInstruments, VideoInstruments
import allure

action = Actions.Actions()
locator = SearchInstruments.Locators()
search_action = SearchInstruments.Actions()
video_action = VideoInstruments.Actions()


@allure.story("Check YouTube video search and video playback")
def test_youtube_video_playback(browser, search, videopart):
    with allure.step("Open YouTube main page"):
        action.assert_wait(browser, 5, *locator.LOGIN_XP, "Main page doesn't open.")

    with allure.step(f'Input search request "{search}" in search string'):
        search_action.search_video(browser, search)

    with allure.step("Check that at least one video is found"):
        search_action.check_results(browser, search, 'Video in the search results')

    with allure.step("Open random video from search results"):
        videos = search_action.collect_results(browser, search, 'Video in the search results')
        video = search_action.random_result(videos)
        video_action.open_video(browser, video)

    with allure.step("Check video playback"):
        video_action.check_video_playback(browser)

    with allure.step("Check that video rewind is correct"):
        video_action.check_video_scale(browser, float(videopart))

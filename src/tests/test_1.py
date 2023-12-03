from resources import Actions
from page_elements import SearchInstruments, VideoInstruments
import allure
import time

action = Actions.Actions()
locator = SearchInstruments.Locators()
search_action = SearchInstruments.Actions()
video_action = VideoInstruments.Actions()

@allure.step("Открытие главной страницы YouTube")
def test_1_step_1(browser):
    action.assert_wait(browser, 5, *locator.LOGIN_XP, 'Страница не открылась.')

@allure.step("Ввод заданного текста в поисковую строку")
def test_1_step_2(browser):
    search_action.search_video(browser, 'Зубарев')

@allure.step("Поиск ролика с заданным названием среди результатов поиска")
def test_1_step_3(browser):
    search_action.check_results(browser, 'Зубарев', 'Видео в результатах поиска')

@allure.step("Переход к просмотру случайного ролика из подходящих результатов поиска")
def test_1_step_4(browser):
    videos = search_action.collect_results(browser, 'Зубарев', 'Видео в результатах поиска')
    video = search_action.random_result(videos)

    video_action.open_searched_video(browser, video)
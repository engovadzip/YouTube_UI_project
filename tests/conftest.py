from selenium import webdriver
import pytest
import allure
from allure_commons.types import AttachmentType


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='chrome')
    parser.addoption('--search', action='store', default='YouTube')
    parser.addoption('--videopart', action='store', default='0.33')

@pytest.fixture(scope='session', autouse=True)
def browser(link, request):
    browser_name = request.config.getoption("browser")

    if browser_name.lower() == 'chrome':
        browser = webdriver.Chrome()
    elif browser_name.lower() == 'firefox':
        browser = webdriver.Firefox()
    elif browser_name.lower() == 'edge':
        browser = webdriver.Edge()
    else:
        raise pytest.UsageError("Choose one of the following browsers: Chrome, Firefox or Edge.")

    browser.maximize_window()
    browser.get(link)

    yield browser
    allure.attach(browser.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
    browser.close()
    browser.quit()

@pytest.fixture(scope='session')
def link():
    link = 'https://www.youtube.com/'

    return link

@pytest.fixture(scope='session')
def videopart(request):
    videopart = request.config.getoption("videopart")
    if float(videopart) < 0 or float(videopart) > 1:
        raise pytest.UsageError("The part of video must be more than 0 and less than 1.")

    return videopart

@pytest.fixture(scope='session')
def search(request):
    search = request.config.getoption("search")

    return search
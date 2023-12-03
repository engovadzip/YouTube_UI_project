from selenium import webdriver
import pytest

def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='firefox')
    parser.addoption('--search', action='store', default='youtube')
    parser.addoption('--videopart', action='store', default='0.33')

@pytest.fixture(scope='session', autouse=True)
def browser(link, request):
    browser_name = request.config.getoption("browser")

    if browser_name  == 'chrome':
        browser = webdriver.Chrome()
    elif browser_name == 'firefox':
        browser = webdriver.Firefox()
    elif browser_name == 'edge':
        browser = webdriver.Edge()

    browser.maximize_window()
    browser.get(link)

    yield browser
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
        raise pytest.UsageError("The part of video must be more than 0 and less than 1!")

    return videopart

@pytest.fixture(scope='session')
def search(request):
    search = request.config.getoption("search")

    return search
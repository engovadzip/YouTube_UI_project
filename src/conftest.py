from selenium import webdriver
import pytest

def pytest_addoption(parser):
    parser.addoption('--search', action='store', default='youtube')

@pytest.fixture(scope='session', autouse=True)
def browser(link):
    browser = webdriver.Firefox()
    browser.maximize_window()
    browser.get(link)

    yield browser
    browser.close()
    browser.quit()

@pytest.fixture(scope='session')
def link():
    link = 'https://www.youtube.com/'

    return link
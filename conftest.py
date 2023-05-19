import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service
#


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")
    parser.addoption('--language', default = 'en')


@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("browser_name")
    user_language = request.config.getoption("language")

    browser = None
    if browser_name == "chrome":
        options = Options()
        print("\nstart chrome browser for test..")
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
        # разворачивает окно во весь экран
        options.add_argument('--start-maximized')
        #скрывает окно браузера
        options.add_argument('headless')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        browser = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        print("\nstart firefox browser for test..")
        options = FirefoxOptions()
        options.binary_location = r'/usr/local/bin/firefox'
        options.set_preference("intl.accept_languages", user_language)
        options.add_argument('--start-maximized')
        options.add_argument('headless')
        s = Service(r'/usr/local/bin/geckodriver')
        browser = webdriver.Firefox(service=s, options=options)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    yield browser
    browser.quit()
    print("\nquit browser..")


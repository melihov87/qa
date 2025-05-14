import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


detmir_url = "https://www.detmir.ru/"

cookie = {
    'name': 'DM_CookieNotification',
    'value': '0'
}


@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--incognito")
    options.add_argument("--window-size=1920,1080")
    # options.add_argument("--headless")  # Разкомментируй для headless
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(detmir_url)
    yield driver
    driver.quit()

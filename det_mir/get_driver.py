import pytest
import functools
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


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


def test_region_and_cookies(driver):
    """Во всплывающем окне Регион, кликаем по кнопке "Верно" и добавляем куки"""
    try:
        geo_click = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, './/span[contains(text(), "Верно!")]')))
        ActionChains(driver).pause(2).click(geo_click).perform()
        driver.add_cookie(cookie)
        driver.refresh()
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")

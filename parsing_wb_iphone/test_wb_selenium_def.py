import os
import ssl
import pandas as pd
from datetime import datetime
from price_chart_wb import generate_html_with_filters
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

ssl._create_default_https_context = ssl._create_unverified_context


# Дата запуска
TODAY = datetime.today().strftime('%Y-%m-%d %H:%M')

def driver():
    browser = uc.Chrome()
    browser.maximize_window()
    browser.get("https://www.wildberries.ru/")
    browser.implicitly_wait(15)
    return browser

def button(browser):
    menu_site = browser.find_element(By.CSS_SELECTOR, '[data-wba-header-name="Catalog"]')
    ActionChains(browser).move_to_element(menu_site).pause(2).click(menu_site).perform()

    el_menu = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-menu-id="4830"]'))
    )
    el_menu.click()

    tel_smart = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span[text()="Смартфоны и телефоны"]'))
    )
    tel_smart.click()

    smart_click = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[text()="Смартфоны"]'))
    )
    smart_click.click()

    filter_button = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Все фильтры")]'))
    )
    filter_button.click()

    apple_button = browser.find_element(By.XPATH, '//li[@class="filter__item"]/div/span[contains(text(), "Apple")]')
    ActionChains(browser).pause(1).move_to_element(apple_button).click().perform()

def product(browser):
    filename = 'wildberries_price_history.xlsx'

    show_button = browser.find_element(By.CLASS_NAME, 'filters-desktop__btn-main')
    ActionChains(browser).move_to_element(show_button).click(show_button).perform()

    for i in range(13):
        ActionChains(browser).pause(1).key_down(Keys.PAGE_DOWN).perform()

    product_cards = browser.find_elements(By.CLASS_NAME, 'product-card')

    new_data = []

    for card in product_cards:
        try:
            product_id = card.get_attribute('data-nm-id')  # Проверь название!
            brand = card.find_element(By.CLASS_NAME, 'product-card__brand').text.strip()
            name = card.find_element(By.CLASS_NAME, 'product-card__name').text.strip()
            price = card.find_element(By.CLASS_NAME, 'price__lower-price').text.strip().replace('₽', '').replace(' ', '')

            new_data.append({
                'ID': product_id,
                'Brand': brand,
                'Name': name,
                TODAY: int(price)
            })

        except Exception as e:
            print(f'Ошибка при обработке карточки: {e}')
            continue

    new_df = pd.DataFrame(new_data)
    new_df[['ID', 'Brand', 'Name']] = new_df[['ID', 'Brand', 'Name']].astype(str)

    if os.path.exists(filename):
        old_df = pd.read_excel(filename)
        old_df[['ID', 'Brand', 'Name']] = old_df[['ID', 'Brand', 'Name']].astype(str)
        merged_df = pd.merge(old_df, new_df, on=['ID', 'Brand', 'Name'], how='outer')
    else:
        merged_df = new_df

    merged_df.to_excel(filename, index=False)
    print(f"✅ Saved updated price history to '{filename}'")


def example():
    browser = driver()
    button(browser)
    product(browser)
    generate_html_with_filters()
    browser.quit()

example()

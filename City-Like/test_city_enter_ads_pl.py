import pytest
from playwright.sync_api import Playwright, sync_playwright, expect
from time import sleep


@pytest.fixture()
def browser_page(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://city-like.com")
    page.set_viewport_size({"width": 1600, "height": 1200})
    yield page
    browser.close()


def enter_auth_data(page):
    click_login = page.locator("p.name_p", has_text="Войдите, чтобы добавить")
    click_login.click()
    enter_email = page.locator("[name='username']")
    enter_email.fill("qwerty@example.com")
    enter_password1 = page.locator("[name='password']")
    enter_password1.fill("qqqqqqq1")
    page.locator('input[value="Войти"]').click()
    # Проверяем Title на странице "City-Like Главная Черногория"
    expect(page).to_have_title("City-Like Главная Черногория")


def click_ads(page):
    ads_category = page.locator("p.category-text", has_text="Куплю - продам")
    ads_category.click()


def title_comparison_ads(page, cat: str):
    ads_category = page.locator("p.category_text_body_first", has_text=cat)
    ads_category.click()
    # Проверяем, что вернулись на страницу "Транспорт"
    expect(page).to_have_title(cat)


def title_comparison_main(page):
    # Проверяем Title на странице "City-Like Главная Черногория"
    expect(page).to_have_title("City-Like Главная Черногория")


def add_ads(page, text: str):
    click_create_an_ad = page.locator('//a[contains(text(), "Создать объявление")]')
    click_create_an_ad.click()
    expect(page).to_have_title(text)


def test_click_buy_trans(browser_page):
    page = browser_page

    main(page, cat="Транспорт", text="Добавление авто")

    page.locator("#id_image1").set_input_files("../Desktop/Обработать/image.png")
    page.mouse.wheel(0, 500)
    page.select_option("#id_type", "auto")
    page.locator("#id_name").type("Автомобиль Renault Clio", delay=100)
    page.locator("#id_manufacturer").type("Renault", delay=100)
    page.locator("#id_model").type("Clio", delay=100)
    page.select_option("#id_fuel", "ДТ")
    page.select_option("#id_alldrive", "Передний")
    page.select_option("#id_bodytype", "Седан")
    page.locator("#id_volume").type("1,5", delay=100)
    page.locator("#id_power").type("150", delay=100)
    page.locator("#id_year").type("2024", delay=100)
    page.locator("#id_mileage").type("20000", delay=100)
    page.locator("#id_price").type("500", delay=100)
    page.mouse.wheel(0, 500)
    page.locator("#id_description").type("Быстрый и мощный автомобиль", delay=100)
    page.locator("#id_phone").type("+79993335577", delay=100)
    page.select_option("#id_city", "Podgorica")
    page.select_option("#id_condition", "БУ")
    page.locator("#id_telegram").type("qwertyuio", delay=100)
    page.mouse.wheel(0, 500)
    page.locator("#id_instagram").type("+79993335577", delay=100)
    page.locator("#id_facebook").type("+79993335577", delay=100)
    page.locator("#id_viber").type("+79993335577", delay=100)
    page.locator("#id_whatsapp").type("+79993335577", delay=100)
    page.locator("button[type='submit']").click()
    # Проверяем, что вернулись на страницу "Транспорт"
    expect(page).to_have_title("Транспорт")
    sleep(2)


def test_click_buy_elec(browser_page):
    page = browser_page

    main(page, cat="Электроника", text="Добавление электроники")

    page.locator("#id_image1").set_input_files("../Desktop/Обработать/image.png")
    page.mouse.wheel(0, 500)
    page.select_option("#id_type", "phones")
    page.locator("#id_name").type("Планшет", delay=100)
    page.locator("#id_model").type("QX500", delay=100)
    page.locator("#id_price").type("300", delay=100)
    page.mouse.wheel(0, 500)
    page.locator("#id_description").type("Быстрый и мощный планшет с большим экраном", delay=100)
    page.locator("#id_phone").type("+79993335577", delay=100)
    page.select_option("#id_city", "Podgorica")
    page.select_option("#id_condition", "БУ")
    page.locator("#id_telegram").type("qwertyuio", delay=100)
    page.locator("#id_instagram").type("+79993335577", delay=100)
    page.locator("#id_facebook").type("+79993335577", delay=100)
    page.locator("#id_viber").type("+79993335577", delay=100)
    page.locator("#id_whatsapp").type("+79993335577", delay=100)
    page.locator("button[type='submit']").click()
    # Проверяем, что вернулись на страницу "Электроника"
    expect(page).to_have_title("Электроника")
    sleep(2)


def test_click_buy_est(browser_page):
    page = browser_page

    main(page, cat="Недвижимость", text="Добавление недвижимости")

    page.locator("#id_image1").set_input_files("../Desktop/Обработать/image.png")
    page.mouse.wheel(0, 500)
    page.select_option("#id_type", "house")
    page.locator("#id_name").type("Красивый и большой дом", delay=100)
    page.locator("#id_area").type("532", delay=100)
    page.locator("#id_room").type("5", delay=100)
    page.locator("#id_floor").type("3", delay=100)
    page.locator("#id_price").type("500", delay=100)
    page.mouse.wheel(0, 500)
    page.locator("#id_description").type("Большой и удобный дом", delay=100)
    page.locator("#id_phone").type("+79993335577", delay=100)
    page.select_option("#id_city", "Podgorica")
    page.select_option("#id_condition", "БУ")
    page.locator("#id_telegram").type("qwertyuio", delay=100)
    page.mouse.wheel(0, 500)
    page.locator("#id_instagram").type("+79993335577", delay=100)
    page.locator("#id_facebook").type("+79993335577", delay=100)
    page.locator("#id_viber").type("+79993335577", delay=100)
    page.locator("#id_whatsapp").type("+79993335577", delay=100)
    page.locator("button[type='submit']").click()
    # Проверяем, что вернулись на страницу "Недвижимость"
    expect(page).to_have_title("Недвижимость")
    sleep(2)


def test_click_buy_things(browser_page):
    page = browser_page

    main(page, cat="Личные вещи", text="Добавление товара")

    page.locator("#id_image1").set_input_files("../Desktop/Обработать/image.png")
    page.select_option("#id_type", "women_clothing")
    page.locator("#id_name").type("Белая рубашка", delay=100)
    page.select_option("#id_condition", "БУ")
    page.locator("#id_price").type("500", delay=100)
    page.mouse.wheel(0, 500)
    page.locator("#id_description").type("Красивая рубашка", delay=100)
    page.locator("#id_phone").type("+79993335577", delay=100)
    page.select_option("#id_city", "Podgorica")
    page.locator("#id_telegram").type("qwertyuio", delay=100)
    page.locator("#id_instagram").type("+79993335577", delay=100)
    page.mouse.wheel(0, 500)
    page.locator("#id_facebook").type("+79993335577", delay=100)
    page.locator("#id_viber").type("+79993335577", delay=100)
    page.locator("#id_whatsapp").type("+79993335577", delay=100)
    page.locator("button[type='submit']").click()
    # Проверяем, что вернулись на страницу "Личные вещи"
    expect(page).to_have_title("Личные вещи")
    sleep(2)


def test_click_buy_hobby(browser_page):
    page = browser_page

    main(page, cat="Хобби и отдых", text="Добавление товара")

    page.locator("#id_image1").set_input_files("../Desktop/Обработать/image.png")
    page.select_option("#id_type", "bicycles")
    page.locator("#id_name").type("Велосипед 25 скоростей", delay=100)
    page.locator("#id_price").type("500", delay=100)
    page.mouse.wheel(0, 500)
    page.locator("#id_description").type("Красный", delay=100)
    page.locator("#id_phone").type("+79993335577", delay=100)
    page.select_option("#id_city", "Podgorica")
    page.select_option("#id_condition", "БУ")
    page.locator("#id_telegram").type("qwertyuio", delay=100)
    page.locator("#id_instagram").type("+79993335577", delay=100)
    page.mouse.wheel(0, 500)
    page.locator("#id_facebook").type("+79993335577", delay=100)
    page.locator("#id_viber").type("+79993335577", delay=100)
    page.locator("#id_whatsapp").type("+79993335577", delay=100)
    page.locator("button[type='submit']").click()
    # Проверяем, что вернулись на страницу "Хобби и отдых"
    expect(page).to_have_title("Хобби и отдых")
    sleep(2)


def test_click_buy_spare(browser_page):
    page = browser_page

    main(page, cat="Автозапчасти", text="Добавление товара")

    page.locator("#id_image1").set_input_files("../Desktop/Обработать/image.png")
    page.select_option("#id_type", "forauto")
    page.locator("#id_name").type("Пыльник для Ауди", delay=100)
    # Производитель
    page.locator("#id_brand").type("DOOO", delay=100)
    page.locator("#id_price").type("500", delay=100)
    page.mouse.wheel(0, 500)
    page.locator("#id_description").type("Универсальный", delay=100)
    page.locator("#id_phone").type("+79993335577", delay=100)
    page.select_option("#id_city", "Podgorica")
    page.select_option("#id_condition", "БУ")
    page.locator("#id_telegram").type("qwertyuio", delay=100)
    page.locator("#id_instagram").type("+79993335577", delay=100)
    page.mouse.wheel(0, 500)
    page.locator("#id_facebook").type("+79993335577", delay=100)
    page.locator("#id_viber").type("+79993335577", delay=100)
    page.locator("#id_whatsapp").type("+79993335577", delay=100)
    page.locator("button[type='submit']").click()
    # Проверяем, что вернулись на страницу "Автозапчасти"
    expect(page).to_have_title("Автозапчасти")
    sleep(2)


def main(page, cat: str, text: str):
    title_comparison_main(page)
    click_ads(page)
    title_comparison_ads(page, cat)
    enter_auth_data(page)
    click_ads(page)
    title_comparison_ads(page, cat)
    add_ads(page, text)


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
  

def test_click_buy(browser_page):
    page = browser_page  # Используем страницу из фикстуры
    click_shop = page.get_by_text("Магазины", exact=True)
    click_shop.click()

    sleep(2)
    assert page.title() == "Магазины"

    print("The test was passed successfully")


    click_party_time = page.get_by_text("Party Time").nth(1)
    click_party_time.click()
    sleep(2)

    page.mouse.wheel(0, 2000)

    # Для публикации объявления выпоняем вход
    click_login = page.locator("p.desc_p_com a")
    click_login.click(force=True)
    sleep(2)


    # Вводим данные для авторизации
    enter_email = page.locator("[name='username']")
    enter_email.fill("qwerty@example.com")
    enter_password1 = page.locator("[name='password']")
    enter_password1.fill("qwerty")
    page.locator('input[value="Войти"]').click()
  
    # # Если требуется регистрация
    # click_reg = page.locator("text=Зарегистрироваться").nth(0)
    # click_reg.click(force=True)
    # sleep(2)
    #
    # # Шаг 1: Заполнение email
    # enter_email = page.locator("[name='email']")
    # enter_email.fill("qwerty@example.com")
    # sleep(1)
    #
    # # Шаг 2: Заполнение номера телефона
    # enter_phone_number = page.locator("[name='phone_number']")
    # enter_phone_number.fill("+79994445578")
    # sleep(1)
    #
    # # Шаг 3: Заполнение никнейма
    # enter_nickname = page.locator("[name='nickname']")
    # enter_nickname.fill("qwerty")
    # sleep(1)
    #
    # # Шаг 4: Заполнение пароля
    # enter_password1 = page.locator("[name='password1']")
    # enter_password1.fill("qwerty")
    # sleep(1)
    #
    # # Шаг 5: Подтверждение пароля
    # enter_password2 = page.locator("[name='password2']")
    # enter_password2.fill("qwerty")
    # sleep(1)
    #
    # # Шаг 6: Подтверждение согласия с условиями
    # checkbox = page.locator("#termsCheckbox")
    # checkbox.click()
    # sleep(1)
    #
    # # Шаг 7: Нажатие на кнопку регистрации
    # reg_button = page.locator("#registerButton")
    # reg_button.click()
    # sleep(3)

    page = browser_page
    click_shop = page.get_by_text("Магазины", exact=True)
    click_shop.click()

    sleep(2)
    assert page.title() == "Магазины"

    print("The test was passed successfully")

    click_party_time = page.get_by_text("Party Time").nth(1)
    click_party_time.click()
    sleep(2)

    page.mouse.wheel(0, 1000)

    input_comment = page.locator("#id_text").fill('"A" * 10000')
    sleep(2)

    enter_com = page.locator("//button[contains(text(), 'Оставить комментарий')]")
    enter_com.click()

    sleep(3)

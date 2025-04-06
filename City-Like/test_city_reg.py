import pytest
from playwright.sync_api import Playwright, sync_playwright, expect
from time import sleep
import allure


@pytest.fixture()
def browser_page(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://city-like.com/myreg/register/")
    page.set_viewport_size({"width": 1600, "height": 1200})
    yield page
    # browser.close()


@allure.feature("Registration Form")
@allure.story("Filling Registration Form")
def test_filling_registration_form(browser_page):
    page = browser_page

    # Шаг 1: Заполнение email
    try:
        with allure.step("Enter email"):
            enter_email = page.locator("[name='email']")
            enter_email.fill("test5@example.com")
            sleep(1)
    except Exception as e:
        allure.attach(str(e), name="Step 1 Error", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"Error in Step 1: {e}")

    # Шаг 2: Заполнение номера телефона
    try:
        with allure.step("Enter phone number"):
            enter_phone_number = page.locator("[name='phone_number']")
            enter_phone_number.fill("+79994445575")
            sleep(1)
    except Exception as e:
        allure.attach(str(e), name="Step 2 Error", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"Error in Step 2: {e}")

    # Шаг 3: Заполнение никнейма
    try:
        with allure.step("Enter nickname"):
            enter_nickname = page.locator("[name='nickname']")
            enter_nickname.fill("example5")
            sleep(1)
    except Exception as e:
        allure.attach(str(e), name="Step 3 Error", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"Error in Step 3: {e}")

    # Шаг 4: Заполнение пароля
    try:
        with allure.step("Enter password"):
            enter_password1 = page.locator("[name='password1']")
            enter_password1.fill("qqqqqqq1")
            sleep(1)
    except Exception as e:
        allure.attach(str(e), name="Step 4 Error", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"Error in Step 4: {e}")

    # Шаг 5: Подтверждение пароля
    try:
        with allure.step("Confirm password"):
            enter_password2 = page.locator("[name='password2']")
            enter_password2.fill("qqqqqqq1")
            sleep(1)
    except Exception as e:
        allure.attach(str(e), name="Step 5 Error", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"Error in Step 5: {e}")

    # Шаг 6: Подтверждение согласия с условиями
    try:
        with allure.step("Click terms and conditions checkbox"):
            checkbox = page.locator("#termsCheckbox")
            checkbox.click()
            sleep(1)
    except Exception as e:
        allure.attach(str(e), name="Step 6 Error", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"Error in Step 6: {e}")

    # Шаг 7: Нажатие на кнопку регистрации
    try:
        with allure.step("Click register button"):
            reg_button = page.locator("#registerButton")
            reg_button.click()
            sleep(3)
    except Exception as e:
        allure.attach(str(e), name="Step 7 Error", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"Error in Step 7: {e}")

    # Шаг 8: Проверка результата
    try:
        with allure.step("Check if the URL matches"):
            expect(browser_page).to_have_url("https://city-like.com/")
    except Exception as e:
        allure.attach(str(e), name="Step 8 Error", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"Error in Step 8: {e}")


    sleep(3)

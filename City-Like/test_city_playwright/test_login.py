import allure
from playwright.sync_api import Page, expect
from locator import MAIN_PAGE, RECOVER_PASSWORD
from conftest import get_browser, login


@allure.feature("Авторизация")
@allure.story("Авторизация по email")
@allure.title("Авторизация по валидным данным email")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_email(page: Page):
    get_browser(page)
    with allure.step("Нажатие на кнопку Войти"):
        login(page).click()
    with allure.step("Ввод email и пароля"):
        enter_email = page.get_by_role("textbox", name="Email или номер телефона:")
        enter_email.type("city3@bk.ru", delay=100)
        enter_password = page.get_by_role("textbox", name="Пароль:")
        enter_password.type("Citylike2", delay=200)
    with allure.step("Нажатие на кнопку Войти"):
        page.get_by_role("button", name="Войти").click()
    with allure.step("Проверка перехода на главную страницу"):
        expect(page).to_have_url(MAIN_PAGE)


@allure.feature("Авторизация")
@allure.story("Авторизация по номеру телефона")
@allure.title("Авторизация по валидным данным phone")
@allure.severity(allure.severity_level.NORMAL)
def test_login_phone(page: Page):
    get_browser(page)
    with allure.step("Нажатие на кнопку Войти"):
        login(page).click()
    with allure.step("Ввод телефона и пароля"):
        enter_email = page.get_by_role("textbox", name="Email или номер телефона:")
        enter_email.type("+34567878990", delay=100)
        enter_password = page.get_by_role("textbox", name="Пароль:")
        enter_password.type("Citylike2", delay=200)
    with allure.step("Нажатие на кнопку Войти"):
        page.get_by_role("button", name="Войти").click()
    with allure.step("Проверка перехода на главную страницу"):
        assert page.url == MAIN_PAGE, f'Ошибка авторизации по номеру телефона'


@allure.feature("Авторизация")
@allure.story("Переход на главную со страницы логина")
@allure.title("Проверка кнопки перехода на главную страницу")
@allure.severity(allure.severity_level.MINOR)
def test_button_main_page_in_login(page: Page):
    get_browser(page)
    with allure.step("Переход на страницу входа"):
        login(page).click()
    with allure.step("Клик по ссылке 'Главную страницу'"):
        page.get_by_role("link", name="Главную страницу").click()
    with allure.step("Проверка перехода на главную страницу"):
        expect(page).to_have_url(MAIN_PAGE)


@allure.feature("Авторизация")
@allure.story("Переход на восстановление пароля")
@allure.title("Проверка кнопки перехода на страницу восстановления пароля")
@allure.severity(allure.severity_level.MINOR)
def test_button_recover_password_in_login(page: Page):
    get_browser(page)
    with allure.step("Переход на страницу входа"):
        login(page).click()
    with allure.step("Клик по ссылке 'Восстановить пароль'"):
        page.get_by_role("link", name="Восстановить пароль").click()
    with allure.step("Проверка перехода на страницу восстановления"):
        expect(page).to_have_url(RECOVER_PASSWORD)

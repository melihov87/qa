import allure
from playwright.sync_api import Page, expect
from locator import MAIN_PAGE, LOGIN_PAGE
from conftest import get_browser, login, registration


@allure.feature("Регистрация")
@allure.story("Успешная регистрация или сообщение об ошибке")
@allure.title("Регистрация пользователя с валидными данными")
@allure.severity(allure.severity_level.CRITICAL)
def test_registration(page: Page):
    with allure.step("Открытие браузера и переход на форму регистрации"):
        get_browser(page)
        login(page).click()
        registration(page).click()

    with allure.step("Заполнение формы регистрации"):
        page.get_by_role("textbox", name="Email: например: qwerty@gmail").type("city3@bk.ru", delay=100)
        page.get_by_role("textbox", name="Номер телефона, например: +").type("+34567878990", delay=100)
        page.get_by_role("textbox", name="Псевдоним, например: qwerty").type("city3", delay=100)
        page.get_by_role("textbox", name="Пароль: 8 символов и 1 цифру").type("Citylike2", delay=200)
        page.get_by_role("textbox", name="Подтвердите пароль").type("Citylike2", delay=200)
        page.get_by_role("checkbox", name="Я принимаю условия Пользовательского соглашения").check()

    with allure.step("Отправка формы регистрации"):
        page.get_by_role("button", name="Регистрация").click()

    with allure.step("Проверка успешной регистрации или отображения ошибки"):
        try:
            expect(page).to_have_url(MAIN_PAGE, timeout=5000)
        except:
            content = page.content()
            assert "уже существует" in content, \
                "Ожидаемый текст 'уже существует' не найден на странице после отправки формы"


@allure.feature("Регистрация")
@allure.story("Навигация")
@allure.title("Переход по ссылке 'Войти' на странице регистрации")
@allure.severity(allure.severity_level.NORMAL)
def test_button_login_in_reg(page: Page):
    with allure.step("Переход на форму регистрации"):
        get_browser(page)
        login(page).click()
        registration(page).click()

    with allure.step("Нажатие на ссылку 'Войти'"):
        page.get_by_role("link", name="Войти").click()

    with allure.step("Проверка перехода на страницу формы входа"):
        expect(page).to_have_url(LOGIN_PAGE, timeout=5000)


@allure.feature("Регистрация")
@allure.story("Навигация")
@allure.title("Переход по ссылке 'На главную' со страницы регистрации")
@allure.severity(allure.severity_level.NORMAL)
def test_button_main_page_in_reg(page: Page):
    with allure.step("Переход на форму регистрации"):
        get_browser(page)
        login(page).click()
        registration(page).click()

    with allure.step("Нажатие на ссылку 'На главную'"):
        page.get_by_role("link", name="На главную").click()

    with allure.step("Проверка перехода на главную страницу"):
        expect(page).to_have_url(MAIN_PAGE, timeout=5000)

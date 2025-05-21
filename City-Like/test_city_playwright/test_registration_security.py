import allure
from playwright.sync_api import Page
from conftest import get_browser, login, registration
from locator import MAIN_PAGE


@allure.feature("Безопасность формы регистрации")
@allure.story("SQL-инъекции в форме регистрации")
@allure.title("Проверка защиты от SQL-инъекций при регистрации")
@allure.severity(allure.severity_level.CRITICAL)
def test_registration_sql_injection(page: Page):
    """Проверка защиты формы регистрации от SQL-инъекций."""
    get_browser(page)

    login(page).click()
    registration(page).click()

    sql_injections = [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "' OR 1=1--",
        "\" OR \"\"=\"",
        "'; EXEC xp_cmdshell('dir'); --"
    ]

    for injection in sql_injections:
        with allure.step(f"Проверка инъекции: {injection}"):
            page.get_by_role("textbox", name="Email: например: qwerty@gmail").fill(f"{injection}@test.com")
            page.get_by_role("textbox", name="Номер телефона, например: +").fill(injection)
            page.get_by_role("textbox", name="Псевдоним, например: qwerty").fill(injection)

            enter_password = page.get_by_role("textbox", name="Пароль: 8 символов и 1 цифру")
            enter_password.click()
            enter_password.type("Citylike2", delay=200)

            confirm_password = page.get_by_role("textbox", name="Подтвердите пароль")
            confirm_password.click()
            confirm_password.type("Citylike2", delay=200)

            page.get_by_role("checkbox", name="Я принимаю условия Пользовательского соглашения").check()
            page.get_by_role("button", name="Регистрация").click()

            with allure.step("Проверка, что SQL-инъекция не прошла"):
                assert "/myreg/register/" in page.url or page.locator("text=Ошибка").is_visible(), \
                    f"SQL-инъекция прошла: {injection}"

            with allure.step("Сброс: переход на главную и повтор открытия формы регистрации"):
                page.goto(MAIN_PAGE)
                login(page).click()
                registration(page).click()

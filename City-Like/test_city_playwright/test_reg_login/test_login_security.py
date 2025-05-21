import pytest
import allure
from playwright.sync_api import Page
from conftest import get_browser, login


SQL_INJECTIONS = [
    "' OR '1'='1",
    "' OR 1=1--",
    "'; DROP TABLE users; --",
    "\" OR \"\"=\"",
    "'; EXEC xp_cmdshell('dir'); --"
]


@allure.feature("Безопасность формы логина")
@allure.story("SQL-инъекции при входе")
@allure.title("Проверка защиты логина от SQL-инъекций")
@pytest.mark.parametrize("injection", SQL_INJECTIONS)
@allure.severity(allure.severity_level.CRITICAL)
def test_login_sql_injection(page: Page, injection: str):
    """Проверка защиты формы логина от SQL-инъекций."""
    with allure.step("Открываем браузер и переходим на страницу логина"):
        get_browser(page)
        login(page).click()

    with allure.step(f"Проверяем инъекцию: {injection}"):
        email_input = page.get_by_role("textbox", name="Email или номер телефона:")
        password_input = page.get_by_role("textbox", name="Пароль:")
        email_input.fill(injection)
        password_input.type("Citylike2", delay=200)
        page.get_by_role("button", name="Войти").click()

    with allure.step("Проверка, что вход не выполнен и показана ошибка"):
        assert "login" in page.url or page.locator("text=Ошибка").is_visible(), \
            f"SQL-инъекция прошла: {injection}"

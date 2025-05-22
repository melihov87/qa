import allure
from playwright.sync_api import Page
from locator import (URL, WHERE_FROM, WHERE, INPUT_WHERE_FROM, INPUT_WHERE, DATE, DATE_START, DATE_END,
                               ADULTS, CHILDREN, INFANTS, PASSENGERS, BUTTON_SEARCH)

@allure.title("Поиск авиабилета из Подгорицы в Москву на Aviasales")
@allure.description("Тест проверяет возможность поиска авиабилета с выбором городов, дат и параметров пассажиров")
def test_pg_msk(page: Page):
    context = page.context

    with allure.step("Открыть сайт Aviasales"):
        page.set_viewport_size({"width": 1920, "height": 1080})
        response = page.goto(URL)
        assert response.status == 200, f"Страница не загрузилась: статус {response.status}"

    with allure.step("Выбрать город отправления — Подгорица"):
        page.locator(WHERE_FROM).click()
        page.locator(WHERE_FROM).fill("Подгори")
        page.locator(INPUT_WHERE_FROM).get_by_text("Подгорица").click()

    with allure.step("Выбрать город назначения — Москва"):
        page.locator(WHERE).click()
        page.wait_for_timeout(1000)
        page.locator(INPUT_WHERE).type("Москва", delay=100)
        page.get_by_text("МоскваMOWРоссия").click()
        page.wait_for_timeout(1000)

    with allure.step("Выбрать даты поездки — 23.05.2025 и 24.05.2025"):
        page.locator(DATE).click()
        page.locator(DATE_START).click()
        page.wait_for_timeout(500)
        page.locator(DATE_END).click()
        page.wait_for_timeout(1000)

    with allure.step("Настроить пассажиров и выбрать класс — Эконом"):
        page.locator(PASSENGERS).click()
        page.locator(ADULTS).click()
        page.locator(CHILDREN).click()
        page.locator(INFANTS).click()
        page.locator("label").filter(has_text="Эконом").locator("span").first.click()

    with allure.step("Нажать кнопку поиска и дождаться новой вкладки"):
        with context.expect_page() as new_page_info:
            page.locator(BUTTON_SEARCH).click()
        new_tab = new_page_info.value

    with allure.step("Проверить появление новой вкладки с текстом 'Ищем билеты'"):
        new_tab.wait_for_load_state(timeout=10000)
        new_tab.bring_to_front()
        new_tab.wait_for_selector("text=Ищем билеты", timeout=10000)
        assert new_tab.locator("text=Ищем билеты").is_visible(), "На новой вкладке не найден текст 'Ищем билеты'"

import allure
from playwright.sync_api import Page


@allure.title("Поиск авиабилета из Подгорицы в Москву на Aviasales")
@allure.description("Тест проверяет возможность поиска авиабилета с выбором городов, дат и параметров пассажиров")
def test_pg_msk(page: Page):
    context = page.context

    with allure.step("Открыть сайт Aviasales"):
        page.set_viewport_size({"width": 1920, "height": 1080})
        response = page.goto("https://www.aviasales.ru/")
        assert response.status == 200, f"Страница не загрузилась: статус {response.status}"

    with allure.step("Выбрать город отправления — Подгорица"):
        page.locator("[data-test-id='origin-input']").click()
        page.locator("[data-test-id='origin-input']").fill("Подгори")
        page.locator("[data-test-id='suggested-city-TGD']").get_by_text("Подгорица").click()

    with allure.step("Выбрать город назначения — Москва"):
        page.locator("[data-test-id='destination-input']").click()
        page.wait_for_timeout(1000)
        page.locator('#avia_form_destination-input').type("Москва", delay=100)
        page.get_by_text("МоскваMOWРоссия").click()
        page.wait_for_timeout(1000)

    with allure.step("Выбрать даты поездки — 23.05.2025 и 24.05.2025"):
        page.locator('[data-test-id="start-date-field"]').click()
        page.locator('[data-test-id="date-23.05.2025"]').click()
        page.wait_for_timeout(500)
        page.locator('[data-test-id="date-24.05.2025"]').click()
        page.wait_for_timeout(1000)

    with allure.step("Настроить пассажиров и выбрать класс — Эконом"):
        page.locator("[data-test-id='passengers-field']").click()
        page.locator("[data-test-id='number-of-adults'] [data-test-id='increase-button']").click()
        page.locator("[data-test-id='number-of-children'] [data-test-id='increase-button']").click()
        page.locator("[data-test-id='number-of-infants'] [data-test-id='increase-button']").click()
        page.locator("label").filter(has_text="Эконом").locator("span").first.click()

    with allure.step("Нажать кнопку поиска"):
        page.locator("[data-test-id='form-submit']").click()

    with allure.step("Проверить появление новой вкладки с текстом 'Ищем билеты'"):
        new_tab = context.wait_for_event("page", timeout=10000)
        new_tab.wait_for_load_state(timeout=10000)
        new_tab.bring_to_front()
        new_tab.wait_for_selector("text=Ищем билеты", timeout=10000)
        assert new_tab.locator("text=Ищем билеты").is_visible(), "На новой вкладке не найден текст 'Ищем билеты'"

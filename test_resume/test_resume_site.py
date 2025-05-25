import allure
from playwright.sync_api import Page


def get_browser(page: Page):
    page.set_viewport_size({'width': 1600, 'height': 1080})
    page.goto('https://qa-ml.ru')


@allure.feature("Резюме")
@allure.title("Проверка заголовков блока резюме")
def test_resume_heading(page: Page):
    with allure.step("Открываем сайт"):
        get_browser(page)

    with allure.step("Проверяем имя"):
        name_text = page.locator('#name').text_content()
        assert name_text == 'Алексей Мелихов'

    with allure.step("Проверяем позицию"):
        name_text2 = page.locator('#position').text_content()
        assert name_text2 == 'QA Engineer | 2 года опыта'

    with allure.step("Проверяем заголовок 'Контакты'"):
        info_contacts = page.locator('#info_contacts h2').text_content()
        assert info_contacts == 'Контакты'

    with allure.step("Проверяем заголовок 'О себе'"):
        info_about = page.locator('#info_about h2').text_content()
        assert info_about.replace('🧪', '').replace('\xa0', '').strip() == 'О себе'

    with allure.step("Проверяем заголовок 'Навыки'"):
        info_skills = page.locator('#info_skills h2').text_content()
        assert info_skills.replace('🛠', '').replace(' ', '').strip() == 'Навыки'

    with allure.step("Проверяем заголовок 'Опыт работы'"):
        info_experience = page.locator('#info_experience h2').text_content()
        assert info_experience.replace('💼', '').replace('\xa0', '').strip() == 'Опыт работы'

    with allure.step("Проверяем заголовок 'Образование'"):
        name_text7 = page.locator('#info_education h2').text_content()
        assert name_text7.replace('🎓', '').replace('\xa0', '').strip() == 'Образование'


@allure.feature("Кнопки")
@allure.title("Проверка кнопок-ссылок")
def test_button(page: Page):
    with allure.step("Открываем сайт"):
        get_browser(page)

    with allure.step("Проверяем общее количество кнопок"):
        count_button = page.locator('#block_button a').count()
        assert count_button == 6

    buttons = {
        '#github': 'GitHub',
        '#linkedin': 'LinkedIn',
        '#hh': 'hh.ru',
        '#telegram': 'Telegram',
        '#whatsapp': 'Whatsapp',
        '#viber': 'Viber',
    }

    for selector, expected_text in buttons.items():
        with allure.step(f"Проверяем кнопку {expected_text}"):
            actual = page.locator(selector).text_content().strip()
            assert actual == expected_text, f"Ожидалось: {expected_text}, получено: {actual}"

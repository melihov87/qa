from playwright.sync_api import Page
from locator import MAIN_PAGE

def get_browser(page: Page):
    viewport_size = {"width": 1920, "height": 1080}
    main_page = MAIN_PAGE
    page.set_viewport_size(viewport_size)
    page.goto(main_page)


def login(page: Page):
    return page.get_by_role("link", name="Войти")

def registration(page: Page):
    return page.get_by_role("link", name="Зарегистрироваться")

def logout(page: Page):
    pass

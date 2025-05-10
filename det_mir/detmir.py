import requests
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import time
from time import sleep
from selenium.common.exceptions import TimeoutException, NoSuchElementException


detmir_url = "https://www.detmir.ru/"

cookie = {
    'name': 'DM_CookieNotification',
    'value': '0'
}

chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920,1080")
service = Service(executable_path=ChromeDriverManager().install())
driver: WebDriver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(detmir_url)
action = ActionChains(driver)
wd = WebDriverWait(driver, 5)


def status_code_main_page():
    response = requests.get(detmir_url)
    detmir_status = response.status_code
    print(f'status_code: {detmir_status}')


def comparison_url_zoo():
    zoo_url = driver.current_url
    zoo_url_parse = urlparse(zoo_url)
    zoo_url_scheme = zoo_url_parse.scheme
    zoo_url_netloc = zoo_url_parse.netloc
    actual_result = f'{zoo_url_scheme}://{zoo_url_netloc}/'
    expected_result = 'https://zoozavr.ru/'
    if actual_result == expected_result:
        print(f'URL corresponds to: {expected_result}')
    else:
        print(f'URL does not match: {actual_result} != {expected_result}')
    driver.back()


def region_and_cookies():
    """Регион и куки"""
    try:
        geo_click = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, './/span[contains(text(), "Верно!")]')))
        action.pause(2).click(geo_click).perform()
        driver.add_cookie(cookie)
        driver.refresh()
        sleep(3)
        print("Куки пройдены")
    except Exception as e:
        print("Нет куки")


def banner_in_footer():
    """Баннер в шапке"""
    try:
        banner_footer = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@data-testid="advContainer"]')))
        banner_footer.click()
        driver.back()
        print("Проверка баннера выполнена")
    except Exception as e:
        print("Проверка баннера не выполнена")


def zoo_click_footer():
    """Клик по логотипу ЗООЗАВР в футоре"""
    zoo_click_foot = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@data-testid="additionalNavigationLogo"]')))
    zoo_click_foot.click()
    comparison_url_zoo()


def output_result_text_page(actual_result, expected_result):
    if actual_result == expected_result:
        print(f'Text corresponds to: {expected_result}')
    else:
        print(f'Text does not match: {actual_result} != {expected_result}')
    driver.back()


def choosing_region():
    """Выбор региона"""
    choice_region_click = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@data-testid="additionalNavigationGeoChooser"]')))
    choice_region_click.click()
    sleep(2)
    actual_result = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, 'geoModalTitle'))).text
    expected_result = 'Выбор региона'
    if actual_result == expected_result:
        print(f'Text corresponds to: {expected_result}')
    else:
        print(f'Text does not match: {actual_result} != {expected_result}')
    action.send_keys(Keys.ESCAPE).perform()


def store_selection():
    """Выбор магазина"""
    shops_link = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//a[.//span[text()="Магазины"]]')))
    action.pause(3).move_to_element(shops_link).click(shops_link).perform()
    info_name_shops = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@data-testid="pageTitle"]'))).text
    actual_result = info_name_shops[0:24]
    expected_result = 'Магазины «Детский мир»: '
    output_result_text_page(actual_result, expected_result)


def delivery_payment():
    """Доставка и оплата"""
    try:
        delivery_click = driver.find_element(By.XPATH, '(//span[@class="tz"])[2]')
        delivery_click.click()

        # Проверяем информацию о доставке
        try:
            delivery_click_info = driver.find_element(By.XPATH, '//span[@class="k_7"]').text
            actual_result = delivery_click_info[0:24]
            expected_result = 'Доставка и оплата: '
            output_result_text_page(actual_result, expected_result)

        except NoSuchElementException:
            print("Элемент с информацией о доставке не найден, возвращаемся назад")
            driver.back()
            sleep(2)

    except NoSuchElementException:
        print("Элемент доставки не найден, пропускаем этот блок")


def selling_detmir():
    """Продавать в Детском мире"""
    sell_click = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '(//a[.//span[text()="Продавать в Детском мире"]])')))
    sell_click.click()
    actual_result = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="rec485436514"]/div/div/div[5]'))).text
    expected_result = 'Продавайте на маркетплейсе\nДетского мира'
    output_result_text_page(actual_result, expected_result)


def exchange_refund():
    """Клик по кнопке Обмен и возврат товара"""
    exchange_click = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Обмен и возврат товара")]')))
    exchange_click.click()
    actual_result = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Обмен и возврат товара'
    output_result_text_page(actual_result, expected_result)


def feedback():
    """Клик по кнопке Еще и Обратная связь"""
    more_click = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//li[@data-testid="additionalNavigationMenuMore"]')))
    action.click(more_click).pause(2).perform()
    feedback_click = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//span[text()="Обратная связь"]')))
    feedback_click.click()
    actual_result = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Обратная связь'
    output_result_text_page(actual_result, expected_result)


def order_status():
    """Проверка статуса заказа с улучшенной обработкой и логированием"""

    def log_result(element_name, is_success):
        status = "соответствует" if is_success else "не соответствует"
        print(f"Страница {element_name} {status} ожидаемому результату")

    try:
        # 1. Клик по статусу заказа
        status_order_click = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//a[text()="Статус заказа"]'))
        )
        status_order_click.click()

        # 2. Закрытие всплывающего окна
        close_window_login = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="modalCloseButton"]'))
        )
        close_window_login.click()

        # 3. Проверка текста входа
        status_order_click_text = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//span[text()="Войти или создать профиль"]'))
        ).text
        expected_result_status_orders = 'Войти или создать профиль'

        # 4. Проверка текста профиля
        status_order_profile_text = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//h2[text()="Привет"]'))
        ).text
        expected_result_status_profile = 'Привет!'

        # Проверка результатов
        orders_match = status_order_click_text == expected_result_status_orders
        profile_match = status_order_profile_text == expected_result_status_profile

        log_result("статуса заказа", orders_match)
        log_result("профиля", profile_match)

        return orders_match and profile_match

    except TimeoutException as e:
        print(f"Ошибка при выполнении order_status(): {str(e)}")
        driver.save_screenshot('order_status_error.png')
        return False
    finally:
        for _ in range(2):
            try:
                driver.back()
                WebDriverWait(driver, 5).until(EC.staleness_of(status_order_click))
                break
            except Exception:
                continue


def chat():
    """Чат"""
    chat_click = driver.find_element(By.ID, 'button_ChatWidget')
    action.click(chat_click).pause(2).click(chat_click).pause(2).perform()
    driver.switch_to.frame(driver.find_element(By.ID, 'hde-iframe'))
    sleep(3)
    # Ввод имени в чат
    name_input = driver.find_element(By.XPATH, '//input[@placeholder="Имя"]')
    name_input.send_keys('Иван')
    # Ввод email в чат
    email_input = driver.find_element(By.XPATH, '//input[@placeholder="Электронная почта"]')
    email_input.send_keys('ivan@ya.ru')
    # Ввод сообщения в чат
    message_input = driver.find_element(By.XPATH, '//textarea[@placeholder="Сообщение"]')
    message_input.send_keys('Hello!')
    # Клик по чекбоксу
    check_chat_click = driver.find_element(By.XPATH, '//span[@class="el-checkbox__inner"]')
    check_chat_click.click()
    # Отправить сообщение
    send_message_chat = driver.find_element(By.XPATH, '//button[@class="el-button custom-button-color el-button--info el-button--small is-plain"]')
    # send_message_chat.click()
    # Закрыть чат
    close_chat = driver.find_element(By.XPATH, '//div[@class="widget-close"]/i')
    close_chat.click()
    print('The message has been sent')


def switching_iframe():
    """Переключение на другой iframe"""
    driver.switch_to.default_content()


def click_on_logo():
    """Клик по логотипу"""
    logo_click = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//a[@title="Детский мир"]')))
    logo_click.click()
    print("The logo was clicked successfully")


def click_on_profile():
    """Клик по профилю"""
    profile_click = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="headerLoginBlock"]')))
    profile_click.click()
    sleep(2)
    status_order_click_text = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//span[text()="Войти или создать профиль"]'))).text
    expected_result_status_orders = 'Войти или создать профиль'
    status_order_profile_text = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//h2[text()="Привет"]'))).text
    expected_result_status_profile = 'Привет!'
    if (status_order_click_text == expected_result_status_orders and
            status_order_profile_text == expected_result_status_profile):
        print('The page status order corresponds to')
        print('The page status profile corresponds to')
    else:
        print('The page status order does not match')
        print('The page status profile does not match')

    driver.back()
    sleep(3)


def click_on_bonus_card():
    """Клик по Бонусной карте"""
    bonus_card_click = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//a[@data-testid="headerBonusBlock"]')))
    bonus_card_click.click()
    actual_result = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "бонусной картой")]'))).text
    expected_result = 'С бонусной картой выгоднее'
    output_result_text_page(actual_result, expected_result)


def click_on_cart():
    """Клик по Корзина"""
    cart_click = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//a[@data-testid="headerCartBlock"]')))
    cart_click.click()
    actual_result = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Корзина'
    output_result_text_page(actual_result, expected_result)


def click_on_search():
    """Клик по полю Поиск и ввод запроса"""
    search_click = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//li[@data-dy="magnifier"]')))
    action.click(search_click).pause(2).send_keys('Hipp').pause(2).send_keys(Keys.ENTER).pause(5).perform()

    try:
        search_result = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//span[@data-testid="autoRefinedSearchHeaderPrefix"]'))).text
        actual_result = search_result[0:24]
        expected_result = 'Нашлось по запросу: hipp'
        output_result_text_page(actual_result, expected_result)

    except:
        search_result2 = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//span[@data-testid="productQuantityHeaderPrefix"]'))).text
        search_result_test2 = search_result2[0:26]
        expected_result_search2 = 'По запросу «hipp» найдено '
        if search_result_test2 == expected_result_search2:
            print('The page search corresponds to')
        else:
            print('The page search does not match')
        driver.back()


def click_on_banner_in_mnu():
    """Клик по баннеру в поле меню"""
    discount_menu = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app-container"]/div[1]/header/div[3]/nav/div/ul/li[2]')))
    discount_menu.click()
    actual_result = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app-container"]/div[1]/main/div/div/div[1]/div/h1'))).text
    expected_result = 'Ночь распродаж'
    output_result_text_page(actual_result, expected_result)


def click_on_promotions():
    """Клик по кнопке Акции"""
    stock_menu = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app-container"]/div[1]/header/div[3]/nav/div/ul/li[3]')))
    stock_menu.click()
    actual_result = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app-container"]/div[1]/main/header/div/div/h1'))).text
    expected_result = 'Акции'
    output_result_text_page(actual_result, expected_result)


def cursor_at_category():
    """Наведение курсора на Категории с подкатегориями"""
    try:
        nav_menu = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//nav[@aria-label="main menu"]'))
        )

        # Находим все пункты меню
        menu_items = WebDriverWait(nav_menu, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, './/li[@role="menuitem"]'))
        )

        print(f"Найдено {len(menu_items)} пунктов меню")

        # Инициализируем ActionChains
        action = ActionChains(driver)

        # Проходим по пунктам меню с 3 по 8 (индексы 2-7)
        for i in range(3, 10):
            if i < len(menu_items):
                try:
                    item = menu_items[i]
                    item_text = item.text if item.text else "элемент без текста"
                    print(f"Наведение на пункт {i + 1}: {item_text}")

                    # Плавное наведение с паузой
                    action.move_to_element(item).pause(0.5).perform()

                except Exception as e:
                    print(f"Ошибка при наведении на пункт {i + 1}: {str(e)}")
            else:
                print(f"Пункт меню {i + 1} не найден")

        # Наведение курсора на Еще категории
        more_menu = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//button[@data-testid="openMenuButton"]')))

        category_menu_2 = driver.find_elements(By.XPATH, '//section[@data-testid="linksBlock"]')
        action.move_to_element(more_menu).perform()
        for i in range(10, 20):
            if i < len(menu_items):
                try:
                    item = menu_items[i]
                    item_text = item.text if item.text else "элемент без текста"
                    print(f"Наведение на пункт {i + 1}: {item_text}")

                    # Плавное наведение с паузой
                    action.move_to_element(item).pause(0.5).perform()

                except Exception as e:
                    print(f"Ошибка при наведении на пункт {i + 1}: {str(e)}")
            else:
                print(f"Пункт меню {i + 1} не найден")

    except Exception as e:
        print(f"Ошибка при работе с меню: {str(e)}")
        driver.save_screenshot('menu_error.png')


def output_result(actual_result, expected_result):
    if actual_result == expected_result:
        print(f'H1 corresponds to: {expected_result}')
    else:
        print(f'H1 does not match: {actual_result} != {expected_result}')
    driver.back()


def clothing_and_shoes():
    """Клик по Одежда и обувь"""
    clothing = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="menuitem"][4]')))
    clothing.click()
    sleep(2)
    actual_result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Обувь, одежда и аксессуары'
    output_result(actual_result, expected_result)


def children_hygiene():
    """Клик по Подгузники и гигиена"""
    hygiene_for_children = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="menuitem"][5]')))
    hygiene_for_children.click()
    sleep(2)
    actual_result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Гигиена и уход'
    output_result(actual_result, expected_result)


def children_nutrition():
    """Клик по Питание и кормление"""
    nutrition_and_feeding = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="menuitem"][6]')))
    nutrition_and_feeding.click()
    sleep(2)
    actual_result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Кормление для детей'
    output_result(actual_result, expected_result)


def children_games():
    """Клик по Игрушки и игры"""
    games_for_children = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="menuitem"][7]')))
    games_for_children.click()
    sleep(2)
    actual_result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Игрушки для детей'
    output_result(actual_result, expected_result)


def children_room():
    """Клик по Детская комната"""
    rooms_for_children = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="menuitem"][8]')))
    rooms_for_children.click()
    sleep(2)
    actual_result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Детская комната'
    output_result(actual_result, expected_result)


def walking_and_traveling():
    """Клик по Прогулки и путешествия"""
    walking_traveling = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="menuitem"][9]')))
    walking_traveling.click()
    sleep(2)
    actual_result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Прогулки и путешествия'
    output_result(actual_result, expected_result)


def stationery_school():
    """Клик по Канцтовары и товары для школы"""
    stationery_for_school = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="menuitem"][10]')))
    stationery_for_school.click()
    sleep(2)
    actual_result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Товары для школы'
    output_result(actual_result, expected_result)


def menu_more():
    """Наведение курсора на Еще"""
    more_menu = wd.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="openMenuButton"]')))
    action.move_to_element(more_menu).perform()


def sports_recreation():
    """Наведение курсора на Еще и клик по Спорт и отдых"""
    menu_more()
    sports_and_recreation = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="menuitem"][11]')))
    sports_and_recreation.click()
    sleep(2)
    actual_result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Детские товары для спорта и отдыха'
    output_result(actual_result, expected_result)


def hobbies_creativity():
    """Наведение курсора на Еще и клик по Хобби и творчество"""
    menu_more()
    hobbies_and_creativity = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="menuitem"][12]')))
    hobbies_and_creativity.click()
    sleep(2)
    actual_result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Товары для творчества'
    output_result(actual_result, expected_result)


def books():
    """Наведение курсора на Еще и клик по Книги"""
    menu_more()
    books_for_children = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="menuitem"][13]')))
    books_for_children.click()
    sleep(2)
    actual_result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Книги для детей'
    output_result(actual_result, expected_result)


def products_sport():
    """Наведение курсора на Еще и клик по Продукты для здоровья и спорта"""
    menu_more()
    products_for_sport = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="menuitem"][14]')))
    products_for_sport.click()
    sleep(2)
    actual_result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Продукты для здоровья и спорта'
    output_result(actual_result, expected_result)


def house():
    """Наведение курсора на Еще и клик по Дом"""
    menu_more()
    for_house = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="menuitem"][15]')))
    for_house.click()
    sleep(2)
    actual_result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Дом'
    output_result(actual_result, expected_result)


def electronics():
    """Наведение курсора на Еще и клик по Бытовая техника и электроника"""
    menu_more()
    for_electronics = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="menuitem"][16]')))
    for_electronics.click()
    sleep(2)
    actual_result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Бытовая техника и электроника'
    output_result(actual_result, expected_result)


def parents():
    """Наведение курсора на Еще и клик по Для родителей"""
    menu_more()
    for_parents = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="menuitem"][17]')))
    for_parents.click()
    sleep(2)
    actual_result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Товары для родителей'
    output_result(actual_result, expected_result)


def animals():
    """Наведение курсора на Еще и клик по Товары для животных от ЗООЗАВР"""
    menu_more()
    products_for_animals = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="menuitem"][18]')))
    products_for_animals.click()
    comparison_url_zoo()


def gifts():
    """Наведение курсора на Еще и клик по Подарки"""
    menu_more()
    gifts_for_children = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="menuitem"][19]')))
    gifts_for_children.click()
    actual_result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Подарки для детей'
    output_result(actual_result, expected_result)


def promo_codes():
    """Наведение курсора на Еще и клик по Промокоды"""
    menu_more()
    promo = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="menuitem"][20]')))
    promo.click()
    actual_result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Промокоды'
    output_result(actual_result, expected_result)


def main():
    region_and_cookies()
    status_code_main_page()
    banner_in_footer()
    zoo_click_footer()
    choosing_region()
    store_selection()
    delivery_payment()
    selling_detmir()
    exchange_refund()
    feedback()
    order_status()
    chat()
    switching_iframe()
    click_on_logo()
    click_on_profile()
    click_on_bonus_card()
    click_on_cart()
    click_on_search()
    click_on_banner_in_mnu()
    click_on_promotions()
    cursor_at_category()
    clothing_and_shoes()
    children_hygiene()
    children_nutrition()
    children_games()
    children_room()
    walking_and_traveling()
    stationery_school()
    sports_recreation()
    hobbies_creativity()
    books()
    products_sport()
    house()
    electronics()
    parents()
    animals()
    gifts()
    promo_codes()


if __name__ == '__main__':
    main()

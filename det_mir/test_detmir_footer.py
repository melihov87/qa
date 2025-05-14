import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from get_driver import driver, log_test, detmir_url


def comparison_url_zoo(driver):
    """Сравнение текущего URL ожидаемым"""
    zoo_url = driver.current_url
    zoo_url_parse = urlparse(zoo_url)
    zoo_url_scheme = zoo_url_parse.scheme
    zoo_url_netloc = zoo_url_parse.netloc
    actual_result = f'{zoo_url_scheme}://{zoo_url_netloc}/'
    expected_result = 'https://zoozavr.ru/'
    assert actual_result == expected_result, f'URL не соответствует: {actual_result} != {expected_result}'
    driver.back()


def output_result_text_page(driver, actual_result, expected_result):
    """Функция сравнивает фактический и одидаемый результат"""
    assert actual_result == expected_result, f'Текст не соответствует ожидаемому: {actual_result} != {expected_result}'
    driver.back()


@log_test
def test_status_code_main_page(driver):
    """Проверка status_code"""
    try:
        response = requests.get(detmir_url)
        detmir_status = response.status_code
        assert detmir_status == 200
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


@log_test
def test_banner_in_footer(driver):
    """Клик по баннеру в шапке"""
    try:
        banner_footer = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@data-testid="advContainer"]')))
        banner_footer.click()
        driver.back()
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


@log_test
def test_zoo_click_footer(driver):
    """Клик по логотипу ЗООЗАВР в футоре и проверка URL адреса"""
    try:
        zoo_click_foot = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@data-testid="additionalNavigationLogo"]')))
        zoo_click_foot.click()
        comparison_url_zoo(driver)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


@log_test
def test_choosing_region(driver):
    """Клик на кнопку 'Выбор региона' и проверка заголовка окна"""
    try:
        region_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@data-testid="additionalNavigationGeoChooser"]')))
        region_button.click()
        modal_title = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'geoModalTitle')))
        actual_result = modal_title.text
        expected_result = 'Выбор региона'
        assert actual_result == expected_result, (f'Текст не соответствует ожидаемому: '
                                                  f'{actual_result} != {expected_result}')
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    except (TimeoutException, NoSuchElementException) as e:
        driver.save_screenshot('choosing_region_error.png')
        pytest.fail(f"Элемент не найден или не кликабелен: {str(e)}")


@log_test
def test_store_selection(driver):
    """Клик по "Выбор магазина" и проверка заголовка страницы"""
    try:
        shops_link = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//a[.//span[text()="Магазины"]]')))
        ActionChains(driver).pause(3).move_to_element(shops_link).click(shops_link).perform()
        info_name_shops = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@data-testid="pageTitle"]'))).text
        actual_result = info_name_shops[0:24]
        expected_result = 'Магазины «Детский мир»: '
        output_result_text_page(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


@log_test
def test_delivery_payment(driver):
    """Клик по "Доставка и оплата" и проверка заголовка страницы"""
    try:
        delivery_click = driver.find_element(By.XPATH, '(//span[@class="tz"])[2]')
        delivery_click.click()
        delivery_click_info = driver.find_element(By.XPATH, '//span[@class="k_7"]').text
        actual_result = delivery_click_info[0:24]
        expected_result = 'Доставка и оплата: '
        output_result_text_page(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


@log_test
def test_selling_detmir(driver):
    """Клик по "Продавать в Детском мире" и проверка заголовка страницы"""
    try:
        sell_click = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '(//a[.//span[text()="Продавать в Детском мире"]])')))
        sell_click.click()
        text_locator = (By.XPATH, '//*[@id="rec485436514"]/div/div/div[5]')
        WebDriverWait(driver, 20).until(
            EC.text_to_be_present_in_element(text_locator, 'Продавайте'))
        actual_result = driver.find_element(*text_locator).text
        expected_result = 'Продавайте на маркетплейсе\nДетского мира'
        output_result_text_page(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден или текст не загрузился")


@log_test
def test_exchange_refund(driver):
    """Клик по "Обмен и возврат товара" и проверка заголовка страницы"""
    try:
        exchange_click = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Обмен и возврат товара")]')))
        exchange_click.click()
        actual_result = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
        expected_result = 'Обмен и возврат товара'
        output_result_text_page(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


@log_test
def test_feedback(driver):
    """Клик по "Еще" и "Обратная связь" и проверка заголовка страницы"""
    try:
        more_click = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//li[@data-testid="additionalNavigationMenuMore"]')))
        ActionChains(driver).click(more_click).pause(2).perform()
        feedback_click = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//span[text()="Обратная связь"]')))
        feedback_click.click()
        actual_result = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
        expected_result = 'Обратная связь'
        output_result_text_page(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


@log_test
def test_order_status(driver):
    """Клик по "Статус заказа", проверка появления окна входа/регистрации и перехода на страницу Профиль"""
    try:
        status_order_click = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//a[text()="Статус заказа"]')))
        status_order_click.click()
        close_window_login = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="modalCloseButton"]')))
        close_window_login.click()
        status_order_click_text = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//span[text()="Войти или создать профиль"]'))).text
        expected_result_status_orders = 'Войти или создать профиль'
        status_order_profile_text = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//h2[text()="Привет"]'))).text
        expected_result_status_profile = 'Привет!'
        try:
            assert status_order_click_text == expected_result_status_orders
        except (TimeoutException, NoSuchElementException):
            print("Всплывающее окно с регистрацией не отображена на странице")
        try:
            assert status_order_profile_text == expected_result_status_profile
        except (TimeoutException, NoSuchElementException):
            print("Страница 'Профиль' не доступна")

        for _ in range(2):
            driver.back()

    except (TimeoutException, NoSuchElementException):
        print(f"Элемент не найден, пропускаем этот блок")
        driver.save_screenshot('order_status_error.png')
        return False


@log_test
def test_chat(driver):
    """Клик по "Чат с помощником" """
    try:
        chat_click = driver.find_element(By.ID, 'button_ChatWidget')
        ActionChains(driver).click(chat_click).pause(2).click(chat_click).pause(2).perform()
        driver.switch_to.frame(driver.find_element(By.ID, 'hde-iframe'))
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
        # # Отправить сообщение
        # send_message_chat = driver.find_element(By.XPATH, '//button[@class="el-button custom-button-color '
        #                                                   'el-button--info el-button--small is-plain"]')
        # send_message_chat.click()
        # Закрыть чат
        close_chat = driver.find_element(By.XPATH, '//div[@class="widget-close"]/i')
        close_chat.click()
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


@log_test
def test_switching_iframe(driver):
    """Переключение на другой iframe"""
    try:
        driver.switch_to.default_content()
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


@log_test
def test_click_on_logo(driver):
    """Клик по логотипу для проверки работоспособности кликабельности"""
    try:
        logo_click = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, '//a[@title="Детский мир"]')))
        logo_click.click()
        print('КЛИК ПО ЭЛЕМЕНТУ')
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


@log_test
def test_click_on_profile(driver):
    """Клик по "Профиль", проверка всплывающего окна авторизации/регистрации и перехода на страницу Профиль"""
    try:
        profile_click = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@data-testid="headerLoginBlock"]')))
        profile_click.click()
        status_order_click_text = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//span[text()="Войти или создать профиль"]'))).text
        expected_result_status_orders = 'Войти или создать профиль'
        status_order_profile_text = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//h2[text()="Привет"]'))).text
        expected_result_status_profile = 'Привет!'
        try:
            assert status_order_click_text == expected_result_status_orders, f'Текст всплывающего окна не соответствует'
        except (TimeoutException, NoSuchElementException):
            print("Окно авторизации не доступно")
        try:
            assert status_order_profile_text == expected_result_status_profile, f'Текст на странице не соответствует'
        except (TimeoutException, NoSuchElementException):
            print('Страница "Профиль" не доступна')
        driver.back()
        driver.refresh()
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


@log_test
def test_click_on_bonus_card(driver):
    """Клик по "Бонусная карта" и проверка соответствия страницы"""
    try:
        bonus_card_click = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@data-testid="headerBonusBlock"]')))
        ActionChains(driver).move_to_element(bonus_card_click).click(bonus_card_click).pause(2).perform()
        print('КЛИК ПО ЭЛЕМЕНТУ')
        actual_result = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "бонусной картой")]'))).text
        print(f'actual_result {actual_result}')
        expected_result = 'С бонусной картой выгоднее'
        output_result_text_page(driver, actual_result, expected_result)
        print('ВЫПОЛНЕНО')
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


@log_test
def test_click_on_cart(driver):
    """Клик по "Корзина"  и проверка соответствия страницы"""
    try:
        cart_click = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//a[@data-testid="headerCartBlock"]')))
        cart_click.click()
        actual_result = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
        expected_result = 'Корзина'
        output_result_text_page(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")

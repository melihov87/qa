import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from get_driver import driver, log_test
from test_detmir_footer import output_result_text_page, comparison_url_zoo


def menu_more(driver):
    """Наведение курсора на "Еще" для отображения скрытых категорий"""
    more_menu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="openMenuButton"]')))
    ActionChains(driver).move_to_element(more_menu).perform()


def output_result(driver, actual_result, expected_result):
    """Проверка ожидаемого и фактического результатов"""
    assert actual_result == expected_result, \
        f'Заголовок не соответствует ожидаемому: {actual_result} != {expected_result}'
    print(f"Текст соответствует: {expected_result}")
    driver.back()


def close_window_discount(driver):
    """Закрытие всплывающего окна "Получи скидку" """
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "flocktory-widget-overlay")))
        driver.execute_script("""
            let el = document.querySelector('.flocktory-widget-overlay');
            if (el) el.remove();
        """)
        ActionChains(driver).pause(3).perform()
        print("Всплывающее окно Flocktory удалено.")
    except TimeoutException:
        print("Flocktory-виджет не появился.")


def test_click_on_search(driver):
    """Клик по полю Поиск и ввод запроса, проверка ответа на запрос"""
    try:
        search_click = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//li[@data-dy="magnifier"]')))
        (ActionChains(driver).move_to_element(search_click).pause(3).click(search_click).pause(2).send_keys('Hipp').
         pause(2).send_keys(Keys.ENTER).pause(2).perform())
        try:
            search_result = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        '//span[@data-testid="autoRefinedSearchHeaderPrefix"]'))).text
            actual_result = search_result[0:24]
            expected_result = 'Нашлось по запросу: hipp'
            output_result_text_page(driver, actual_result, expected_result)
        except (TimeoutException, NoSuchElementException):
            search_result2 = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        '//span[@data-testid="productQuantityHeaderPrefix"]'))).text
            search_result_test2 = search_result2[0:26]
            expected_result_search2 = 'По запросу «hipp» найдено '
            assert search_result_test2 == expected_result_search2, \
                f'Заголовок не соответствует ожидаемому: {search_result_test2} != {expected_result_search2}'
            driver.back()
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_click_on_banner_in_menu(driver):
    """Клик по баннеру в поле меню"""
    try:
        discount_menu = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        '//*[@id="app-container"]'
                                                        '/div[1]/header/div[3]/nav/div/ul/li[2]')))
        discount_menu.click()
        actual_result = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        '//*[@id="app-container"]'
                                                        '/div[1]/main/div/div/div[1]/div/h1'))).text
        expected_result = ['КиберДни', 'Ночь распродаж']
        output_result_text_page(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_click_on_promotions(driver):
    """Клик по кнопке Акции"""
    driver.refresh()
    try:
        stock_menu = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//li[@role="menuitem"]//span[text()="Акции"]')))
        ActionChains(driver).pause(3).move_to_element(stock_menu).move_to_element(stock_menu).pause(3).click(stock_menu).pause(2).perform()
        actual_result = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//h1[contains(text(), "Акции")]'))).text
        expected_result = 'Акции'
        output_result_text_page(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_cursor_at_category(driver):
    """Наведение курсора на Категории с подкатегориями"""
    try:
        nav_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//nav[@aria-label="main menu"]')))
        menu_items = WebDriverWait(nav_menu, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, './/li[@role="menuitem"]')))

        for i in range(3, 10):
            if i < len(menu_items):
                try:
                    item = menu_items[i]
                    item_text = item.text if item.text else "элемент без текста"
                    print(f"Наведение на пункт {i + 1}: {item_text}")
                    ActionChains(driver).move_to_element(item).pause(0.5).perform()
                except Exception as e:
                    print(f"Ошибка при наведении на пункт {i + 1}: {str(e)}")
            else:
                print(f"Пункт меню {i + 1} не найден")

        more_menu = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//button[@data-testid="openMenuButton"]')))
        ActionChains(driver).move_to_element(more_menu).perform()

        for i in range(10, 20):
            if i < len(menu_items):
                try:
                    item = menu_items[i]
                    item_text = item.text if item.text else "элемент без текста"
                    print(f"Наведение на пункт {i + 1}: {item_text}")
                    ActionChains(driver).move_to_element(item).pause(0.5).perform()
                except Exception as e:
                    print(f"Ошибка при наведении на пункт {i + 1}: {str(e)}")
            else:
                print(f"Пункт меню {i + 1} не найден")
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_clothing_and_shoes(driver):
    """Клик по Одежда и обувь и сравнение текста тега h1"""
    try:
        clothing = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[text()="Одежда и обувь"]')))
        ActionChains(driver).move_to_element(clothing).pause(1).click(clothing).pause(1).perform()
        actual_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
        expected_result = 'Обувь, одежда и аксессуары'
        print(f'{actual_result} ----{expected_result}')
        output_result(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_children_hygiene(driver):
    """Клик по Подгузники и гигиена и сравнение текста тега h1"""
    try:
        hygiene_for_children = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Подгузники и гигиена"]')))
        (ActionChains(driver).move_to_element(hygiene_for_children).pause(1).click(hygiene_for_children).
         pause(1).perform())
        actual_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
        expected_result = 'Гигиена и уход'
        print(f'{actual_result} ----{expected_result}')
        output_result(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_children_nutrition(driver):
    """Клик по Питание и кормление и сравнение текста тега h1"""
    try:
        nutrition_and_feeding = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Питание и кормление"]')))
        (ActionChains(driver).move_to_element(nutrition_and_feeding).pause(1).click(nutrition_and_feeding).
         pause(1).perform())
        actual_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
        expected_result = 'Кормление для детей'
        output_result(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_children_games(driver):
    """Клик по Игрушки и игры и сравнение текста тега h1"""
    try:
        games_for_children = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Игрушки и игры"]')))
        ActionChains(driver).move_to_element(games_for_children).pause(1).click(games_for_children).pause(1).perform()
        actual_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
        expected_result = 'Игрушки для детей'
        output_result(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_children_room(driver):
    """Клик по Детская комната и сравнение текста тега h1"""
    try:
        rooms_for_children = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Детская комната"]')))
        ActionChains(driver).move_to_element(rooms_for_children).pause(1).click(rooms_for_children).pause(1).perform()
        actual_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
        expected_result = 'Детская комната'
        output_result(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_walking_and_traveling(driver):
    """Клик по Прогулки и путешествия и сравнение текста тега h1"""
    try:
        walking_traveling = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Прогулки и путешествия"]')))
        ActionChains(driver).move_to_element(walking_traveling).pause(1).click(walking_traveling).pause(1).perform()
        actual_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
        expected_result = 'Прогулки и путешествия'
        output_result(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_stationery_school(driver):
    """Клик по Канцтовары и товары для школы и сравнение текста тега h1"""
    try:
        stationery_for_school = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Канцтовары и товары для школы"]')))
        (ActionChains(driver).move_to_element(stationery_for_school).pause(1).click(stationery_for_school).
         pause(1).perform())
        actual_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
        expected_result = 'Товары для школы'
        output_result(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_sports_recreation(driver):
    """Наведение курсора на Еще и клик по Спорт и отдых и сравнение текста тега h1"""
    try:
        menu_more(driver)
        sports_and_recreation = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Спорт и отдых"]')))
        (ActionChains(driver).move_to_element(sports_and_recreation).pause(1).click(sports_and_recreation).
         pause(1).perform())
        actual_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
        expected_result = 'Детские товары для спорта и отдыха'
        output_result(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_hobbies_creativity(driver):
    """Наведение курсора на Еще и клик по Хобби и творчество и сравнение текста тега h1"""
    try:
        menu_more(driver)
        hobbies_and_creativity = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Хобби и творчество"]')))
        (ActionChains(driver).move_to_element(hobbies_and_creativity).pause(1).click(hobbies_and_creativity).
         pause(1).perform())
        actual_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
        expected_result = 'Товары для творчества'
        output_result(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_books(driver):
    """Наведение курсора на Еще и клик по Книги и сравнение текста тега h1"""
    try:
        menu_more(driver)
        books_for_children = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Книги"]')))
        ActionChains(driver).move_to_element(books_for_children).pause(1).click(books_for_children).pause(1).perform()
        actual_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
        expected_result = 'Книги для детей'
        output_result(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_products_sport(driver):
    """Наведение курсора на Еще и клик по Продукты для здоровья и спорта и сравнение текста тега h1"""
    try:
        menu_more(driver)
        products_for_sport = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Продукты для здоровья и спорта"]')))
        ActionChains(driver).move_to_element(products_for_sport).pause(1).click(products_for_sport).pause(1).perform()
        actual_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
        expected_result = 'Продукты для здоровья и спорта'
        output_result(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_house(driver):
    """Наведение курсора на Еще и клик по Дом и сравнение текста тега h1"""
    try:
        menu_more(driver)
        for_house = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Дом"]')))
        ActionChains(driver).move_to_element(for_house).pause(1).click(for_house).pause(1).perform()
        actual_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
        expected_result = 'Дом'
        output_result(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_electronics(driver):
    """Наведение курсора на Еще и клик по Бытовая техника и электроника и сравнение текста тега h1"""
    try:
        menu_more(driver)
        for_electronics = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Бытовая техника и электроника"]')))
        ActionChains(driver).move_to_element(for_electronics).pause(1).click(for_electronics).pause(1).perform()
        actual_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
        expected_result = 'Бытовая техника и электроника'
        output_result(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_parents(driver):
    """Наведение курсора на Еще и клик по Для родителей и сравнение текста тега h1"""
    menu_more(driver)
    for_parents = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span[text()="Для родителей"]')))
    ActionChains(driver).move_to_element(for_parents).pause(2).click(for_parents).pause(1).perform()
    actual_result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
    expected_result = 'Товары для родителей'
    output_result(driver, actual_result, expected_result)


def test_animals(driver):
    """Наведение курсора на Еще и клик по Товары для животных от ЗООЗАВР"""
    try:
        menu_more(driver)
        products_for_animals = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Товары для животных от Зоозавра"]')))
        (ActionChains(driver).move_to_element(products_for_animals).pause(1).click(products_for_animals).
         pause(1).perform())
        comparison_url_zoo(driver)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_gifts(driver):
    """Наведение курсора на Еще и клик по Подарки и сравнение текста тега h1"""
    try:
        menu_more(driver)
        gifts_for_children = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Подарки"]')))
        ActionChains(driver).move_to_element(gifts_for_children).pause(1).click(gifts_for_children).pause(1).perform()
        actual_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
        expected_result = 'Подарки для детей'
        output_result(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_close_window(driver):
    """Закрываем всплывающее окно если оно появляется и мешает выполнению теста"""
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-fl-close]')))
        if close_button:
            close_button.click()
        else:
            print(f'Всплывающее окно не отображено')
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")


def test_promo_codes(driver):
    """Наведение курсора на Еще и клик по Промокоды и сравнение текста тега h1"""
    try:
        menu_more(driver)
        promo = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Промокоды"]')))
        ActionChains(driver).move_to_element(promo).pause(1).click(promo).pause(1).perform()
        actual_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="pageTitle"]'))).text
        expected_result = 'Промокоды'
        output_result(driver, actual_result, expected_result)
    except (TimeoutException, NoSuchElementException):
        pytest.fail("Элемент не найден, пропускаем этот блок")

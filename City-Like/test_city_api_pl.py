import json
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture
def api_request_context():
    """Фикстура для создания контекста API-запросов."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        request_context = context.request
        yield request_context
        browser.close()

def test_get_api_root(api_request_context):
    url = "http://city-like.com/api/"

    # Отправка GET-запроса
    response = api_request_context.fetch(url)

    # Проверка статус-кода ответа
    assert response.status == 200, f"Expected 200, but got {response.status}"
    print(f"Response Status: {response.status}")

    # Проверка заголовков
    headers = response.headers
    assert "application/json" in headers.get("content-type", ""), "Response is not JSON"
    assert "GET" in headers.get("allow", ""), "GET method is not allowed"

    # Проверка содержимого ответа
    data = response.json()
    assert "monteads" in data, "Key 'monteads' is missing in response"
    assert data["monteads"] == "http://city-like.com/api/monteads/", \
        f"Unexpected URL in 'monteads': {data['monteads']}"

    # ✅ Красивый вывод JSON
    print("Response JSON:\n", json.dumps(data, indent=4, ensure_ascii=False))

import json
import pytest
import requests


@pytest.fixture
def api_session():
    """Фикстура для создания сессии API-запросов."""
    session = requests.Session()
    yield session
    session.close()

def test_get_api_root(api_session):
    url = "http://city-like.com/api/"

    # Отправка GET-запроса
    response = api_session.get(url)

    # Проверка статус-кода ответа
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}"
    print(f"Response Status: {response.status_code}")

    # Проверка заголовков
    headers = response.headers
    assert "application/json" in headers.get("Content-Type", ""), "Response is not JSON"
    assert "GET" in headers.get("Allow", ""), "GET method is not allowed"

    # Проверка содержимого ответа
    data = response.json()
    assert "monteads" in data, "Key 'monteads' is missing in response"
    assert data["monteads"] == "http://city-like.com/api/monteads/", \
        f"Unexpected URL in 'monteads': {data['monteads']}"

    # Вывод JSON
    print("Response JSON:\n", json.dumps(data, indent=4, ensure_ascii=False))


def test_monteads(api_session):
    url = "http://city-like.com/api/monteads/"
    response = api_session.get(url)

    assert response.status_code == 200, f"Expected 200, but got {response.status_code}"
    print(f"Response Status monteads: {response.status_code}")

    headers = response.headers
    print("Response Headers:", headers)
    print("Content-Type:", headers.get("Content-Type", "Not Found"))
    print("Allow:", headers.get("Allow", "Not Found"))

    assert "application/json" in headers.get("Content-Type", ""), "Response is not JSON"
    assert "GET" in headers.get("Allow", ""), "GET method is not allowed"

    data = response.json()
    print("Response JSON:\n", json.dumps(data, indent=4, ensure_ascii=False))

    assert any(item["name"] == "Транспорт" for item in data), "Key 'Транспорт' is missing in response"

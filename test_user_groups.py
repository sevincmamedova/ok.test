import os
import requests
import pytest
from dotenv import load_dotenv

# Загрузка переменных среды
load_dotenv()

# Константы для доступа к API, извлеченные из переменных среды для обеспечения безопасности
BASE_URL = "https://api.ok.ru/api"
APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY")
SESSION_KEY = os.getenv("SESSION_KEY")
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")

def make_request(endpoint, params):
    """Функция для выполнения запросов к API и возвращения ответа."""
    response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
    return response

def test_valid_user_groups_request():
    """
    Тестирование корректности получения списка групп пользователей с валидными параметрами.
    """
    params = {
        'application_id': APP_ID,
        'application_key': APP_KEY,
        'session_secret_key': SESSION_SECRET_KEY,
        'session_key': SESSION_KEY,
        'method': 'group.getUserGroupsV2',
        'format': 'json'
    }
    response = make_request('fb.do', params)
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert 'groups' in data, "Ответ должен содержать ключ 'groups'"

def test_invalid_session_key():
    """Тестирование ответа API на недействительный ключ сессии."""
    params = {
        'application_id': APP_ID,
        'application_key': APP_KEY,
        'session_secret_key': SESSION_SECRET_KEY,
        'session_key': 'INVALID_SESSION_KEY',
        'method': 'group.getUserGroupsV2',
        'format': 'json'
    }
    response = make_request('fb.do', params)
    data = response.json()
    print(data)
    assert response.status_code == 200  # API по-видимому возвращает статус 200 OK даже при ошибках
    assert 'error_code' in data or 'error_msg' in data, "Ответ должен содержать код ошибки или сообщение об ошибке"

def test_response_structure():
    """Тестирование структуры и содержания ответа API при опущенном параметре 'uid'."""
    params = {
        'application_id': APP_ID,
        'application_key': APP_KEY,
        'session_secret_key': SESSION_SECRET_KEY,
        'session_key': SESSION_KEY,
        'method': 'group.getUserGroupsV2',
        'format': 'json'
    }
    response = make_request('fb.do', params)
    data = response.json()
    assert response.status_code == 200, "Ожидается успешный статус ответа"

    assert 'groups' in data, "Ответ должен содержать ключ 'groups'"
    assert isinstance(data['groups'], list), "Ожидается, что 'groups' будет списком"
    assert data['groups'], "Ожидается непустой список групп"
    required_keys = {'groupId', 'userId', 'status'}
    for group in data['groups']:
        assert required_keys.issubset(group.keys()), f"Каждая группа должна содержать ключи {required_keys}"
        assert group['status'] == 'ACTIVE', "Ожидается, что статус группы будет 'ACTIVE'"
    assert 'anchor' in data, "Ожидается наличие 'anchor' в ответе"

# Запуск тестов, если скрипт выполняется напрямую
if __name__ == "__main__":
    pytest.main()

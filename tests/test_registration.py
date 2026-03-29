import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."


def test_add_current_user(setup_database, connection):
    """Тест добавления пользователя с существующим логином."""
    add_user('testuser', 'testuser@example.com', 'password123')
    result = add_user('testuser', 'testuser2@example.com', 'password456')
    assert result == False


def test_authenticate_user(setup_database, connection):
    """Тест аутентификации пользователя с правильными данными."""
    add_user('authuser', 'authuser@example.com', 'password123')
    result = authenticate_user('authuser', 'password123')
    assert result == True

def test_authenticate_nonexistent_user(setup_database, connection):
    """Тест аутентификации несуществующего пользователя."""
    result = authenticate_user('nonexistent', 'password123')
    assert result == False

def test_authenticate_user_wrong_password(setup_database, connection):
    """Тест аутентификации пользователя с неправильным паролем."""
    add_user('authuser', 'authuser@example.com', 'password123')
    result = authenticate_user('authuser', 'wrongpassword')
    assert result == False

# Возможные варианты тестов:
"""


Тест отображения списка пользователей.
"""
from fastapi.testclient import TestClient
from main import app
from config.variables import API_KEY

client = TestClient(app)

login = {
    "username": "foobar",
    "password": "123456"
}

header = {
    "authorization": "",
    "x-api-key": ""
}


def test_health():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": "Hello, API!"
    }


def test_create_user():
    header["x-api-key"] = API_KEY
    user = {
        "full_name": "foobar",
        "email": "foo@bar.com",
    }
    user.update(login)
    response = client.post('/users', json=user, headers=header)
    assert response.status_code == 201


def test_create_user_failed():
    user = {
        "full_name": "foobar",
        "email": "foo@bar.com",
    }
    user.update(login)
    response = client.post('/users', json=user, headers=header)
    assert response.status_code == 400


def test_login():
    response = client.post('/login', json=login)
    body = response.json()
    header.update({"authorization": "Bearer {0}".format(body["access_token"])})
    assert response.status_code == 200


def test_me():
    response = client.get('/users/me', headers=header)
    body = response.json()
    assert response.status_code == 200
    assert body["username"] == login["username"]


def test_login_failed():
    login["username"] = 'foo'
    login["password"] = 'bar'
    response = client.post('/login', json=login)
    assert response.status_code == 401


def test_all_books():
    response = client.get('/books', headers=header)
    assert response.status_code == 200


def test_all_books_failed():
    response = client.get('/books')
    assert response.status_code == 401

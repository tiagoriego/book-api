from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

login = {
    "username": "jdoido",
    "password": "123456"
}

header = {
    "authorization": ""
}


def test_health():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": "Hello, API!"
    }


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

# BOOK API

## Install

Install [pyenv](https://github.com/pyenv/pyenv)

Python Version `3.10.5`

1:

```bash
pyenv install 3.10.5
```

2:

```bash
pyenv virtualenv 3.10.5 book-api
```

3:

```bash
git clone git@github.com:tiagoriego/book-api.git
```

4:

```bash
cd book-api
echo book-api > .python-version
```

Install Packages

```bash
pip install -r requirements.txt
```

## Secret Key

```
openssl rand -hex 32
SECRET_KEY="insert here"
```

## DataBase

```bash
docker-compose up -d
```

Restart when necessary

```bash
docker restart postgres_container
```

### Create Tables

* `books`
* `users`

Books

```sql
CREATE TABLE public.books (
	id varchar(255) NOT NULL,
	author varchar(255) NOT NULL,
	dimensions varchar(255) NOT NULL,
	format varchar(255) NOT NULL,
	isbn varchar(255) NOT NULL,
	"language" varchar(255) NOT NULL,
	paperback varchar(255) NOT NULL,
	publication_date varchar(255) NOT NULL,
	publisher varchar(255) NOT NULL,
	title varchar(255) NOT NULL,
	CONSTRAINT books_pkey PRIMARY KEY (id)
);
```

Users

```sql
CREATE TABLE public.users (
	id varchar(255) NOT NULL,
	full_name varchar(255) NOT NULL,
	email varchar(255) NOT NULL,
	username varchar(255) NOT NULL,
	hashed_password varchar(255) NOT NULL,
	disabled bool NOT NULL,
	CONSTRAINT users_pkey PRIMARY KEY (id)
);
CREATE UNIQUE INDEX users_email_idx ON public.users (email);
CREATE UNIQUE INDEX users_username_idx ON public.users (username);
```

## Start

```bash
cd src/app
uvicorn main:app --reload
uvicorn main:app --port 3000 --reload
```

## Test
```bash
pytest
```

Ex.
```bash
platform linux -- Python 3.10.5, pytest-7.2.0, pluggy-1.0.0
rootdir: /home/user/projects/python/book-api/src/app
plugins: anyio-3.6.2
collected 6 items



test/test_main.py .....														[100%]

==================== 6 passed in 0.76s ==============
```

## Script

```bash
cd src/app
touch script.py
```
Content:

```python
from config.db import Session
from schemas.user import User
from utils.security import get_password_hash

session = Session()


def create_user():
    user = User(
        username="jdoido",
        hashed_password=get_password_hash("123456"),
        full_name="Joao Doido",
        email="joao@doido.com",
        disabled=False
    )

    session.add(user)
    session.flush()
    print(user.id, user.username, user.email)
    session.commit()


if __name__ == "__main__":
    create_user()
```

```bash
python script.py
```

## Helpful Links
* [FastAPI](https://fastapi.tiangolo.com/)
* [About Swagger](https://fastapi.tiangolo.com/advanced/extending-openapi/)
* [Sync Await](https://fastapi.tiangolo.com/async/#in-a-hurry)
* [uvicorn](https://www.uvicorn.org/)
* [sqlalchemy](https://docs.sqlalchemy.org/en/14/orm/examples.html)
* [Docker PostgreSQL](https://hub.docker.com/_/postgres)
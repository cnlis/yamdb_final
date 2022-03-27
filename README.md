![example workflow](https://github.com/cnlis/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# yamdb_final (api_yamdb v1)

Docker-контейнеризация c web-сервером Nginx и базой данных Postgres первой
версии API пока еще неизвестного сервиса рецензирования произведений **YaMDB**.
Предоставляет доступ к данным моделей Category, Comment, Genre, Review, User,
Title всем пользователям на чтение, аутентифицированным по JWT-токену
пользователям - на запись и изменение только
своих данных (кроме модели Title, Category, Genre). Персонал (admin, moderator)
и суперюзеры имеют все права на чтение и запись.

### Ссылка на приложение **api_yamdb**, запущенное на "боевом" сервере:
http://cnlis.ddns.net/api/v1/

### Документация: 
http://cnlis.ddns.net/redoc/

### Технологии приложения:
- Python 3.7
- Django 2.2.16
- djangorestframework 3.12.4

### Технологии сервера:
- Docker 20.10.13
- docker-compose 1.29.2
- Nginx 1.21.3
- Postgres 13.0

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```console
git clone https://github.com/cnlis/infra_sp2.git
```

```console
cd infra_sp2/infra
```

Создать в папке файл .env:
```console
nano .env
```
Заполнить файл следующими данными:
```
DJANGO_SECRET_KEY=  # секретный ключ Django
DJANGO_ALLOWED_HOSTS=["localhost"]  # список хостов в формате JSON
DB_ENGINE=django.db.backends.postgresql # используемая СУБД
DB_NAME=postgres  # название базы данных
POSTGRES_USER=  # имя пользователя БД
POSTGRES_PASSWORD=  # пароль БД
DB_HOST=db  # название сервиса (контейнера)
DB_PORT=5432  # используемый порт БД
```

Запустить docker-compose:

```console
docker-compose up -v
```

Выполнить миграции базы данных, создать суперпользователя, собрать статику:

```console
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

Загрузить тестовые данные в базу (опционально):

```console
docker-compose exec web python manage.py loaddata fixtures.json
```

### Полная документация к API в формате ReDoc приведена по адресу /redoc/

### Примеры запросов

#### GET-запрос на получение списка произведений
```url
/api/v1/titles/
```

Пример результата:
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
  {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
         "name": "string",
         "slug": "string"
      }
  }]
}
```

#### POST-запрос на создание произведения
```url
/api/v1/titles/
```
Передаваемые данные:
- name (обязательное)
- year (обязательное)
- description
- category (обязательное)
- genre (обязательное)

Пример результата:
```json
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
        {
            "name": "string",
            "slug": "string"
        }
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
}
```

#### GET-запрос на получение произведения
```url
/api/v1/titles/{id}/
```

Пример результата:
```json
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
        {
            "name": "string",
            "slug": "string"
        }
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
}
```

#### POST-запрос на создание рецензии
```url
/api/v1/titles/{id}/reviews/
```

Передаваемые данные:
- text (обязательное)
- score (обязательное)

Пример результата:
```json
{
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2022-02-05T14:15:22Z"
}
```

#### GET-запрос на получение рецензии
```url
/api/v1/titles/{id}/reviews/{id}/
```

Пример результата:
```json
{
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2022-02-05T14:15:22Z"
}
```

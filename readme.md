# TeamFinder

> Платформа для поиска команды на pet-проекты

TeamFinder помогает разработчикам, дизайнерам и другим специалистам находить интересные проекты, вступать в команды и искать единомышленников. Создавайте проекты, набирайте участников и добавляйте понравившиеся проекты в избранное.

---

## Стек технологий

- **Python** 3.12
- **Django** 5.2
- **PostgreSQL** 16
- **Pillow** - генерация аватаров
- **python-decouple** - управление конфигурацией через `.env`
- **Docker / Docker Compose** - запуск базы данных

---

## Функциональность

### Пользователи

- Регистрация и авторизация по email
- Редактирование профиля (имя, фамилия, аватар, телефон, GitHub, о себе)
- Автогенерация аватара при регистрации (первая буква имени на цветном фоне)
- Смена пароля
- Список участников платформы с пагинацией

### Проекты

- Создание, редактирование и завершение проектов
- Список проектов с пагинацией
- Страница проекта со списком участников
- Участие в проектах (вступить / выйти)

### Вариант 1 - Избранное + фильтрация пользователей

- Добавление и удаление проектов в избранное
- Страница избранных проектов
- Фильтрация пользователей по 4 критериям:
  - Авторы избранных проектов
  - Авторы проектов, в которых я участвую
  - Пользователи, которым нравятся мои проекты
  - Участники моих проектов

---

## Требования

- Python 3.12+
- Docker и Docker Compose
- Git

---

## Развёртывание

### 1. Клонировать репозиторий

```bash
git clone <url-репозитория>
cd team-finder-ad
```

### 2. Создать виртуальное окружение

```bash
python -m venv venv
```

Активировать:

- **Linux / Mac:**
  ```bash
  source venv/bin/activate
  ```
- **Windows (PowerShell):**
  ```bash
  venv\Scripts\Activate.ps1
  ```
- **Windows (cmd):**
  ```bash
  venv\Scripts\activate
  ```

Установить зависимости:

```bash
pip install -r requirements.txt
```

### 3. Создать файл `.env`

```bash
cp .env_example .env
```

Открыть `.env` и заполнить значения:

| Переменная  | Описание                                            | Пример            |
| --------------------- | ----------------------------------------------------------- | ----------------------- |
| `DJANGO_SECRET_KEY` | Секретный ключ Django                          | `django-insecure-...` |
| `DJANGO_DEBUG`      | Режим отладки                                   | `True`                |
| `POSTGRES_DB`       | Имя базы данных                                | `team_finder`         |
| `POSTGRES_USER`     | Пользователь БД                               | `team_finder`         |
| `POSTGRES_PASSWORD` | Пароль БД                                           | `team_finder`         |
| `POSTGRES_HOST`     | Хост БД                                               | `localhost`           |
| `POSTGRES_PORT`     | Порт БД                                               | `5432`                |
| `ALLOWED_HOSTS`     | Разрешённые хосты через запятую | `localhost,127.0.0.1` |

Сгенерировать `DJANGO_SECRET_KEY` можно так:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Запустить PostgreSQL через Docker

```bash
docker compose up -d
```

Остановить контейнер:

```bash
docker compose down
```

> Если порт `5432` уже занят - измените его в `docker-compose.yml` (например `"5433:5432"`) и в `.env` (`POSTGRES_PORT=5433`).

### 5. Применить миграции

```bash
python manage.py migrate
```

### 6. Загрузить тестовые данные

```bash
python manage.py shell
```

```python
exec(open('test_data.py', encoding='utf-8').read())
```

### 7. Запустить сервер

```bash
python manage.py runserver
```

Приложение доступно по адресу: [http://localhost:8000](http://localhost:8000)

---

## Тестовые аккаунты

| Email               | Пароль    | Описание                                   |
| ------------------- | --------------- | -------------------------------------------------- |
| `lev@yandex.ru`   | `password123` | Владелец проектов HLTV, Genius     |
| `sacha@gmail.com` | `password123` | Владелец проектов Songless, Twitch |
| `vitalik@mail.ru` | `password123` | Владелец проекта Max                |
| `pasha@yandex.ru` | `1234`        | Суперпользователь                 |

---

## Запуск тестов

```bash
python manage.py test
```

Ожидаемый результат: `Ran 11 tests ... OK`

---

## Структура проекта

```
team_finder/
├── settings.py         - настройки проекта
├── urls.py             - корневые маршруты
├── mixins.py           - общие миксины (GithubUrlMixin)
└── service.py          - общие сервисы (paginate)

users/
├── constants.py        - константы (длины полей, аватар, пагинация)
├── managers.py         - UserManager
├── models.py           - модель User
├── forms.py            - формы регистрации, входа, редактирования профиля
├── views.py            - представления
├── urls.py             - маршруты
├── admin.py            - регистрация в админке
└── tests.py            - тесты

projects/
├── constants.py        - константы (статусы, пагинация, длины полей)
├── models.py           - модель Project
├── forms.py            - форма проекта
├── views.py            - представления
├── urls.py             - маршруты
├── admin.py            - регистрация в админке
└── tests.py            - тесты

templates_var1/         - HTML-шаблоны (Вариант 1)
static/                 - CSS, JS, изображения
test_data.py            - скрипт загрузки тестовых данных
```

---

## Автор

**Павел Петров**

- GitHub: [pashaa66](https://github.com/pashaa66)
- Email: pasha10428@yandex.ru

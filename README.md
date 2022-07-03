## Название проекта
**«YaMDb API»** - проект YaMDb собирает отзывы пользователей на различные произведения.
---
Проект должен быть доступен по следующей ссылке: <http://51.250.96.8/redoc/>
#У меня, видимо, какой-то косяк в образах, но я не могу никак понять где именно и что с этим делать.
---
![yamdb_workflow](https://github.com/mirmir32/yamdb_final/workflows/yamdb_workflow/badge.svg)
---

**Возможности:**<br>
:black_small_square: Регистрация на сайте, получение токена, изменение данных своей учетной записи<br>
:black_small_square: Раздаление прав пользователей согласно, назначенной ему роли<br>
:black_small_square: Возможность, согласно авторизации выполнять следующие дествия: получать, добавлять и удалять - категорию, жанр, произведение, отзыв и комментарий<br>
:black_small_square: Администрирование пользователями<br><br>

## Инструкции по запуску
1. Склонировать репозиторий через консоль:
```sh
git clone https://github.com/Amaterasq/infra_sp2.git
```
2. Создать .env файл внутри директории infra (на одном уровне с docker-compose.yaml)
Пример .env файла:
```sh
SECRET_KEY = 'абракадаб№№№ра155523'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123
DB_HOST=db
DB_PORT=5432
```
3. Запуск тестов (опционально, если не нужно - переходите к следующему шагу)
Создать и активировать виртуальное пространство, установить зависимости.<br>

```sh
cd infra_sp2
python -m venv venv
source venv/Scripts/activate
cd api_yamdb
pip install -r requirements.txt
cd ..
pytest
```

4. Запуск Docker контейнеров:
Убедиться, что Docker установлен и готов к работе
```sh
docker --version
```
Запустите docker-compose
```sh
cd infra/
docker-compose up -d
```
5. Выполните миграции, создайте суперпользователя и перенесите статику:
```sh
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
6. Наполните базу данных тестовыми данными:
```sh
docker-compose exec web python manage.py dbfill
```
7. Проверьте доступность сервиса
```sh
http://localhost/admin
```

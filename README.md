# CookingCircle

---

## Описание

Сайт является - базой кулинарных рецептов.
Пользователи могут создавать свои рецепты, читать рецепты
других пользователей, подписываться на интересных авторов,
добавлять лучшие рецепты в избранное, а также создавать список
покупок и загружать его в txt формате. Также присутствует файл
docker-compose, позволяющий , быстро развернуть контейнер базы
данных (PostgreSQL), контейнер проекта django + gunicorn и
контейнер nginx

---

## Стек технологий

- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker
- Github Actions

---

## Зависимости

- Перечислены в файле `backend/requirements.txt`

---

## Для запуска на собственном сервере:

1. Скопируйте из репозитория файлы, расположенные в директории infra:
    - docker-compose.yml
    - nginx.conf
2. На сервере создайте директорию cookingcircle;
3. В директории cookingcircle создайте директорию infra и поместите в неё файлы:
    - docker-compose.yml
    - nginx.conf
    - .env
4. Файл .env должен быть заполнен следующими данными:

```
SECRET_KEY=<КЛЮЧ>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<ИМЯ БАЗЫ ДАННЫХ>
POSTGRES_USER=<ИМЯ ЮЗЕРА БД>
POSTGRES_PASSWORD=<ПАРОЛЬ БД>
DB_HOST=db
DB_PORT=5432
```

5. В директории infra следует выполнить команды:
6.

```
docker-compose up -d
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
```

6. Для создания суперпользователя, выполните команду:

```
docker-compose exec backend python manage.py createsuperuser
```

7. Для добавления ингредиентов в базу данных, выполните команду:

```
docker-compose exec backend python manage.py add_data ingredients.csv tags_ingr_ingredient
```

После выполнения этих действий проект будет запущен в трех контейнерах (backend, db, nginx) и доступен по адресам:

- Главная страница: http://<ip-адрес>/recipes/
- API проекта: http://<ip-адрес>/api/
- Admin-зона: http://<ip-адрес>/admin/

8. Теги вручную добавляются в админ-зоне в модель Tags;
9. Проект запущен и готов к регистрации пользователей и добавлению рецептов.

---

## Связь со мной

Если есть интересующие Вас вопросы и предложения по улучшению кода
или тестов, то связаться со мной можно по электронной почте
[danil.volodchenko@inbox.ru](mailto:danil.volodchenko@inbox.ru)
и в [telegram](https://t.me/VolodchenkoDanil).

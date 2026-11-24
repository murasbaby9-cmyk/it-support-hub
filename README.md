# IT / SUPPORT PRO
Выездная IT-поддержка • Django 5.2 • PostgreSQL • Render

Каталог услуг, калькулятор, заявки с закрытыми контактами, отслеживание по UUID, сценарный чат, отзывы с модерацией, Django Admin и CSV. Цены демонстрационные — уточните их перед коммерческим запуском. Оборудование нарисовано CSS 3D, анимация зависит от прокрутки. Интерфейс преимущественно русский.

## Windows / PyCharm
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Вставьте ключ в SECRET_KEY файла .env. Затем:
```powershell
.\.venv\Scripts\python manage.py migrate
.\.venv\Scripts\python manage.py createsuperuser
.\.venv\Scripts\python manage.py runserver
```
Откройте http://127.0.0.1:8000/ и /admin/. CSV: /admin/export/. В админке можно менять услуги, статусы, модерировать отзывы.

## Render
Создайте PostgreSQL и Web Service из GitHub. Build: `bash build.sh`. Start: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`. Environment: SECRET_KEY (новый), DEBUG=False, ALLOWED_HOSTS (домен без https), DATABASE_URL (Internal URL). Создайте администратора через доступную консоль Render или локально с временным подключением к внешнему URL базы (не сохраняйте его в Git). Не публикуйте .env.

## Лабораторная 12
Отправьте корректную заявку (INFO), затем с темой abc (WARNING). Для DisallowedHost локально задайте DEBUG=False и ALLOWED_HOSTS=localhost, перезапустите и откройте 127.0.0.1:8000. Верните 127.0.0.1 в ALLOWED_HOSTS. Сделайте реальные скриншоты журналов и добавьте ссылки после публикации.

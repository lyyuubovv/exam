# Exam Project (Django + DRF)

## Установка и запуск

```bash
git clone  https://github.com/lyyuubovv/exam.git

cd YOUR_REPO_NAME
pip install -r requirements.txt
```

Создайте файл `.env` в корне проекта и вставьте туда:

```env
SECRET_KEY="hdf9eshfseufhues38"

EMAIL_HOST_USER="admin@mail.com"
EMAIL_HOST_PASSWORD="Exam2025$Admin"
```

Примените миграции:

```bash
python manage.py migrate
```

Создайте суперпользователя:

```bash
python manage.py createsuperuser
```

Запустите сервер:

```bash
python manage.py runserver
```

Документация API доступна по адресу:

```
http://127.0.0.1:8000/swagger/
```

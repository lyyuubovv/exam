Exam project (Django REST Framework) - minimal working project for the news service exam.

What is included:
- Custom user model (email as username) with registration and activation via code (console email backend).
- JWT authentication (SimpleJWT): /auth/login/ and /auth/refresh/
- Articles app with endpoints:
    POST /articles/update/  (requires auth) - fetches from NewsAPI and saves new articles (caches update lock for 30 min)
    GET  /articles/         (public) - list articles, supports filters: fresh=true, title_contains=<str>
- Swagger UI at /swagger/

Quick start (Windows):
1. Create and activate virtual env:
    python -m venv venv
    venv\Scripts\activate

2. Install requirements:
    pip install -r requirements.txt

3. (Optional) Provide NEWSAPI_KEY in environment or edit exam_project/settings.py:
    set NEWSAPI_KEY=your_key_here    (Windows CMD)
    $env:NEWSAPI_KEY="your_key_here" (PowerShell)

4. Run migrations and start server:
    python manage.py migrate
    python manage.py createsuperuser  # optional
    python manage.py runserver

Notes / TODOs:
- You need to run Redis if you want caching via Redis. Alternatively, change CACHES to LocMemCache in settings for local testing.
- NewsAPI requires an API key. For testing you can pass api_key in POST body to /articles/update/ or set NEWSAPI_KEY.
- Migrations are not included (run migrate to generate them).
- This project is minimal and intended for the exam task only.

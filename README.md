📝 Django REST API для Форуму

Форум з авторизацією користувачів, профілем, постами та коментарями.
Backend: Django REST Framework (хостинг – Render)
Frontend: Nuxt.js (хостинг – Vercel)
База даних: Supabase (PostgreSQL)
Зображення: Cloudinary

📌 Це бекенд для форуму на Django REST Framework, який працює разом із фронтендом на Nuxt.js.
Фронтенд доступний тут
https://github.com/VitKhomen/nuxt_js_forum.git
https://nuxt-js-forum.vercel.app

## 🚀 Деплой
API: https://django-rest-45pc.onrender.com/api

## ⚙️ Локальний запуск
```bash
git clone https://github.com/VitKhomen/django_rest.git
cd forum-backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

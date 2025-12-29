# Фитнес-клуб "Энергия"

Django веб-приложение для управления фитнес-клубом с системой заказов абонементов.

##  Функционал

### Для пользователей:
-  Регистрация и авторизация
-  Гостевой вход (с ограничениями)
-  Просмотр и покупка абонементов
-  Поиск по абонементам
-  История заказов

### Для администраторов:
-  Панель администратора Django
-  Экспорт данных в Excel (выбор записей → Action → Экспорт)
-  Управление пользователями и заказами

## 🛠 Технологии

- **Backend:** Django 5.2, Python 3.11
- **Database:** PostgreSQL (продакшен), SQLite (разработка)
- **Frontend:** HTML5, CSS3, JavaScript
- **Контейнеризация:** Docker, Docker Compose
- **Дополнительно:** Openpyxl (Excel), Pillow (изображения)

##  Установка и запуск

```bash
# 1. Клонировать репозиторий
git clone https://github.com/futbik4/My_project_gym.git
cd My_project_gym

# 2. Запустить контейнеры
docker-compose up --build

# 3. В другом терминале выполнить миграции
docker-compose exec web python manage.py migrate

# 4. Создать администратора (опционально)
docker-compose exec web python manage.py createsuperuser

# 5. Открыть в браузере:
#    - Веб-сайт: http://localhost:8000
#    - Админ-панель: http://localhost:8000/admin
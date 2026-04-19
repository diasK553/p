# 🅿️ Parking Management System

Веб-приложение для управления парковкой на Flask + Python ООП.

## 🚀 Быстрый старт (локально)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/ВАШ_ЛОГИН/parking-system.git
cd parking-system

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Запустить
python app.py

# 4. Открыть в браузере
# http://localhost:5000
```

## 📁 Структура проекта

```
parking-system/
├── app.py               # Flask-сервер, все API маршруты
├── parking_system.py    # Логика: ООП классы
├── templates/
│   └── index.html       # Веб-интерфейс
├── tests/
│   └── test_parking.py  # Тесты (pytest)
├── .github/
│   └── workflows/
│       └── ci.yml       # GitHub Actions CI/CD
├── requirements.txt
├── Procfile             # Для деплоя на Render/Railway
└── .gitignore
```

## 🌐 API эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/status` | Статус парковки |
| POST | `/api/register` | Регистрация ТС |
| POST | `/api/enter` | Въезд |
| POST | `/api/exit` | Выезд + расчёт |
| GET | `/api/search?plate=XXX` | Поиск |
| GET | `/api/history` | История |
| GET | `/api/registry` | Список ТС |

## ☁️ Деплой на Render (бесплатно)

1. Зайти на [render.com](https://render.com) → New → Web Service
2. Подключить GitHub репозиторий
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. Нажать **Deploy** — готово!

## 🏗️ ООП принципы

- **Абстракция** — `ParkingEntity` (ABC)
- **Инкапсуляция** — `private`/`protected` атрибуты + `@property`
- **Наследование** — `Car`, `Truck`, `Motorcycle` → `Vehicle`
- **Полиморфизм** — `get_info()`, `get_type()` у каждого типа свой

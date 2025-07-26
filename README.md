# NegoBot Server

FastAPI сервер для AI голосового ассистента NegoBot.

## API Endpoints

- `GET /` - Информация о сервере
- `GET /api/v1/health` - Проверка здоровья сервера
- `POST /api/v1/stt` - Приём аудио от ESP32 для распознавания речи

## Деплой на Railway

1. Подключите этот репозиторий к Railway
2. Railway автоматически определит FastAPI приложение
3. Сервер будет доступен по публичному URL

## Локальная разработка

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Структура проекта

```
server/
├── app/
│   ├── __init__.py
│   └── main.py          # Основное FastAPI приложение
├── requirements.txt     # Python зависимости
├── Procfile            # Конфигурация для Railway
└── README.md
```

## TODO

- [ ] Интеграция с Google Speech-to-Text
- [ ] Интеграция с OpenAI GPT-4
- [ ] Интеграция с Google Text-to-Speech
- [ ] Обработка аудио файлов
- [ ] Возврат аудио ответа на ESP32 
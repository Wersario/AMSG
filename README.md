# CQRS Messenger

Мессенджер реального времени на Django + Channels + WebSocket с архитектурным паттерном CQRS.

## Технологии

- Python 3.12
- Django 5 + Django Channels 4
- PostgreSQL 16
- Redis 7 (channel layer)
- WebSocket
- CQRS (command / query separation)
- asyncio.create_task (асинхронная запись)
- Docker + Docker Compose

## Функциональность

- Регистрация и авторизация
- Создание чатов и вступление по invite-коду
- Обмен сообщениями в реальном времени через WebSocket
- Редактирование и удаление сообщений
- Экспорт истории чата в JSON

## Требования

- Docker
- Docker Compose

## Запуск

**1. Клонировать репозиторий**

```bash
git clone <repo-url>
cd AMSG
```

**2. Создать файл окружения**

```bash
cp .env.example .env
```

Содержимое `.env`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True

DB_NAME=messenger
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

**3. Запустить**

```bash
docker-compose up --build
```

Приложение будет доступно на http://localhost:8000

При первом запуске автоматически применяются все миграции.

## Структура проекта

```
AMSG/
├── backend/
│   ├── apps/
│   │   ├── chats/
│   │   │   ├── command/        # команды и хендлеры (write side)
│   │   │   ├── query/          # запросы и хендлеры (read side)
│   │   │   ├── infrastructure/ # broadcaster, async queue
│   │   │   ├── projection/     # projector: MessageLog → MessageReadModel
│   │   │   └── transport/      # views, consumers, routing
│   │   └── users/              # модель пользователя, views
│   ├── messenger/              # settings, urls, asgi
│   └── templates/              # Django templates
├── scripts/
│   └── run_dev.sh              # entrypoint контейнера
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Управление

Остановить контейнеры:

```bash
docker-compose down
```

Пересобрать после изменений в коде:

```bash
docker-compose up --build
```

Создать новые миграции вручную:

```bash
docker-compose exec python backend/manage.py makemigrations
```

Применить новые миграции вручную:

```bash
docker-compose exec python backend/manage.py migrate
```

Создать суперпользователя:

```bash
docker-compose exec python backend/manage.py createsuperuser
```

Открыть Django shell:

```bash
docker-compose exec python backend/manage.py shell
```

## Архитектура

Приложение реализует CQRS: операции записи (отправка, редактирование, удаление сообщений) проходят через `CommandHandlers` и пишутся в `MessageLog`. Асинхронный `Projector` копирует данные в денормализованную `MessageReadModel`, из которой `QueryHandlers` читают историю без JOIN-запросов.

WebSocket-соединения обслуживает `ChatConsumer` через Django Channels. Рассылка сообщений всем участникам чата происходит через Redis channel layer.

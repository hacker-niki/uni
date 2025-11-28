# Инструкция по запуску проекта TestGen с базой данных

## Быстрый старт

### 1. Проверка предварительных требований

Убедитесь, что у вас установлены:

- **Docker** (версия 20.10 или выше)
- **Docker Compose** (версия 1.29 или выше)

Проверка версий:

```bash
docker --version
docker-compose --version
```

### 2. Подготовка проекта

Перейдите в директорию проекта:

```bash
cd /home/nikita/uni/PROJECT_X/application
```

### 3. Запуск всех сервисов

Запустите все контейнеры (база данных, backend, frontend):

```bash
docker-compose up -d
```

Эта команда:
- Скачает образ MariaDB 11.2
- Создаст контейнер с базой данных
- Инициализирует БД из `database/init.sql`
- Запустит backend на порту 8000
- Запустит frontend на порту 3000

### 4. Проверка статуса контейнеров

```bash
docker-compose ps
```

Все контейнеры должны быть в статусе "Up":
- `testgen-db` - база данных MariaDB
- `testgen-backend` - FastAPI backend
- `testgen-frontend` - React/Next.js frontend

### 5. Проверка работы системы

#### Проверка API:

```bash
curl http://localhost:8000/
```

Должен вернуть JSON с информацией об API.

#### Проверка health endpoint:

```bash
curl http://localhost:8000/health
```

Должен вернуть статус "healthy" и статистику БД.

#### Проверка в браузере:

- **API документация**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000

### 6. Остановка системы

Остановка всех контейнеров:

```bash
docker-compose down
```

Остановка с удалением данных БД:

```bash
docker-compose down -v
```

---

## Подробная информация

### Структура базы данных

База данных автоматически инициализируется из файла `database/init.sql` при первом запуске.

Включает:

- **10 таблиц**: users, roles, groups, source_documents, questions, answer_options, tests, test_sessions, user_answers, audit_log
- **Триггеры** для автоматического обновления полей
- **Хранимые процедуры** для сложных запросов
- **Систему аудита** всех изменений данных
- **Демонстрационные данные**: 4 пользователя, 10 вопросов, 1 тест

Подробная документация: см. файл `DATABASE.md`

### Доступы к базе данных

#### Подключение к MariaDB через командную строку:

```bash
docker exec -it testgen-db mysql -u testgen_user -ptestgen_pass testgen
```

#### Параметры подключения:

- **Host**: localhost (или `db` внутри Docker сети)
- **Port**: 3306
- **Database**: testgen
- **User**: testgen_user
- **Password**: testgen_pass
- **Root password**: testgen_root_pass

### Демонстрационные пользователи

Все пользователи имеют пароль: `admin123`

| Email                    | Роль     | Полное имя                |
|--------------------------|----------|---------------------------|
| admin@testgen.com        | admin    | Администратор Системы     |
| teacher@testgen.com      | teacher  | Преподаватель Иванов И.И. |
| student1@testgen.com     | student  | Студент Петров П.П.       |
| student2@testgen.com     | student  | Студент Сидоров С.С.      |

### API Endpoints

После запуска доступны следующие endpoints:

#### Основные:

- `GET /` - Информация об API
- `GET /health` - Health check
- `GET /docs` - Swagger UI документация
- `GET /redoc` - ReDoc документация

#### Вопросы:

- `GET /api/questions` - Список вопросов
- `GET /api/questions/{id}` - Конкретный вопрос
- `POST /api/questions/{id}/approve` - Одобрить вопрос
- `DELETE /api/questions/{id}` - Удалить вопрос

#### Документы:

- `GET /api/documents` - Список документов

#### Тесты:

- `GET /api/tests` - Список тестов
- `GET /api/tests/{id}` - Детали теста
- `GET /api/tests/{id}/questions` - Вопросы теста

#### Статистика:

- `GET /api/stats/overview` - Общая статистика системы

### Примеры запросов

#### Получение всех вопросов:

```bash
curl http://localhost:8000/api/questions
```

#### Получение только одобренных вопросов:

```bash
curl http://localhost:8000/api/questions?approved_only=true
```

#### Получение вопросов по сложности:

```bash
curl http://localhost:8000/api/questions?difficulty=easy
```

#### Получение деталей теста:

```bash
curl http://localhost:8000/api/tests/1
```

#### Получение вопросов теста:

```bash
curl http://localhost:8000/api/tests/1/questions
```

#### Получение статистики:

```bash
curl http://localhost:8000/api/stats/overview
```

---

## Полезные команды

### Просмотр логов

#### Все сервисы:

```bash
docker-compose logs -f
```

#### Только база данных:

```bash
docker-compose logs -f db
```

#### Только backend:

```bash
docker-compose logs -f backend
```

### Перезапуск отдельного сервиса

```bash
docker-compose restart backend
```

### Пересборка контейнеров

После изменения кода или requirements.txt:

```bash
docker-compose up -d --build
```

### Выполнение SQL запросов

```bash
docker exec -it testgen-db mysql -u testgen_user -ptestgen_pass testgen -e "SELECT * FROM users;"
```

### Бэкап базы данных

```bash
docker exec testgen-db mysqldump -u testgen_user -ptestgen_pass testgen > backup.sql
```

### Восстановление из бэкапа

```bash
docker exec -i testgen-db mysql -u testgen_user -ptestgen_pass testgen < backup.sql
```

---

## Решение проблем

### База данных не запускается

1. Проверьте логи:
   ```bash
   docker-compose logs db
   ```

2. Убедитесь, что порт 3306 свободен:
   ```bash
   sudo netstat -tulpn | grep 3306
   ```

3. Удалите volume и пересоздайте:
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

### Backend не подключается к БД

1. Проверьте, что контейнер БД запущен:
   ```bash
   docker-compose ps
   ```

2. Проверьте переменные окружения:
   ```bash
   docker-compose exec backend env | grep DB_
   ```

3. Попробуйте подключиться вручную:
   ```bash
   docker-compose exec backend python -c "from database import check_db_connection; print(check_db_connection())"
   ```

### Ошибки импорта в Python

Пересоберите контейнер backend:

```bash
docker-compose up -d --build backend
```

### Сброс всех данных

```bash
docker-compose down -v
docker-compose up -d
```

Это удалит все данные и создаст чистую БД с демо-данными.

---

## Разработка

### Изменение структуры БД

После изменения `database/init.sql`:

```bash
docker-compose down -v
docker-compose up -d
```

### Изменение моделей SQLAlchemy

После изменения `backend/models.py` перезапустите backend:

```bash
docker-compose restart backend
```

### Добавление зависимостей Python

После изменения `backend/requirements.txt`:

```bash
docker-compose up -d --build backend
```

### Hot reload

Backend настроен на автоматическую перезагрузку при изменении кода (uvicorn с флагом `--reload`).

---

## Архитектура

```
┌─────────────────┐
│    Frontend     │
│  (React/Next)   │
│   Port: 3000    │
└────────┬────────┘
         │
         │ HTTP
         ▼
┌─────────────────┐
│     Backend     │
│    (FastAPI)    │
│   Port: 8000    │
└────────┬────────┘
         │
         │ SQLAlchemy
         ▼
┌─────────────────┐
│    Database     │
│    (MariaDB)    │
│   Port: 3306    │
└─────────────────┘
```

---

## Дополнительные ресурсы

- **Документация по БД**: `DATABASE.md`
- **API документация**: http://localhost:8000/docs
- **Пример .env файла**: `.env.example`
- **Структура проекта**: `PROJECT_STRUCTURE.md`

---

## Контакты

При возникновении проблем обращайтесь к администратору проекта.

# TestGen MVP - Система автоматизированного тестирования

MVP приложение для дипломной работы - система генерации тестов на основе документов с использованием нейросети.

## Структура проекта

```
application/
├── backend/              # Python FastAPI backend
│   ├── main.py          # Основной файл с API endpoints
│   ├── requirements.txt # Python зависимости
│   └── Dockerfile       # Docker конфигурация для backend
├── frontend/            # React frontend
│   ├── src/            # Исходный код React приложения
│   │   ├── pages/      # Страницы приложения
│   │   ├── App.jsx     # Главный компонент
│   │   └── main.jsx    # Точка входа
│   ├── package.json    # Node.js зависимости
│   └── Dockerfile      # Docker конфигурация для frontend
└── docker-compose.yml  # Оркестрация всех сервисов
```

## Возможности

### Реализовано в MVP:
- ✅ Просмотр списка документов
- ✅ Просмотр сгенерированных вопросов
- ✅ Одобрение/удаление вопросов
- ✅ Создание и прохождение тестов
- ✅ Система таймера для тестов
- ✅ Подсчет результатов
- ✅ Захардкоженные демо-данные (10 вопросов по SQL)

### Дизайн:
- Стиль из шаблонов files/ (фиолетово-синий градиент)
- Шрифт: Manrope
- Адаптивный интерфейс
- Анимации и transitions

## Запуск приложения

### Требования:
- Docker
- Docker Compose

### Команды:

```bash
# Запуск всего приложения
cd application
docker-compose up --build

# Остановка
docker-compose down

# Перезапуск с очисткой
docker-compose down -v
docker-compose up --build
```

### Доступ к приложению:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## API Endpoints

### Вопросы:
- `GET /api/questions` - Получить все вопросы
- `GET /api/questions?approved_only=true` - Только одобренные
- `GET /api/questions/{id}` - Получить вопрос по ID
- `POST /api/questions/{id}/approve` - Одобрить вопрос
- `DELETE /api/questions/{id}` - Удалить вопрос

### Документы:
- `GET /api/documents` - Список документов

### Тесты:
- `GET /api/tests` - Список тестов
- `GET /api/tests/{id}` - Получить тест
- `GET /api/tests/{id}/questions` - Вопросы для теста

## Демо-данные

### Вопросы (10 шт.):
Захардкожены в `backend/main.py` - вопросы по SQL для демонстрации

### Документы (2 шт.):
- Основы SQL.pdf (обработан, 10 вопросов)
- Реляционные СУБД.docx (в обработке)

### Тесты (1 шт.):
- "Основы SQL" (45 минут, 70% проходной балл)

## Технологический стек

### Backend:
- Python 3.11
- FastAPI
- Uvicorn
- Pydantic

### Frontend:
- React 18
- Vite
- React Router DOM
- Axios

### Infrastructure:
- Docker
- Docker Compose

## Отличия от полной версии

В MVP версии:
- ❌ Нет реальной генерации через Ollama (вместо этого захардкоженные данные)
- ❌ Нет загрузки документов
- ❌ Нет базы данных (данные в памяти)
- ❌ Нет аутентификации
- ❌ Нет создания новых тестов через UI

Это позволяет:
- ✅ Быстро показать функционал на презентации
- ✅ Не требует запущенного Ollama
- ✅ Работает полностью автономно
- ✅ Демонстрирует весь пользовательский интерфейс

## Для презентации

1. Запустите приложение: `docker-compose up`
2. Откройте http://localhost:3000
3. Демонстрируйте:
   - Главную страницу со статистикой
   - Список документов
   - Проверку вопросов (можно одобрять/удалять)
   - Прохождение теста с таймером
   - Результаты теста

## Разработка

Для локальной разработки без Docker:

### Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend:
```bash
cd frontend
npm install
npm run dev
```

---

**Создано для дипломной работы**
*Система автоматизированного тестирования с использованием нейросети*

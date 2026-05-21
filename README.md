

# ego-rag-agent
RAG агент с поддержкой ProxyAPI

## О проекте
Этот проект является форком [Toxap/agent](https://github.com/Toxap/agent) с расширенным функционалом для работы через ProxyAPI.

## Мои доработки
- ✨ Добавлена поддержка ProxyAPI для работы с LLM-моделями
- [другие доработки по мере реализации]

## Оригинальный проект
Основан на проекте [agent by Toxap](https://github.com/Toxap/agent).

---

## Установка

**Первый раз:**
```bash
# Активация виртуального окружения
.\.venv\Scripts\Activate.ps1

# Установка зависимостей
pip install -r requirements.txt
```

**Создание .env файла:**
Скопируйте `.env.example` в `.env` и заполните необходимыми ключами:
```bash
Copy-Item .env.example .env
# Или на Linux/Mac:
# cp .env.example .env
```
Затем отредактируйте `.env` и вставьте свои токены.

## Запуск

### 🚀 Windows (самый простой способ):

**Первый раз - установка:**
```bash
SETUP.bat
```

**Индексация документов:**
```bash
INDEX_DATA.bat
```

**Запуск бота:**
```bash
START.bat
```

### 💻 Универсальный способ:

```bash
# Из папки agent/
python main.py
```

### 📦 Как модуль (из корня проекта):
```bash
python -m agent
```

## Использование

1. Найдите вашего бота в Telegram
2. Отправьте `/start`
3. Задайте вопрос
4. Получите ответ на основе базы знаний!

### Команды бота:

- `/start` - начать работу
- `/help` - справка
- `/stats` - статистика системы
- `/clear` - очистить историю диалога

## Структура проекта

```
agent/
├── __init__.py
├── main.py                      # Точка входа
├── requirements.txt             # Зависимости
├── README.md                    # Документация
│
├── config/                      # Конфигурация
│   ├── __init__.py
│   └── settings.py              # Настройки приложения
│
├── interface/                   # 1. Интерфейс
│   ├── __init__.py
│   ├── telegram_bot.py
│   └── handlers.py
│
├── dialog_controller/           # 2. Контроллер диалогов
│   ├── __init__.py
│   ├── session_manager.py
│   └── user_context.py
│
├── memory_manager/              # 3. Менеджер памяти
│   ├── __init__.py
│   ├── prompt_builder.py
│   └── context_retriever.py
│
├── ai_processor/                # 4. Обработка через ИИ
│   ├── __init__.py
│   ├── openai_client.py
│   └── response_generator.py
│
├── storage/                     # 5. Хранилище данных
│   ├── __init__.py
│   ├── vector_db.py
│   ├── user_db.py
│   └── document_loader.py
│
└── utils/                       # Утилиты
    ├── __init__.py
    └── logging_config.py
```

## Преимущества модульной архитектуры

✅ **Разделение ответственности** - каждый модуль решает свою задачу
✅ **Легкое тестирование** - модули независимы
✅ **Масштабируемость** - легко добавлять новые функции
✅ **Переиспользование** - модули можно использовать отдельно
✅ **Читаемость** - понятная структура кода

## Расширение функциональности

### Добавление нового интерфейса

Создайте новый обработчик в `interface/`, используя существующие компоненты:

```python
from agent.dialog_controller import SessionManager
from agent.memory_manager import ContextRetriever
from agent.ai_processor import ResponseGenerator

# Ваш новый интерфейс (API, Web, CLI и т.д.)
```

### Добавление нового хранилища

Реализуйте интерфейс в `storage/` для работы с другой БД.

### Изменение модели ИИ

Измените настройки в `.env` или создайте новый процессор в `ai_processor/`.

## Логирование

Логи выводятся в консоль. Уровень логирования можно изменить в `main.py`:

```python
setup_logging(level="DEBUG")  # DEBUG, INFO, WARNING, ERROR
```

## Лицензия

Свободно используйте для обучения и коммерческих проектов.


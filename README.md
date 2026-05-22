

# ego-rag-agent
RAG агент с поддержкой ProxyAPI

## О проекте
Этот проект является форком [Toxap/agent](https://github.com/Toxap/agent) с расширенным функционалом для работы через ProxyAPI.

## Мои доработки
- ✨ Добавлена поддержка ProxyAPI для работы с LLM-моделями
- 🔐 Поддержка прокси через ProxyAPI
- ⚙️ Гибкая конфигурация через переменные окружения
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

---

## Поддержка ProxyAPI

Проект поддерживает работу через **ProxyAPI** — российское решение для доступа к AI-моделям (OpenAI, Anthropic, Gemini) через единую точку входа.

### О ProxyAPI

**ProxyAPI** (`https://api.proxyapi.ru`) — это универсальный прокси-сервис, который:
- Предоставляет доступ к API ведущих AI-провайдеров (OpenAI, Anthropic, Gemini)
- Выступает посредником: запросы отправляются через серверы в Европе
- Не требует создания аккаунтов в сторонних системах — управление через личный кабинет ProxyAPI
- Централизует оплату и управление ключами

### Настройка ProxyAPI

1. **Получите ключ API:**
   - Зарегистрируйтесь на [console.proxyapi.ru](https://console.proxyapi.ru/)
   - Перейдите в раздел [Ключи API](https://console.proxyapi.ru/keys)
   - Скопируйте ключ (можно увидеть полностью только один раз при создании!)

2. **Настройте переменные окружения:**

```env
# Выбор провайдера
AI_PROVIDER=proxyapi

# ProxyAPI настройки
PROXYAPI_API_KEY=your_api_key_here
PROXYAPI_MODEL=gpt-4o-mini
PROXYAPI_TEMPERATURE=0.7
PROXYAPI_MAX_TOKENS=1000
PROXYAPI_BASE_URL=https://api.proxyapi.ru

# Опционально: прокси для ProxyAPI
# PROXYAPI_PROXY_URL=http://proxy.example.com:8080
```

3. **Структура запросов:**
```
https://api.proxyapi.ru/{provider}/v1
```
   - OpenAI: `https://api.proxyapi.ru/openai/v1`
   - Anthropic: `https://api.proxyapi.ru/anthropic/v1`
   - Gemini: `https://api.proxyapi.ru/gemini/v1`

### Преимущества ProxyAPI

- 🔒 **Безопасность** — централизованное управление ключами
- 🔄 **Гибкость** — легкое переключение между моделями и провайдерами
- 🌐 **Прокси** — поддержка корпоративных прокси-серверов
- ⚡ **Производительность** — оптимизированные запросы
- 💰 **Оплата** — единая система оплаты через личный кабинет

### Доступные модели через ProxyAPI

**OpenAI модели:**
- gpt-4o-mini
- gpt-4o
- gpt-4-turbo
- text-embedding-3-small (для embeddings)

**Anthropic модели:**
- claude-3-opus
- claude-3-sonnet
- claude-3-haiku

**Gemini модели:**
- gemini-pro
- gemini-1.5-pro

*Доступность моделей зависит от вашего тарифа и конфигурации ProxyAPI*

### Важные замечания

1. **Ключ ProxyAPI** работает только при отправке запросов на `https://api.proxyapi.ru`
2. При прямом обращении к провайдеру (OpenAI, Anthropic, Gemini) ключ ProxyAPI работать не будет
3. Для работы с ProxyAPI **не требуются** аккаунты у внешних провайдеров
4. Ключ можно увидеть полностью только **один раз** при создании — сохраните его надежно!


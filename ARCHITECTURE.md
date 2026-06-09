# 🏗️ Архитектура Ego-RAG-Agent

**Версия:** 1.0  
**Дата:** 2026.06.08

---

## 📋 Содержание

1. [Обзор системы](#обзор-системы)
2. [Компонентная диаграмма](#компонентная-диаграмма)
3. [Структура проекта](#структура-проекта)
4. [Потоки данных](#потоки-данных)
5. [AI-провайдеры](#ai-провайдеры)
6. [Управление памятью](#управление-памятью)
7. [Хранение данных](#хранение-данных)
8. [Конфигурация](#конфигурация)

---

## Обзор системы

Ego-RAG-Agent — Telegram-бот с Retrieval-Augmented Generation (RAG) для ответа на вопросы на основе корпоративной базы знаний.

### Ключевые возможности

- 🔍 **Поиск по базе знаний** — векторный поиск в ChromaDB
- 🤖 **Множественные AI-провайдеры** — OpenAI, GigaChat, ProxyAPI
- 💬 **Контекстные диалоги** — история сообщений в сессиях
- 📚 **Индексация документов** — загрузка PDF/TXT и создание эмбеддингов

---

## Компонентная диаграмма

```
┌─────────────────────────────────────────────────────────────────┐
│                        Telegram Bot                             │
│                     (interface/telegram_bot.py)                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BotHandlers                                 │
│                   (interface/handlers.py)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  /start     │  │  /help      │  │  /stats     │              │
│  │  /clear     │  │  message    │  │             │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└───────────────────────────┬─────────────────────────────────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
┌──────────────────┐ ┌──────────────  ┐ ┌──────────────────┐
│ SessionManager   │ │ContextRetriever│ │ResponseGenerator │
│ (dialog_control- │ │(memory_mana-   │ │(ai_*/response_   │
│ ler/session_     │ │ ger/)          │ │ generator.py)    │
│ manager.py)      │ │                │ │                  │
└──────────────────┘ └──────┬───────  ┘ └────────┬─────────┘
                            │                  │
                            ▼                  ▼
                   ┌────────────────┐  ┌─────────────────┐
                   │  VectorDatabase│  │  AIClient       │
                   │  (storage/)    │  │  (ai_*/client)  │
                   └────────────────┘  └─────────────────┘
                            │                  │
                            ▼                  ▼
                   ┌──────────────────────────────────┐
                   │           ChromaDB               │
                   │      (vector_db/)                │
                   └──────────────────────────────────┘
```

---

## Структура проекта

```
ego-rag-agent/
├── main.py                      # Точка входа
├── config/                      # Конфигурация
│   ├── __init__.py
│   ├── base_config.py          # BaseAIConfig (базовый класс)
│   └── settings.py             # Settings (основная конфигурация)
│
├── interface/                   # Telegram интерфейс
│   ├── __init__.py
│   ├── telegram_bot.py         # Основной класс бота
│   └── handlers.py             # Обработчики команд
│
├── dialog_controller/           # Управление диалогами
│   ├── __init__.py
│   ├── session_manager.py      # Управление сессиями
│   └── user_context.py         # Контекст пользователя
│
├── memory_manager/              # Управление памятью
│   ├── __init__.py
│   ├── prompt_builder.py       # Утилиты для контекста
│   ├── context_retriever.py    # Поиск в векторной БД
│   └── response_generator.py   # BaseResponseGenerator
│
├── ai_processor/                # OpenAI провайдер
│   ├── __init__.py
│   ├── openai_client.py        # OpenAIClient
│   └── response_generator.py   # ResponseGenerator (OpenAI)
│
├── ai_gigachat_processor/       # GigaChat провайдер
│   ├── __init__.py
│   ├── config.py               # GigaChatConfig
│   ├── gigachat_client.py      # GigaChatClient
│   └── response_generator.py   # ResponseGenerator (GigaChat)
│
├── ai_proxyapi_processor/       # ProxyAPI провайдер
│   ├── __init__.py
│   ├── config.py               # ProxyAPIConfig
│   ├── proxyapi_client.py      # ProxyAPIClient
│   └── response_generator.py   # ResponseGenerator (ProxyAPI)
│
├── storage/                     # Хранение данных
│   ├── __init__.py
│   ├── vector_db.py            # VectorDatabase (ChromaDB)
│   ├── user_db.py              # UserDatabase (JSON)
│   └── document_loader.py      # DocumentLoader (PDF/TXT)
│
├── tools/                       # Утилиты
│   ├── __init__.py
│   └── ingest_documents.py     # Индексация документов
│
├── utils/                       # Утилиты
│   ├── __init__.py
│   └── logging_config.py       # Настройка логирования
│
├── tests/                       # Тесты
│   ├── test_config.py
│   └── test_storage.py
│
├── .env                         # Переменные окружения
├── requirements.txt             # Зависимости
└── README.md                    # Документация
```

---

## Потоки данных

### Обработка вопроса пользователя

```
1. Пользователь отправляет сообщение в Telegram
           │
           ▼
2. BotHandlers.handle_message() получает сообщение
           │
           ▼
3. SessionManager добавляет сообщение в историю
           │
           ▼
4. ContextRetriever.retrieve() ищет релевантные документы
           │
           ▼
5. ResponseGenerator.generate() строит промпт + вызывает AI
           │
           ▼
6. AI-провайдер (OpenAI/GigaChat/ProxyAPI) генерирует ответ
           │
           ▼
7. Ответ сохраняется в историю + отправляется пользователю
```

### Индексация документов

```
1. python -m tools.ingest_documents <файл>
           │
           ▼
2. DocumentLoader.load() читает PDF/TXT
           │
           ▼
3. Текст разбивается на чанки (chunk_size=500, overlap=100)
           │
           ▼
4. SentenceTransformers создает эмбеддинги (локально)
           │
           ▼
5. ChromaDB.add() сохраняет чанки + эмбеддинги
```

---

## AI-провайдеры

### Архитектура абстракции

```
BaseResponseGenerator (memory_manager/)
         │
    ┌────┼────┬─────────────┐
    │    │    │             │
    ▼    ▼    ▼             ▼
OpenAI GigaChat ProxyAPI  ...
```

### Интерфейс AI-провайдера

Все провайдеры реализуют единый интерфейс:

```python
class BaseAIClient:
    def generate_response(
        messages: List[Dict[str, str]],
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        ...
    
    def generate_streaming_response(
        messages: List[Dict[str, str]],
        temperature: float = None,
        max_tokens: int = None
    ) -> Generator[str, None, None]:
        ...
```

### Добавление нового провайдера

1. Создать `ai_<provider>_processor/`
2. Реализовать `<Provider>Client` (наследует логику из `BaseAIClient`)
3. Реализовать `ResponseGenerator` (наследует `BaseResponseGenerator`)
4. Добавить конфиг в `config/`
5. Обновить `main.py:_init_ai_provider()`

---

## Управление памятью

### Сессии

```python
Session:
├── session_id: str
├── user_id: int
├── created_at: datetime
├── last_active: datetime
└── conversation_history: List[Dict]
    ├── {role: "user", content: "...", timestamp: "..."}
    └── {role: "assistant", content: "...", timestamp: "..."}
```

### Очистка сессий

- Фоновая задача удаляет сессии старше `session_timeout` (по умолчанию 1 час)
- Команда `/clear` очищает текущую сессию

---

## Хранение данных

### ChromaDB (векторная БД)

```
Collection: "documents"
├── IDs: UUID
├── Embeddings: float[384] (sentence-transformers)
├── Documents: текст чанка
└── Metadatas:
    ├── source: путь к файлу
    ├── type: тип документа
    └── chunk_id: номер чанка
```

### UserDatabase (JSON)

```json
{
  "users": {
    "123456789": {
      "name": "Иван",
      "message_count": 42,
      "created_at": "2026-01-15T10:30:00",
      "last_active": "2026-06-08T14:20:00"
    }
  }
}
```

---

## Конфигурация

### Иерархия конфигов

```
BaseAIConfig (config/base_config.py)
├── model: str = "gpt-4o-mini"
├── temperature: float = 0.7
├── max_tokens: int = 1000
└── timeout: int = 30

ProxyAPIConfig (наследует BaseAIConfig)
├── api_key: str
├── base_url: str
└── proxy_url: Optional[str]

GigaChatConfig (наследует BaseAIConfig)
├── authorization_key: str
├── scope: str
├── oauth_url: str
├── api_base_url: str
└── verify_ssl: bool
```

### Переменные окружения

```bash
# Telegram
TELEGRAM_BOT_TOKEN=your_token

# AI Provider
AI_PROVIDER=proxyapi  # openai | gigachat | proxyapi

# ProxyAPI
PROXYAPI_API_KEY=your_key
PROXYAPI_MODEL=gpt-4o-mini
PROXYAPI_TEMPERATURE=0.7
PROXYAPI_MAX_TOKENS=1000

# OpenAI
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o-mini

# GigaChat
GIGACHAT_AUTHORIZATION_KEY=your_key
GIGACHAT_MODEL=GigaChat

# RAG
RAG_N_RESULTS=5
CHUNK_SIZE=500
CHUNK_OVERLAP=100

# Session
SESSION_TIMEOUT=3600
```

---

## Безопасность

- API ключи хранятся в `.env` (в `.gitignore`)
- SSL верификация для GigaChat отключена по умолчанию (разработка)
- Валидация всех входных данных

См. `SECURITY.md` для деталей.

---

## Производительность

### Узкие места

1. **Локальные эмбеддинги** — `sentence-transformers` ~2GB RAM
2. **ChromaDB поиск** — O(n) без индексов
3. **AI-запросы** — network latency

### Рекомендации

- Для продакшена: использовать GPU для эмбеддингов
- Кэшировать часто запрашиваемые чанки
- Добавить rate limiting для AI-запросов

---

## Версионирование

| Версия | Изменения |
|--------|-----------|
| 1.0 | Initial release: OpenAI, GigaChat, ProxyAPI, ChromaDB |

---

**См. также:**
- [README.md](README.md) — Основное описание
- [REFACTORING_PLAN.md](REFACTORING_PLAN.md) — План рефакторинга
- [SECURITY.md](SECURITY.md) — Безопасность
- [CONTRIBUTING.md](CONTRIBUTING.md) — Руководство для контрибьюторов

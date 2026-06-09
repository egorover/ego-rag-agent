# 🔄 План рефакторинга проекта Ego-RAG-Agent

**Дата анализа:** 2026.06.08  
**Аналитик:** Koda AI Assistant

---

## 📊 Сводка анализа

| Категория | Количество | Статус |
|-----------|------------|--------|
| Модули AI-процессоров | 3 | ⚠️ Дублирование |
| Конфигурационные классы | 3 | ⚠️ Дублирование |
| ResponseGenerator | 3 | ⚠️ Почти идентичны |
| Клиенты API | 3 | ✅ Разная логика |
| Файлов кода | ~35 | ✅ Приемлемо |

---

## 1. 🚨 КРИТИЧЕСКИЕ ДУБЛИКАТЫ

### 1.1. ResponseGenerator (3 копии)

**Файлы:**
- `ai_processor/response_generator.py` (OpenAI)
- `ai_gigachat_processor/response_generator.py` (GigaChat)
- `ai_proxyapi_processor/response_generator.py` (ProxyAPI)

**Дублирование:** ~90% кода идентично

```python
# ВСЕ ТРИ ФАЙЛА ИМЕЮТ:
class ResponseGenerator:
    DEFAULT_SYSTEM_PROMPT = "..."  # Почти одинаковый
    def __init__(self, client, system_prompt=None):
    def generate(self, query, context_documents, conversation_history):
    def generate_streaming(self, query, context_documents, conversation_history):
    def _build_messages(...)  # Логика построения сообщений
```

**Проблема:**
- При изменении логики нужно править 3 файла
- Разные системные промпты создают несогласованность
- Дублирование форматирования контекста

**Решение:**
```
Создать единый BaseResponseGenerator в memory_manager/
Каждый процессор наследуется и переопределяет только client-specific методы
```

---

### 1.2. Конфигурационные классы (3 копии)

**Файлы:**
- `config/settings.py` (главная конфигурация)
- `ai_proxyapi_processor/config.py` (ProxyAPIConfig)
- `ai_gigachat_processor/config.py` (GigaChatConfig)

**Дублирование:**

```python
# ВСЕ ТРИ ИМЕЮТ:
@dataclass
class XXXConfig:
    model: str = "..."
    temperature: float = 0.7
    max_tokens: int = 1000
    
    @classmethod
    def from_env(cls):
        # Почти одинаковый код чтения из os.getenv()
```

**Проблема:**
- Изменение параметра требует правки в 3 местах
- Несогласованные значения по умолчанию
- Дублирование логики валидации

**Решение:**
```
Создать BaseAIConfig с общими полями
Каждый специфичный конфиг наследуется и добавляет свои поля
```

---

### 1.3. Клиенты API (разная логика, но одинаковая структура)

**Файлы:**
- `ai_processor/openai_client.py`
- `ai_gigachat_processor/gigachat_client.py`
- `ai_proxyapi_processor/proxyapi_client.py`

**Дублирование структуры:**

```python
class XXXClient:
    def __init__(self, api_key, model, temperature, max_tokens):
    def generate_response(self, messages, temperature=None, max_tokens=None):
    def generate_streaming_response(self, messages, ...):
```

**Оценка:** ✅ Структурное дублирование ОПРАВДАНО — разная реализация запросов

---

## 2. ⚠️ ВОЗМОЖНОСТИ УПРОЩЕНИЯ

### 2.1. Удалить предустановленные конфигурации

**Файлы:**
- `ai_proxyapi_processor/config.py` (4 конфигурации)
- `ai_gigachat_processor/config.py` (5 конфигураций)

```python
# ПРИМЕР ДУБЛИРОВАНИЯ:
PROXYAPI_BASE_CONFIG = ProxyAPIConfig(api_key="YOUR_API_KEY_HERE", ...)
PROXYAPI_ADVANCED_CONFIG = ProxyAPIConfig(api_key="YOUR_API_KEY_HERE", ...)
PROXYAPI_CREATIVE_CONFIG = ProxyAPIConfig(api_key="YOUR_API_KEY_HERE", ...)
PROXYAPI_PRECISE_CONFIG = ProxyAPIConfig(api_key="YOUR_API_KEY_HERE", ...)
```

**Проблема:**
- Никто не использует (нет импортов в коде)
- Загромождают код
- Требуют поддержки

**Решение:** УДАЛИТЬ все предустановленные конфигурации

---

### 2.2. Упростить PromptBuilder

**Файл:** `memory_manager/prompt_builder.py`

**Проблема:** Класс содержит методы, которые дублируют логику в ResponseGenerator:

```python
# prompt_builder.py
def build_context_from_documents(self, documents):
def build_messages_for_ai(self, query, context_documents, history):

# response_generator.py (каждый из 3-х!)
def _build_messages(self, query, context_documents, history):
    # ИДЕНТИЧНАЯ ЛОГИКА
```

**Решение:**
```
Перенести _build_messages в PromptBuilder
ResponseGenerator использует PromptBuilder
```

---

### 2.3. Упростить ContextRetriever

**Файл:** `memory_manager/context_retriever.py`

**Проблема:** Методы редко используются:

```python
def retrieve_with_threshold(self, query, relevance_threshold):  # Не используется
def get_sources(self, documents):  # Не используется
```

**Проверка:**
- `retrieve_with_threshold` — 0 вызовов в коде
- `get_sources` — 0 вызовов в коде

**Решение:**
```
УДАЛИТЬ неиспользуемые методы
Оставить только retrieve()
```

---

### 2.4. Упростить main.py

**Файл:** `main.py`

**Проблема:** Функция `initialize_components` слишком большая (100+ строк)

```python
def initialize_components(settings):
    # 1. Storage (10 строк)
    # 2. AI Processor (60 строк if/elif)
    # 3. Memory Manager (10 строк)
    # 4. Dialog Controller (5 строк)
    # 5. Interface (5 строк)
```

**Решение:**
```
Разбить на подфункции:
- _init_storage(settings)
- _init_ai_provider(settings)
- _init_memory_manager(settings)
- _init_dialog_controller(settings)
- _init_interface(settings)
```

---

### 2.5. Убрать дублирование системных промптов

**Где:**
- `ai_processor/response_generator.py`
- `ai_gigachat_processor/response_generator.py`
- `ai_proxyapi_processor/response_generator.py`

**Проблема:**
```python
# ВСЕ ТРИ ИМЕЮТ ПОЧТИ ИДЕНТИЧНЫЕ ПРОМПТЫ
DEFAULT_SYSTEM_PROMPT = """Ты - полезный AI ассистент...
1. Используй ТОЛЬКО информацию...
2. Если информации недостаточно...
..."""
```

**Решение:**
```
Создать единый файл prompts.py
Хранить все системные промпты в одном месте
```

---

## 3. 📋 ПЛАН РЕФАКТОРИНГА

### Этап 1: Удаление мусора (1-2 часа)

| Действие | Файлы | Риск |
|----------|-------|------|
| Удалить предустановленные конфигурации | `ai_*/config.py` | Низкий |
| Удалить неиспользуемые методы ContextRetriever | `memory_manager/context_retriever.py` | Низкий |
| Проверить тесты на покрытие | `tests/` | Средний |

**Результат:** -100 строк кода, чище код

---

### Этап 2: Объединение дубликатов (3-4 часа)

| Действие | Файлы | Риск |
|----------|-------|------|
| Создать BaseResponseGenerator | `memory_manager/response_generator.py` | Высокий |
| Перенести логику _build_messages | `ai_*/response_generator.py` | Высокий |
| Упростить main.py | `main.py` | Средний |
| Создать единые системные промпты | `memory_manager/prompts.py` | Низкий |

**Результат:** -300 строк, единая точка изменений

---

### Этап 3: Оптимизация конфигурации (2-3 часа)

| Действие | Файлы | Риск |
|----------|-------|------|
| Создать BaseAIConfig | `config/base_config.py` | Средний |
| Переписать ProxyAPIConfig/GigaChatConfig | `ai_*/config.py` | Средний |
| Обновить Settings.from_env() | `config/settings.py` | Низкий |

**Результат:** -150 строк, согласованная конфигурация

---

### Этап 4: Тестирование (2-3 часа)

| Действие | Файлы | Риск |
|----------|-------|------|
| Запустить все тесты | `pytest tests/` | - |
| Проверить ручной запуск бота | `python main.py` | - |
| Проверить индексацию | `python -m tools.ingest_documents` | - |

**Результат:** Гарантия работоспособности

---

## 4. 📈 ОЖИДАЕМЫЕ РЕЗУЛЬТАТЫ

| Метрика | До | После | Изменение |
|---------|-----|-------|-----------|
| Строки кода | ~3500 | ~2500 | -28% |
| ResponseGenerator файлы | 3 | 1 + наследники | -66% |
| Конфигурационных классов | 6 | 1 базовый + 2 специфичных | -33% |
| Дублирование кода | ~40% | ~10% | -75% |
| Тестов | 10 | 15+ | +50% |

---

## 5. ⚠️ РИСКИ И МИТИГАЦИЯ

| Риск | Вероятность | Митигация |
|------|-------------|-----------|
| Поломка тестов | Средняя | Полный регрессионный тест |
| Несовместимость API | Низкая | Сохранить интерфейсы |
| Потеря функциональности | Низкая | Пошаговый рефакторинг |
| Ошибки в наследовании | Средняя | Unit-тесты для каждого провайдера |

---

## 6. 🧪 СТРАТЕГИЯ ТЕСТИРОВАНИЯ

### 6.1. Автоматические тесты (добавить)

```python
# tests/test_response_generator.py
def test_openai_response_generator():
def test_gigachat_response_generator():
def test_proxyapi_response_generator():
def test_all_generators_have_same_interface():

# tests/test_config.py
def test_base_config_inheritance():
def test_all_configs_from_env():
```

### 6.2. Ручное тестирование

1. Запустить бота с OpenAI
2. Запустить бота с GigaChat
3. Запустить бота с ProxyAPI
4. Проверить все команды: /start, /help, /stats, /clear
5. Отправить вопрос с контекстом
6. Проверить streaming ответ

---

## 7. 📝 КОНКРЕТНЫЕ ШАГИ

### ШАГ 1: Создать BaseResponseGenerator

**Новый файл:** `memory_manager/response_generator.py`

```python
class BaseResponseGenerator:
    DEFAULT_SYSTEM_PROMPT = "..."  # Единый промпт
    
    def __init__(self, client):
        self.client = client
        self.system_prompt = self.DEFAULT_SYSTEM_PROMPT
    
    def generate(self, query, context_documents, conversation_history):
        messages = self._build_messages(query, context_documents, conversation_history)
        return self.client.generate_response(messages)
    
    def generate_streaming(self, query, context_documents, conversation_history):
        messages = self._build_messages(query, context_documents, conversation_history)
        yield from self.client.generate_streaming_response(messages)
    
    def _build_messages(self, query, context_documents, conversation_history):
        # ЕДИНАЯ ЛОГИКА построения сообщений
        ...
```

**Изменить:**
- `ai_processor/response_generator.py` — наследуется от BaseResponseGenerator
- `ai_gigachat_processor/response_generator.py` — наследуется
- `ai_proxyapi_processor/response_generator.py` — наследуется

---

### ШАГ 2: Создать BaseAIConfig

**Новый файл:** `config/base_config.py`

```python
@dataclass
class BaseAIConfig:
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 1000
    timeout: int = 30
    
    @classmethod
    def from_env(cls, prefix):
        return cls(
            model=os.getenv(f"{prefix}_MODEL", cls.model),
            temperature=float(os.getenv(f"{prefix}_TEMPERATURE", cls.temperature)),
            max_tokens=int(os.getenv(f"{prefix}_MAX_TOKENS", cls.max_tokens)),
        )
```

**Изменить:**
- `ai_proxyapi_processor/config.py` — наследуется от BaseAIConfig
- `ai_gigachat_processor/config.py` — наследуется

---

### ШАГ 3: Упростить main.py

```python
def _init_ai_provider(settings: Settings):
    if settings.ai_provider == "openai":
        return _init_openai(settings)
    elif settings.ai_provider == "gigachat":
        return _init_gigachat(settings)
    elif settings.ai_provider == "proxyapi":
        return _init_proxyapi(settings)

def _init_openai(settings):
    # 10 строк вместо 20
```

---

## 8. 🚦 РЕКОМЕНДАЦИИ

### Приоритет 1 (КРИТИЧНО):
- ✅ Удалить предустановленные конфигурации
- ✅ Удалить неиспользуемые методы ContextRetriever
- ✅ Объединить ResponseGenerator

### Приоритет 2 (ВАЖНО):
- ✅ Создать BaseAIConfig
- ✅ Упростить main.py
- ✅ Создать единые промпты

### Приоритет 3 (ОПЦИОНАЛЬНО):
- ⚪ Добавить больше тестов
- ⚪ Рефакторинг документаци
- ⚪ Оптимизация производительности

---

## 9. ✅ ЧЕКЛИСТ ГОТОВНОСТИ

Перед началом рефакторинга:

- [ ] Все тесты проходят (`pytest tests/`)
- [ ] Бот запускается и работает (`python main.py`)
- [ ] Индексация работает (`python -m tools.ingest_documents`)
- [ ] Создан бэкап кода (git commit)
- [ ] Подготовлена ветка для рефакторинга

После рефакторинга:

- [ ] Все тесты проходят
- [ ] Бот запускается с OpenAI
- [ ] Бот запускается с GigaChat
- [ ] Бот запускается с ProxyAPI
- [ ] Индексация работает
- [ ] Нет предупреждений в логах
- [ ] Код прошел security_scan

---

**Примечание:** SPECIFICATION.md не найден в проекте. Рефакторинг основан на анализе фактического кода.

**Рекомендация:** Перед началом рефакторинга создайте ветку:
```bash
git checkout -b refactor/cleanup-2026-06-08
```

---

**Готов к выполнению рефакторинга по вашей команде!**

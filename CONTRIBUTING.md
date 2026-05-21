# Руководство для разработчиков

## Структура проекта

```
ego-rag-agent/
├── ai_processor/           # OpenAI процессор
├── ai_gigachat_processor/  # GigaChat процессор
├── ai_proxyapi_processor/  # ProxyAPI процессор
├── config/                 # Конфигурация
├── storage/                # Хранилища данных
├── dialog_controller/      # Управление диалогами
├── memory_manager/         # Управление памятью
├── interface/              # Telegram бот
├── utils/                  # Утилиты
└── tools/                  # Утилиты (индексация и т.д.)
```

## Добавление нового AI провайдера

1. Создайте новую директорию `ai_newprovider_processor/`
2. Создайте файлы:
   - `__init__.py` - экспорт классов
   - `config.py` - конфигурация
   - `newprovider_client.py` - клиент API
   - `response_generator.py` - генератор ответов

3. Пример структуры:

```python
# config.py
from dataclasses import dataclass

@dataclass
class NewProviderConfig:
    api_key: str
    model: str = "model-name"
    temperature: float = 0.7
    max_tokens: int = 1000
```

4. Обновите `config/settings.py` - добавьте настройки
5. Обновите `main.py` - добавьте инициализацию
6. Добавьте переменные в `.env.example`

## Стандарты кода

- Используйте type hints
- Документируйте функции docstrings
- Следуйте PEP 8
- Используйте async/async где возможно

## Переменные окружения

Все API ключи должны храниться в `.env`:

```env
PROVIDER_API_KEY=your_key_here
PROVIDER_MODEL=model-name
PROVIDER_TEMPERATURE=0.7
```

Никогда не коммитьте реальные ключи!

## Тестирование

Перед коммитом проверьте:

```bash
# Синтаксис Python
python -m compileall .

# Импорт всех модулей
python -c "import config; import ai_processor; ..."
```

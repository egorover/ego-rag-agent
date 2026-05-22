# Тесты проекта

## Запуск тестов

```bash
# Активация виртуального окружения
.\.venv\Scripts\Activate.ps1

# Запуск всех тестов
python -m unittest discover tests -v

# Запуск конкретного теста
python -m unittest tests.test_config -v
```

## Структура тестов

| Файл | Описание |
|------|----------|
| `test_config.py` | Настройки, провайдеры, `validate()`, ingest |
| `test_storage.py` | Локальные эмбеддинги и ChromaDB (без внешних API) |

```bash
python -m pytest tests/ -v
```

## Добавление новых тестов

1. Создайте файл `test_*.py` в директории `tests/`
2. Используйте `unittest` framework
3. Добавьте тесты в `__init__.py` если нужно

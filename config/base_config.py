"""
Базовые конфигурации для AI-провайдеров.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class BaseAIConfig:
    """Базовая конфигурация для всех AI-провайдеров."""
    
    # Общие параметры модели
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 1000
    
    # Timeout для запросов (в секундах)
    timeout: int = 30
    
    @classmethod
    def _get_env_float(cls, key: str, default: float) -> float:
        """Получает float из переменной окружения."""
        try:
            return float(os.getenv(key, str(default)))
        except (ValueError, TypeError):
            return default
    
    @classmethod
    def _get_env_int(cls, key: str, default: int) -> int:
        """Получает int из переменной окружения."""
        try:
            return int(os.getenv(key, str(default)))
        except (ValueError, TypeError):
            return default

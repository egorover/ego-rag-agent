"""
Конфигурация для GigaChat клиента.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class GigaChatConfig:
    """Конфигурация для GigaChat API."""
    
    # Аутентификация
    authorization_key: str
    scope: str = "GIGACHAT_API_PERS"
    
    # Параметры модели
    model: str = "GigaChat"  # GigaChat, GigaChat-Pro, GigaChat-Plus
    temperature: float = 0.7
    max_tokens: int = 1000
    
    # API endpoints
    oauth_url: str = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    api_base_url: str = "https://gigachat.devices.sberbank.ru/api/v1"
    
    # SSL верификация
    verify_ssl: bool = True
    
    # Timeout для запросов (в секундах)
    timeout: int = 30
    
    @classmethod
    def from_env(cls) -> "GigaChatConfig":
        """
        Создает конфигурацию из переменных окружения.
        
        Переменные окружения:
        - GIGACHAT_AUTHORIZATION_KEY: authorization key
        - GIGACHAT_MODEL: модель (опционально)
        - GIGACHAT_TEMPERATURE: температура (опционально)
        - GIGACHAT_MAX_TOKENS: макс токены (опционально)
        """
        import os
        
        auth_key = os.getenv("GIGACHAT_AUTHORIZATION_KEY")
        if not auth_key:
            raise ValueError("GIGACHAT_AUTHORIZATION_KEY не установлена")

        auth_key = auth_key.strip()
        if auth_key.lower().startswith("basic "):
            auth_key = auth_key[6:].strip()

        return cls(
            authorization_key=auth_key,
            model=os.getenv("GIGACHAT_MODEL", "GigaChat"),
            temperature=float(os.getenv("GIGACHAT_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("GIGACHAT_MAX_TOKENS", "1000"))
        )



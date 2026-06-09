"""
Конфигурация для GigaChat клиента.
"""

from dataclasses import dataclass, field
from typing import Optional

from config.base_config import BaseAIConfig


@dataclass
class GigaChatConfig(BaseAIConfig):
    """Конфигурация для GigaChat API."""
    
    # Аутентификация (обязательный параметр)
    authorization_key: str = field(default="")  # Пустой дефолт, проверяется в from_env
    
    # Дополнительные поля GigaChat
    scope: str = "GIGACHAT_API_PERS"
    oauth_url: str = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    api_base_url: str = "https://gigachat.devices.sberbank.ru/api/v1"
    verify_ssl: bool = True
    
    @classmethod
    def from_env(cls) -> "GigaChatConfig":
        """
        Создает конфигурацию из переменных окружения.
        
        Переменные окружения:
        - GIGACHAT_AUTHORIZATION_KEY: authorization key
        - GIGACHAT_MODEL: модель (опционально)
        - GIGACHAT_TEMPERATURE: температура (опционально)
        - GIGACHAT_MAX_TOKENS: макс токены (опционально)
        - GIGACHAT_TIMEOUT: timeout (опционально)
        - GIGACHAT_SCOPE: область доступа (опционально)
        """
        auth_key = os.getenv("GIGACHAT_AUTHORIZATION_KEY")
        if not auth_key:
            raise ValueError("GIGACHAT_AUTHORIZATION_KEY не установлена")

        auth_key = auth_key.strip()
        if auth_key.lower().startswith("basic "):
            auth_key = auth_key[6:].strip()

        return cls(
            authorization_key=auth_key,
            model=os.getenv("GIGACHAT_MODEL", cls.model),
            temperature=cls._get_env_float("GIGACHAT_TEMPERATURE", cls.temperature),
            max_tokens=cls._get_env_int("GIGACHAT_MAX_TOKENS", cls.max_tokens),
            timeout=cls._get_env_int("GIGACHAT_TIMEOUT", cls.timeout),
            scope=os.getenv("GIGACHAT_SCOPE", cls.scope),
        )



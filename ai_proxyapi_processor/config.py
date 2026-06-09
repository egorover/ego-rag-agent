"""
Конфигурация для ProxyAPI клиента.
"""

from dataclasses import dataclass, field
from typing import Optional

from config.base_config import BaseAIConfig


@dataclass
class ProxyAPIConfig(BaseAIConfig):
    """Конфигурация для ProxyAPI."""
    
    # Аутентификация (обязательный параметр)
    # Используем field(default_factory) чтобы обойти ограничение dataclass
    api_key: str = field(default="")  # Пустой дефолт, проверяется в from_env
    
    # API endpoint
    base_url: str = "https://api.proxyapi.ru"
    
    # Прокси настройки (опционально)
    proxy_url: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> "ProxyAPIConfig":
        """
        Создает конфигурацию из переменных окружения.
        
        Переменные окружения:
        - PROXYAPI_API_KEY: API ключ ProxyAPI
        - PROXYAPI_MODEL: модель (опционально)
        - PROXYAPI_TEMPERATURE: температура (опционально)
        - PROXYAPI_MAX_TOKENS: макс токены (опционально)
        - PROXYAPI_BASE_URL: базовый URL (опционально)
        - PROXYAPI_PROXY_URL: URL прокси (опционально)
        - PROXYAPI_TIMEOUT: timeout (опционально)
        """
        api_key = os.getenv("PROXYAPI_API_KEY")
        if not api_key:
            raise ValueError("PROXYAPI_API_KEY не установлена")
        
        return cls(
            api_key=api_key,
            model=os.getenv("PROXYAPI_MODEL", cls.model),
            temperature=cls._get_env_float("PROXYAPI_TEMPERATURE", cls.temperature),
            max_tokens=cls._get_env_int("PROXYAPI_MAX_TOKENS", cls.max_tokens),
            timeout=cls._get_env_int("PROXYAPI_TIMEOUT", cls.timeout),
            base_url=os.getenv("PROXYAPI_BASE_URL", cls.base_url),
            proxy_url=os.getenv("PROXYAPI_PROXY_URL"),
        )


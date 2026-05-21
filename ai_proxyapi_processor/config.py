"""
Конфигурация для ProxyAPI клиента.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ProxyAPIConfig:
    """Конфигурация для ProxyAPI."""
    
    # Аутентификация
    api_key: str
    
    # Параметры модели
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 1000
    
    # API endpoint
    base_url: str = "https://proxyapi.example.com/v1"
    
    # Timeout для запросов (в секундах)
    timeout: int = 30
    
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
        """
        import os
        
        api_key = os.getenv("PROXYAPI_API_KEY")
        if not api_key:
            raise ValueError("PROXYAPI_API_KEY не установлена")
        
        return cls(
            api_key=api_key,
            model=os.getenv("PROXYAPI_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("PROXYAPI_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("PROXYAPI_MAX_TOKENS", "1000")),
            base_url=os.getenv("PROXYAPI_BASE_URL", "https://proxyapi.example.com/v1"),
            proxy_url=os.getenv("PROXYAPI_PROXY_URL"),
        )


# Предустановленные конфигурации

# Конфигурация для базовой модели
PROXYAPI_BASE_CONFIG = ProxyAPIConfig(
    api_key="YOUR_API_KEY_HERE",
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=1000
)

# Конфигурация для продвинутой модели
PROXYAPI_ADVANCED_CONFIG = ProxyAPIConfig(
    api_key="YOUR_API_KEY_HERE",
    model="gpt-4-turbo",
    temperature=0.7,
    max_tokens=2000
)

# Конфигурация для креативных задач
PROXYAPI_CREATIVE_CONFIG = ProxyAPIConfig(
    api_key="YOUR_API_KEY_HERE",
    model="gpt-4o",
    temperature=1.2,
    max_tokens=2000
)

# Конфигурация для точных ответов
PROXYAPI_PRECISE_CONFIG = ProxyAPIConfig(
    api_key="YOUR_API_KEY_HERE",
    model="gpt-4o-mini",
    temperature=0.3,
    max_tokens=1000
)

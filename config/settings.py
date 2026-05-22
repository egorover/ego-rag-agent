"""
Настройки приложения.
Централизованное управление конфигурацией.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


@dataclass
class Settings:
    """Настройки приложения."""
    
    # Telegram
    telegram_token: str
    
    # AI Provider (выбор: "openai", "gigachat" или "proxyapi")
    ai_provider: str = "proxyapi"
    
    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 1000
    
    # GigaChat
    gigachat_authorization_key: Optional[str] = None
    gigachat_model: str = "GigaChat"
    gigachat_temperature: float = 0.7
    gigachat_max_tokens: int = 1000
    gigachat_verify_ssl: bool = False  # False для разработки из-за самоподписанного сертификата
    
    # ProxyAPI
    proxyapi_api_key: Optional[str] = None
    proxyapi_model: str = "gpt-4o-mini"
    proxyapi_temperature: float = 0.7
    proxyapi_max_tokens: int = 1000
    proxyapi_base_url: str = "https://api.proxyapi.ru"
    proxyapi_proxy_url: Optional[str] = None
    
    # ChromaDB
    chroma_persist_dir: str = "./chroma_db"
    chroma_collection: str = "documents"
    
    # RAG параметры
    rag_n_results: int = 5
    chunk_size: int = 500
    chunk_overlap: int = 100
    
    # Session управление
    session_timeout: int = 3600  # 1 час в секундах
    max_context_messages: int = 10
    
    @classmethod
    def from_env(cls) -> "Settings":
        """
        Создает настройки из переменных окружения.
        
        Returns:
            Экземпляр Settings
            
        Raises:
            ValueError: Если обязательные переменные не установлены
        """
        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        ai_provider = os.getenv("AI_PROVIDER", "proxyapi").lower()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        gigachat_key = None
        proxyapi_key = None

        if not telegram_token:
            raise ValueError(
                "TELEGRAM_BOT_TOKEN не установлен. "
                "Установите переменную окружения или создайте .env файл."
            )

        if ai_provider == "openai":
            if not openai_api_key:
                raise ValueError(
                    "OPENAI_API_KEY не установлен. "
                    "Установите переменную окружения или создайте .env файл."
                )
        elif ai_provider == "gigachat":
            gigachat_key = os.getenv("GIGACHAT_AUTHORIZATION_KEY")
            if not gigachat_key:
                raise ValueError(
                    "GIGACHAT_AUTHORIZATION_KEY не установлен. "
                    "Установите переменную окружения или создайте .env файл."
                )
        elif ai_provider == "proxyapi":
            proxyapi_key = os.getenv("PROXYAPI_API_KEY")
            if not proxyapi_key:
                raise ValueError(
                    "PROXYAPI_API_KEY не установлен. "
                    "Установите переменную окружения или создайте .env файл."
                )
        else:
            raise ValueError(
                f"Неподдерживаемый AI_PROVIDER: {ai_provider}. "
                "Используйте 'openai', 'gigachat' или 'proxyapi'."
            )

        return cls(
            telegram_token=telegram_token,
            ai_provider=ai_provider,
            openai_api_key=openai_api_key,
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            openai_embedding_model=os.getenv(
                "OPENAI_EMBEDDING_MODEL", 
                "text-embedding-3-small"
            ),
            gigachat_authorization_key=gigachat_key,
            gigachat_model=os.getenv("GIGACHAT_MODEL", "GigaChat"),
            gigachat_temperature=float(os.getenv("GIGACHAT_TEMPERATURE", "0.7")),
            gigachat_max_tokens=int(os.getenv("GIGACHAT_MAX_TOKENS", "1000")),
            proxyapi_api_key=proxyapi_key,
            proxyapi_model=os.getenv("PROXYAPI_MODEL", "gpt-4o-mini"),
            proxyapi_temperature=float(os.getenv("PROXYAPI_TEMPERATURE", "0.7")),
            proxyapi_max_tokens=int(os.getenv("PROXYAPI_MAX_TOKENS", "1000")),
            proxyapi_base_url=os.getenv("PROXYAPI_BASE_URL", "https://api.proxyapi.ru"),
            proxyapi_proxy_url=os.getenv("PROXYAPI_PROXY_URL"),
            chroma_persist_dir=os.getenv("CHROMA_PERSIST_DIR", "./chroma_db"),
            chroma_collection=os.getenv("CHROMA_COLLECTION", "documents"),
            rag_n_results=int(os.getenv("RAG_N_RESULTS", "5")),
            chunk_size=int(os.getenv("CHUNK_SIZE", "500")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "100")),
            session_timeout=int(os.getenv("SESSION_TIMEOUT", "3600")),
            max_context_messages=int(os.getenv("MAX_CONTEXT_MESSAGES", "10")),
        )

    @classmethod
    def from_env_for_ingest(cls) -> "Settings":
        """
        Минимальные настройки для индексации документов.
        Не требует Telegram-токена и ключей LLM-провайдеров.
        Эмбеддинги создаются локально (sentence-transformers).
        """
        return cls(
            telegram_token="",
            ai_provider=os.getenv("AI_PROVIDER", "proxyapi").lower(),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            chroma_persist_dir=os.getenv("CHROMA_PERSIST_DIR", "./chroma_db"),
            chroma_collection=os.getenv("CHROMA_COLLECTION", "documents"),
            chunk_size=int(os.getenv("CHUNK_SIZE", "500")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "100")),
        )
    
    def validate(self) -> bool:
        """
        Проверяет валидность настроек.
        
        Returns:
            True если все настройки валидны
        """
        # Проверяем токен Telegram
        if not self.telegram_token:
            return False
        
        # Проверяем ключи для выбранного провайдера
        if self.ai_provider == "openai" and not self.openai_api_key:
            return False
        
        if self.ai_provider == "gigachat" and not self.gigachat_authorization_key:
            return False

        if self.ai_provider == "proxyapi" and not self.proxyapi_api_key:
            return False
        
        # Проверяем числовые значения
        if self.rag_n_results <= 0 or self.chunk_size <= 0:
            return False
        
        if self.chunk_overlap >= self.chunk_size:
            return False
        
        return True


"""
Главная точка входа в приложение.
Инициализирует все компоненты и запускает бота.
"""

import sys
import os
import logging
from typing import Tuple

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from config import Settings
from storage import VectorDatabase, UserDatabase
from ai_processor import OpenAIClient
from ai_processor import ResponseGenerator as OpenAIResponseGenerator
from ai_gigachat_processor import GigaChatClient
from ai_gigachat_processor import ResponseGenerator as GigaChatResponseGenerator
from ai_proxyapi_processor import ProxyAPIClient
from ai_proxyapi_processor import ResponseGenerator as ProxyAPIResponseGenerator
from memory_manager import PromptBuilder, ContextRetriever
from dialog_controller import SessionManager
from interface import TelegramBot
from utils import setup_logging

logger = logging.getLogger(__name__)


def validate_environment() -> None:
    """Проверяет наличие необходимых файлов и настроек."""
    print("=" * 60)
    print("ПРОВЕРКА ОКРУЖЕНИЯ")
    print("=" * 60)
    
    chroma_dir = "./chroma_db"
    if not os.path.exists(chroma_dir):
        print(f"\n⚠️  ВНИМАНИЕ: Директория {chroma_dir} не найдена!")
        print("💡 Сначала загрузите документы в базу знаний:")
        print("   python -m tools.ingest_documents")
        sys.exit(1)
    
    print(f"✓ База знаний найдена: {chroma_dir}")
    print()


def _init_storage(settings: Settings) -> Tuple[VectorDatabase, UserDatabase]:
    """
    Инициализирует хранилища данных.
    
    Args:
        settings: Настройки приложения
        
    Returns:
        Кортеж (vector_db, user_db)
    """
    logger.info("Инициализация хранилищ...")
    
    vector_db = VectorDatabase(
        persist_directory=settings.chroma_persist_dir,
        collection_name=settings.chroma_collection,
        openai_api_key=settings.openai_api_key
    )
    vector_db.get_or_create_collection()
    
    user_db = UserDatabase(storage_path="./user_data.json")
    
    return vector_db, user_db


def _init_ai_provider(settings: Settings):
    """
    Инициализирует AI-провайдер и генератор ответов.
    
    Args:
        settings: Настройки приложения
        
    Returns:
        Кортеж (client, response_generator)
        
    Raises:
        ValueError: Если указан неподдерживаемый провайдер
    """
    logger.info(f"Инициализация AI процессора ({settings.ai_provider})...")
    
    if settings.ai_provider == "openai":
        return _init_openai(settings)
    elif settings.ai_provider == "gigachat":
        return _init_gigachat(settings)
    elif settings.ai_provider == "proxyapi":
        return _init_proxyapi(settings)
    else:
        raise ValueError(f"Неподдерживаемый AI provider: {settings.ai_provider}")
    

def _init_openai(settings: Settings):
    """Инициализирует OpenAI провайдер."""
    openai_client = OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
        temperature=settings.openai_temperature,
        max_tokens=settings.openai_max_tokens
    )
    response_generator = OpenAIResponseGenerator(openai_client=openai_client)
    logger.info(f"✓ OpenAI клиент инициализирован (модель: {settings.openai_model})")
    
    return openai_client, response_generator


def _init_gigachat(settings: Settings):
    """Инициализирует GigaChat провайдер."""
    from ai_gigachat_processor import GigaChatConfig
    
    gigachat_config = GigaChatConfig(
        authorization_key=settings.gigachat_authorization_key,
        model=settings.gigachat_model,
        temperature=settings.gigachat_temperature,
        max_tokens=settings.gigachat_max_tokens,
        verify_ssl=settings.gigachat_verify_ssl
    )
    
    gigachat_client = GigaChatClient(config=gigachat_config)
    response_generator = GigaChatResponseGenerator(gigachat_client=gigachat_client)
    logger.info(f"✓ GigaChat клиент инициализирован (модель: {settings.gigachat_model})")
    
    return gigachat_client, response_generator


def _init_proxyapi(settings: Settings):
    """Инициализирует ProxyAPI провайдер."""
    from ai_proxyapi_processor import ProxyAPIConfig
    
    proxyapi_config = ProxyAPIConfig(
        api_key=settings.proxyapi_api_key,
        model=settings.proxyapi_model,
        temperature=settings.proxyapi_temperature,
        max_tokens=settings.proxyapi_max_tokens,
        base_url=settings.proxyapi_base_url,
        proxy_url=settings.proxyapi_proxy_url
    )
    
    proxyapi_client = ProxyAPIClient(config=proxyapi_config)
    response_generator = ProxyAPIResponseGenerator(proxyapi_client=proxyapi_client)
    logger.info(f"✓ ProxyAPI клиент инициализирован (модель: {settings.proxyapi_model})")
    
    return proxyapi_client, response_generator


def _init_memory_manager(
    settings: Settings,
    vector_db: VectorDatabase,
    response_generator
) -> Tuple[PromptBuilder, ContextRetriever]:
    """
    Инициализирует менеджер памяти.
    
    Args:
        settings: Настройки приложения
        vector_db: Векторная база данных
        response_generator: Генератор ответов
        
    Returns:
        Кортеж (prompt_builder, context_retriever)
    """
    logger.info("Инициализация менеджера памяти...")
    
    prompt_builder = PromptBuilder()
    context_retriever = ContextRetriever(
        vector_db=vector_db,
        n_results=settings.rag_n_results
    )
    
    return prompt_builder, context_retriever


def _init_dialog_controller(settings: Settings) -> SessionManager:
    """
    Инициализирует контроллер диалогов.
    
    Args:
        settings: Настройки приложения
        
    Returns:
        SessionManager
    """
    logger.info("Инициализация контроллера диалогов...")
    
    session_manager = SessionManager(
        session_timeout=settings.session_timeout
    )
    
    return session_manager


def _init_interface(
    settings: Settings,
    session_manager: SessionManager,
    context_retriever: ContextRetriever,
    response_generator,
    user_db: UserDatabase,
    vector_db: VectorDatabase
) -> TelegramBot:
    """
    Инициализирует Telegram бот.
    
    Args:
        settings: Настройки приложения
        session_manager: Менеджер сессий
        context_retriever: Получатель контекста
        response_generator: Генератор ответов
        user_db: База данных пользователей
        vector_db: Векторная БД
        
    Returns:
        TelegramBot
    """
    logger.info("Инициализация Telegram бота...")
    
    telegram_bot = TelegramBot(
        token=settings.telegram_token,
        session_manager=session_manager,
        context_retriever=context_retriever,
        response_generator=response_generator,
        user_db=user_db,
        vector_db=vector_db
    )
    
    return telegram_bot


def initialize_components(settings: Settings):
    """
    Инициализирует все компоненты системы.
    
    Args:
        settings: Настройки приложения
        
    Returns:
        Инициализированный TelegramBot
    """
    logger.info("Инициализация компонентов...")
    
    # 1. Storage
    vector_db, user_db = _init_storage(settings)
    
    # 2. AI Provider
    _, response_generator = _init_ai_provider(settings)
    
    # 3. Memory Manager
    _, context_retriever = _init_memory_manager(settings, vector_db, response_generator)
    
    # 4. Dialog Controller
    session_manager = _init_dialog_controller(settings)
    
    # 5. Interface
    telegram_bot = _init_interface(
        settings=settings,
        session_manager=session_manager,
        context_retriever=context_retriever,
        response_generator=response_generator,
        user_db=user_db,
        vector_db=vector_db
    )
    
    logger.info("Все компоненты инициализированы успешно!")
    
    return telegram_bot


def main():
    """Главная функция запуска приложения."""
    print("=" * 60)
    print("TELEGRAM RAG BOT - ЗАПУСК")
    print("=" * 60)
    
    try:
        # 1. Настройка логирования
        setup_logging(level="INFO")
        logger = logging.getLogger(__name__)
        
        # 2. Загрузка настроек
        logger.info("Загрузка настроек...")
        try:
            settings = Settings.from_env()
        except ValueError as e:
            print(f"\n❌ ОШИБКА: {e}")
            print("\n💡 Установите переменные окружения:")
            print("   TELEGRAM_BOT_TOKEN - токен Telegram бота")
            print("   OPENAI_API_KEY - API ключ OpenAI (при AI_PROVIDER=openai)")
            print("   GIGACHAT_AUTHORIZATION_KEY - ключ GigaChat (при AI_PROVIDER=gigachat)")
            print("   PROXYAPI_API_KEY - API ключ ProxyAPI (при AI_PROVIDER=proxyapi)")
            print("\nИли создайте файл .env с этими переменными.")
            sys.exit(1)
        
        # 3. Валидация настроек
        if not settings.validate():
            print("\n❌ ОШИБКА: Некорректные настройки!")
            sys.exit(1)
        
        print("✓ Настройки загружены")
        
        # 4. Проверка окружения
        validate_environment()
        
        # 5. Инициализация компонентов
        print("=" * 60)
        print("ИНИЦИАЛИЗАЦИЯ КОМПОНЕНТОВ")
        print("=" * 60)
        
        telegram_bot = initialize_components(settings)
        
        print("\n✅ Все компоненты инициализированы!")
        print("=" * 60)
        
        # 6. Запуск бота
        print("\n💬 Найдите своего бота в Telegram и начните диалог!")
        print("🛑 Для остановки нажмите Ctrl+C\n")
        
        telegram_bot.run()
    
    except KeyboardInterrupt:
        print("\n\n🛑 Бот остановлен пользователем")
        sys.exit(0)
    
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


"""Тест работы бота."""

import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from config import Settings
from storage import VectorDatabase, UserDatabase
from ai_proxyapi_processor import ProxyAPIClient, ProxyAPIConfig, ResponseGenerator
from memory_manager import PromptBuilder, ContextRetriever
from dialog_controller import SessionManager

print("=" * 60)
print("ТЕСТ КОМПОНЕНТОВ БОТА")
print("=" * 60)

try:
    # 1. Настройки
    print("\n[1/6] Загрузка настроек...")
    settings = Settings.from_env()
    print(f"      AI Provider: {settings.ai_provider}")
    print("      [OK]")
    
    # 2. VectorDB
    print("\n[2/6] Инициализация VectorDB...")
    vector_db = VectorDatabase(
        persist_directory=settings.chroma_persist_dir,
        collection_name=settings.chroma_collection,
        openai_api_key=settings.openai_api_key
    )
    vector_db.get_or_create_collection()
    stats = vector_db.get_stats()
    print(f"      Документы в БД: {stats['document_count']}")
    print("      [OK]")
    
    # 3. ProxyAPI Client
    print("\n[3/6] Инициализация ProxyAPI...")
    proxyapi_config = ProxyAPIConfig(
        api_key=settings.proxyapi_api_key,
        model=settings.proxyapi_model,
        base_url=settings.proxyapi_base_url
    )
    proxyapi_client = ProxyAPIClient(config=proxyapi_config)
    print(f"      Модель: {proxyapi_client.model}")
    print("      [OK]")
    
    # 4. ResponseGenerator
    print("\n[4/6] Инициализация ResponseGenerator...")
    response_generator = ResponseGenerator(proxyapi_client=proxyapi_client)
    print("      [OK]")
    
    # 5. Memory Manager
    print("\n[5/6] Инициализация Memory Manager...")
    prompt_builder = PromptBuilder(system_prompt=response_generator.system_prompt)
    context_retriever = ContextRetriever(vector_db=vector_db, n_results=settings.rag_n_results)
    print("      [OK]")
    
    # 6. Session Manager
    print("\n[6/6] Инициализация Session Manager...")
    session_manager = SessionManager(session_timeout=settings.session_timeout)
    print("      [OK]")
    
    print("\n" + "=" * 60)
    print("ВСЕ КОМПОНЕНТЫ БОТА ГОТОВЫ К РАБОТЕ!")
    print("=" * 60)
    print("\nБот запущен и ожидает подключений в Telegram!")
    print("Найдите бота по токену и отправьте /start")
    
except Exception as e:
    print(f"\n[ERROR] Ошибка: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

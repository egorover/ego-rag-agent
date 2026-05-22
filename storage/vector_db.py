"""
Векторная база данных на основе ChromaDB.
Инкапсулирует логику работы с векторным хранилищем.
"""

import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Optional
import logging
import numpy as np

logger = logging.getLogger(__name__)


class VectorDatabase:
    """Обертка для работы с ChromaDB."""
    
    def __init__(
        self,
        persist_directory: str,
        collection_name: str,
        openai_api_key: str = None
    ):
        """
        Инициализирует векторную БД.
        
        Args:
            persist_directory: Директория хранения данных
            collection_name: Имя коллекции
            openai_api_key: API ключ OpenAI (не используется для локальных эмбеддингов)
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.openai_api_key = openai_api_key
        
        # Инициализируем ChromaDB клиент с персистентностью
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=ChromaSettings(
                anonymized_telemetry=False
            )
        )
        
        # Для локальных эмбеддингов
        self.embedding_model = None
        try:
            from sentence_transformers import SentenceTransformer
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Локальная модель эмбеддингов загружена: all-MiniLM-L6-v2")
        except ImportError:
            logger.warning("sentence-transformers не установлен, используем случайные эмбеддинги")
        except Exception as e:
            logger.warning(f"Не удалось загрузить локальную модель: {e}")
        
        # Коллекция
        self.collection = None
        
        logger.info(f"VectorDB инициализирован: {persist_directory}")
    
    def get_or_create_collection(self):
        """Получает или создает коллекцию."""
        try:
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "RAG документы"}
            )
            logger.info(f"Коллекция '{self.collection_name}' готова")
            return self.collection
        except Exception as e:
            logger.error(f"Ошибка создания коллекции: {e}")
            raise
    
    def add_documents(
        self,
        texts: List[str],
        metadatas: List[Dict],
        ids: Optional[List[str]] = None
    ):
        """
        Добавляет документы в коллекцию.
        
        Args:
            texts: Список текстов
            metadatas: Список метаданных
            ids: Список ID документов
        """
        if not self.collection:
            self.get_or_create_collection()
        
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(texts))]
        
        try:
            logger.info(f"Создание эмбеддингов для {len(texts)} документов...")
            embeddings = self._create_embeddings(texts)
            
            # Добавляем в коллекцию
            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Добавлено {len(texts)} документов")
        except Exception as e:
            logger.error(f"Ошибка добавления документов: {e}")
            raise
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        where: Optional[Dict] = None
    ) -> Dict:
        """
        Выполняет семантический поиск.
        
        Args:
            query: Поисковый запрос
            n_results: Количество результатов
            where: Фильтр по метаданным
            
        Returns:
            Результаты поиска
        """
        if not self.collection:
            self.get_or_create_collection()
        
        try:
            # Создаем эмбеддинг для запроса
            query_embedding = self._create_embeddings([query])[0]
            
            # Выполняем поиск
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where
            )
            
            return results
        except Exception as e:
            logger.error(f"Ошибка поиска: {e}")
            raise
    
    def _create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Создает эмбеддинги (локально через sentence-transformers).
        
        Args:
            texts: Список текстов
            
        Returns:
            Список векторов эмбеддингов
        """
        if self.embedding_model:
            try:
                logger.info(f"Создание эмбеддингов для {len(texts)} документов через локальную модель...")
                embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
                return embeddings.tolist()
            except Exception as e:
                logger.error(f"Ошибка создания эмбеддингов: {e}")
                raise
        else:
            # Генерируем случайные эмбеддинги (только для тестирования)
            logger.warning("Используются случайные эмбеддинги (для тестирования)")
            return [np.random.rand(384).tolist() for _ in texts]
        
    def get_stats(self) -> Dict:
        """
        Получает статистику коллекции.
        
        Returns:
            Словарь со статистикой
        """
        if not self.collection:
            self.get_or_create_collection()
        
        try:
            count = self.collection.count()
            return {
                "name": self.collection_name,
                "document_count": count
            }
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return {"error": str(e)}
    
    def delete_collection(self):
        """Удаляет коллекцию."""
        try:
            self.client.delete_collection(name=self.collection_name)
            logger.info(f"Коллекция '{self.collection_name}' удалена")
        except Exception as e:
            logger.error(f"Ошибка удаления коллекции: {e}")


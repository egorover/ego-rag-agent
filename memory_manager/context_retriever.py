"""
Получение контекста из хранилища.
Работает с векторной БД для получения релевантного контекста.
"""

from typing import List, Dict
import logging

import sys
from pathlib import Path
# Добавляем родительскую директорию в путь для импортов
sys.path.insert(0, str(Path(__file__).parent.parent))

from storage import VectorDatabase

logger = logging.getLogger(__name__)


class ContextRetriever:
    """Получатель контекста из векторной БД."""
    
    def __init__(
        self,
        vector_db: VectorDatabase,
        n_results: int = 5
    ):
        """
        Инициализирует получатель контекста.
        
        Args:
            vector_db: Векторная база данных
            n_results: Количество результатов по умолчанию
        """
        self.vector_db = vector_db
        self.n_results = n_results
        
        logger.info("ContextRetriever инициализирован")
    
    def retrieve(
        self,
        query: str,
        n_results: int = None,
        filter_metadata: Dict = None
    ) -> List[Dict]:
        """
        Получает релевантный контекст для запроса.
        
        Args:
            query: Поисковый запрос
            n_results: Количество результатов (опционально)
            filter_metadata: Фильтр по метаданным
            
        Returns:
            Список документов с метаданными
        """
        try:
            # Выполняем поиск в векторной БД
            results = self.vector_db.search(
                query=query,
                n_results=n_results or self.n_results,
                where=filter_metadata
            )
            
            # Форматируем результаты
            documents = []
            if results['documents'] and results['documents'][0]:
                for doc, metadata, distance in zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                ):
                    documents.append({
                        'text': doc,
                        'source': metadata.get('source', 'unknown'),
                        'type': metadata.get('type', 'unknown'),
                        'chunk_id': metadata.get('chunk_id', 0),
                        'relevance': 1 - distance,  # Преобразуем distance в релевантность
                        'distance': distance
                    })
            
            logger.info(f"Найдено {len(documents)} релевантных документов")
            
            return documents
        
        except Exception as e:
            logger.error(f"Ошибка получения контекста: {e}")
            return []
    

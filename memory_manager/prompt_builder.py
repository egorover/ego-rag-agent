"""
Построитель промптов.
Вспомогательные утилиты для работы с контекстом.

Примечание: Основная логика построения сообщений находится в BaseResponseGenerator._build_messages()
"""

from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Вспомогательный построитель для работы с контекстом документов."""
    
    def __init__(
        self,
        max_context_length: int = 4000
    ):
        """
        Инициализирует построитель промптов.
        
        Args:
            max_context_length: Максимальная длина контекста
        """
        self.max_context_length = max_context_length
        
        logger.info("PromptBuilder инициализирован")
    
    def build_context_from_documents(
        self,
        documents: List[Dict]
    ) -> str:
        """
        Формирует контекст из найденных документов.
        
        Args:
            documents: Список документов с метаданными
            
        Returns:
            Отформатированный контекст
        """
        if not documents:
            return "Контекст отсутствует."
        
        context_parts = []
        total_length = 0
        
        for i, doc in enumerate(documents, 1):
            text = doc.get('text', '')
            source = doc.get('source', 'unknown')
            relevance = doc.get('relevance', 0)
            
            # Проверяем, не превысим ли лимит
            doc_text = f"Документ {i} (Источник: {source}, Релевантность: {relevance:.2f}):\n{text}\n"
            
            if total_length + len(doc_text) > self.max_context_length:
                logger.warning(
                    f"Достигнут лимит контекста. "
                    f"Использовано {i-1} из {len(documents)} документов"
                )
                break
            
            context_parts.append(doc_text)
            total_length += len(doc_text)
        
        return "\n---\n".join(context_parts)
    
    def build_conversation_context(
        self,
        history: List[Dict],
        max_messages: int = 10
    ) -> List[Dict]:
        """
        Формирует контекст истории диалога.
        
        Args:
            history: История сообщений
            max_messages: Максимальное количество сообщений
            
        Returns:
            Отфильтрованная история для контекста
        """
        if not history:
            return []
        
        # Берем последние N сообщений
        recent_history = history[-max_messages:]
        
        return recent_history
    

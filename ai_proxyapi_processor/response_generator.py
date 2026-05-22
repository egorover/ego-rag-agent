"""
Генератор ответов.
Формирует финальные ответы на основе контекста и запроса с использованием ProxyAPI.
"""

from typing import List, Dict, Optional
import logging

from .proxyapi_client import ProxyAPIClient

logger = logging.getLogger(__name__)


class ResponseGenerator:
    """Генератор ответов с использованием ProxyAPI."""
    
    # Системный промпт по умолчанию
    DEFAULT_SYSTEM_PROMPT = """Ты полезный ассистент, отвечающий на вопросы на основе предоставленного контекста.
    
Правила:
1. Отвечай только на основе предоставленного контекста
2. Если контекст не содержит ответа, честно скажи об этом
3. Будь краток и конкретен
4. Используй тот же язык, что и вопрос пользователя"""
    
    def __init__(
        self,
        proxyapi_client: ProxyAPIClient,
        system_prompt: str = None
    ):
        """
        Инициализирует генератор ответов.
        
        Args:
            proxyapi_client: Клиент ProxyAPI
            system_prompt: Системный промпт (опционально)
        """
        self.proxyapi_client = proxyapi_client
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        
        logger.info("ResponseGenerator (ProxyAPI) инициализирован")
    
    def generate(
        self,
        query: str,
        context_documents: List[Dict] = None,
        conversation_history: List[Dict] = None,
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """
        Генерирует ответ на запрос пользователя.
        
        Args:
            query: Вопрос пользователя
            context_documents: Документы из базы знаний (опционально)
            conversation_history: История диалога (опционально)
            temperature: Температура (опционально)
            max_tokens: Макс токены (опционально)
            
        Returns:
            Сгенерированный ответ
        """
        messages = self._build_messages(query, context_documents, conversation_history)
        
        # Генерируем ответ
        try:
            answer = self.proxyapi_client.generate_response(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return answer
        except Exception as e:
            logger.error(f"Ошибка генерации ответа: {e}")
            raise
    
    def generate_streaming(
        self,
        query: str,
        context_documents: List[Dict] = None,
        conversation_history: List[Dict] = None,
        temperature: float = None,
        max_tokens: int = None
    ):
        """
        Генерирует ответ с потоковой передачей.
        
        Args:
            query: Вопрос пользователя
            context_documents: Документы из базы знаний (опционально)
            conversation_history: История диалога (опционально)
            temperature: Температура (опционально)
            max_tokens: Макс токены (опционально)
            
        Yields:
            Части ответа
        """
        messages = self._build_messages(query, context_documents, conversation_history)
        
        try:
            for chunk in self.proxyapi_client.generate_streaming_response(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            ):
                yield chunk
        except Exception as e:
            logger.error(f"Ошибка streaming генерации: {e}")
            raise
    
    def _build_messages(
        self,
        query: str,
        context_documents: List[Dict] = None,
        conversation_history: List[Dict] = None
    ) -> List[Dict[str, str]]:
        """
        Строит список сообщений для API.
        
        Args:
            query: Текущий вопрос пользователя
            context_documents: Документы из базы знаний
            conversation_history: История диалога
            
        Returns:
            Список сообщений в формате OpenAI
        """
        messages = []
        
        # Добавляем системный промпт
        messages.append({
            "role": "system",
            "content": self.system_prompt
        })
        
        # Добавляем историю диалога
        if conversation_history:
            for msg in conversation_history:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
        
        # Добавляем контекст если есть
        if context_documents:
            context_parts = []
            for i, doc in enumerate(context_documents, 1):
                text = doc.get('text', '')
                source = doc.get('source', 'unknown')
                context_parts.append(f"Источник {i} ({source}):\n{text}")
            
            context_text = "\n\n---\n\n".join(context_parts)
            context_message = f"""Контекст из базы знаний:

{context_text}

---

Используй этот контекст для ответа на вопрос."""
            messages.append({
                "role": "user",
                "content": f"{context_message}\n\nВопрос: {query}"
            })
        else:
            messages.append({
                "role": "user",
                "content": query
            })
        
        return messages

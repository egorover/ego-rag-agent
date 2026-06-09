"""
Базовый генератор ответов.
Общая логика для всех AI-провайдеров.
"""

from typing import List, Dict, Optional, Generator
import logging

logger = logging.getLogger(__name__)


class BaseResponseGenerator:
    """Базовый класс для генераторов ответов всех провайдеров."""
    
    # Системный промпт по умолчанию (единый для всех)
    DEFAULT_SYSTEM_PROMPT = """Ты - полезный AI ассистент, который отвечает на вопросы на основе предоставленного контекста из базы знаний.

Правила работы:
1. Используй ТОЛЬКО информацию из предоставленного контекста
2. Если информации недостаточно или её нет - честно сообщи об этом
3. Давай точные и структурированные ответы
4. Указывай источники информации, когда это уместно
5. Отвечай на том же языке, на котором задан вопрос
6. Будь вежливым и профессиональным

Если в контексте нет информации для ответа, скажи: "К сожалению, в базе знаний нет информации по этому вопросу."
"""
    
    def __init__(self, client):
        """
        Инициализирует генератор ответов.
        
        Args:
            client: Клиент AI-провайдера (OpenAIClient, GigaChatClient, ProxyAPIClient)
        """
        self.client = client
        self.system_prompt = self.DEFAULT_SYSTEM_PROMPT
        
        logger.info(f"BaseResponseGenerator инициализирован: {self.__class__.__name__}")
    
    def generate(
        self,
        query: str,
        context_documents: List[Dict],
        conversation_history: List[Dict] = None,
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """
        Генерирует ответ на запрос с учетом контекста.
        
        Args:
            query: Вопрос пользователя
            context_documents: Документы из базы знаний
            conversation_history: История диалога (опционально)
            temperature: Температура (опционально)
            max_tokens: Макс токены (опционально)
            
        Returns:
            Сгенерированный ответ
        """
        messages = self._build_messages(query, context_documents, conversation_history)
        
        try:
            answer = self.client.generate_response(
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
        context_documents: List[Dict],
        conversation_history: List[Dict] = None,
        temperature: float = None,
        max_tokens: int = None
    ) -> Generator[str, None, None]:
        """
        Генерирует ответ с потоковой передачей.
        
        Args:
            query: Вопрос пользователя
            context_documents: Документы из базы знаний
            conversation_history: История диалога (опционально)
            temperature: Температура (опционально)
            max_tokens: Макс токены (опционально)
            
        Yields:
            Части ответа
        """
        messages = self._build_messages(query, context_documents, conversation_history)
        
        try:
            yield from self.client.generate_streaming_response(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
        except Exception as e:
            logger.error(f"Ошибка streaming генерации: {e}")
            raise
    
    def _build_messages(
        self,
        query: str,
        context_documents: List[Dict],
        conversation_history: Optional[List[Dict]]
    ) -> List[Dict[str, str]]:
        """
        Строит список сообщений для API.
        ЕДИНАЯ ЛОГИКА для всех провайдеров.
        
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
                relevance = doc.get('relevance', 0)
                context_parts.append(
                    f"Документ {i} (Источник: {source}, Релевантность: {relevance:.2f}):\n{text}\n"
                )
            
            context_text = "\n---\n".join(context_parts)
            context_message = f"""Контекст из базы знаний:

{context_text}

---

Вопрос пользователя: {query}

Ответь на вопрос, используя информацию из предоставленного контекста."""
            messages.append({
                "role": "user",
                "content": context_message
            })
        else:
            messages.append({
                "role": "user",
                "content": query
            })
        
        return messages

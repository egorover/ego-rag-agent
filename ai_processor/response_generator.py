"""
Генератор ответов для OpenAI.
Наследуется от базового класса.
"""

from typing import List, Dict
import logging

from memory_manager.response_generator import BaseResponseGenerator
from .openai_client import OpenAIClient

logger = logging.getLogger(__name__)


class ResponseGenerator(BaseResponseGenerator):
    """Генератор ответов с использованием OpenAI."""
    
    def __init__(
        self,
        openai_client: OpenAIClient,
        system_prompt: str = None
    ):
        """
        Инициализирует генератор ответов.
        
        Args:
            openai_client: Клиент OpenAI
            system_prompt: Системный промпт (опционально)
        """
        super().__init__(client=openai_client)
        if system_prompt:
            self.system_prompt = system_prompt
        
        logger.info("ResponseGenerator (OpenAI) инициализирован")


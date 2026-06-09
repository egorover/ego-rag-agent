"""
Генератор ответов для GigaChat.
Наследуется от базового класса.
"""

from typing import List, Dict
import logging

from memory_manager.response_generator import BaseResponseGenerator
from .gigachat_client import GigaChatClient

logger = logging.getLogger(__name__)


class ResponseGenerator(BaseResponseGenerator):
    """Генератор ответов с использованием GigaChat."""
    
    def __init__(
        self,
        gigachat_client: GigaChatClient,
        system_prompt: str = None
    ):
        """
        Инициализирует генератор ответов.
        
        Args:
            gigachat_client: Клиент GigaChat
            system_prompt: Системный промпт (опционально)
        """
        super().__init__(client=gigachat_client)
        if system_prompt:
            self.system_prompt = system_prompt
        
        logger.info("ResponseGenerator (GigaChat) инициализирован")
    

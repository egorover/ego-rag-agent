"""
Генератор ответов для ProxyAPI.
Наследуется от базового класса.
"""

from typing import List, Dict
import logging

from memory_manager.response_generator import BaseResponseGenerator
from .proxyapi_client import ProxyAPIClient

logger = logging.getLogger(__name__)


class ResponseGenerator(BaseResponseGenerator):
    """Генератор ответов с использованием ProxyAPI."""
    
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
        super().__init__(client=proxyapi_client)
        if system_prompt:
            self.system_prompt = system_prompt
        
        logger.info("ResponseGenerator (ProxyAPI) инициализирован")
    

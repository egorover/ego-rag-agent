"""
Клиент для работы с ProxyAPI.
Инкапсулирует логику общения с ProxyAPI.
"""

import requests
from typing import List, Dict, Optional
import logging

from .config import ProxyAPIConfig

logger = logging.getLogger(__name__)


class ProxyAPIClient:
    """Клиент для ProxyAPI."""
    
    CHAT_COMPLETIONS_ENDPOINT = "/chat/completions"
    
    def __init__(
        self,
        api_key: str = None,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        base_url: str = "https://proxyapi.example.com/v1",
        proxy_url: Optional[str] = None,
        timeout: int = 30,
        config: ProxyAPIConfig = None
    ):
        """
        Инициализирует ProxyAPI клиент.
        
        Args:
            api_key: API ключ ProxyAPI
            model: Модель для использования
            temperature: Температура генерации
            max_tokens: Максимальное количество токенов
            base_url: Базовый URL API
            proxy_url: URL прокси (опционально)
            timeout: Timeout для запросов
            config: Объект конфигурации (приоритетнее отдельных параметров)
        """
        if config:
            self.api_key = config.api_key
            self.model = config.model
            self.temperature = config.temperature
            self.max_tokens = config.max_tokens
            self.base_url = config.base_url
            self.proxy_url = config.proxy_url
            self.timeout = config.timeout
        else:
            self.api_key = api_key
            self.model = model
            self.temperature = temperature
            self.max_tokens = max_tokens
            self.base_url = base_url
            self.proxy_url = proxy_url
            self.timeout = timeout
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
        
        if self.proxy_url:
            self.session.proxies.update({
                "http": self.proxy_url,
                "https": self.proxy_url
            })
        
        logger.info(f"ProxyAPI клиент инициализирован: модель={self.model}, base_url={self.base_url}")
    
    def generate_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """
        Генерирует ответ с помощью ProxyAPI.
        
        Args:
            messages: Список сообщений для ProxyAPI (формат: [{"role": "user/assistant/system", "content": "text"}])
            temperature: Температура (опционально)
            max_tokens: Макс токены (опционально)
            
        Returns:
            Сгенерированный ответ
        """
        url = f"{self.base_url}{self.CHAT_COMPLETIONS_ENDPOINT}"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature or self.temperature,
            "max_tokens": max_tokens or self.max_tokens,
            "stream": False
        }
        
        try:
            logger.info(f"Отправка запроса к ProxyAPI: {len(messages)} сообщений")
            
            response = self.session.post(
                url,
                json=payload,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            answer = data["choices"][0]["message"]["content"]
            logger.info(f"Ответ сгенерирован: {len(answer)} символов")
            
            return answer
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка сетевого запроса: {e}")
            raise
        except (KeyError, IndexError, ValueError) as e:
            logger.error(f"Ошибка парсинга ответа: {e}")
            raise
    
    def generate_streaming_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float = None,
        max_tokens: int = None
    ):
        """
        Генерирует ответ с потоковой передачей.
        
        Args:
            messages: Список сообщений для ProxyAPI
            temperature: Температура (опционально)
            max_tokens: Макс токены (опционально)
            
        Yields:
            Части ответа
        """
        url = f"{self.base_url}{self.CHAT_COMPLETIONS_ENDPOINT}"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature or self.temperature,
            "max_tokens": max_tokens or self.max_tokens,
            "stream": True
        }
        
        try:
            logger.info(f"Отправка streaming запроса к ProxyAPI")
            
            with self.session.post(
                url,
                json=payload,
                timeout=self.timeout,
                stream=True
            ) as response:
                response.raise_for_status()
                
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            data = line[6:]
                            if data == '[DONE]':
                                break
                            try:
                                import json
                                data_json = json.loads(data)
                                if "choices" in data_json:
                                    delta = data_json["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        yield content
                            except json.JSONDecodeError:
                                continue
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка streaming запроса: {e}")
            raise

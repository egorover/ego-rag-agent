"""Тесты конфигурации."""

import os
import unittest
from unittest.mock import patch


class TestSettings(unittest.TestCase):
    """Тесты для config/settings.py"""

    @patch.dict(os.environ, {
        "TELEGRAM_BOT_TOKEN": "test_token",
        "AI_PROVIDER": "proxyapi",
        "OPENAI_API_KEY": "test_openai_key",
        "PROXYAPI_API_KEY": "test_proxyapi_key"
    })
    def test_settings_proxyapi_provider(self):
        """Тест загрузки настроек с ProxyAPI"""
        from config import Settings
        settings = Settings.from_env()
        
        self.assertEqual(settings.ai_provider, "proxyapi")
        self.assertIsNotNone(settings.proxyapi_api_key)
        self.assertIsNotNone(settings.openai_api_key)

    @patch.dict(os.environ, {
        "TELEGRAM_BOT_TOKEN": "test_token",
        "AI_PROVIDER": "gigachat",
        "OPENAI_API_KEY": "test_openai_key",
        "GIGACHAT_AUTHORIZATION_KEY": "test_gigachat_key"
    })
    def test_settings_gigachat_provider(self):
        """Тест загрузки настроек с GigaChat"""
        from config import Settings
        settings = Settings.from_env()
        
        self.assertEqual(settings.ai_provider, "gigachat")
        self.assertIsNotNone(settings.gigachat_authorization_key)

    @patch.dict(os.environ, {
        "TELEGRAM_BOT_TOKEN": "test_token",
        "AI_PROVIDER": "openai",
        "OPENAI_API_KEY": "test_openai_key"
    })
    def test_settings_openai_provider(self):
        """Тест загрузки настроек с OpenAI"""
        from config import Settings
        settings = Settings.from_env()
        
        self.assertEqual(settings.ai_provider, "openai")

    @patch.dict(os.environ, {
        "TELEGRAM_BOT_TOKEN": "test_token"
    })
    def test_settings_missing_provider_keys(self):
        """Тест ошибки при отсутствии ключей провайдера"""
        from config import Settings
        
        with self.assertRaises(ValueError):
            Settings.from_env()


class TestProxyAPIConfig(unittest.TestCase):
    """Тесты для ai_proxyapi_processor/config.py"""

    @patch.dict(os.environ, {
        "PROXYAPI_API_KEY": "test_key",
        "PROXYAPI_MODEL": "gpt-4o-mini",
        "PROXYAPI_BASE_URL": "https://test.proxyapi.com/v1"
    })
    def test_proxyapi_config_from_env(self):
        """Тест загрузки конфигурации ProxyAPI из окружения"""
        from ai_proxyapi_processor import ProxyAPIConfig
        config = ProxyAPIConfig.from_env()
        
        self.assertEqual(config.api_key, "test_key")
        self.assertEqual(config.model, "gpt-4o-mini")
        self.assertEqual(config.base_url, "https://test.proxyapi.com/v1")


if __name__ == "__main__":
    unittest.main()

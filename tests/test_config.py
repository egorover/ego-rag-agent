"""Тесты конфигурации."""

import os
import unittest
from unittest.mock import patch


class TestSettings(unittest.TestCase):
    """Тесты для config/settings.py"""

    @patch.dict(os.environ, {
        "TELEGRAM_BOT_TOKEN": "test_token",
        "AI_PROVIDER": "proxyapi",
        "PROXYAPI_API_KEY": "test_proxyapi_key",
    }, clear=True)
    def test_settings_proxyapi_without_openai(self):
        """ProxyAPI не требует OPENAI_API_KEY (локальные эмбеддинги)."""
        from config import Settings
        settings = Settings.from_env()

        self.assertEqual(settings.ai_provider, "proxyapi")
        self.assertIsNotNone(settings.proxyapi_api_key)
        self.assertIsNone(settings.openai_api_key)

    @patch.dict(os.environ, {
        "TELEGRAM_BOT_TOKEN": "test_token",
        "AI_PROVIDER": "proxyapi",
        "OPENAI_API_KEY": "test_openai_key",
        "PROXYAPI_API_KEY": "test_proxyapi_key",
    }, clear=True)
    def test_settings_proxyapi_with_optional_openai(self):
        """OPENAI_API_KEY опционален при proxyapi."""
        from config import Settings
        settings = Settings.from_env()

        self.assertEqual(settings.ai_provider, "proxyapi")
        self.assertEqual(settings.openai_api_key, "test_openai_key")

    @patch.dict(os.environ, {
        "TELEGRAM_BOT_TOKEN": "test_token",
        "AI_PROVIDER": "gigachat",
        "GIGACHAT_AUTHORIZATION_KEY": "test_gigachat_key",
    }, clear=True)
    def test_settings_gigachat_without_openai(self):
        """GigaChat не требует OPENAI_API_KEY."""
        from config import Settings
        settings = Settings.from_env()

        self.assertEqual(settings.ai_provider, "gigachat")
        self.assertIsNotNone(settings.gigachat_authorization_key)

    @patch.dict(os.environ, {
        "TELEGRAM_BOT_TOKEN": "test_token",
        "AI_PROVIDER": "openai",
        "OPENAI_API_KEY": "test_openai_key",
    }, clear=True)
    def test_settings_openai_provider(self):
        """Тест загрузки настроек с OpenAI."""
        from config import Settings
        settings = Settings.from_env()

        self.assertEqual(settings.ai_provider, "openai")
        self.assertEqual(settings.openai_api_key, "test_openai_key")

    @patch.dict(os.environ, {
        "TELEGRAM_BOT_TOKEN": "test_token",
    }, clear=True)
    def test_settings_missing_provider_keys(self):
        """Ошибка при отсутствии ключей провайдера по умолчанию (proxyapi)."""
        from config import Settings

        with self.assertRaises(ValueError):
            Settings.from_env()

    @patch.dict(os.environ, {
        "CHROMA_PERSIST_DIR": "./test_chroma",
        "CHROMA_COLLECTION": "test_docs",
    }, clear=True)
    def test_settings_from_env_for_ingest(self):
        """Индексация не требует Telegram и ключей LLM."""
        from config import Settings
        settings = Settings.from_env_for_ingest()

        self.assertEqual(settings.telegram_token, "")
        self.assertEqual(settings.chroma_persist_dir, "./test_chroma")
        self.assertEqual(settings.chroma_collection, "test_docs")

    @patch.dict(os.environ, {
        "TELEGRAM_BOT_TOKEN": "test_token",
        "AI_PROVIDER": "proxyapi",
        "PROXYAPI_API_KEY": "test_proxyapi_key",
    }, clear=True)
    def test_settings_validate_proxyapi(self):
        """validate() проходит для корректных настроек proxyapi."""
        from config import Settings
        settings = Settings.from_env()
        self.assertTrue(settings.validate())

    @patch.dict(os.environ, {
        "TELEGRAM_BOT_TOKEN": "test_token",
        "AI_PROVIDER": "proxyapi",
        "PROXYAPI_API_KEY": "test_proxyapi_key",
        "CHUNK_SIZE": "500",
        "CHUNK_OVERLAP": "500",
    }, clear=True)
    def test_settings_validate_invalid_chunk_overlap(self):
        """validate() отклоняет chunk_overlap >= chunk_size."""
        from config import Settings
        settings = Settings.from_env()
        self.assertFalse(settings.validate())


class TestProxyAPIConfig(unittest.TestCase):
    """Тесты для ai_proxyapi_processor/config.py"""

    @patch.dict(os.environ, {
        "PROXYAPI_API_KEY": "test_key",
        "PROXYAPI_MODEL": "gpt-4o-mini",
        "PROXYAPI_BASE_URL": "https://test.proxyapi.com/v1",
    }, clear=True)
    def test_proxyapi_config_from_env(self):
        """Тест загрузки конфигурации ProxyAPI из окружения."""
        from ai_proxyapi_processor import ProxyAPIConfig
        config = ProxyAPIConfig.from_env()

        self.assertEqual(config.api_key, "test_key")
        self.assertEqual(config.model, "gpt-4o-mini")
        self.assertEqual(config.base_url, "https://test.proxyapi.com/v1")


if __name__ == "__main__":
    unittest.main()

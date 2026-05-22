"""Тесты хранилища (локальные эмбеддинги, без внешних API)."""

import os
import shutil
import tempfile
import unittest


class TestVectorDatabase(unittest.TestCase):
    """Тесты VectorDatabase с локальными эмбеддингами."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="ego_rag_test_")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_embeddings_and_stats(self):
        """Создание эмбеддингов и добавление документов в ChromaDB."""
        from storage import VectorDatabase

        vector_db = VectorDatabase(
            persist_directory=self.temp_dir,
            collection_name="test_collection",
        )
        vector_db.get_or_create_collection()

        texts = ["Тестовый документ о DevOps.", "Второй фрагмент текста."]
        metadatas = [
            {"source": "test1.txt", "chunk_id": 0},
            {"source": "test2.txt", "chunk_id": 1},
        ]
        ids = ["doc_0", "doc_1"]

        vector_db.add_documents(texts=texts, metadatas=metadatas, ids=ids)
        stats = vector_db.get_stats()

        self.assertEqual(stats["name"], "test_collection")
        self.assertEqual(stats["document_count"], 2)

        results = vector_db.search(query="DevOps", n_results=1)
        self.assertIn("documents", results)
        self.assertGreaterEqual(len(results["documents"][0]), 1)


if __name__ == "__main__":
    unittest.main()

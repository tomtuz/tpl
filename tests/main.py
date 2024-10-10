import os
import unittest

from src.core import config_manager
from src.core.config_manager import (
    decrypt_value,
    encrypt_value,
    ensure_config_dir,
    get_config_dir,
    get_config_value,
    load_config,
    remove_config_value,
    save_config,
    set_config_value,
)


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.test_config_dir = os.path.join(os.path.dirname(__file__), "test_config")
        self.original_get_config_dir = get_config_dir
        config_manager.get_config_dir = lambda: self.test_config_dir

    def tearDown(self):
        config_manager.get_config_dir = self.original_get_config_dir
        if os.path.exists(self.test_config_dir):
            for file in os.listdir(self.test_config_dir):
                os.remove(os.path.join(self.test_config_dir, file))
            os.rmdir(self.test_config_dir)

    def test_ensure_config_dir(self):
        ensure_config_dir()
        self.assertTrue(os.path.exists(self.test_config_dir))

    def test_save_and_load_config(self):
        test_config = {"key": "value"}
        save_config(test_config)
        loaded_config = load_config()
        self.assertEqual(test_config, loaded_config)

    def test_get_set_remove_config_value(self):
        set_config_value("test_key", "test_value")
        self.assertEqual(get_config_value("test_key"), "test_value")
        remove_config_value("test_key")
        self.assertIsNone(get_config_value("test_key"))

    def test_sensitive_config_value(self):
        set_config_value("sensitive_key", "sensitive_value", sensitive=True)
        encrypted_value = load_config()["sensitive_key"]
        self.assertNotEqual(encrypted_value, "sensitive_value")
        self.assertEqual(get_config_value("sensitive_key", sensitive=True), "sensitive_value")

    def test_encryption_decryption(self):
        original_value = "test_value"
        encrypted = encrypt_value(original_value)
        decrypted = decrypt_value(encrypted)
        self.assertNotEqual(original_value, encrypted)
        self.assertEqual(original_value, decrypted)


if __name__ == "__main__":
    unittest.main()

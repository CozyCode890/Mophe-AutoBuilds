import os
import unittest
from unittest.mock import patch

from src.__main__ import _resolve_patch_option


class TestPatchOptions(unittest.TestCase):
    """"key=value" lines in patches/*.txt pull secrets from the environment."""

    @patch.dict(os.environ, {"TELEGRAM_API_ID": "12345", "TELEGRAM_API_HASH": " abc123 "})
    def test_env_references_are_expanded(self):
        self.assertEqual(_resolve_patch_option("apiId='${TELEGRAM_API_ID}'"), "apiId='12345'")
        self.assertEqual(_resolve_patch_option("apiHash='${TELEGRAM_API_HASH}'"), "apiHash='abc123'")

    def test_plain_value_passes_through(self):
        self.assertEqual(_resolve_patch_option("darkMode=true"), "darkMode=true")

    @patch.dict(os.environ, {"TELEGRAM_API_ID": ""})
    def test_unset_secret_skips_option(self):
        os.environ.pop("TELEGRAM_API_HASH", None)
        self.assertIsNone(_resolve_patch_option("apiId='${TELEGRAM_API_ID}'"))
        self.assertIsNone(_resolve_patch_option("apiHash='${TELEGRAM_API_HASH}'"))


if __name__ == "__main__":
    unittest.main()

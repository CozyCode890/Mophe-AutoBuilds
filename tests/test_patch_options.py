import os
import unittest
from pathlib import Path
from unittest.mock import patch

from src.__main__ import _morphe_selection_args, _resolve_patch_option


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


class TestSelectionPlacement(unittest.TestCase):
    """morphe-cli binds -e/-d/-O to the bundle they follow."""

    SOURCE, GLOBAL = Path("hush.mpp"), Path("morphe-patches.mpp")
    NAMES = {
        "hush.mpp": {"Use registered Telegram API credentials", "Hide ads"},
        "morphe-patches.mpp": {"Disable Play Store updates"},
    }

    def _args(self, selections, options=None):
        with patch("src.__main__._bundle_patch_names", side_effect=lambda cli, b: self.NAMES.get(b.name, set())):
            return _morphe_selection_args(Path("cli.jar"), [self.SOURCE, self.GLOBAL], selections, options or {})

    def test_each_selection_follows_its_bundle(self):
        args = self._args(
            [("-d", "Hide ads"), ("-e", "Use registered Telegram API credentials"), ("-e", "Disable Play Store updates")],
            {"Use registered Telegram API credentials": ["apiId='1'"]},
        )
        self.assertEqual(args, [
            "--patches", "hush.mpp",
            "-d", "Hide ads",
            "-e", "Use registered Telegram API credentials", "-OapiId='1'",
            "--patches", "morphe-patches.mpp",
            "-e", "Disable Play Store updates",
        ])

    def test_unknown_name_goes_after_last_bundle(self):
        self.assertEqual(self._args([("-e", "Typo patch")]),
                         ["--patches", "hush.mpp", "--patches", "morphe-patches.mpp", "-e", "Typo patch"])


if __name__ == "__main__":
    unittest.main()

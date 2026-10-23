import os
import tempfile
import unittest
from unittest.mock import patch

from src import __main__ as build


class TestKeystoreArgs(unittest.TestCase):

    def test_public_keystore_when_unconfigured(self):
        with patch.dict(os.environ, {"KEYSTORE_PATH": ""}):
            args = build._keystore_args()
        self.assertEqual(args[:2], ["--ks", "keystore/public.jks"])
        self.assertIn("pass:public", args)

    def test_private_keystore_reads_passwords_from_env(self):
        with tempfile.NamedTemporaryFile(suffix=".p12", delete=False) as ks:
            path = ks.name
        try:
            env = {"KEYSTORE_PATH": path, "KEY_ALIAS": "Morphe", "KEY_PASSWORD": ""}
            with patch.dict(os.environ, env):
                args = build._keystore_args()
        finally:
            os.unlink(path)
        self.assertEqual(args, [
            "--ks", path,
            "--ks-pass", "env:KEYSTORE_PASSWORD",
            "--key-pass", "env:KEYSTORE_PASSWORD",
            "--ks-key-alias", "Morphe",
        ])
        self.assertFalse(any(a.startswith("pass:") for a in args))

    def test_separate_key_password(self):
        with tempfile.NamedTemporaryFile(suffix=".jks", delete=False) as ks:
            path = ks.name
        try:
            env = {"KEYSTORE_PATH": path, "KEY_ALIAS": "", "KEY_PASSWORD": "secret"}
            with patch.dict(os.environ, env):
                args = build._keystore_args()
        finally:
            os.unlink(path)
        self.assertIn("env:KEY_PASSWORD", args)
        self.assertNotIn("--ks-key-alias", args)

    def test_missing_keystore_never_falls_back_to_public(self):
        with patch.dict(os.environ, {"KEYSTORE_PATH": os.path.join(tempfile.gettempdir(), "missing.p12")}):
            with self.assertRaises(RuntimeError):
                build._keystore_args()


if __name__ == "__main__":
    unittest.main()

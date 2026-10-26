import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from scripts.cleanup_old_apks import identity_prefix
from scripts.generate_obtainium import build_obtainium_app
from scripts.generate_release_notes import parse_apk_details
from scripts.record_build import extract_version_from_filename
from src import utils

STAMPED = "instagram-arm64-v8a-hushgram-patches-v452.1.0.53.64-b202610250504.apk"
UNSTAMPED = "instagram-arm64-v8a-hushgram-patches-v452.1.0.53.64.apk"
PAGES_URL = "https://u.github.io/r/downloads.html"


class TestBuildStamp(unittest.TestCase):
    """Every rebuild gets a new "-b{stamp}" file name so Obtainium notices
    patch-only rebuilds, while the pipeline still reads the plain app version."""

    def test_stamp_shape(self):
        self.assertRegex(f"x-b{utils.build_stamp()}", utils.BUILD_STAMP_RE)

    def test_recorded_version_excludes_stamp(self):
        self.assertEqual(extract_version_from_filename(STAMPED), "452.1.0.53.64")
        self.assertEqual(extract_version_from_filename(UNSTAMPED), "452.1.0.53.64")

    def test_stamped_build_supersedes_unstamped(self):
        self.assertEqual(identity_prefix(STAMPED), identity_prefix(UNSTAMPED))
        self.assertEqual(identity_prefix(STAMPED), "instagram-arm64-v8a-hushgram-patches")

    def test_release_notes_version_excludes_stamp(self):
        self.assertEqual(parse_apk_details(STAMPED)[2], "v452.1.0.53.64")
        self.assertEqual(parse_apk_details(UNSTAMPED)[2], "v452.1.0.53.64")

    def test_obtainium_version_changes_with_stamp(self):
        """Same app version, new stamp -> a different Obtainium version string."""
        entry = {"app_name": "instagram", "arch": "arm64-v8a", "apk": STAMPED}
        s = json.loads(build_obtainium_app("k", entry, "u/r", "u", {}, PAGES_URL)["additionalSettings"])
        link = f"https://github.com/u/r/releases/latest/download/{STAMPED}"
        newer = link.replace("202610250504", "202610270530")
        self.assertRegex(link, s["apkFilterRegEx"])
        self.assertEqual(re.search(s["versionExtractionRegEx"], link).group(1),
                         "452.1.0.53.64-b202610250504")
        self.assertNotEqual(re.search(s["versionExtractionRegEx"], newer).group(1),
                            re.search(s["versionExtractionRegEx"], link).group(1))


if __name__ == "__main__":
    unittest.main()

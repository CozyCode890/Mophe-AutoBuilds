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

    def test_filename_version_is_path_and_asset_safe(self):
        """Teams' "/" and MEGA's "(...)" tokens never reach the file name."""
        self.assertEqual(utils.filename_version("1416/1.0.0.2026152302"), "1.0.0.2026152302")
        self.assertEqual(utils.filename_version("16.12(262370820)(dcdf0a7f27)"), "16.12")
        self.assertEqual(utils.filename_version("2.0.3-rc0"), "2.0.3-rc0")
        self.assertEqual(utils.filename_version("18.2.4-armeabi-v7a"), "18.2.4")
        name = f"teams-arm64-v8a-morphe-patches-v{utils.filename_version('1416/1.0.0.2026152302')}-b202610300730.apk"
        self.assertEqual(extract_version_from_filename(name), "1.0.0.2026152302")
        self.assertEqual(identity_prefix(name), "teams-arm64-v8a-morphe-patches")


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from instagram_tools import storage as storage_module
from instagram_tools.storage import Storage


class StorageNamespaceRegressionTestCase(unittest.TestCase):
    def test_fresh_linux_install_uses_product_namespace(self) -> None:
        with TemporaryDirectory() as temporary:
            data_home = Path(temporary)
            with (
                patch.object(storage_module.sys, "platform", "linux"),
                patch.dict(os.environ, {"XDG_DATA_HOME": str(data_home)}, clear=False),
            ):
                storage = Storage.default()

            self.assertEqual(storage.paths.root, data_home / "instagram-tools")

    def test_existing_linux_legacy_install_keeps_current_profile(self) -> None:
        with TemporaryDirectory() as temporary:
            data_home = Path(temporary)
            legacy_root = data_home / "following-auto-liker"
            legacy_profile = legacy_root / "chrome-profile"
            legacy_profile.mkdir(parents=True)
            (legacy_profile / "Local State").write_text("legacy", encoding="utf-8")
            with (
                patch.object(storage_module.sys, "platform", "linux"),
                patch.dict(os.environ, {"XDG_DATA_HOME": str(data_home)}, clear=False),
            ):
                storage = Storage.default()

            self.assertEqual(storage.paths.root, legacy_root)

    def test_empty_product_directory_cannot_hide_legacy_state(self) -> None:
        with TemporaryDirectory() as temporary:
            data_home = Path(temporary)
            preferred_root = data_home / "instagram-tools"
            (preferred_root / "chrome-profile").mkdir(parents=True)
            legacy_root = data_home / "following-auto-liker"
            legacy_profile = legacy_root / "chrome-profile"
            legacy_profile.mkdir(parents=True)
            (legacy_profile / "Cookies").write_text("legacy", encoding="utf-8")
            with (
                patch.object(storage_module.sys, "platform", "linux"),
                patch.dict(os.environ, {"XDG_DATA_HOME": str(data_home)}, clear=False),
            ):
                storage = Storage.default()

            self.assertEqual(storage.paths.root, legacy_root)

    def test_product_namespace_wins_once_it_contains_user_state(self) -> None:
        with TemporaryDirectory() as temporary:
            data_home = Path(temporary)
            legacy_root = data_home / "following-auto-liker"
            legacy_root.mkdir(parents=True)
            preferred_root = data_home / "instagram-tools"
            preferred_root.mkdir(parents=True)
            (preferred_root / "config.json").write_text("{}", encoding="utf-8")
            with (
                patch.object(storage_module.sys, "platform", "linux"),
                patch.dict(os.environ, {"XDG_DATA_HOME": str(data_home)}, clear=False),
            ):
                storage = Storage.default()

            self.assertEqual(storage.paths.root, preferred_root)

    def test_fresh_windows_install_uses_product_namespace(self) -> None:
        with TemporaryDirectory() as temporary:
            local_app_data = Path(temporary)
            with (
                patch.object(storage_module.sys, "platform", "win32"),
                patch.dict(os.environ, {"LOCALAPPDATA": str(local_app_data)}, clear=False),
            ):
                storage = Storage.default()

            self.assertEqual(storage.paths.root, local_app_data / "InstagramTools")


if __name__ == "__main__":
    unittest.main()

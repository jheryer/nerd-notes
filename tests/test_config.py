import os
import re
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import frontmatter
import yaml

# Import the modules to be tested.
import config
import note
import sync


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_config_dir = config.CONFIG_DIR
        self.original_settings_file = config.SETTINGS_FILE
        config.CONFIG_DIR = self.test_dir.name
        config.SETTINGS_FILE = os.path.join(self.test_dir.name, "settings.yaml")

    def tearDown(self):
        config.CONFIG_DIR = self.original_config_dir
        config.SETTINGS_FILE = self.original_settings_file
        self.test_dir.cleanup()

    def test_load_settings_creates_file(self):
        if os.path.exists(config.SETTINGS_FILE):
            os.remove(config.SETTINGS_FILE)
        settings = config.load_settings()
        self.assertIn("notes_dir", settings)
        self.assertTrue(os.path.exists(config.SETTINGS_FILE))

    def test_set_notes_path(self):
        new_path = os.path.join(self.test_dir.name, "new_notes")
        config.set_notes_path(new_path)
        settings = config.load_settings()
        self.assertEqual(settings["notes_dir"], new_path)
        self.assertTrue(os.path.exists(new_path))

    def test_set_editor(self):
        editor = "vim"
        config.set_editor(editor)
        settings = config.load_settings()
        self.assertEqual(settings["editor"], editor)

    def test_set_openai_token(self):
        token = "test_token"
        config.set_openai_token(token)
        settings = config.load_settings()
        self.assertEqual(settings["openai_token"], token)

    def test_set_git_remote(self):
        repo = "https://github.com/example/repo.git"
        config.set_git_remote(repo)
        settings = config.load_settings()
        self.assertEqual(settings["git_remote"], repo)

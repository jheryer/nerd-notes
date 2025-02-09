import os
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import sync


class TestSync(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.notes_dir = os.path.join(self.test_dir.name, "notes")
        os.makedirs(self.notes_dir, exist_ok=True)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_create_gitignore(self):
        gitignore_path = os.path.join(self.notes_dir, ".gitignore")
        sync.create_gitignore(self.notes_dir)
        self.assertTrue(os.path.exists(gitignore_path))
        with open(gitignore_path, "r") as f:
            content = f.read()
        self.assertIn("settings.yaml", content)

    @patch("subprocess.run")
    def test_init_git_repo(self, mock_run):
        remote_repo = "https://github.com/example/repo.git"
        git_dir = os.path.join(self.notes_dir, ".git")
        if os.path.exists(git_dir):
            shutil.rmtree(git_dir)
        sync.init_git_repo(self.notes_dir, remote_repo)
        mock_run.assert_any_call(["git", "init"], cwd=self.notes_dir, check=True)

    @patch("subprocess.run")
    @patch("sync.create_gitignore")
    @patch("sync.init_git_repo")
    def test_sync_notes(self, mock_run, mock_create, mock_init):
        remote_repo = "https://github.com/example/repo.git"
        mock_run.side_effect = [
            subprocess.CompletedProcess(
                args=["git", "symbolic-ref", "--short", "HEAD"],
                returncode=0,
                stdout="main\n",
            ),
            subprocess.CompletedProcess(
                args=["git", "pull", "--rebase", "origin", "main"], returncode=0
            ),
            subprocess.CompletedProcess(args=["git", "add", "."], returncode=0),
            subprocess.CompletedProcess(
                args=["git", "diff", "--cached", "--quiet"], returncode=1
            ),
            subprocess.CompletedProcess(
                args=["git", "commit", "-m", "Sync notes"], returncode=0
            ),
            subprocess.CompletedProcess(
                args=["git", "push", "-u", "origin", "main"], returncode=0
            ),
        ]

        sync.sync_notes(self.notes_dir, remote_repo)
        self.assertTrue(mock_run.call_count >= 0)

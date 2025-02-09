import os
import tempfile
import unittest
from unittest.mock import patch

import note


class TestNote(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.notes_dir = os.path.join(self.test_dir.name, "notes")
        os.makedirs(self.notes_dir, exist_ok=True)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_sanitize_title(self):
        title = "Meeting: Today @ 3:00 PM"
        sanitized = note.sanitize_title(title)
        self.assertEqual(sanitized, "Meeting-Today-3-00-PM")

    def test_create_note(self):
        title = "Test Note"
        tags = ["test", "note"]
        note.create_note(title, tags, self.notes_dir)
        files = os.listdir(self.notes_dir)
        self.assertEqual(len(files), 1)
        filepath = os.path.join(self.notes_dir, files[0])
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("# Raw Notes", content)
        self.assertIn("Test Note", content)

    def test_get_note_files(self):
        filenames = ["note1.md", "note2.md", "note3.txt"]
        for fname in filenames:
            with open(os.path.join(self.notes_dir, fname), "w") as f:
                f.write("Dummy content")
        note_files = note.get_note_files(self.notes_dir)
        self.assertEqual(note_files, sorted(["note1.md", "note2.md"]))

    def test_extract_section(self):
        content = (
            "# Raw Notes\n"
            "This is raw notes content.\n"
            "# Processing\n"
            "Processing details here.\n"
            "# Summary\n"
            "Old summary."
        )
        raw = note.extract_section(content, "Raw Notes")
        processing = note.extract_section(content, "Processing")
        summary = note.extract_section(content, "Summary")
        self.assertEqual(raw, "This is raw notes content.")
        self.assertEqual(processing, "Processing details here.")
        self.assertEqual(summary, "Old summary.")

    def test_update_section(self):
        content = "# Summary\n" "Old summary.\n" "# Reflection\n" "Some reflections."
        new_text = "New summary with updates."
        updated_content = note.update_section(content, "Summary", new_text)
        self.assertIn(new_text, updated_content)
        self.assertIn("Some reflections.", updated_content)

    # openai.chat.completions.create
    @patch("note.get_openai_response")
    def test_summarize_note_file(self, mock_chat):
        note_content = (
            "# Raw Notes\n"
            "Raw content here.\n\n"
            "# Processing\n"
            "Processing info here.\n\n"
            "# Connecting\n"
            "Connection details.\n\n"
            "# Summary\n"
            "Old summary.\n\n"
            "# Reflection\n"
            "Reflections."
        )
        note_path = os.path.join(self.notes_dir, "test_note.md")
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(note_content)

        mock_response = "Generated summary and action items."

        mock_chat.return_value = mock_response

        dummy_token = "dummy_token"
        summary = note.summarize_note_file(note_path, dummy_token)
        self.assertEqual(summary, "Generated summary and action items.")

        with open(note_path, "r", encoding="utf-8") as f:
            updated_content = f.read()
        self.assertIn("Generated summary and action items.", updated_content)

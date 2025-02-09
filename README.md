
# Nerd Notes CLI

**Nerd Notes CLI** is a command-line tool designed for managing Markdown notes using an efficient, customizable workflow. It provides a standardized note template, tagging and filtering capabilities, Markdown viewing with Rich cli rendering, automated summarization using OpenAI, and synchronization with a remote Git repository.

## Features

- **Create Notes:**  
  Create new Markdown notes with a built-in template that includes the following sections:
  - **Raw Notes**
  - **Processing**
  - **Connecting**
  - **Summary** (populated via summarization)
  - **Reflection**

- **List & Filter Notes:**  
  List all notes with index numbers and filter notes by tags for quick access.

- **View & Open Notes:**  
  View notes directly in your terminal with rich Markdown rendering or open them in your default editor. You can specify notes by filename or by their index number.

- **Summarization:**  
  Automatically summarize the contents of a note by extracting the **Raw Notes**, **Processing**, and **Connecting** sections, and then using OpenAI's GPT-4 to generate a concise summary along with action items. The summary is automatically updated in the note's **Summary** section.

- **Git Sync:**  
  Synchronize your notes with a remote Git repository. The tool can initialize a Git repository if needed, set the remote URL, pull remote changes (to sync with other devices), and then commit and push local changes.

- **Consolidated Settings:**  
  Configure your tool with a single `settings` command. You can update the notes directory, default editor, OpenAI API token, and remote Git repository URL. Default settings are stored in `~/.nerd_notes/settings.yaml`.

## Project Structure

```
nerd_notes/
├── cli.py         # Main command-line interface
├── config.py      # Configuration module (manages settings)
├── note.py        # Note operations (create, list, summarize, etc.)
├── sync.py        # Git synchronization module (init, pull, push)
└── __init__.py    # Package initializer (optional)
```

## Installation

1. **Clone the Repository:**

   ```bash
   git clone git@github.com:jheryer/nerd-notes.git 
   cd nerd_notes
   ```

2. **Install Dependencies:**

   The project depends on several Python packages:
   - [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)
   - [python-frontmatter](https://pypi.org/project/python-frontmatter/)
   - [Rich](https://rich.readthedocs.io/en/stable/)
   - [openai](https://pypi.org/project/openai/)

   Install them via pip:

   ```bash
   pip install PyYAML python-frontmatter rich openai
   ```

## Usage

Run the CLI tool using Python:

```bash
python cli.py <command> [options]
```

### Commands

#### Create a New Note

Creates a new Markdown note with an optional list of tags.

```bash
python cli.py new --title "Meeting Notes" --tags meeting project
```

#### List All Notes

Lists all notes in your repository with index numbers.

```bash
python cli.py list
```

#### Open a Note

Opens a note in your default editor. You can specify the note by filename or by its index number.

- By filename:

  ```bash
  python cli.py open --file "2025-02-08-Meeting-Notes.md"
  ```

- By index number:

  ```bash
  python cli.py open --file 3
  ```

#### View a Note

Displays the note with Markdown rendering in your terminal using Rich.

```bash
python cli.py view --file 2
```

or

```bash
python cli.py view --file "2025-02-08-Meeting-Notes.md"
```

#### Summarize a Note

Uses OpenAI GPT-4 to generate a summary and action items from the **Raw Notes**, **Processing**, and **Connecting** sections. The summary is then updated in the **Summary** section of the note.

> **Note:** Before summarizing, set your OpenAI API token using the settings command.

```bash
python cli.py summarize --file 2
```

or

```bash
python cli.py summarize --file "2025-02-08-Meeting-Notes.md"
```

#### Git Sync

Synchronize your notes with a remote Git repository. The sync command will:
- Initialize a Git repository (if one does not exist)
- Set the remote (if not already set)
- Pull changes from the remote (to update with changes from another computer)
- Commit and push local changes

```bash
python cli.py sync
```

Optionally, override the remote URL with:

```bash
python cli.py sync --repo https://github.com/yourusername/notes-repo.git
```

#### Settings

View or update configuration settings. If no options are provided, the current settings are displayed.

- **Set the Notes Directory:**

  ```bash
  python cli.py settings --path "~/Documents/CustomNotes"
  ```

- **Set the Default Editor:**

  ```bash
  python cli.py settings --editor vim
  ```

- **Set the OpenAI API Token:**

  ```bash
  python cli.py settings --token YOUR_OPENAI_API_TOKEN
  ```

- **Set the Remote Git Repository URL:**

  ```bash
  python cli.py settings --git  <YOUR_REPO_URL>
  ```

To view your current settings:

```bash
python cli.py settings
```

## Contributing

Contributions are welcome. If you encounter issues or have suggestions, feel free to open an issue on the GitHub repository.

## License

This project is licensed under the MIT License.


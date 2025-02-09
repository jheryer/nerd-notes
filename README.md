# nerd-notes
```markdown
# Nerd Notes CLI

**Nerd Notes CLI** is a command-line tool designed to help you manage your Markdown notes with an efficient workflow. It provides a customizable note template, tagging, viewing, and editing capabilities, as well as an integrated summarization feature powered by OpenAI's GPT-4. With Nerd Notes CLI, you can create, list, filter, view, and open notes easily while automatically generating summaries and extracting action items from your notes.

## Features

- **Create Notes:**  
  Generate new Markdown notes with a pre-defined template that includes:
  - **Raw Notes**
  - **Processing**
  - **Connecting**
  - **Summary** (to be auto-generated)
  - **Reflection**

- **List and Filter Notes:**  
  List all your notes with index numbers, and filter notes by tags for quick access.

- **Open and View Notes:**  
  Open notes in your default editor or view them directly in the terminal with Markdown rendering using Rich.

- **Summarization:**  
  Use OpenAI's GPT-4 to automatically summarize your notes. The summarization feature extracts content from the **Raw Notes**, **Processing**, and **Connecting** sections, then populates the **Summary** section with a concise summary and a list of action items.

- **Configurable Settings:**  
  Persist configuration settings such as the notes directory, default editor, and OpenAI API token in a YAML file (`~/.nerd_notes/settings.yaml`). Easily update these settings via CLI commands.

## Project Structure

```
nerd_notes/
├── nerd_notes.py         # Main CLI entry point
├── config.py      # Configuration module (settings, paths, API token)
├── note.py        # Note handling module (create, list, summarize, etc.)
└── __init__.py    # Package initializer (if needed)
```

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/jheryer/nerd_notes.git
   cd nerd_notes
   ```

2. **Install Dependencies:**

   The project requires the following Python packages:
   - [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)
   - [python-frontmatter](https://pypi.org/project/python-frontmatter/)
   - [Rich](https://rich.readthedocs.io/en/stable/)
   - [openai](https://pypi.org/project/openai/)

   Install them using pip:

   ```bash
   pip install PyYAML python-frontmatter rich openai
   ```

## Usage

Run the CLI tool using Python. Below are some common commands:

### Create a New Note

```bash
python cli.py new --title "Meeting Notes" --tags meeting project
```

### List All Notes

List all your notes with index numbers:

```bash
python cli.py list
```

### Open a Note in Your Default Editor

Open a note by filename or by its index number (as shown in the list):

- By filename:

  ```bash
  python cli.py open --file "2025-02-08-Meeting-Notes.md"
  ```

- By index number:

  ```bash
  python cli.py open --file 3
  ```

### View a Note in the Terminal with Markdown Rendering

View the note content rendered as Markdown in your terminal:

```bash
python cli.py view --file 2
```

or

```bash
python cli.py view --file "2025-02-08-Meeting-Notes.md"
```

### Summarize a Note with OpenAI GPT-4

Before summarizing, set your OpenAI API token:

```bash
python cli.py settoken --token YOUR_OPENAI_API_TOKEN
```

Then, summarize a note (by filename or index):

```bash
python cli.py summarize --file 2
```

or

```bash
python cli.py summarize --file "2025-02-08-Meeting-Notes.md"
```

The summarization feature extracts the **Raw Notes**, **Processing**, and **Connecting** sections, sends them to OpenAI's GPT-4, and updates the **Summary** section with a generated summary and action items.

### Update Configuration Settings

- **Set the Notes Directory:**

  ```bash
  python cli.py setpath --path "~/Documents/CustomNotes"
  ```

- **Set the Default Editor:**

  ```bash
  python cli.py seteditor --editor vim
  ```

- **Set the OpenAI API Token:**

  ```bash
  python cli.py settoken --token YOUR_OPENAI_API_TOKEN
  ```

## Contributing

Contributions are welcome! 

## License

This project is licensed under the MIT License.

---

```

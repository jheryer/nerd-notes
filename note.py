import datetime
import os
import re
import subprocess

import frontmatter
import openai
from rich.console import Console
from rich.markdown import Markdown


def sanitize_title(title):
    """
    Converts the note title into a safe filename by replacing non-word characters with hyphens.
    """
    return re.sub(r"[^\w]+", "-", title.strip()).strip("-")


def create_note(title, tags, notes_dir):
    """
    Creates a new Markdown note with YAML front matter and a standard template.
    """
    if not os.path.exists(notes_dir):
        os.makedirs(notes_dir)

    date_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    safe_title = sanitize_title(title)
    filename = f"{safe_title}-{date_str}.md"
    filepath = os.path.join(notes_dir, filename)

    if tags:
        tags_list = ", ".join([f'"{tag}"' for tag in tags])
    else:
        tags_list = ""

    front_matter = (
        f"---\n"
        f'title: "{title}"\n'
        f'date: "{date_str}"\n'
        f"tags: [{tags_list}]\n"
        f"---\n\n"
    )

    template = front_matter + (
        "# Raw Notes\n"
        "- Start your note here.\n\n"
        "# Processing\n"
        "*Add clarifications or additional context here.*\n\n"
        "# Connecting\n"
        "*Link related notes or external resources here.*\n\n"
        "# Summary\n"
        "*LLM-generated summary will appear here.*\n\n"
        "# Reflection\n"
        "*Your personal reflections here.*\n"
    )

    with open(filepath, "w") as f:
        f.write(template)

    print(f"Note created: {filepath}")


def get_note_file(note_input, notes_dir) -> str:

    note_file = None

    if note_input.isdigit():
        index = int(note_input) - 1
        files = get_note_files(notes_dir)
        if index < 0 or index > len(files):
            print("Invalid note index.")
            return ""

        note_input = files[index - 1]
        note_file = os.path.join(notes_dir, files[index])
    else:
        note_file = note_input
        if not os.path.isabs(note_input):
            note_input = os.path.join(notes_dir, note_input)

    return note_file


def open_note(note_input, notes_dir, editor):
    """
    Open or views a note.
    """
    note_file = get_note_file(note_input, notes_dir)

    if not os.path.exists(note_file):
        print(f"Note file not found: {note_input}")
        return

    if editor is None:
        try:
            with open(note_file, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading note file: {e}")
            return

        console = Console()
        markdown = Markdown(content)
        console.print(markdown)
    else:
        subprocess.run([editor, note_file])


def list_notes(notes_dir, filtered_notes=None):
    """
    Lists all Markdown files in the specified notes directory.
    """
    files = get_note_files(notes_dir)

    if files is None or len(files) == 0:
        print("No notes found.")
    else:
        print("Notes in repository:")
        for index, file in enumerate(files, start=1):
            if filtered_notes is not None and file in filtered_notes:
                continue
            print(f"{index} {file}")


def get_note_files(notes_dir) -> list:
    """
    Indexes all Markdown files in the specified notes directory.
    """
    if not os.path.exists(notes_dir):
        print("No notes directory found.")
        return []
    files = sorted([f for f in os.listdir(notes_dir) if f.endswith(".md")])
    return files


def print_tags(tags):
    """
    Prints the list of tags.
    """
    if not tags:
        print("No tags found.")
    else:
        print("Tags:")
        for tag in tags:
            print(f"- {tag}")


def list_all_tags(notes_dir) -> list:
    """
    Iterates through all Markdown files and collects unique tags from the YAML front matter.
    Returns a sorted list of tags.
    """
    tags = set()
    if not os.path.exists(notes_dir):
        print("Notes directory not found.")
        return []
    for filename in os.listdir(notes_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(notes_dir, filename)
            try:
                post = frontmatter.load(filepath)
                note_tags = post.get("tags", [])
                if note_tags is None:
                    note_tags = []
                if isinstance(note_tags, list):
                    for tag in note_tags:
                        if isinstance(tag, str):
                            tags.add(tag)
                        else:
                            tags.add(str(tag))
                elif isinstance(note_tags, str):
                    for tag in note_tags.split(","):
                        tag = tag.strip().strip('"')
                        if tag:
                            tags.add(tag)
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
    return sorted(tags)


def filter_notes_by_tags(notes_dir, required_tags):
    """
    Returns a list of note filenames that contain all of the required_tags.
    """
    matching_notes = []
    if not os.path.exists(notes_dir):
        print("Notes directory not found.")
        return matching_notes
    for filename in os.listdir(notes_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(notes_dir, filename)
            try:
                post = frontmatter.load(filepath)
                note_tags = post.get("tags", [])
                if note_tags is None:
                    note_tags = []
                if isinstance(note_tags, str):
                    note_tags = [
                        t.strip().strip('"') for t in note_tags.split(",") if t.strip()
                    ]
                if all(tag in note_tags for tag in required_tags):
                    matching_notes.append(filename)
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
    return sorted(matching_notes)


def extract_section(content, section_title):
    """
    Extracts and returns the text of a given section from the markdown content.
    """
    pattern = rf"^#\s*{re.escape(section_title)}\s*\n(.*?)(?=\n#|\Z)"
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""


def update_section(content, section_title, new_text):
    """
    Updates the specified section with new_text and returns the updated content.
    """
    pattern = rf"(^#\s*{re.escape(section_title)}\s*\n)(.*?)(?=\n#|\Z)"
    replacement = rf"\1{new_text}\n"
    new_content, count = re.subn(
        pattern, replacement, content, flags=re.DOTALL | re.MULTILINE
    )
    if count == 0:
        new_content = content + f"\n# {section_title}\n{new_text}\n"
    return new_content


def summarize_note_file(note_file, openai_token):
    """
    Uses OpenAI's API to summarize the note based on its Raw Notes, Processing, and Connecting sections.
    The summary and action items are then placed in the Summary section.
    """
    try:
        with open(note_file, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading note file: {e}")
        return None

    raw_notes = extract_section(content, "Raw Notes")
    processing = extract_section(content, "Processing")
    connecting = extract_section(content, "Connecting")

    prompt = (
        "Summarize the following sections and outline any action items mentioned:\n\n"
        f"Raw Notes:\n{raw_notes}\n\n"
        f"Processing:\n{processing}\n\n"
        f"Connecting:\n{connecting}\n\n"
        "Please provide a concise summary and list of action items."
        "Provide any additional context or insights as needed."
        "Record decisions made, who made them, and the rationale behind them."
        "Note agreed-upon follow-up meetings or checkpoints."
        "Describe the client's expressed needs, challenges, and goals."
        "Detail potential solutions discussed to address action items."
        "Outline next steps for the meeting, including any documents or information to be exchanged."
    )

    openai.api_key = openai_token
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes notes and extracts action items.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=2000,
        )
        summary_text = response.choices[0].message.content
    except Exception as e:
        print("Error calling OpenAI API:", e)
        return None

    new_content = update_section(content, "Summary", summary_text)
    try:
        with open(note_file, "w", encoding="utf-8") as f:
            f.write(new_content)
    except Exception as e:
        print(f"Error writing updated note file: {e}")
        return None

    return summary_text

import datetime
import os
import re
import subprocess

import frontmatter


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
    filename = f"{date_str}-{safe_title}.md"
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


def open_note(note_file, notes_dir, editor):
    if not os.path.isabs(note_file):
        note_file = os.path.join(notes_dir, note_file)
    if not os.path.exists(note_file):
        print(f"Note file not found: {note_file}")
        return
    subprocess.run([editor, note_file])


def list_notes(notes_dir):
    """
    Lists all Markdown files in the specified notes directory.
    """
    if not os.path.exists(notes_dir):
        print("No notes directory found.")
        return
    files = sorted([f for f in os.listdir(notes_dir) if f.endswith(".md")])
    if not files:
        print("No notes found.")
    else:
        print("Notes in repository:")
        for index, file in enumerate(files):
            print(f"{index} {file}")


def list_all_tags(notes_dir):
    """
    Iterates through all Markdown files and collects unique tags from the YAML front matter.
    Returns a sorted list of tags.
    """
    tags = set()
    if not os.path.exists(notes_dir):
        print("Notes directory not found.")
        return tags
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

import argparse

from config import DEFAULT_NOTES_DIR, load_settings, set_editor, set_notes_path
from note import (create_note, filter_notes_by_tags, list_all_tags, list_notes,
                  open_note)


def main():
    # Load settings to determine the current notes directory.
    settings = load_settings()
    notes_dir = settings.get("notes_dir", DEFAULT_NOTES_DIR)

    parser = argparse.ArgumentParser(
        description="A CLI tool for managing Markdown notes with persistent settings and tag filtering."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Command: Create a new note.
    parser_new = subparsers.add_parser("new", help="Create a new note")
    parser_new.add_argument(
        "--title", type=str, required=True, help="Title of the note"
    )
    parser_new.add_argument(
        "--tags", type=str, nargs="*", help="Optional tags for the note"
    )

    # Command: List all notes.
    parser_list = subparsers.add_parser("list", help="List all notes in the repository")

    # Command: Update the notes directory path.
    parser_setpath = subparsers.add_parser(
        "setpath", help="Set a new notes directory path"
    )
    parser_setpath.add_argument(
        "--path", type=str, required=True, help="New path for the notes directory"
    )

    # Command: List all unique tags.
    parser_tags = subparsers.add_parser(
        "tags", help="List all unique tags across notes"
    )

    # Command: Filter notes by one or more tags.
    parser_filter = subparsers.add_parser(
        "filter", help="List notes that have all specified tag(s)"
    )
    parser_filter.add_argument(
        "--tags", type=str, nargs="+", required=True, help="Tag(s) to filter notes by"
    )

    parser_seteditor = subparsers.add_parser(
        "seteditor", help="Set the default editor for opening notes"
    )
    parser_seteditor.add_argument(
        "--editor",
        type=str,
        required=True,
        help="Editor command (e.g., vim, nano, code)",
    )

    parser_open = subparsers.add_parser(
        "open", help="Open a note using the default editor"
    )
    parser_open.add_argument(
        "--file", type=str, required=True, help="Filename of the note to open"
    )

    args = parser.parse_args()

    if args.command == "new":
        create_note(args.title, args.tags, notes_dir)
    elif args.command == "list":
        list_notes(notes_dir)
    elif args.command == "setpath":
        set_notes_path(args.path)
    elif args.command == "seteditor":
        set_editor(args.editor)
    elif args.command == "tags":
        all_tags = list_all_tags(notes_dir)
        if all_tags:
            print("Unique tags found:")
            for tag in all_tags:
                print(f"- {tag}")
        else:
            print("No tags found.")
    elif args.command == "filter":
        matching_notes = filter_notes_by_tags(notes_dir, args.tags)
        if matching_notes:
            print(f"Notes containing the tags {args.tags}:")
            for note in matching_notes:
                print(f"- {note}")
        else:
            print(f"No notes found with tags {args.tags}.")
    elif args.command == "open":
        settings = load_settings()
        editor = settings.get("editor")
        if not editor:
            print("No default editor set. Use the 'seteditor' command to set one.")
            return
        note_file = args.file
        open_note(note_file, notes_dir, editor)


if __name__ == "__main__":
    main()

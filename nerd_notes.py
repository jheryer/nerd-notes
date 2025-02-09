import argparse

from config import (DEFAULT_NOTES_DIR, load_settings, print_config, set_editor,
                    set_git_remote, set_notes_path, set_openai_token)
from note import (create_note, filter_notes_by_tags, get_note_file,
                  list_all_tags, list_notes, open_note, print_tags,
                  summarize_note_file)
from sync import sync_notes


def main():
    settings = load_settings()
    notes_dir = settings.get("notes_dir", DEFAULT_NOTES_DIR)

    parser = argparse.ArgumentParser(
        description="A CLI tool for managing Markdown notes with persistent settings and tag filtering."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_new = subparsers.add_parser("new", help="Create a new note")
    parser_new.add_argument(
        "--title", type=str, required=True, help="Title of the note"
    )

    parser_new.add_argument(
        "--tags", type=str, nargs="*", help="Optional tags for the note"
    )

    parser_filter = subparsers.add_parser(
        "filter", help="List notes that have all specified tag(s)"
    )
    parser_filter.add_argument(
        "--tags", type=str, nargs="+", required=True, help="Tag(s) to filter notes by"
    )

    parser_open = subparsers.add_parser(
        "open", help="Open a note using the default editor"
    )

    subparsers.add_parser("list", help="List all notes in the repository")

    parser_open.add_argument(
        "--file", type=str, required=True, help="Filename of the note to open"
    )

    parser_view = subparsers.add_parser(
        "view", help="View a note in the CLI with markdown rendering"
    )
    parser_view.add_argument(
        "--file",
        type=str,
        required=True,
        help="Filename or index number of the note to view",
    )

    parser_summarize = subparsers.add_parser(
        "summarize", help="Summarize a note and update its Summary section"
    )
    parser_summarize.add_argument(
        "--file",
        type=str,
        required=True,
        help="Filename or index number of the note to summarize",
    )

    parser_sync = subparsers.add_parser(
        "sync", help="Sync the notes directory to the remote Git repository"
    )
    parser_sync.add_argument(
        "--repo",
        type=str,
        help="Optional: Override the configured remote repository URL",
    )

    parser_settings = subparsers.add_parser(
        "settings", help="View or update configuration settings"
    )
    parser_settings.add_argument(
        "--path", type=str, help="Set a new notes directory path"
    )
    parser_settings.add_argument(
        "--editor", type=str, help="Set the default editor (e.g., vim, nano, code)"
    )
    parser_settings.add_argument("--token", type=str, help="Set the OpenAI API token")
    parser_settings.add_argument(
        "--git", type=str, help="Set the remote Git repository URL for syncing notes"
    )

    args = parser.parse_args()

    if args.command == "new":
        create_note(args.title, args.tags, notes_dir)
    elif args.command == "list":
        list_notes(notes_dir)
    elif args.command == "settings":

        changed = False
        if args.path:
            set_notes_path(args.path)
            changed = True
        if args.editor:
            set_editor(args.editor)
            changed = True
        if args.token:
            set_openai_token(args.token)
            changed = True
        if args.git:
            set_git_remote(args.git)
            changed = True
        if not changed:
            settings = load_settings()
            print_config(settings)

    elif args.command == "tags":

        all_tags = list_all_tags(notes_dir)
        print_tags(all_tags)

    elif args.command == "filter":

        matching_notes = filter_notes_by_tags(notes_dir, args.tags)

        if matching_notes:
            list_notes(notes_dir, matching_notes)
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

    elif args.command == "view":

        note_file = args.file
        open_note(note_file, notes_dir, None)

    elif args.command == "summarize":

        note_input = args.file
        settings = load_settings()
        openai_token = settings.get("openai_token")

        if not openai_token:
            print("No OpenAI API token set. Use the 'settoken' command to set one.")
            return

        note_file = get_note_file(note_input, notes_dir)

        if not note_file:
            print("Note not found.")
            return

        summary = summarize_note_file(note_file, openai_token)

        if summary:
            print("Summary updated successfully:")
            print(summary)
        else:
            print("Failed to generate summary.")

    elif args.command == "sync":

        repo = args.repo if args.repo else settings.get("git_remote")
        if not repo:
            print(
                "No Git remote repository configured. Use the 'setgit' command or pass --repo to set one."
            )
            return
        sync_notes(notes_dir, repo)


if __name__ == "__main__":
    main()

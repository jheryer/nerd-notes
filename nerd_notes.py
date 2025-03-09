import argparse

from arg_parser import get_args
from config import (DEFAULT_NOTES_DIR, load_settings, print_config, set_editor,
                    set_git_remote, set_notes_path, set_openai_token)
from note import (create_note, filter_notes_by_tags, get_note_file,
                  list_all_tags, list_notes, open_note, print_tags,
                  summarize_note_file)
from sync import sync_notes


def execute_create_note(args):
    settings = load_settings()
    notes_dir = settings.get("notes_dir", DEFAULT_NOTES_DIR)
    create_note(args.title, args.tags, notes_dir)


def execute_list_notes(args):
    settings = load_settings()
    notes_dir = settings.get("notes_dir", DEFAULT_NOTES_DIR)
    list_notes(notes_dir)


def execute_change_settings(args):
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


# def execute_print_config(args):
#     pass
def execute_list_tags(args):
    settings = load_settings()
    notes_dir = settings.get("notes_dir", DEFAULT_NOTES_DIR)
    all_tags = list_all_tags(notes_dir)
    print_tags(all_tags)


def execute_print_tags(args):
    settings = load_settings()
    notes_dir = settings.get("notes_dir", DEFAULT_NOTES_DIR)
    all_tags = list_all_tags(notes_dir)
    print_tags(all_tags)


def execute_filter_notes_by_tags(args):
    settings = load_settings()
    notes_dir = settings.get("notes_dir", DEFAULT_NOTES_DIR)
    matching_notes = filter_notes_by_tags(notes_dir, args.tags)

    if matching_notes:
        list_notes(notes_dir, matching_notes)
    else:
        print(f"No notes found with tags {args.tags}.")


def execute_view_note(args):
    settings = load_settings()
    notes_dir = settings.get("notes_dir", DEFAULT_NOTES_DIR)

    note_file = args.file
    open_note(note_file, notes_dir, None)


def execute_open_note(args):
    settings = load_settings()
    notes_dir = settings.get("notes_dir", DEFAULT_NOTES_DIR)
    editor = settings.get("editor")

    if not editor:
        print("No default editor set. Use the 'seteditor' command to set one.")
        return

    note_file = args.file
    open_note(note_file, notes_dir, editor)


def execute_summary_note_file(args):
    note_input = args.file
    settings = load_settings()
    notes_dir = settings.get("notes_dir", DEFAULT_NOTES_DIR)
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


def execute_sync_notes(args):
    settings = load_settings()
    notes_dir = settings.get("notes_dir", DEFAULT_NOTES_DIR)
    repo = args.repo if args.repo else settings.get("git_remote")
    if not repo:
        print(
            "No Git remote repository configured. Use the 'setgit' command or pass --repo to set one."
        )
        return
    sync_notes(notes_dir, repo)


def main():

    command_handlers = {
        "new": execute_create_note,
        "list": execute_list_notes,
        "settings": execute_change_settings,
        "tags": execute_list_tags,
        "filter": execute_filter_notes_by_tags,
        "open": execute_open_note,
        "view": execute_view_note,
        "summarize": execute_summary_note_file,
        "sync": execute_sync_notes,
    }

    args = get_args()

    command_handlers[args.command](args)

    # if args.command == "new":
    #     create_note(args.title, args.tags, notes_dir)
    # elif args.command == "list":
    #     list_notes(notes_dir)
    # elif args.command == "settings":
    #
    #     changed = False
    #     if args.path:
    #         set_notes_path(args.path)
    #         changed = True
    #     if args.editor:
    #         set_editor(args.editor)
    #         changed = True
    #     if args.token:
    #         set_openai_token(args.token)
    #         changed = True
    #     if args.git:
    #         set_git_remote(args.git)
    #         changed = True
    #     if not changed:
    #         settings = load_settings()
    #         print_config(settings)
    #
    # elif args.command == "tags":
    #
    #     all_tags = list_all_tags(notes_dir)
    #     print_tags(all_tags)
    #
    # elif args.command == "filter":
    #
    #     matching_notes = filter_notes_by_tags(notes_dir, args.tags)
    #
    #     if matching_notes:
    #         list_notes(notes_dir, matching_notes)
    #     else:
    #         print(f"No notes found with tags {args.tags}.")
    #
    # elif args.command == "open":
    #
    #     settings = load_settings()
    #     editor = settings.get("editor")
    #
    #     if not editor:
    #         print("No default editor set. Use the 'seteditor' command to set one.")
    #         return
    #
    #     note_file = args.file
    #     open_note(note_file, notes_dir, editor)
    #
    # elif args.command == "view":
    #
    #     note_file = args.file
    #     open_note(note_file, notes_dir, None)
    #
    # elif args.command == "summarize":
    #
    #     note_input = args.file
    #     settings = load_settings()
    #     openai_token = settings.get("openai_token")
    #
    #     if not openai_token:
    #         print("No OpenAI API token set. Use the 'settoken' command to set one.")
    #         return
    #
    #     note_file = get_note_file(note_input, notes_dir)
    #
    #     if not note_file:
    #         print("Note not found.")
    #         return
    #
    #     summary = summarize_note_file(note_file, openai_token)
    #
    #     if summary:
    #         print("Summary updated successfully:")
    #         print(summary)
    #     else:
    #         print("Failed to generate summary.")
    #
    # elif args.command == "sync":
    #
    #     repo = args.repo if args.repo else settings.get("git_remote")
    #     if not repo:
    #         print(
    #             "No Git remote repository configured. Use the 'setgit' command or pass --repo to set one."
    #         )
    #         return
    #     sync_notes(notes_dir, repo)


if __name__ == "__main__":
    main()

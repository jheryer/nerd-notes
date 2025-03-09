import argparse


def get_args():

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
    return args

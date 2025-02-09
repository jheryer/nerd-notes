import os

import yaml

CONFIG_DIR = os.path.expanduser("~/.nerd_notes")
SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.yaml")
DEFAULT_NOTES_DIR = os.path.join(CONFIG_DIR, "notes")


def load_settings():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    if not os.path.exists(SETTINGS_FILE):
        settings = {"notes_dir": DEFAULT_NOTES_DIR}
        save_settings(settings)
    else:
        with open(SETTINGS_FILE, "r") as f:
            settings = yaml.safe_load(f)
            if not settings:
                settings = {"notes_dir": DEFAULT_NOTES_DIR}
    return settings


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        yaml.dump(settings, f)


def print_config(settings):
    print("Current settings:")
    print(f"  Notes Directory: {settings.get('notes_dir')}")
    print(f"  Default Editor: {settings.get('editor') or '(not set)'}")
    print(f"  Git Remote: {settings.get('git_remote') or '(not set)'}")
    token_status = "set" if settings.get("openai_token") else "not set"
    print(f"  OpenAI Token: ({token_status})")


def set_notes_path(new_path):
    new_path = os.path.expanduser(new_path)
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    settings = load_settings()
    settings["notes_dir"] = new_path
    save_settings(settings)
    print(f"Notes directory updated to: {new_path}")


def set_editor(editor_command):
    settings = load_settings()
    settings["editor"] = editor_command
    save_settings(settings)
    print(f"Default editor updated to: {editor_command}")


def set_openai_token(token):
    settings = load_settings()
    settings["openai_token"] = token
    save_settings(settings)
    print("OpenAI API token set.")


def set_git_remote(remote):
    settings = load_settings()
    settings["git_remote"] = remote
    save_settings(settings)
    print("git remote url set.")

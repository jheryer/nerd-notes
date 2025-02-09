import os

import yaml

# Define the default configuration directory and file.
CONFIG_DIR = os.path.expanduser("~/.nerd_notes")
SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.yaml")
DEFAULT_NOTES_DIR = os.path.join(CONFIG_DIR, "notes")


def load_settings():
    """
    Loads settings from the SETTINGS_FILE.
    If the file (or config directory) doesn't exist, it creates them with default settings.
    """
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
    """
    Saves the settings dictionary to the SETTINGS_FILE.
    """
    with open(SETTINGS_FILE, "w") as f:
        yaml.dump(settings, f)


def set_notes_path(new_path):
    """
    Updates the settings with a new notes directory path.
    The new directory is created if it doesn't exist.
    """
    new_path = os.path.expanduser(new_path)
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    settings = load_settings()
    settings["notes_dir"] = new_path
    save_settings(settings)
    print(f"Notes directory updated to: {new_path}")


def set_editor(editor_command):
    """
    Updates the settings with the default editor command.
    """
    settings = load_settings()
    settings["editor"] = editor_command
    save_settings(settings)
    print(f"Default editor updated to: {editor_command}")


def set_openai_token(token):
    """
    Updates the settings with the OpenAI API token.
    """
    settings = load_settings()
    settings["openai_token"] = token
    save_settings(settings)
    print("OpenAI API token set.")

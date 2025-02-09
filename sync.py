import os
import subprocess


def create_gitignore(notes_dir):
    """
    Create or update a .gitignore file in the notes directory to ignore settings.yaml.
    """
    gitignore_path = os.path.join(notes_dir, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            lines = f.read().splitlines()
    else:
        lines = []
    if "settings.yaml" not in lines:
        lines.append("settings.yaml")
    with open(gitignore_path, "w") as f:
        f.write("\n".join(lines) + "\n")


def init_git_repo(notes_dir, remote_repo):
    """
    Initializes a git repository in the notes directory if not already present
    and sets the remote repository URL.
    """
    git_dir = os.path.join(notes_dir, ".git")
    if not os.path.exists(git_dir):
        print("Initializing git repository...")
        subprocess.run(["git", "init"], cwd=notes_dir, check=True)
    remotes = subprocess.run(
        ["git", "remote"], cwd=notes_dir, capture_output=True, text=True
    )
    if "origin" not in remotes.stdout:
        print(f"Setting remote repository to {remote_repo}...")
        subprocess.run(
            ["git", "remote", "add", "origin", remote_repo], cwd=notes_dir, check=True
        )


def sync_notes(notes_dir, remote_repo):
    """
    Syncs the notes directory with the remote Git repository:
    - Ensures .gitignore includes settings.yaml.
    - Initializes the git repo and sets the remote if needed.
    - Pulls changes from the remote repository.
    - Adds, commits, and pushes all changes.
    """
    create_gitignore(notes_dir)
    init_git_repo(notes_dir, remote_repo)

    branch_proc = subprocess.run(
        ["git", "symbolic-ref", "--short", "HEAD"],
        cwd=notes_dir,
        capture_output=True,
        text=True,
        check=True,
    )
    branch_name = branch_proc.stdout.strip()
    if not branch_name:
        branch_name = "main"

    # Pull remote changes first.
    print("Pulling changes from remote repository...")
    try:
        subprocess.run(
            ["git", "pull", "--rebase", "origin", branch_name],
            cwd=notes_dir,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"No files pulled. {e}")

    print("Adding changes to git...")
    subprocess.run(["git", "add", "."], cwd=notes_dir, check=True)

    # Check if there are changes to commit.
    commit_check = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=notes_dir)
    if commit_check.returncode != 0:
        print("Committing changes...")
        subprocess.run(["git", "commit", "-m", "Sync notes"], cwd=notes_dir, check=True)
    else:
        print("No changes to commit.")

    print("Pushing changes to remote repository...")
    subprocess.run(
        ["git", "push", "-u", "origin", branch_name], cwd=notes_dir, check=True
    )
    print("Sync complete.")

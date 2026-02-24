#!/usr/bin/env python3
"""
Generate GitHub wiki pages from the repository README and commit history.

Pages generated:
  Home.md            - Current README content
  Version-History.md - Changelog grouped by version across all commits to main
"""

import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "wiki"


def run(cmd: list[str], cwd: Path = REPO_ROOT) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def parse_version_from_readme(readme_text: str) -> str:
    """Extract version string from README (e.g. '> Version 1.0' → '1.0')."""
    match = re.search(r">\s*[Vv]ersion\s+([\d.]+)", readme_text)
    return match.group(1) if match else "unknown"


def get_commits() -> list[dict]:
    """Return all commits reachable from HEAD, oldest first."""
    log = run([
        "git", "--no-pager", "log",
        "--reverse",
        "--format=%H|%ad|%s",
        "--date=short",
        "HEAD",
    ])
    commits = []
    for line in log.splitlines():
        if not line.strip():
            continue
        sha, date, subject = line.split("|", 2)
        commits.append({"sha": sha, "date": date, "subject": subject})
    return commits


def get_changed_files(sha: str) -> list[str]:
    """List files changed in a commit."""
    output = run(["git", "--no-pager", "diff-tree", "--no-commit-id", "-r", "--name-only", sha])
    return [f for f in output.splitlines() if f.strip()]


def get_readme_at(sha: str) -> str:
    """Read README.md content at a given commit (empty string if not present)."""
    result = subprocess.run(
        ["git", "show", f"{sha}:README.md"],
        capture_output=True, text=True, cwd=REPO_ROOT
    )
    return result.stdout if result.returncode == 0 else ""


def build_home_page() -> str:
    """Return the Home wiki page content (mirrors current README)."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    header = (
        "> _This page is auto-generated from the repository README._\n\n"
    )
    return header + readme


def build_version_history_page() -> str:
    """Return the Version History wiki page content."""
    commits = get_commits()

    lines = [
        "# Version History\n",
        "> _Auto-generated from commit history. Each entry represents a commit to `main`._\n",
    ]

    # Walk commits newest → oldest for display
    for commit in reversed(commits):
        sha = commit["sha"]
        date = commit["date"]
        subject = commit["subject"]

        readme_text = get_readme_at(sha)
        version = parse_version_from_readme(readme_text) if readme_text else "unknown"

        changed = get_changed_files(sha)
        files_section = ""
        if changed:
            file_list = "\n".join(f"  - `{f}`" for f in changed)
            files_section = f"\n**Changed files:**\n{file_list}\n"

        lines.append(
            f"\n---\n\n"
            f"## v{version}  \n"
            f"**Commit:** `{sha[:8]}`  \n"
            f"**Date:** {date}  \n"
            f"**Summary:** {subject}\n"
            f"{files_section}"
        )

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append("\n---")
    lines.append(f"\n_Last updated: {now}_\n")
    return "\n".join(lines)


def write_wiki_pages() -> None:
    WIKI_DIR.mkdir(parents=True, exist_ok=True)

    home = build_home_page()
    (WIKI_DIR / "Home.md").write_text(home, encoding="utf-8")
    print("Written: Home.md")

    version_history = build_version_history_page()
    (WIKI_DIR / "Version-History.md").write_text(version_history, encoding="utf-8")
    print("Written: Version-History.md")


if __name__ == "__main__":
    write_wiki_pages()

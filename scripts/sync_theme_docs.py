#!/usr/bin/env python3
"""
Copies the theme docs into the wiki, from where they're written:

  PortMaster-GUI/THEME.md                 -> docs/contribute/gui/theme-engine.md  (the reference)
  PortMaster-Themes/CREATING_A_THEME.md   -> docs/contribute/gui/creating-a-theme.md  (the guide)

and their pictures into docs/assets/images/themes/. Links between the two become links between
the wiki pages; links to the repositories' files become GitHub links.

    python3 scripts/sync_theme_docs.py --gui ../PortMaster-GUI --themes ../PortMaster-Themes

Run it after either file changes, then build and check the pages. Edit the docs in their
repositories, not here: the next sync replaces these pages.
"""
import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "docs" / "contribute" / "gui"
IMAGES = ROOT / "docs" / "assets" / "images" / "themes"
## From docs/contribute/gui/<page>.md to docs/assets/images/themes/
IMAGE_LINK = "../../assets/images/themes"

GUI_BLOB = "https://github.com/PortsMaster/PortMaster-GUI/blob/main"
THEMES_TREE = "https://github.com/PortsMaster/PortMaster-Themes/tree/main"
THEMES_BLOB = "https://github.com/PortsMaster/PortMaster-Themes/blob/main"

HEADER = """---
# Made from {source} by scripts/sync_theme_docs.py: change it there, then sync.
# Its text has {{tags}} and {{{{ that aren't template tags.
render_macros: false
---

"""


## Links to other files in the repository, not to the wiki's own pages or pictures.
REPO_LINK = r"\]\((?!https?:|#|\.\./|theme-engine\.md|creating-a-theme\.md)([^)]+)\)"


def outside_code(text, change):
    """change() applied to the text outside ``` blocks: examples in them stay as they are."""
    parts = re.split(r"(\n[ \t]*```.*?\n[ \t]*```)", text, flags=re.S)
    return "".join(part if part.lstrip(" \t\n").startswith("```") else change(part) for part in parts)


def drop_contents(text):
    """The page's own table of contents: the wiki's navigation has one."""
    return re.sub(r"\n## Contents\n.*?(?=\n## )", "\n", text, count=1, flags=re.S)


def reference(gui):
    text = (gui / "THEME.md").read_text(encoding="utf-8")
    text = drop_contents(text)
    text = text.replace("](docs/theme/", f"]({IMAGE_LINK}/reference/")
    text = re.sub(r"\]\(https://github\.com/PortsMaster/PortMaster-Themes/blob/main/CREATING_A_THEME\.md(#[^)]*)?\)",
                  lambda m: f"](creating-a-theme.md{m.group(1) or ''})", text)
    ## On the wiki the guide is the next page, not another repository's.
    text = text.replace("(creating-a-theme.md), in the PortMaster-Themes repository.", "(creating-a-theme.md).")
    ## Repository paths in the text ("`tools/theme_docs.py`" stays as it is; links become GitHub's).
    text = outside_code(text, lambda part: re.sub(REPO_LINK, lambda m: f"]({GUI_BLOB}/{m.group(1)})", part))
    note = (f"\n!!! info \"Also in PortMaster-GUI\"\n    This page is [THEME.md]({GUI_BLOB}/THEME.md), PortMaster's theme reference. "
            "Its tests check it names every key the theme engine has.\n")
    text = re.sub(r"(\n\*\*New to themes\?\*\*[^\n]*\n)", lambda m: m.group(1) + note, text, count=1)
    (PAGES / "theme-engine.md").write_text(HEADER.format(source="PortMaster-GUI's THEME.md") + text, encoding="utf-8")

    target = IMAGES / "reference"
    shutil.rmtree(str(target), ignore_errors=True)
    shutil.copytree(str(gui / "docs" / "theme"), str(target))


def guide(themes):
    text = (themes / "CREATING_A_THEME.md").read_text(encoding="utf-8")
    text = drop_contents(text)
    text = text.replace("](docs/images/", f"]({IMAGE_LINK}/guide/")
    text = text.replace("](docs/tutorial/step-6/buttons.png)", f"]({IMAGE_LINK}/guide/buttons.png)")
    text = re.sub(r"\]\(https://github\.com/PortsMaster/PortMaster-GUI/blob/main/THEME\.md(#[^)]*)?\)",
                  lambda m: f"](theme-engine.md{m.group(1) or ''})", text)

    def repo_link(match):
        path = match.group(1)
        if path.endswith("/"):
            return f"]({THEMES_TREE}/{path.rstrip('/')})"
        return f"]({THEMES_BLOB}/{path})"

    text = outside_code(text, lambda part: re.sub(REPO_LINK, repo_link, part))
    (PAGES / "creating-a-theme.md").write_text(HEADER.format(source="PortMaster-Themes' CREATING_A_THEME.md") + text, encoding="utf-8")

    target = IMAGES / "guide"
    shutil.rmtree(str(target), ignore_errors=True)
    shutil.copytree(str(themes / "docs" / "images"), str(target))
    shutil.copy(str(themes / "docs" / "tutorial" / "step-6" / "buttons.png"), str(target / "buttons.png"))


def main():
    parser = argparse.ArgumentParser(description="Copies the theme docs into the wiki.")
    parser.add_argument("--gui", type=Path, default=ROOT.parent / "PortMaster-GUI")
    parser.add_argument("--themes", type=Path, default=ROOT.parent / "PortMaster-Themes")
    options = parser.parse_args()
    reference(options.gui)
    guide(options.themes)
    print("theme-engine.md, creating-a-theme.md and their pictures: done")


if __name__ == "__main__":
    main()

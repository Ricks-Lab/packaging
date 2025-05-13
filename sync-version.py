#!/usr/bin/env python3

import re
from datetime import datetime
import tzlocal
from pathlib import Path

def get_version_from_init(init_file):
    content = init_file.read_text()
    match = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", content)
    if not match:
        raise ValueError("No version found in __init__.py")
    return match.group(1)

def update_pyproject(version):
    pyproject = Path("pyproject.toml")
    text = pyproject.read_text()
    text = re.sub(r'version\s*=\s*"[0-9a-zA-Z.\-]+"', f'version = "{version}"', text)
    pyproject.write_text(text)
    print(f"Updated pyproject.toml to version {version}")

def update_changelog(version):
    changelog = Path("debian/changelog")
    text = changelog.read_text()

    # Update version (first match in first line)
    text = re.sub(r"\([^\)]+\)", f"({version})", text, count=1)

    # Update timestamp in the maintainer signature line
    now = datetime.now(tzlocal.get_localzone())
    debian_time = now.strftime("%a, %d %b %Y %H:%M:%S %z")

    # Replace timestamp in the last line (starts with "-- ")
    text = re.sub(
        r"(-- .+?)  .+",
        rf"\1  {debian_time}",
        text,
        count=1
    )

    changelog.write_text(text)
    print(f"Updated debian/changelog to version {version} and timestamp {debian_time}")


def main():
    version = get_version_from_init(Path("src/SLOmodules/__init__.py"))
    update_pyproject(version)
    update_changelog(version)

if __name__ == "__main__":
    main()


# Packaging Environment - README

This `packaging` virtual environment is dedicated to building, validating, and distributing Python projects. It supports **PyPI uploads** and **Debian (.deb) package builds**.

---

## 1. System Requirements

Install these **APT packages** before using this environment:

```bash
sudo apt update
sudo apt install -y \
    python3-venv python3-pip \
    fakeroot devscripts debhelper dh-python lintian gpg
```

| Package        | Purpose                                          |
| -------------- | ------------------------------------------------ |
| `python3-venv` | Create virtual environments                      |
| `python3-pip`  | Install Python packages                          |
| `fakeroot`     | Build `.deb` files without real root permissions |
| `devscripts`   | Tools like `debuild`, `dch` for Debian packaging |
| `debhelper`    | Scripts to help Debian packaging                 |
| `dh-python`    | Integrate Python packages into Debian builds     |
| `lintian`      | Validate `.deb` quality                          |
| `gpg`          | Sign packages or uploads if needed               |

---

## 2. Initial venv Setup

```bash
cd ~/pydev/packaging
python3 -m venv venv
source venv/bin/activate
```

Upgrade and install critical Python packaging tools:

```bash
pip install --upgrade pip setuptools wheel
pip install build twine stdeb check-manifest validate-pyproject setuptools_scm
```

Optional extras:

```bash
pip install hatchling flit
```

---

## 3. Building and Publishing Projects

### 3.1 Build PyPI package

```bash
python -m build
```

Artifacts appear under `dist/`.

### 3.2 Upload to PyPI

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi

[pypi]
username = __token__
password = pypi-<your-token-here>
```

Then upload:

```bash
twine upload dist/*
```

### 3.3 Build Debian package (.deb)

Simple build:

```bash
python setup.py --command-packages=stdeb.command bdist_deb
```

Full manual control:

```bash
debuild -us -uc
```

Check `.deb` with:

```bash
lintian ../your-package_*.deb
```

---

## 4. Validating Packaging

Before releasing:

```bash
check-manifest
validate-pyproject
```

Useful when using `pyproject.toml` structure.

---

## 5. Recommended Directory Layout

```text
~/pydev/packaging/
├── README.md
├── venv/               # Virtual environment only for packaging
├── Makefile            # (Optional) Automate builds
├── project-srcs/       # (Optional) Source trees ready to package
```

---

## 6. Troubleshooting

- **Problem**: Missing system package?

  - **Solution**: Re-run `apt install` list from Section 1.

- **Problem**: GPG key error during PyPI upload?

  - **Solution**: Run `gpg --list-keys` and configure signing properly, or upload without signing if using token auth.

- **Problem**: Wrong Python version?

  - **Solution**: Create a separate virtual environment under Python 3.10/3.11.

---

## 7. Best Practices

- Build **from clean git tags**.
- Use **setuptools\_scm** for versioning if possible.
- Always **test installs** inside a fresh venv.
- Only install packaging-specific tools into this environment.
- \*\*Use \*\*\`\` before uploads.

---

*Updated: 2025-04-27*

Maintained by **Rick's Lab**.




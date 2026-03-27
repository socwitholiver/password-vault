# OJ Vault 2.0

OJ Vault 2.0 is a premium desktop password vault built with Python, `ttkbootstrap`, and `cryptography`. It stores credentials locally, encrypts them with Fernet, and now ships with a darker security-focused interface, faster entry management, and a packaged Windows app.

## What's New in v2.0

- Premium dark desktop redesign with custom branding
- Branded shield-and-lock header mark
- Searchable vault table with password-strength labels
- Edit entry workflow without leaving the main screen
- Copy-to-clipboard from the selected entry or by double-clicking a row
- First-run key generation so the app boots cleanly for new users

## Features

- Add, edit, view, search, copy, and delete passwords
- Local Fernet encryption for stored credentials
- Fully offline desktop workflow
- Windows executable build with PyInstaller

## Quick Start

### Launch locally with one click

On Windows, you can double-click `launch-oj-vault.bat` to start the source version of the app from the project folder.

### Run from source

```bash
pip install cryptography ttkbootstrap pyinstaller
python vault_gui.py
```

On first launch, the app creates `key.key` automatically if it does not already exist.

## Windows App Download

For the GitHub release, attach the packaged executable asset and use this direct-download pattern in the release notes or README:

`https://github.com/socwitholiver/password-vault/releases/download/v2.0.0/OJ-Vault-2.0.exe`

That link will download the app immediately when clicked once the `v2.0.0` release asset is published.

Recommended README button/link:

`[Download OJ Vault 2.0 for Windows](https://github.com/socwitholiver/password-vault/releases/download/v2.0.0/OJ-Vault-2.0.exe)`

## Build the Executable

```bash
pyinstaller --clean --noconfirm vault_gui.spec
```

The packaged app will be generated in `dist/`.

Local helper launcher:

- `launch-oj-vault.bat`

## Release Plan

1. Commit the v2.0 changes.
2. Push to `origin`.
3. Create tag `v2.0.0`.
4. Upload the packaged executable to the GitHub release.
5. Point users to the direct release asset link.

## Security Notes

- `key.key` is unique to each installation and should not be shared.
- `vault.txt` stays local and encrypted with the generated key.
- If a user loses their original key, previously encrypted entries cannot be recovered with a new one.

## Author

[oliverjacksonvictor](https://github.com/oliverjacksonvictor)

 🔐 PVAULT By OJ

**PVAULT By OJ** is a secure, offline desktop password manager built in Python. It allows users to store, view, and delete encrypted passwords locally — no internet needed. The app features a sleek modern GUI, AES encryption, a master password system, activity logging, and `.exe` packaging for easy use.

---

## 🚀 Features

- 🔒 Master password protection before access
- 💾 Add, view, and delete encrypted passwords
- 🧪 AES encryption using `Fernet` from `cryptography`
- 👁 Toggle show/hide password visibility
- 🌗 Switch between dark mode and light mode
- 📜 Activity logging (login attempts, changes)
- 🔁 Auto-builds `.exe` when Python files are updated
- ✅ Fully offline — no data leaves your computer

---

## 📁 Project Structure

password-vault/
├── main.py # Core logic (encryption, vault ops)
├── gui.py # Modern GUI using customtkinter
├── key.key # AES encryption key (auto-generated)
├── vault.txt # Encrypted password storage
├── master.key # Encrypted master password
├── activity.log # Action log file
├── auto_build.py # Auto rebuilds .exe when code changes
├── requirements.txt # Python dependencies
├── README.md # This file
└── dist/ # Output folder for .exe

yaml
Copy
Edit

---

## 💡 How It Works

1. **Master Password**: On first use, you’re prompted to set a master password (encrypted in `master.key`).
2. **Key Generation**: App generates `key.key` to use with AES encryption.
3. **Add Passwords**: You enter a site and password, which gets encrypted and saved in `vault.txt`.
4. **View Passwords**: The app decrypts and displays all stored entries.
5. **Delete Passwords**: Easily remove any entry by its site name.
6. **Logs**: All activities are logged in `activity.log`.

---

## 🧑‍💻 Installation

### 🔧 Option 1: Run the Python Code

1. Clone this repo:
   ```bash
   git clone https://github.com/socwitholiver/password-vault
   cd password-vault
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Launch the app:

bash
Copy
Edit
python gui.py
🧊 Option 2: Run the .exe
Go to the dist/ folder

Run:
PVAULT-By-OJ.exe
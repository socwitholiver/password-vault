import os
from cryptography.fernet import Fernet
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox, Querybox

# --- Load or create key ---
def load_key():
    return open("key.key", "rb").read()

def encrypt_password(password, key):
    return Fernet(key).encrypt(password.encode())

def decrypt_password(encrypted_password, key):
    return Fernet(key).decrypt(encrypted_password).decode()

# --- GUI Logic ---
class PasswordVaultGUI:
    def __init__(self, root):
        self.key = load_key()
        self.root = root
        self.root.title("🔐 Password Vault")
        self.root.geometry("420x520")
        self.root.resizable(False, False)

        # Theme
        style = ttk.Style("darkly")

        # Title
        ttk.Label(root, text="Password Vault", font=("Segoe UI", 18, "bold")).pack(pady=15)

        # Site input
        ttk.Label(root, text="Site:", font=("Segoe UI", 10)).pack()
        self.site_entry = ttk.Entry(root, width=35)
        self.site_entry.pack(pady=5)

        # Password input
        ttk.Label(root, text="Password:", font=("Segoe UI", 10)).pack()
        self.pass_entry = ttk.Entry(root, show="*", width=35)
        self.pass_entry.pack(pady=5)

        # Buttons
        ttk.Button(root, text="➕ Add Password", bootstyle="success", command=self.add_password).pack(pady=10)
        ttk.Button(root, text="👁 View Passwords", bootstyle="info", command=self.view_passwords).pack(pady=5)
        ttk.Button(root, text="🗑 Delete Password", bootstyle="danger", command=self.delete_password).pack(pady=5)

        # Output area
        self.output = ttk.ScrolledText(root, width=45, height=15, wrap="word")
        self.output.pack(pady=10)

    def add_password(self):
        site = self.site_entry.get().strip()
        pwd = self.pass_entry.get().strip()
        if site and pwd:
            encrypted = encrypt_password(pwd, self.key)
            with open("vault.txt", "a") as vault:
                vault.write(f"{site}|{encrypted.decode()}\n")
            Messagebox.show_info(f"Password for '{site}' saved!", title="Success")
            self.site_entry.delete(0, "end")
            self.pass_entry.delete(0, "end")
        else:
            Messagebox.show_error("Please fill in both fields.", title="Error")

    def view_passwords(self):
        self.output.delete("1.0", "end")
        if not os.path.exists("vault.txt"):
            self.output.insert("end", "Vault is empty.")
            return

        with open("vault.txt", "r") as vault:
            for line in vault:
                site, enc_pass = line.strip().split("|")
                try:
                    dec_pass = decrypt_password(enc_pass.encode(), self.key)
                    self.output.insert("end", f"{site}: {dec_pass}\n")
                except:
                    self.output.insert("end", f"{site}: [Decryption Error]\n")

    def delete_password(self):
        site = Querybox.get_string("Enter site name to delete:", title="Delete Password")
        if site:
            lines = []
            found = False
            with open("vault.txt", "r") as vault:
                lines = vault.readlines()
            with open("vault.txt", "w") as vault:
                for line in lines:
                    if not line.startswith(site + "|"):
                        vault.write(line)
                    else:
                        found = True
            if found:
                Messagebox.show_info(f"Password for '{site}' deleted.", title="Deleted")
            else:
                Messagebox.show_warning(f"No password found for '{site}'.", title="Not Found")

# --- Run GUI ---
if __name__ == "__main__":
    root = ttk.Window(themename="cyborg")
    app = PasswordVaultGUI(root)
    root.mainloop()
import cryptography.hazmat.backends.openssl.backend

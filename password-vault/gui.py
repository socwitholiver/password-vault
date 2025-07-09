# gui.py

import customtkinter as ctk
from main import (
    add_password,
    get_passwords,
    delete_password,
    verify_master_password,
    set_master_password,
    MASTER_FILE
)
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PVAULT By OJ - Login")
        self.geometry("400x250")
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text="Enter Master Password" if os.path.exists(MASTER_FILE) else "Set Master Password", font=ctk.CTkFont(size=16, weight="bold"))
        self.label.pack(pady=20)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Master Password", show="*")
        self.password_entry.pack(pady=10)

        self.show_password = False
        self.toggle_button = ctk.CTkButton(self, text="Show", width=60, command=self.toggle_visibility)
        self.toggle_button.pack(pady=5)

        self.login_button = ctk.CTkButton(self, text="Submit", command=self.submit)
        self.login_button.pack(pady=10)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=5)

    def toggle_visibility(self):
        self.show_password = not self.show_password
        self.password_entry.configure(show="" if self.show_password else "*")
        self.toggle_button.configure(text="Hide" if self.show_password else "Show")

    def submit(self):
        password = self.password_entry.get()
        if not password:
            self.error_label.configure(text="Enter a password")
            return

        if os.path.exists(MASTER_FILE):
            if verify_master_password(password):
                self.destroy()
                app = VaultApp()
                app.mainloop()
            else:
                self.error_label.configure(text="Incorrect master password")
        else:
            set_master_password(password)
            self.destroy()
            app = VaultApp()
            app.mainloop()

class VaultApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🔐 PVAULT By OJ")
        self.geometry("600x600")
        self.resizable(False, False)

        self.site_entry = ctk.CTkEntry(self, placeholder_text="Site Name")
        self.site_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        self.show_password = False
        self.toggle_pass_btn = ctk.CTkButton(self, text="Show Password", command=self.toggle_password_visibility)
        self.toggle_pass_btn.pack(pady=5)

        self.add_btn = ctk.CTkButton(self, text="➕ Add Password", command=self.add)
        self.add_btn.pack(pady=5)

        self.view_btn = ctk.CTkButton(self, text="👁 View Passwords", command=self.view)
        self.view_btn.pack(pady=5)

        self.delete_btn = ctk.CTkButton(self, text="🗑 Delete Password", command=self.delete)
        self.delete_btn.pack(pady=5)

        self.theme_toggle_btn = ctk.CTkButton(self, text="🌗 Toggle Dark/Light Mode", command=self.toggle_theme)
        self.theme_toggle_btn.pack(pady=10)

        self.output_box = ctk.CTkTextbox(self, width=550, height=250)
        self.output_box.pack(pady=10)

    def toggle_password_visibility(self):
        self.show_password = not self.show_password
        self.password_entry.configure(show="" if self.show_password else "*")
        self.toggle_pass_btn.configure(text="Hide Password" if self.show_password else "Show Password")

    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current_mode == "Dark" else "Dark")

    def add(self):
        site = self.site_entry.get()
        password = self.password_entry.get()
        if site and password:
            add_password(site, password)
            self.output_box.insert("end", f"✅ Saved password for {site}\n")
            self.site_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')

    def view(self):
        self.output_box.delete("1.0", "end")
        passwords = get_passwords()
        if not passwords:
            self.output_box.insert("end", "No passwords found.\n")
        else:
            for site, pwd in passwords:
                self.output_box.insert("end", f"{site}: {pwd}\n")

    def delete(self):
        site = self.site_entry.get()
        if site:
            delete_password(site)
            self.output_box.insert("end", f"🗑 Deleted password for {site}\n")
            self.site_entry.delete(0, 'end')

if __name__ == "__main__":
    login = LoginWindow()
    login.mainloop()

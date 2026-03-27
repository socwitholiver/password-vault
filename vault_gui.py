import os
import tkinter as tk
from cryptography.fernet import Fernet
import ttkbootstrap as ttk
from ttkbootstrap.constants import CENTER, EW, LEFT, NSEW, W, Y
from ttkbootstrap.dialogs import Messagebox


VAULT_FILE = "vault.txt"
KEY_FILE = "key.key"
APP_NAME = "OJ Vault 2.0"
APP_VERSION = "v2.0.0"
APP_SUBTITLE = "Offline credential security with local encryption"
BRAND_LABEL = "Oliver Jackson Secure Systems"
BG = "#08111f"
SURFACE = "#101a2b"
SURFACE_ALT = "#13233a"
BORDER = "#1f3552"
TEXT = "#ecf3ff"
MUTED = "#8fa6c6"
ACCENT = "#39c6b5"
ACCENT_2 = "#57a4ff"
DANGER = "#ff6b6b"


def ensure_key():
    if not os.path.exists(KEY_FILE):
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(Fernet.generate_key())


def load_key():
    ensure_key()
    return open(KEY_FILE, "rb").read()


def encrypt_password(password, key):
    return Fernet(key).encrypt(password.encode())


def decrypt_password(encrypted_password, key):
    return Fernet(key).decrypt(encrypted_password).decode()


def password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(ch.islower() for ch in password) and any(ch.isupper() for ch in password):
        score += 1
    if any(ch.isdigit() for ch in password):
        score += 1
    if any(not ch.isalnum() for ch in password):
        score += 1

    if score <= 2:
        return "Low"
    if score == 3:
        return "Moderate"
    return "Strong"


class PasswordVaultGUI:
    def __init__(self, root):
        self.key = load_key()
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("980x700")
        self.root.minsize(920, 640)
        self.root.configure(background=BG, padx=20, pady=20)

        self.entries = []
        self.selected_index = None
        self.edit_index = None
        self.status_var = ttk.StringVar(value="Vault ready. Credentials stay encrypted on this device.")
        self.search_var = ttk.StringVar()
        self.search_var.trace_add("write", self.filter_entries)
        self.show_password_var = ttk.BooleanVar(value=False)
        self.form_title_var = ttk.StringVar(value="Create Entry")
        self.primary_button_var = ttk.StringVar(value="Save Entry")
        self.selected_site_var = ttk.StringVar(value="No entry selected")
        self.selected_password_var = ttk.StringVar(value="Select an entry to reveal its password.")
        self.selected_strength_var = ttk.StringVar(value="-")

        self.configure_styles()
        self.build_layout()
        self.refresh_entries()

    def configure_styles(self):
        style = ttk.Style("darkly")
        style.configure("App.TFrame", background=BG)
        style.configure("Panel.TFrame", background=SURFACE)
        style.configure("PanelAlt.TFrame", background=SURFACE_ALT)
        style.configure("Hero.TLabel", background=SURFACE, foreground=TEXT, font=("Segoe UI Semibold", 26))
        style.configure("Subhero.TLabel", background=SURFACE, foreground=MUTED, font=("Segoe UI", 10))
        style.configure("CardTitle.TLabel", background=SURFACE_ALT, foreground=TEXT, font=("Segoe UI Semibold", 12))
        style.configure("Label.TLabel", background=SURFACE_ALT, foreground=MUTED, font=("Segoe UI", 10))
        style.configure("Value.TLabel", background=SURFACE, foreground=TEXT, font=("Segoe UI Semibold", 11))
        style.configure("Status.TLabel", background=BG, foreground=MUTED, font=("Segoe UI", 10))
        style.configure("Treeview", rowheight=34, fieldbackground=SURFACE, background=SURFACE, foreground=TEXT, bordercolor=BORDER)
        style.configure("Treeview.Heading", background=SURFACE_ALT, foreground=TEXT, font=("Segoe UI Semibold", 10))
        style.map("Treeview", background=[("selected", ACCENT_2)], foreground=[("selected", "#ffffff")])

    def build_layout(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        header = ttk.Frame(self.root, style="Panel.TFrame", padding=22)
        header.grid(row=0, column=0, sticky=EW, pady=(0, 18))
        header.columnconfigure(1, weight=1)

        self.build_brand_mark(header)

        title_block = ttk.Frame(header, style="Panel.TFrame")
        title_block.grid(row=0, column=1, sticky=EW, padx=(18, 0))
        title_block.columnconfigure(0, weight=1)

        ttk.Label(title_block, text=APP_NAME, style="Hero.TLabel").grid(row=0, column=0, sticky=W)
        ttk.Label(title_block, text=APP_SUBTITLE, style="Subhero.TLabel").grid(row=1, column=0, sticky=W, pady=(5, 4))
        ttk.Label(title_block, text=BRAND_LABEL, style="Subhero.TLabel").grid(row=2, column=0, sticky=W)

        meta = ttk.Frame(header, style="Panel.TFrame")
        meta.grid(row=0, column=2, sticky=EW)
        ttk.Label(meta, text="LOCAL ENCRYPTION", bootstyle="success", padding=(12, 7)).grid(row=0, column=0, pady=(0, 8))
        ttk.Label(meta, text="DARK DESKTOP EDITION", bootstyle="info", padding=(12, 7)).grid(row=1, column=0)

        content = ttk.Frame(self.root, style="App.TFrame")
        content.grid(row=1, column=0, sticky=NSEW)
        content.columnconfigure(0, weight=0)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        self.build_left_panel(content)
        self.build_right_panel(content)

        footer = ttk.Frame(self.root, style="App.TFrame")
        footer.grid(row=2, column=0, sticky=EW, pady=(14, 0))
        footer.columnconfigure(0, weight=1)

        ttk.Label(footer, textvariable=self.status_var, style="Status.TLabel", anchor=W).grid(
            row=0, column=0, sticky=EW
        )
        ttk.Label(footer, text=APP_VERSION, style="Status.TLabel", anchor=W).grid(
            row=0, column=1, sticky=W, padx=(12, 0)
        )

    def build_brand_mark(self, parent):
        canvas = tk.Canvas(parent, width=96, height=96, bg=SURFACE, highlightthickness=0)
        canvas.grid(row=0, column=0, sticky=W)
        canvas.create_oval(8, 8, 88, 88, fill="#0e2742", outline=ACCENT_2, width=2)
        canvas.create_polygon(48, 20, 73, 32, 68, 64, 48, 80, 28, 64, 23, 32, fill="#113252", outline=ACCENT, width=2)
        canvas.create_arc(34, 34, 62, 58, start=0, extent=180, style=tk.ARC, outline=TEXT, width=3)
        canvas.create_rectangle(34, 46, 62, 66, fill=TEXT, outline=TEXT)
        canvas.create_oval(45, 51, 51, 57, fill="#113252", outline="#113252")
        canvas.create_line(48, 57, 48, 62, fill="#113252", width=2)

    def build_left_panel(self, parent):
        panel = ttk.Frame(parent, style="App.TFrame")
        panel.grid(row=0, column=0, sticky=NSEW, padx=(0, 18))
        panel.columnconfigure(0, weight=1)

        form_card = ttk.Frame(panel, style="PanelAlt.TFrame", padding=20)
        form_card.grid(row=0, column=0, sticky=EW)
        form_card.columnconfigure(0, weight=1)

        ttk.Label(form_card, textvariable=self.form_title_var, style="CardTitle.TLabel").grid(row=0, column=0, sticky=W)
        ttk.Label(
            form_card,
            text="Create, update, and manage credentials without leaving the main screen.",
            style="Label.TLabel",
            wraplength=280,
            justify=LEFT,
        ).grid(row=1, column=0, sticky=W, pady=(4, 16))

        ttk.Label(form_card, text="Site or App", style="Label.TLabel").grid(row=2, column=0, sticky=W)
        self.site_entry = ttk.Entry(form_card)
        self.site_entry.grid(row=3, column=0, sticky=EW, pady=(6, 14))

        ttk.Label(form_card, text="Password", style="Label.TLabel").grid(row=4, column=0, sticky=W)
        self.pass_entry = ttk.Entry(form_card, show="*")
        self.pass_entry.grid(row=5, column=0, sticky=EW, pady=(6, 10))

        ttk.Checkbutton(
            form_card,
            text="Reveal while typing",
            variable=self.show_password_var,
            bootstyle="round-toggle",
            command=self.toggle_password_visibility,
        ).grid(row=6, column=0, sticky=W, pady=(0, 16))

        button_row = ttk.Frame(form_card, style="PanelAlt.TFrame")
        button_row.grid(row=7, column=0, sticky=EW)
        button_row.columnconfigure(0, weight=1)
        button_row.columnconfigure(1, weight=1)

        ttk.Button(button_row, textvariable=self.primary_button_var, bootstyle="success", command=self.save_entry).grid(
            row=0, column=0, sticky=EW, padx=(0, 8)
        )
        ttk.Button(button_row, text="Clear Form", bootstyle="secondary", command=self.reset_form).grid(
            row=0, column=1, sticky=EW
        )

        notes_card = ttk.Frame(panel, style="Panel.TFrame", padding=20)
        notes_card.grid(row=1, column=0, sticky=EW, pady=(16, 0))
        notes_card.columnconfigure(0, weight=1)
        ttk.Label(notes_card, text="Why this feels better", style="CardTitle.TLabel").grid(row=0, column=0, sticky=W)
        ttk.Label(
            notes_card,
            text="The darker palette, framed surfaces, and restrained accent colors make the vault feel more premium and security-focused.",
            style="Label.TLabel",
            wraplength=280,
            justify=LEFT,
        ).grid(row=1, column=0, sticky=W, pady=(6, 0))

    def build_right_panel(self, parent):
        panel = ttk.Frame(parent, style="App.TFrame")
        panel.grid(row=0, column=1, sticky=NSEW)
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(1, weight=1)

        actions = ttk.Frame(panel, style="App.TFrame")
        actions.grid(row=0, column=0, sticky=EW, pady=(0, 12))
        actions.columnconfigure(1, weight=1)

        ttk.Button(actions, text="Refresh", bootstyle="info", command=self.refresh_entries).grid(row=0, column=0, padx=(0, 10))
        ttk.Entry(actions, textvariable=self.search_var).grid(row=0, column=1, sticky=EW, padx=(0, 10))
        ttk.Button(actions, text="Edit Selected", bootstyle="warning", command=self.begin_edit_selected).grid(
            row=0, column=2, padx=(0, 10)
        )
        ttk.Button(actions, text="Delete", bootstyle="danger", command=self.delete_password).grid(row=0, column=3)

        vault_card = ttk.Frame(panel, style="Panel.TFrame", padding=18)
        vault_card.grid(row=1, column=0, sticky=NSEW)
        vault_card.columnconfigure(0, weight=1)
        vault_card.rowconfigure(1, weight=1)

        ttk.Label(vault_card, text="Stored Entries", style="CardTitle.TLabel").grid(row=0, column=0, sticky=W, pady=(0, 12))

        table_wrap = ttk.Frame(vault_card, style="Panel.TFrame")
        table_wrap.grid(row=1, column=0, sticky=NSEW)
        table_wrap.columnconfigure(0, weight=1)
        table_wrap.rowconfigure(0, weight=1)

        columns = ("site", "strength", "preview")
        self.tree = ttk.Treeview(table_wrap, columns=columns, show="headings")
        self.tree.heading("site", text="Site")
        self.tree.heading("strength", text="Strength")
        self.tree.heading("preview", text="Preview")
        self.tree.column("site", width=260, anchor=W)
        self.tree.column("strength", width=110, anchor=CENTER)
        self.tree.column("preview", width=200, anchor=W)
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", self.copy_selected_password)

        scrollbar = ttk.Scrollbar(table_wrap, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        detail_card = ttk.Frame(panel, style="PanelAlt.TFrame", padding=18)
        detail_card.grid(row=2, column=0, sticky=EW, pady=(14, 0))
        detail_card.columnconfigure(1, weight=1)
        detail_card.columnconfigure(2, weight=1)

        ttk.Label(detail_card, text="Selected Entry", style="CardTitle.TLabel").grid(row=0, column=0, sticky=W)
        ttk.Label(detail_card, text="Strength", style="Label.TLabel").grid(row=0, column=2, sticky=E)
        ttk.Label(detail_card, textvariable=self.selected_strength_var, style="Value.TLabel").grid(row=0, column=3, sticky=W)

        ttk.Label(detail_card, text="Site", style="Label.TLabel").grid(row=1, column=0, sticky=W, pady=(14, 0))
        ttk.Label(detail_card, textvariable=self.selected_site_var, style="Value.TLabel").grid(row=1, column=1, columnspan=3, sticky=W, pady=(14, 0))

        ttk.Label(detail_card, text="Password", style="Label.TLabel").grid(row=2, column=0, sticky=W, pady=(12, 0))
        ttk.Entry(detail_card, textvariable=self.selected_password_var, state="readonly").grid(
            row=2, column=1, columnspan=3, sticky=EW, pady=(12, 0)
        )

        ttk.Button(detail_card, text="Copy Password", bootstyle="primary", command=self.copy_selected_password).grid(
            row=3, column=1, sticky=EW, pady=(16, 0), padx=(0, 8)
        )
        ttk.Button(detail_card, text="Edit Entry", bootstyle="warning", command=self.begin_edit_selected).grid(
            row=3, column=2, sticky=EW, pady=(16, 0), padx=(0, 8)
        )
        ttk.Button(detail_card, text="Reset View", bootstyle="secondary", command=self.clear_selection).grid(
            row=3, column=3, sticky=EW, pady=(16, 0)
        )

    def toggle_password_visibility(self):
        self.pass_entry.configure(show="" if self.show_password_var.get() else "*")

    def load_entries(self):
        entries = []
        if not os.path.exists(VAULT_FILE):
            return entries

        with open(VAULT_FILE, "r", encoding="utf-8") as vault:
            for line in vault:
                line = line.strip()
                if not line or "|" not in line:
                    continue
                site, enc_pass = line.split("|", 1)
                try:
                    password = decrypt_password(enc_pass.encode(), self.key)
                except Exception:
                    password = "[Decryption Error]"
                entries.append({"site": site, "password": password})
        return entries

    def persist_entries(self):
        with open(VAULT_FILE, "w", encoding="utf-8") as vault:
            for entry in self.entries:
                encrypted = encrypt_password(entry["password"], self.key).decode()
                vault.write(f"{entry['site']}|{encrypted}\n")

    def refresh_entries(self):
        self.entries = self.load_entries()
        self.filter_entries()
        self.clear_selection(reset_tree=False)
        count = len(self.entries)
        if count:
            self.status_var.set(f"Vault synced. {count} entr{'y' if count == 1 else 'ies'} secured.")
        else:
            self.status_var.set("Vault is empty. Add your first secure entry.")

    def filter_entries(self, *_):
        query = self.search_var.get().strip().lower()
        current_selection = self.tree.selection()
        selected_id = current_selection[0] if current_selection else None
        self.tree.delete(*self.tree.get_children())

        for index, entry in enumerate(self.entries):
            if query and query not in entry["site"].lower():
                continue
            preview = ("*" * min(max(len(entry["password"]), 8), 14)) if entry["password"] != "[Decryption Error]" else "[Locked]"
            self.tree.insert("", "end", iid=str(index), values=(entry["site"], password_strength(entry["password"]), preview))

        if selected_id and self.tree.exists(selected_id):
            self.tree.selection_set(selected_id)
        elif not self.tree.get_children():
            self.selected_site_var.set("No matching entry")
            self.selected_password_var.set("Try a different search or create a new entry.")
            self.selected_strength_var.set("-")
            self.selected_index = None

    def save_entry(self):
        site = self.site_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not site or not password:
            Messagebox.show_error("Please enter both a site name and password.", title="Missing Details")
            self.status_var.set("Save failed. Both fields are required.")
            return

        if self.edit_index is None:
            self.entries.append({"site": site, "password": password})
            action = "saved"
        else:
            self.entries[self.edit_index] = {"site": site, "password": password}
            action = "updated"

        self.persist_entries()
        self.refresh_entries()
        self.reset_form()
        self.status_var.set(f"Entry {action} for {site}.")
        Messagebox.show_info(f"Credential entry {action} for '{site}'.", title="Vault Updated")

    def begin_edit_selected(self):
        if self.selected_index is None:
            Messagebox.show_warning("Select an entry before trying to edit it.", title="No Selection")
            self.status_var.set("Edit skipped. No entry selected.")
            return

        entry = self.entries[self.selected_index]
        self.edit_index = self.selected_index
        self.form_title_var.set("Edit Entry")
        self.primary_button_var.set("Update Entry")
        self.site_entry.delete(0, "end")
        self.site_entry.insert(0, entry["site"])
        self.pass_entry.delete(0, "end")
        self.pass_entry.insert(0, entry["password"])
        self.status_var.set(f"Editing entry for {entry['site']}.")

    def reset_form(self):
        self.edit_index = None
        self.form_title_var.set("Create Entry")
        self.primary_button_var.set("Save Entry")
        self.site_entry.delete(0, "end")
        self.pass_entry.delete(0, "end")
        self.status_var.set("Form reset. Ready for a new secure entry.")

    def on_tree_select(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            return

        index = int(selected[0])
        if index >= len(self.entries):
            return

        self.selected_index = index
        entry = self.entries[index]
        self.selected_site_var.set(entry["site"])
        self.selected_password_var.set(entry["password"])
        self.selected_strength_var.set(password_strength(entry["password"]))
        self.status_var.set(f"Viewing entry for {entry['site']}.")

    def copy_selected_password(self, _event=None):
        if self.selected_index is None:
            Messagebox.show_warning("Select an entry before copying its password.", title="No Selection")
            self.status_var.set("Copy skipped. No entry selected.")
            return

        password = self.entries[self.selected_index]["password"]
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update()
        self.status_var.set(f"Password copied for {self.entries[self.selected_index]['site']}.")

    def clear_selection(self, reset_tree=True):
        self.selected_index = None
        self.selected_site_var.set("No entry selected")
        self.selected_password_var.set("Select an entry to reveal its password.")
        self.selected_strength_var.set("-")
        if reset_tree:
            self.tree.selection_remove(self.tree.selection())

    def delete_password(self):
        if self.selected_index is None:
            Messagebox.show_warning("Select an entry before deleting it.", title="No Selection")
            self.status_var.set("Delete skipped. No entry selected.")
            return

        entry = self.entries[self.selected_index]
        confirm = Messagebox.yesno(
            f"Delete the stored password for '{entry['site']}'?",
            title="Confirm Delete",
            alert=True,
        )
        if confirm != "Yes":
            self.status_var.set("Delete canceled.")
            return

        del self.entries[self.selected_index]
        self.persist_entries()
        self.refresh_entries()
        self.reset_form()
        self.status_var.set(f"Entry deleted for {entry['site']}.")
        Messagebox.show_info(f"Password for '{entry['site']}' deleted.", title="Deleted")


if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = PasswordVaultGUI(root)
    root.mainloop()

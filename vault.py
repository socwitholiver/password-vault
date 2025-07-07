from cryptography.fernet import Fernet

# --- Generate Encryption Key (Only run once!) ---
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# --- Load the Existing Key ---
def load_key():
    return open("key.key", "rb").read()

# --- Encrypt a Password ---
def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode())

# --- Decrypt a Password ---
def decrypt_password(token, key):
    f = Fernet(key)
    return f.decrypt(token).decode()

# --- Add New Password ---
def add_password(site, password, key):
    encrypted = encrypt_password(password, key)
    with open("vault.txt", "a") as vault:
        vault.write(f"{site}|{encrypted.decode()}\n")
    print("✅ Password added.")

# --- View All Passwords ---
def view_passwords(key):
    try:
        with open("vault.txt", "r") as vault:
            for line in vault:
                site, enc_pass = line.strip().split("|")
                decrypted = decrypt_password(enc_pass.encode(), key)
                print(f"{site}: {decrypted}")
    except FileNotFoundError:
        print("⚠️ Vault is empty or missing.")

# --- Delete Password by Site Name ---
def delete_password(site_name):
    lines = []
    found = False
    try:
        with open("vault.txt", "r") as vault:
            lines = vault.readlines()
        with open("vault.txt", "w") as vault:
            for line in lines:
                if not line.startswith(site_name + "|"):
                    vault.write(line)
                else:
                    found = True
        if found:
            print(f"🗑️ Password for '{site_name}' deleted.")
        else:
            print("❌ Site not found.")
    except FileNotFoundError:
        print("⚠️ Vault file not found.")

def main():
    key = load_key()
    while True:
        print("\n🔐 Password Vault")
        print("1. Add Password")
        print("2. View Passwords")
        print("3. Delete Password")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            site = input("Enter site name: ")
            pwd = input("Enter password: ")
            add_password(site, pwd, key)
        elif choice == "2":
            view_passwords(key)
        elif choice == "3":
            site = input("Enter site name to delete: ")
            delete_password(site)
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()

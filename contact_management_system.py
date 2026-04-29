import json
import re

# =========================
# Constants (UI Styling)
# =========================
LINE = "=" * 45
SUBLINE = "-" * 45
# =========================
# Validation Functions
# =========================
def is_valid_phone(phone):
    return phone.isdigit() and len(phone) >= 7

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)
# =========================
# Display Helpers (UI Layer)
# =========================
def print_header(title):
    print(f"\n{LINE}")
    print(f"{title.center(len(LINE))}")
    print(f"{LINE}")


def print_success(message):
    print(f"{message}")


def print_error(message):
    print(f"{message}")


def format_contact(name, info):
    print(f"\n{name}")
    print(f"{info.get('phone', '')}")
    print(f"{info.get('email', '')}")
    print(f"{info.get('address', '')}")
    print(f"{info.get('group', '')}")
# =========================
# CRUD Functions
# =========================
def add_contact(contacts):
    print_header("ADD NEW CONTACT")

    name = input("Enter contact name: ")
    phone = input("Enter phone number: ")
    email = input("Enter email (optional): ")
    address = input("Enter address (optional): ")
    group = input("Enter group (Friends/Work/Family/Other): ")

    if name in contacts:
        print_error("Contact already exists.")
        return

    if not is_valid_phone(phone):
        print_error("Invalid phone number.")
        return

    if email and not is_valid_email(email):
        print_error("Invalid email.")
        return

    contacts[name] = {
        "phone": phone,
        "email": email,
        "address": address,
        "group": group
    }

    print_success(f"Contact '{name}' added successfully!")


def search_contact(contacts):
    keyword = input("Enter name to search: ")
    results = {
        name: info
        for name, info in contacts.items()
        if keyword.lower() in name.lower()
    }

    print(f"\nFound {len(results)} contact(s):")
    print(SUBLINE)

    for name, info in results.items():
        format_contact(name, info)


def update_contact(contacts):
    name = input("Enter contact name to update: ")

    if name not in contacts:
        print_error("Contact not found.")
        return

    phone = input("New phone (leave blank to skip): ")
    email = input("New email (leave blank to skip): ")
    address = input("New address (leave blank to skip): ")
    group = input("New group (leave blank to skip): ")

    if phone:
        if not is_valid_phone(phone):
            print_error("Invalid phone.")
            return
        contacts[name]["phone"] = phone

    if email:
        if not is_valid_email(email):
            print_error("Invalid email.")
            return
        contacts[name]["email"] = email

    if address:
        contacts[name]["address"] = address

    if group:
        contacts[name]["group"] = group

    print_success("Contact updated successfully!")


def delete_contact(contacts):
    name = input("Enter contact name to delete: ")

    if name not in contacts:
        print_error("Contact not found.")
        return

    confirm = input(f"Delete '{name}'? (y/n): ")
    if confirm.lower() == "y":
        del contacts[name]
        print_success("Contact deleted.")

def display_all(contacts):
    print_header(f"ALL CONTACTS ({len(contacts)} total)")

    if not contacts:
        print("No contacts available.")
        return

    for name, info in contacts.items():
        format_contact(name, info)
        print(SUBLINE)
# =========================
# File Operations
# =========================
def save_to_file(contacts, filename="contacts_data.json"):
    with open(filename, "w") as f:
        json.dump(contacts, f, indent=4)
    print_success(f"Contacts saved to {filename}")
def load_from_file(filename="contacts_data.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
def export_to_csv(contacts, filename="contacts.csv"):
    with open(filename, "w") as f:
        f.write("Name,Phone,Email,Address,Group\n")
        for name, info in contacts.items():
            f.write(
                f"{name},{info.get('phone','')},{info.get('email','')},"
                f"{info.get('address','')},{info.get('group','')}\n"
            )
    print_success("Exported to CSV.")
# =========================
# Stats
# =========================
def show_stats(contacts):
    print_header("STATISTICS")
    print(f"Total contacts: {len(contacts)}")
# =========================
# Menu
# =========================
def show_menu():
    print_header("MAIN MENU")
    print("1. Add New Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. View All Contacts")
    print("6. Export to CSV")
    print("7. View Statistics")
    print("8. Exit")
    print(LINE)


def main():
    contacts = load_from_file()

    while True:
        show_menu()
        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            add_contact(contacts)
            save_to_file(contacts)

        elif choice == "2":
            search_contact(contacts)

        elif choice == "3":
            update_contact(contacts)
            save_to_file(contacts)

        elif choice == "4":
            delete_contact(contacts)
            save_to_file(contacts)

        elif choice == "5":
            display_all(contacts)

        elif choice == "6":
            export_to_csv(contacts)

        elif choice == "7":
            show_stats(contacts)

        elif choice == "8":
            save_to_file(contacts)
            print("\nGoodbye!")
            break

        else:
            print_error("Invalid choice. Try again.")
#================================   
# Entry Point
#=================================
if __name__ == "__main__":
    main()
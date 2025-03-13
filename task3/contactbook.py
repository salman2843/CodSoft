import json
import re
import os
from datetime import datetime

class Contact:
    def __init__(self, name, phone, email, address, group="General"):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.group = group
        self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_modified = self.created_date

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "group": self.group,
            "created_date": self.created_date,
            "last_modified": self.last_modified
        }

class ContactBook:
    def __init__(self):
        self.contacts = []
        self.filename = "contacts.json"
        self.load_contacts()

    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def validate_phone(self, phone):
        pattern = r'^\+?1?\d{9,15}$'
        return re.match(pattern, phone) is not None

    def add_contact(self):
        print("\n=== Add New Contact ===")
        name = input("Enter name: ").strip()
        
        while True:
            phone = input("Enter phone number: ").strip()
            if self.validate_phone(phone):
                break
            print("Invalid phone number! Please use format: +1234567890 or 1234567890")
        
        while True:
            email = input("Enter email: ").strip()
            if self.validate_email(email):
                break
            print("Invalid email format!")
        
        address = input("Enter address: ").strip()
        
        print("\nAvailable groups:", self.get_all_groups())
        group = input("Enter group name (or press Enter for 'General'): ").strip() or "General"
        
        contact = Contact(name, phone, email, address, group)
        self.contacts.append(contact)
        self.save_contacts()
        print("Contact added successfully!")

    def view_contacts(self):
        if not self.contacts:
            print("\nNo contacts found!")
            return

        print("\n=== Contact List ===")
        self.display_contacts(self.contacts)

    def display_contacts(self, contacts_to_display):
        for i, contact in enumerate(contacts_to_display, 1):
            print(f"\n{i}. Name: {contact.name}")
            print(f"   Phone: {contact.phone}")
            print(f"   Email: {contact.email}")
            print(f"   Address: {contact.address}")
            print(f"   Group: {contact.group}")
            print(f"   Created: {contact.created_date}")
            print(f"   Last Modified: {contact.last_modified}")

    def search_contact(self):
        if not self.contacts:
            print("\nNo contacts to search!")
            return

        print("\n=== Search Contact ===")
        search_term = input("Enter name or phone number to search: ").lower()
        
        results = [
            contact for contact in self.contacts
            if search_term in contact.name.lower() or search_term in contact.phone
        ]
        
        if results:
            print(f"\nFound {len(results)} matching contacts:")
            self.display_contacts(results)
        else:
            print("No matching contacts found!")

    def update_contact(self):
        if not self.contacts:
            print("\nNo contacts to update!")
            return

        print("\n=== Update Contact ===")
        self.view_contacts()
        try:
            index = int(input("\nEnter the number of the contact to update: ")) - 1
            if 0 <= index < len(self.contacts):
                contact = self.contacts[index]
                print("\nLeave blank to keep current value")
                
                name = input(f"Current name: {contact.name}\nNew name: ").strip()
                if name:
                    contact.name = name
                
                while True:
                    phone = input(f"Current phone: {contact.phone}\nNew phone: ").strip()
                    if not phone:
                        break
                    if self.validate_phone(phone):
                        contact.phone = phone
                        break
                    print("Invalid phone number!")
                
                while True:
                    email = input(f"Current email: {contact.email}\nNew email: ").strip()
                    if not email:
                        break
                    if self.validate_email(email):
                        contact.email = email
                        break
                    print("Invalid email format!")
                
                address = input(f"Current address: {contact.address}\nNew address: ").strip()
                if address:
                    contact.address = address
                
                print("\nAvailable groups:", self.get_all_groups())
                group = input(f"Current group: {contact.group}\nNew group: ").strip()
                if group:
                    contact.group = group
                
                contact.last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_contacts()
                print("Contact updated successfully!")
            else:
                print("Invalid contact number!")
        except ValueError:
            print("Invalid input!")

    def delete_contact(self):
        if not self.contacts:
            print("\nNo contacts to delete!")
            return

        print("\n=== Delete Contact ===")
        self.view_contacts()
        try:
            index = int(input("\nEnter the number of the contact to delete: ")) - 1
            if 0 <= index < len(self.contacts):
                contact = self.contacts.pop(index)
                self.save_contacts()
                print(f"Contact '{contact.name}' deleted successfully!")
            else:
                print("Invalid contact number!")
        except ValueError:
            print("Invalid input!")

    def view_by_group(self):
        if not self.contacts:
            print("\nNo contacts found!")
            return

        groups = self.get_all_groups()
        print("\n=== View by Group ===")
        print("Available groups:", groups)
        group = input("Enter group name to view (or press Enter for all): ").strip()
        
        filtered_contacts = [c for c in self.contacts if not group or c.group == group]
        if filtered_contacts:
            self.display_contacts(filtered_contacts)
        else:
            print("No contacts found in this group!")

    def get_all_groups(self):
        return sorted(set(contact.group for contact in self.contacts) | {"General"})

    def save_contacts(self):
        with open(self.filename, 'w') as f:
            json_data = [contact.to_dict() for contact in self.contacts]
            json.dump(json_data, f, indent=2)

    def load_contacts(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.contacts = []
                    for contact_data in data:
                        contact = Contact(
                            contact_data["name"],
                            contact_data["phone"],
                            contact_data["email"],
                            contact_data["address"],
                            contact_data["group"]
                        )
                        contact.created_date = contact_data["created_date"]
                        contact.last_modified = contact_data["last_modified"]
                        self.contacts.append(contact)
            except json.JSONDecodeError:
                print("Error loading contacts file!")

def main():
    contact_book = ContactBook()
    
    while True:
        print("\n=== Contact Book Menu ===")
        print("1. Add Contact")
        print("2. View All Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. View Contacts by Group")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            contact_book.add_contact()
        elif choice == '2':
            contact_book.view_contacts()
        elif choice == '3':
            contact_book.search_contact()
        elif choice == '4':
            contact_book.update_contact()
        elif choice == '5':
            contact_book.delete_contact()
        elif choice == '6':
            contact_book.view_by_group()
        elif choice == '7':
            print("\nThank you for using Contact Book!")
            break
        else:
            print("\nInvalid choice! Please try again.")

if __name__ == "__main__":
    main()
import os
import json
import re

class Contact:
    def __init__(self, name, phone, email="", address=""):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        
    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["phone"],
            data.get("email", ""),
            data.get("address", "")
        )
        
    def __str__(self):
        return f"{self.name} - {self.phone}"

class ContactBook:
    def __init__(self):
        self.contacts = []
        self.filename = "contacts.json"
        self.load_contacts()
        
    def load_contacts(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    contacts_data = json.load(file)
                    self.contacts = [Contact.from_dict(data) for data in contacts_data]
            except json.JSONDecodeError:
                print("Error reading contacts file. Starting with empty contacts.")
                self.contacts = []
        
    def save_contacts(self):
        contacts_data = [contact.to_dict() for contact in self.contacts]
        with open(self.filename, 'w') as file:
            json.dump(contacts_data, file, indent=4)
            
    def add_contact(self, name, phone, email="", address=""):
        # Validate inputs
        if not name or not phone:
            return False, "Name and phone number are required."
            
        # Check for duplicate phone
        if any(contact.phone == phone for contact in self.contacts):
            return False, f"Contact with phone number {phone} already exists."
            
        # Validate phone format
        if not self._validate_phone(phone):
            return False, "Invalid phone number format."
            
        # Validate email if provided
        if email and not self._validate_email(email):
            return False, "Invalid email format."
            
        # Add contact
        self.contacts.append(Contact(name, phone, email, address))
        self.save_contacts()
        return True, f"Contact {name} added successfully!"
        
    def view_contacts(self):
        return self.contacts
        
    def search_contacts(self, query):
        query = query.lower()
        results = []
        
        for contact in self.contacts:
            if query in contact.name.lower() or query in contact.phone:
                results.append(contact)
                
        return results
        
    def get_contact_by_phone(self, phone):
        for contact in self.contacts:
            if contact.phone == phone:
                return contact
        return None
        
    def update_contact(self, old_phone, name=None, phone=None, email=None, address=None):
        contact = self.get_contact_by_phone(old_phone)
        
        if not contact:
            return False, f"Contact with phone number {old_phone} not found."
            
        # Validate new phone if changing
        if phone and phone != old_phone:
            if any(c.phone == phone for c in self.contacts):
                return False, f"Contact with phone number {phone} already exists."
                
            if not self._validate_phone(phone):
                return False, "Invalid phone number format."
                
        # Validate new email if changing
        if email and not self._validate_email(email):
            return False, "Invalid email format."
            
        # Update fields
        if name:
            contact.name = name
        if phone:
            contact.phone = phone
        if email is not None:  # Allow empty email for clearing
            contact.email = email
        if address is not None:  # Allow empty address for clearing
            contact.address = address
            
        self.save_contacts()
        return True, "Contact updated successfully!"
        
    def delete_contact(self, phone):
        contact = self.get_contact_by_phone(phone)
        
        if not contact:
            return False, f"Contact with phone number {phone} not found."
            
        self.contacts.remove(contact)
        self.save_contacts()
        return True, f"Contact {contact.name} deleted successfully!"
        
    def _validate_phone(self, phone):
        # Simple validation - adjust pattern as needed
        pattern = re.compile(r'^\+?\d{10,15}$')
        return bool(pattern.match(phone))
        
    def _validate_email(self, email):
        pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        return bool(pattern.match(email))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_contact_details(contact):
    print("\n" + "="*50)
    print(f"Contact: {contact.name}")
    print("-"*50)
    print(f"Phone: {contact.phone}")
    print(f"Email: {contact.email}")
    print(f"Address: {contact.address}")
    print("="*50)

def main():
    contact_book = ContactBook()
    
    while True:
        clear_screen()
        print("\n===== CONTACT BOOK =====")
        print("1. Add Contact")
        print("2. View All Contacts")
        print("3. Search Contacts")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            clear_screen()
            print("\n===== ADD CONTACT =====")
            name = input("Enter name: ")
            phone = input("Enter phone number: ")
            email = input("Enter email (optional): ")
            address = input("Enter address (optional): ")
            
            success, message = contact_book.add_contact(name, phone, email, address)
            print(f"\n{message}")
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            clear_screen()
            print("\n===== ALL CONTACTS =====")
            contacts = contact_book.view_contacts()
            
            if not contacts:
                print("No contacts found!")
            else:
                print(f"\n{'NAME':<20}{'PHONE':<15}")
                print("-"*35)
                for contact in contacts:
                    print(f"{contact.name[:19]:<20}{contact.phone:<15}")
                    
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            clear_screen()
            print("\n===== SEARCH CONTACTS =====")
            query = input("Enter name or phone to search: ")
            results = contact_book.search_contacts(query)
            
            if not results:
                print(f"No contacts found matching '{query}'")
            else:
                print(f"\nFound {len(results)} contact(s):")
                print(f"\n{'NAME':<20}{'PHONE':<15}")
                print("-"*35)
                for contact in results:
                    print(f"{contact.name[:19]:<20}{contact.phone:<15}")
                    
                # Option to view detailed information
                if len(results) > 0:
                    view_detail = input("\nEnter phone number to view details (or press Enter to go back): ")
                    if view_detail:
                        contact = contact_book.get_contact_by_phone(view_detail)
                        if contact:
                            display_contact_details(contact)
                        else:
                            print("Contact not found with that phone number.")
                            
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            clear_screen()
            print("\n===== UPDATE CONTACT =====")
            phone = input("Enter phone number of contact to update: ")
            contact = contact_book.get_contact_by_phone(phone)
            
            if not contact:
                print(f"No contact found with phone number {phone}")
            else:
                display_contact_details(contact)
                print("\nLeave field empty to keep current value")
                name = input(f"Enter new name [{contact.name}]: ") or None
                new_phone = input(f"Enter new phone [{contact.phone}]: ") or None
                email = input(f"Enter new email [{contact.email}]: ") or None
                address = input(f"Enter new address [{contact.address}]: ") or None
                
                success, message = contact_book.update_contact(phone, name, new_phone, email, address)
                print(f"\n{message}")
                
            input("\nPress Enter to continue...")
            
        elif choice == '5':
            clear_screen()
            print("\n===== DELETE CONTACT =====")
            phone = input("Enter phone number of contact to delete: ")
            contact = contact_book.get_contact_by_phone(phone)
            
            if not contact:
                print(f"No contact found with phone number {phone}")
            else:
                display_contact_details(contact)
                confirm = input("\nAre you sure you want to delete this contact? (y/n): ")
                
                if confirm.lower() == 'y':
                    success, message = contact_book.delete_contact(phone)
                    print(f"\n{message}")
                else:
                    print("\nDeletion cancelled.")
                    
            input("\nPress Enter to continue...")
            
        elif choice == '6':
            print("\nThank you for using Contact Book!")
            break
            
        else:
            print("\nInvalid choice! Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
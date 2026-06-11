"""Contact Book Application

A console-based contact management system that allows users to:
- Add, view, search, delete, and update contacts
- Store contacts as Contact objects within a list
- Sort contacts alphabetically

Contacts are stored as Contact objects (each containing name, phone, and email fields)
within a list. Users interact through a menu-driven command-line interface.
"""

from typing import Iterator, List, Optional


class Contact:
    """Represents a single contact with name, phone, and email.

    This class stores contact information as individual attributes and provides
    iteration and string representation capabilities.
    """

    def __init__(self, name: str, phone: str, email: str) -> None:
        """Initialize a Contact with name, phone, and email.

        Args:
            name: The contact's full name.
            phone: The contact's phone number.
            email: The contact's email address.
        """
        self.name = name
        self.phone = phone
        self.email = email

    def __iter__(self) -> Iterator[str]:
        """Enable iteration over contact fields (name, phone, email).

        Returns:
            An iterator over the instance attribute values.
        """
        # vars(self) returns a dictionary of all instance attributes
        yield from vars(self).values()

    def __repr__(self) -> str:
        """Return a developer-friendly string representation of the Contact.

        Returns:
            A string in the format: Contact(name='...', phone='...', email='...')
        """
        return (
            f"Contact(name='{self.name}', phone='{self.phone}', email='{self.email}')"
        )


class ContactBook:
    """Manages a collection of contacts.

    Provides methods to add, view, search, delete, and update contacts
    stored as Contact objects in a list.
    """

    def __init__(self) -> None:
        """Initialize an empty ContactBook with no contacts."""
        self.contacts: List[Contact] = []

    def _display_contact(
        self, contact: "Contact", include_index: bool = False, index: int = 0
    ) -> None:
        """Display a single contact's details in formatted output.

        Args:
            contact: The Contact object to display.
            include_index: If True, display the contact with an index number.
            index: The 1-based index to display (only used if include_index is True).
        """
        print("────────────────────────────────────────")
        if include_index:
            print(f"{index}. Name: {contact.name}")
            print(f"   Phone: {contact.phone}")
            print(f"   Email: {contact.email}")
        else:
            print(f"Name: {contact.name}")
            print(f"Phone: {contact.phone}")
            print(f"Email: {contact.email}")
        print("────────────────────────────────────────")

    def check_if_name_exists(self, name_to_search: str) -> bool:
        """Check if a contact with the given name already exists.

        Args:
            name_to_search: The name to search for (case-insensitive).

        Returns:
            True if a contact with this name exists, False otherwise.
        """
        for contact in self.contacts:
            if contact.name.lower() == name_to_search.lower():
                return True
        return False

    def add_contact(self, name: str, phone: str, email: str) -> None:
        """Add a new contact to the contact book.

        Prevents duplicate names (case-insensitive) and validates input.

        Args:
            name: The contact's name.
            phone: The contact's phone number.
            email: The contact's email address.
        """
        if self.check_if_name_exists(name.strip()):
            print(f"Contact with name: {name.strip()} already exists!")
        else:
            # Validate that all fields are non-empty
            if name and phone and email:
                self.contacts.append(
                    Contact(name.strip(), phone.strip(), email.strip())
                )
                print(f"✔ Contact added: {name}")
            else:
                print("Invalid input! Try again..")

    def view_contacts(self, sort_by_name=False, reverse=False) -> None:
        """Display all contacts in a formatted list.

        Args:
            sort_by_name: If True, sort contacts alphabetically by name (default: False).
            reverse: If True, sort in reverse alphabetical order (default: False).
                     Only used if sort_by_name is True.
        """
        contacts = self.contacts
        # Sort contacts if requested
        if sort_by_name:
            contacts = sorted(
                self.contacts,
                key=lambda contact: contact.name.lower(),
                reverse=reverse,
            )
        if contacts:
            print("All Contacts:")
            # Display each contact with formatting
            for idx, contact in enumerate(contacts):
                self._display_contact(contact, include_index=True, index=idx + 1)
            print()
        else:
            print("No contacts added yet.")

    def search_contact(self, name_to_search: str) -> None:
        """Search for contacts by name (case-insensitive, partial match).

        Args:
            name_to_search: The name or partial name to search for.
        """
        # Filter contacts where the search term appears in the name
        filtered_contacts = [
            contact
            for contact in self.contacts
            if name_to_search.lower() in contact.name.lower()
        ]
        # Display each matching contact
        for contact in filtered_contacts:
            self._display_contact(contact)
        print()

        # Notify if no matches found
        if not filtered_contacts:
            print(f'No contacts found for "{name_to_search}"')

    def delete_contact(self, contact_id: Optional[int]) -> None:
        """Delete a contact by its ID.

        Args:
            contact_id: The 1-based index of the contact to delete.
        """
        # Validate that the contact ID is within range
        if contact_id and 1 <= contact_id <= len(self.contacts):
            contact: Contact = self.contacts.pop(contact_id - 1)
            print(f"Successfully deleted contact: {contact.name}")
        else:
            print("Invalid contact id! Try again..")

    def update_contact(
        self, contact_id: Optional[int], name: str, phone: str, email: str
    ) -> None:
        """Update an existing contact's information.

        The old contact is removed and a new one is added with updated values.
        Fields left blank retain their original values.

        Args:
            contact_id: The 1-based index of the contact to update.
            name: The new name (or empty string to keep existing).
            phone: The new phone number (or empty string to keep existing).
            email: The new email (or empty string to keep existing).
        """
        # Validate that the contact ID is within range
        if contact_id and 1 <= contact_id <= len(self.contacts):
            if name.strip().lower() != self.contacts[
                contact_id - 1
            ].name and self.check_if_name_exists(name.strip()):
                print(f"Contact with name: {name.strip()} already exists!")
            else:
                # Remove the old contact
                contact: Contact = self.contacts.pop(contact_id - 1)

                # Use new values if provided, otherwise keep old values
                updated_name: str = name if name.strip() else contact.name
                updated_phone: str = phone if phone.strip() else contact.phone
                updated_email: str = email if email.strip() else contact.email

                # Create and add the updated contact
                updated_contact: Contact = Contact(
                    updated_name, updated_phone, updated_email
                )

                self.contacts.append(updated_contact)
                print(f"Updated contact: {updated_name}")
        else:
            print("Invalid contact id! Try again..")

    @staticmethod
    def print_menu():
        """Display the main menu options to the user."""
        print("════════════════════════════════════════")
        print("            CONTACT BOOK                ")
        print("════════════════════════════════════════")
        print("1. Add a contact")
        print("2. View all contacts")
        print("3. Search for a contact")
        print("4. Delete a contact")
        print("5. View contacts sorted by name")
        print("6. Edit a contact")
        print("0. Exit")


def try_cast_to_int(prompt: str) -> Optional[int]:
    """
    Prompt the user for input and attempt to convert it to an integer.

    Args:
        prompt: The message to display to the user.

    Returns:
        The integer value if conversion is successful, None if a ValueError occurs.
    """
    input_str: str = input(prompt)
    try:
        return int(input_str)
    except ValueError as e:
        print(f"Error encountered while converting to int: {e}")


if __name__ == "__main__":
    # Initialize the contact book and display the main menu
    contact_book: ContactBook = ContactBook()
    contact_book.print_menu()

    # Main program loop - continue until user selects option 0 (exit)
    while True:
        print("════════════════════════════════════════")
        selection: Optional[int] = try_cast_to_int(prompt="Select an option: ")

        # Route to the appropriate function based on user selection
        match selection:
            case 0:
                print("Goodbye!")
                break
            case 1:
                # Add a new contact
                name: str = input("Enter name  : ")
                phone: str = input("Enter phone : ")
                email: str = input("Enter email : ")
                contact_book.add_contact(name, phone, email)
            case 2:
                # View all contacts
                contact_book.view_contacts()
            case 3:
                # Search for a contact by name
                name_to_search: str = input("Enter name to search: ")
                contact_book.search_contact(name_to_search)
            case 4:
                # Delete a contact
                contact_book.view_contacts()
                contact_id: Optional[int] = try_cast_to_int(
                    prompt="Enter contact id to delete: "
                )
                contact_book.delete_contact(contact_id)
            case 5:
                # View contacts sorted by name
                sort_choice: Optional[int] = try_cast_to_int(
                    prompt="Enter 0 for alphabetical order or 1 for reverse alphabetical order: "
                )
                if sort_choice in (0, 1):
                    contact_book.view_contacts(
                        sort_by_name=True, reverse=bool(sort_choice)
                    )
                else:
                    print("Invalid sort choice! Try again..")
            case 6:
                # Edit (update) an existing contact
                contact_book.view_contacts()
                contact_id: Optional[int] = try_cast_to_int(
                    prompt="Enter contact id to update contact: "
                )
                print("Leave a field blank if you don't want to change it.")
                name: str = input("Enter name  : ")
                phone: str = input("Enter phone : ")
                email: str = input("Enter email : ")
                contact_book.update_contact(contact_id, name, phone, email)
            case _:
                print("Invalid choice! Try again..")
                continue

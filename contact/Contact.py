import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

CONTACTS_FILE = "contact/contacts.json"

# Load contacts from file
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    return []

# Save contacts to file
def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

# Add a new contact
def add_contact():
    name = simpledialog.askstring("Add Contact", "Enter name:")
    phone = simpledialog.askstring("Add Contact", "Enter phone number:")
    email = simpledialog.askstring("Add Contact", "Enter email:")
    address = simpledialog.askstring("Add Contact", "Enter address:")
    
    if name and phone:
        contacts.append({"name": name, "phone": phone, "email": email, "address": address})
        save_contacts(contacts)
        messagebox.showinfo("Success", f"Contact '{name}' added!")
        view_contacts()
    else:
        messagebox.showwarning("Input Error", "Name and phone number are required!")

# View all contacts
def view_contacts():
    contact_list.delete(0, tk.END)
    for contact in contacts:
        contact_list.insert(tk.END, f"{contact['name']} - {contact['phone']}")

# Search contact
def search_contact():
    keyword = simpledialog.askstring("Search Contact", "Enter name or phone:")
    results = [c for c in contacts if keyword.lower() in c['name'].lower() or keyword in c['phone']]
    contact_list.delete(0, tk.END)
    for c in results:
        contact_list.insert(tk.END, f"{c['name']} - {c['phone']}")
    if not results:
        messagebox.showinfo("Search", "No contact found.")

# Get selected contact index
def get_selected_index():
    selection = contact_list.curselection()
    if selection:
        name_phone = contact_list.get(selection[0])
        for i, contact in enumerate(contacts):
            if f"{contact['name']} - {contact['phone']}" == name_phone:
                return i
    return None

# Update selected contact
def update_contact():
    index = get_selected_index()
    if index is not None:
        contact = contacts[index]
        name = simpledialog.askstring("Update Contact", "Edit name:", initialvalue=contact["name"])
        phone = simpledialog.askstring("Update Contact", "Edit phone:", initialvalue=contact["phone"])
        email = simpledialog.askstring("Update Contact", "Edit email:", initialvalue=contact["email"])
        address = simpledialog.askstring("Update Contact", "Edit address:", initialvalue=contact["address"])

        if name and phone:
            contacts[index] = {"name": name, "phone": phone, "email": email, "address": address}
            save_contacts(contacts)
            view_contacts()
            messagebox.showinfo("Updated", "Contact updated successfully.")
        else:
            messagebox.showwarning("Error", "Name and phone are required!")
    else:
        messagebox.showwarning("Selection Error", "No contact selected.")

# Delete selected contact
def delete_contact():
    index = get_selected_index()
    if index is not None:
        confirm = messagebox.askyesno("Delete Contact", "Are you sure?")
        if confirm:
            deleted_name = contacts[index]["name"]
            contacts.pop(index)
            save_contacts(contacts)
            view_contacts()
            messagebox.showinfo("Deleted", f"Contact '{deleted_name}' deleted.")
    else:
        messagebox.showwarning("Selection Error", "No contact selected.")

# ---------------- GUI ----------------
contacts = load_contacts()
root = tk.Tk()
root.title("Contact Book")
root.geometry("450x400")
root.resizable(False, False)

# Contact list
contact_list = tk.Listbox(root, width=50, height=15)
contact_list.pack(pady=10)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Add", width=12, command=add_contact).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Search", width=12, command=search_contact).grid(row=0, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="Update", width=12, command=update_contact).grid(row=1, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Delete", width=12, command=delete_contact).grid(row=1, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="Refresh", width=26, command=view_contacts).grid(row=2, column=0, columnspan=2, pady=5)

view_contacts()
root.mainloop()

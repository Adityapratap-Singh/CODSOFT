import tkinter as tk
from tkinter import messagebox
import string
import random

# Function to generate password
def generate_password():
    try:
        length = int(length_entry.get())
        if length < 4:
            messagebox.showerror("Error", "Password length must be at least 4.")
            return

        password_type = type_var.get()

        if password_type == "Alphabetic":
            chars = string.ascii_letters
        elif password_type == "Numeric":
            chars = string.digits
        elif password_type == "Alphanumeric":
            chars = string.ascii_letters + string.digits
        elif password_type == "All":
            chars = string.ascii_letters + string.digits + string.punctuation
        else:
            messagebox.showerror("Error", "Please select a valid password type.")
            return

        password = ''.join(random.choices(chars, k=length))
        messagebox.showinfo("Generated Password", f"🔐 Your Password:\n\n{password}")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for length.")

# GUI Setup
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x250")
root.resizable(False, False)

# Heading
tk.Label(root, text="🛡️ Secure Password Generator", font=("Arial", 16, "bold")).pack(pady=10)

# Password length input
tk.Label(root, text="Enter Password Length:", font=("Arial", 12)).pack()
length_entry = tk.Entry(root, font=("Arial", 12), justify='center')
length_entry.pack(pady=5)

# Password type selection
tk.Label(root, text="Select Password Type:", font=("Arial", 12)).pack()
type_var = tk.StringVar(value="Alphanumeric")
type_options = ["Alphabetic", "Numeric", "Alphanumeric", "All"]
tk.OptionMenu(root, type_var, *type_options).pack(pady=5)

# Generate button
tk.Button(root, text="Generate Password", font=("Arial", 12, "bold"), bg="green", fg="white",
          command=generate_password).pack(pady=15)

# Run the app
root.mainloop()

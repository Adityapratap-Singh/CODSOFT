import subprocess
import sys

# Automatically install required packages (if any)
def install_missing_packages():
    try:
        import sympy  # Example external package
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "sympy"])

# Run auto-installer
install_missing_packages()

import tkinter as tk
import ast
import operator

# Safe evaluation using AST
def safe_eval(expr):
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg
    }

    def _eval(node):
        if isinstance(node, ast.Num):  # For Python 3.7 and earlier
            return node.n
        elif isinstance(node, ast.Constant):  # For Python 3.8+
            return node.value
        elif isinstance(node, ast.BinOp):
            return allowed_operators[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return allowed_operators[type(node.op)](_eval(node.operand))
        else:
            raise ValueError("Unsupported expression")

    node = ast.parse(expr, mode='eval').body
    return _eval(node)

# Core functions
def update_display(value):
    current = display_var.get()
    if current == "0" or current == "Error":
        display_var.set(value)
    else:
        display_var.set(current + value)

def clear_display():
    display_var.set("0")

def backspace():
    current = display_var.get()
    if current in ["0", "Error"]:
        display_var.set("0")
    elif len(current) == 1:
        display_var.set("0")
    else:
        display_var.set(current[:-1])

def calculate_result():
    try:
        result = safe_eval(display_var.get())
        display_var.set(str(result))
    except Exception:
        display_var.set("Error")

# UI setup
parent = tk.Tk()
parent.title("Advanced Calculator")
parent.geometry("350x500")
parent.resizable(False, False)

display_var = tk.StringVar(value="0")

# Display
display_label = tk.Label(parent, textvariable=display_var, font=("Consolas", 28),
                         anchor="e", bg="white", fg="black", relief="sunken",
                         padx=10, pady=20, height=2)
display_label.grid(row=0, column=0, columnspan=4, sticky="nsew")

# Button layout
buttons = [
    ("C", 1, 0, clear_display, "#ff9999"),
    ("←", 1, 1, backspace, "#ffcc99"),
    ("/", 1, 2, lambda: update_display("/"), "#ccffff"),
    ("*", 1, 3, lambda: update_display("*"), "#ccffff"),

    ("7", 2, 0, lambda: update_display("7"), "#e6e6e6"),
    ("8", 2, 1, lambda: update_display("8"), "#e6e6e6"),
    ("9", 2, 2, lambda: update_display("9"), "#e6e6e6"),
    ("-", 2, 3, lambda: update_display("-"), "#ccffff"),

    ("4", 3, 0, lambda: update_display("4"), "#e6e6e6"),
    ("5", 3, 1, lambda: update_display("5"), "#e6e6e6"),
    ("6", 3, 2, lambda: update_display("6"), "#e6e6e6"),
    ("+", 3, 3, lambda: update_display("+"), "#ccffff"),

    ("1", 4, 0, lambda: update_display("1"), "#e6e6e6"),
    ("2", 4, 1, lambda: update_display("2"), "#e6e6e6"),
    ("3", 4, 2, lambda: update_display("3"), "#e6e6e6"),
    ("=", 4, 3, calculate_result, "#99ff99"),

    ("0", 5, 0, lambda: update_display("0"), "#e6e6e6"),
    (".", 5, 1, lambda: update_display("."), "#e6e6e6"),
]

# Add buttons to window
for (text, row, col, command, color) in buttons:
    btn = tk.Button(parent, text=text, command=command, bg=color,
                    font=("Consolas", 20), relief="raised", padx=10, pady=10)
    btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

# Special case for wide 0 and = button
tk.Button(parent, text="0", command=lambda: update_display("0"), bg="#e6e6e6",
          font=("Consolas", 20)).grid(row=5, column=0, columnspan=2, sticky="nsew", padx=1, pady=1)
tk.Button(parent, text=".", command=lambda: update_display("."), bg="#e6e6e6",
          font=("Consolas", 20)).grid(row=5, column=2, sticky="nsew", padx=1, pady=1)
tk.Button(parent, text="=", command=calculate_result, bg="#99ff99",
          font=("Consolas", 20)).grid(row=5, column=3, sticky="nsew", padx=1, pady=1)

# Keyboard bindings
def keypress(event):
    key = event.char
    if key.isdigit() or key in "+-*/.":
        update_display(key)
    elif key == "\r":  # Enter
        calculate_result()
    elif key == "\x08":  # Backspace
        backspace()

parent.bind("<Key>", keypress)

# Set uniform button size
for i in range(6):
    parent.grid_rowconfigure(i, weight=1)
for j in range(4):
    parent.grid_columnconfigure(j, weight=1)

# Run the app
parent.mainloop()

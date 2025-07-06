# 🧮 Advanced Calculator using Tkinter

A modern and safe desktop calculator built with Python's Tkinter. Designed to offer a smooth user experience, clean layout, and secure expression evaluation (no `eval()` risk).

---

## 🚀 Features

- ✅ **Simple & Responsive GUI** using `Tkinter`
- ✅ **Safe evaluation** using Python's `ast` module (no use of `eval()`)
- ✅ **Keyboard support** (digits, operators, Enter, Backspace)
- ✅ **Backspace** (`←`) and **Clear** (`C`) functionality
- ✅ **Colored buttons** for better UX
- ✅ **Error handling** for invalid expressions
- ✅ Fixed-size window layout

---

## 🖼️ Preview

> ![image](https://github.com/user-attachments/assets/e1f63cfa-4604-484b-af6c-e91531547eb5)


---

## 📁 Project Structure

```plaintext
CalculatorProject/
├── calculator.py         # Main application file
├── requirements.txt      # Dependency file (currently none)
└── README.md             # You're reading it!

🔧 Requirements
Python 3.7 or higher

Tkinter (pre-installed with Python on most systems)

💡 No external libraries required currently.

▶️ How to Run
Clone or Download this repository.

Open terminal or command prompt in the project directory.

Run the app:
python calculator.py

💡 If external libraries are used in the future, install them with:
pip install -r requirements.txt


⌨️ Keyboard Shortcuts
Key	Action
0–9, +, -, *, /, .	Type expression
Enter	Calculate result
Backspace	Delete last char
C or Esc	Clear expression

📌 Future Improvements (Ideas)
Add scientific functions (sin, cos, log, etc.)

Support for parentheses

History of calculations

Theme switch (Light/Dark)

Export expression history to file

🛡️ Security Note
This calculator does not use eval() for expression evaluation. Instead, it uses Python's ast module to safely parse and compute expressions, preventing code injection or execution of arbitrary Python code.

📄 License
This project is open-source and free to use for learning and personal projects.

🙋‍♂️ Author
Adityapratap Singh

Feel free to reach out for any improvements or suggestions!

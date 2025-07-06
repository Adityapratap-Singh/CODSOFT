# 🎯 Modern To-Do Manager

A modern, theme-friendly, GUI-based task management application built using Python and `ttkbootstrap`. This app lets you create, manage, and track tasks with features like countdown timers, smart reminders, calendar view, and data export (CSV, PDF, JSON).

---

## 🧰 Features

- ✅ **Add/Edit Tasks** with:
  - Title, Description, Start Time, Deadline
  - Priority (High / Medium / Low)
  - Tags and Recurring task support

- 📋 **Task Management**:
  - Mark tasks as complete
  - View pending vs completed tasks
  - Delete tasks easily

- ⏳ **Live Countdown Timers**
  - See time left until deadlines in real time
  - Visual "Overdue" indication

- ⏰ **Smart Reminders**
  - Alerts you when a task is about to start or is nearing its deadline (within 60 seconds)

- 📅 **Calendar View**
  - View your tasks by date
  - See the number of tasks due each day

- 🌗 **Dark/Light Mode**
  - Toggle between `flatly` (light) and `darkly` themes

- 📤 **Export Your Tasks**
  - JSON: For data backups or integrations
  - PDF: Professional printable report
  - CSV: Compatible with Excel, Google Sheets

---

## 📦 Installation

1. Clone the Repository
git clone https://github.com/your-username/modern-todo-manager.git
cd modern-todo-manager


2. Install Requirements
The app will auto-install required libraries at runtime, but you can install manually: pip install ttkbootstrap reportlab firebase_admin scikit-learn TkinterDnD2



🚀 Run the App
python main.py
The GUI will launch with all features ready.

🗂 File Structure
├── main.py              # GUI entry point
├── models.py            # Task data model
├── task_manager.py      # Task handling logic (CRUD + save/load)
├── export_utils.py      # CSV / PDF / JSON exporters
├── tasks.json           # Auto-generated task storage
🔁 Recurring Tasks
The system supports a recurring flag (e.g., daily, weekly) for tasks, and you can extend functionality via the apply_recurring() method in TaskManager.



🛠 Future Ideas
🔒 Login with Firebase (auth + cloud sync)

📱 Mobile responsive GUI (via web or Kivy)

🔁 Subtask nesting and recurring rule builder

📊 Analytics Dashboard



👨‍💻 Built With
~ Python 3.x
~ Tkinter + ttkbootstrap
~ ReportLab (PDF generation)
~ threading (background countdown)
~ json (data storage)
~calendar (native module)

📝 License
This project is licensed under the MIT License.

💬 Contact
Feel free to connect:
📧 Email: [adityaprataps406@gmail.com]
💼 LinkedIn: [https://www.linkedin.com/in/adityapratap-singh-447159215/]
🌐 GitHub: [https://github.com/Adityapratap-Singh]


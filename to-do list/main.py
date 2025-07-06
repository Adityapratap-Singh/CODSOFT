# -----------------------------------------------
# Auto-install required libraries if missing
# -----------------------------------------------
import subprocess
import sys
import importlib

def install(package):
    print(f"🔧 Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Required packages
required = ["ttkbootstrap", "reportlab", "firebase_admin", "scikit-learn", "TkinterDnD2"]


for pkg in required:
    try:
        importlib.import_module(pkg)
    except ImportError:
        print(f"🔧 Installing missing package: {pkg}...")
        install(pkg)


import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap.constants import *
from datetime import datetime
from models import Task
from task_manager import TaskManager
import threading, time

from export_utils import export_to_csv, export_to_pdf, export_to_json

# ----------------------------
# Global Constants & Settings
# ----------------------------
TASKS = TaskManager()
PRIORITY_STYLE = {"High": "danger", "Medium": "warning", "Low": "success"}


# ----------------------------
# Main To-Do App Class
# ----------------------------
class ModernToDo:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Modern To-Do Manager")
        self.root.geometry("900x650")
        self.dark_mode = False
        self.countdowns = {}  # Maps index -> countdown label widget
        self.view_mode = "pending"  # <-- Add this line

        self.setup_ui()

        # Background threads
        threading.Thread(target=self.reminders, daemon=True).start()
        threading.Thread(target=self.update_countdowns, daemon=True).start()

    # ------------------------
    # UI Setup
    # ------------------------
    def setup_ui(self):
        self._build_header()
        self._build_form()
        self._build_panel()
        self._build_add_task_form()

    def _build_header(self):
        header = ttk.Frame(self.root, padding=10)
        header.pack(fill='x')

        # Title
        ttk.Label(header, text="📋 My Tasks", font=("Segoe UI", 18, "bold")).pack(side='left')

        # Right-aligned controls
        view_frame = ttk.Frame(header)
        view_frame.pack(side='right', padx=10)

        # View Mode Buttons
        ttk.Button(view_frame, text="🕒 Pending", bootstyle="outline-warning",
                   command=lambda: self.set_view("pending")).pack(side='left', padx=2)
        ttk.Button(view_frame, text="✅ Completed", bootstyle="outline-success",
                   command=lambda: self.set_view("completed")).pack(side='left', padx=2)

        # Export Buttons
        ttk.Button(view_frame, text="📦 JSON", bootstyle="outline", command=lambda: export_to_json(TASKS.tasks)).pack(side='left', padx=2)
        ttk.Button(view_frame, text="📝 PDF", bootstyle="outline", command=lambda: export_to_pdf(TASKS.tasks)).pack(side='left', padx=2)
        ttk.Button(view_frame, text="📤 CSV", bootstyle="outline", command=lambda: export_to_csv(TASKS.tasks)).pack(side='left', padx=2)

        # Calendar & Theme Toggle
        ttk.Button(view_frame, text="🗓 Calendar", bootstyle="outline-primary", command=self.show_calendar).pack(side='left', padx=2)
        ttk.Button(view_frame, text="🌙 Theme", bootstyle="outline-info", command=self.toggle_theme).pack(side='left', padx=2)

    def _build_form(self):
        self.form = ttk.Labelframe(self.root, text="Add / Edit Task", padding=20, bootstyle="secondary")
        self.form.pack(fill='x', padx=20, pady=10)

        frm = self.form

        # Title & Priority
        ttk.Label(frm, text="Title:").grid(row=0, column=0, sticky='w')
        self.title = ttk.Entry(frm, width=30)
        self.title.grid(row=0, column=1, padx=10)

        ttk.Label(frm, text="Priority:").grid(row=0, column=2, sticky='w')
        self.priority = ttk.Combobox(frm, values=["High", "Medium", "Low"], width=14, state="readonly")
        self.priority.grid(row=0, column=3)

        # Dropdown values
        self.days = [f"{d:02}" for d in range(1, 32)]
        self.months = [f"{m:02}" for m in range(1, 13)]
        self.years = [str(y) for y in range(datetime.now().year, datetime.now().year + 5)]
        self.hours = [f"{h:02}" for h in range(0, 24)]
        self.minutes = [f"{m:02}" for m in range(0, 60)]

        # Start Date & Time
        ttk.Label(frm, text="Start Date:").grid(row=1, column=0, sticky='w', pady=5)
        self.start_day = ttk.Combobox(frm, values=self.days, width=4, state="readonly")
        self.start_month = ttk.Combobox(frm, values=self.months, width=4, state="readonly")
        self.start_year = ttk.Combobox(frm, values=self.years, width=6, state="readonly")
        self.start_day.grid(row=1, column=1, sticky='w', padx=12)
        self.start_month.grid(row=1, column=1)
        self.start_year.grid(row=1, column=1, padx=(105, 0))

        ttk.Label(frm, text="Start Time:").grid(row=1, column=2, sticky='w')
        self.start_hour = ttk.Combobox(frm, values=self.hours, width=4, state="readonly")
        self.start_min = ttk.Combobox(frm, values=self.minutes, width=4, state="readonly")
        self.start_hour.grid(row=1, column=3, sticky='w')
        self.start_min.grid(row=1, column=3, padx=(60, 0), sticky='w')

        # End Date & Time
        ttk.Label(frm, text="Deadline Date:").grid(row=2, column=0, sticky='w', pady=5)
        self.end_day = ttk.Combobox(frm, values=self.days, width=4, state="readonly")
        self.end_month = ttk.Combobox(frm, values=self.months, width=4, state="readonly")
        self.end_year = ttk.Combobox(frm, values=self.years, width=6, state="readonly")
        self.end_day.grid(row=2, column=1, sticky='w', padx=12)
        self.end_month.grid(row=2, column=1)
        self.end_year.grid(row=2, column=1, padx=(105, 0))

        ttk.Label(frm, text="Deadline Time:").grid(row=2, column=2, sticky='w')
        self.end_hour = ttk.Combobox(frm, values=self.hours, width=4, state="readonly")
        self.end_min = ttk.Combobox(frm, values=self.minutes, width=4, state="readonly")
        self.end_hour.grid(row=2, column=3, sticky='w')
        self.end_min.grid(row=2, column=3, padx=(60, 0), sticky='w')

        # Tags
        ttk.Label(frm, text="Tags (comma-separated):").grid(row=3, column=0, sticky='w', pady=5)
        self.tags = ttk.Entry(frm, width=30)
        self.tags.grid(row=3, column=1, padx=10)

        # Add Task Button
        ttk.Button(frm, text="➕ Add Task", bootstyle="success", command=self.add_task).grid(row=3, column=3, pady=10)

        # Set initial placeholders
        for f in [self.start_day, self.start_month, self.start_year, self.start_hour, self.start_min,
                  self.end_day, self.end_month, self.end_year, self.end_hour, self.end_min]:
            f.set("")

    def _build_panel(self):
        self.panel = ttk.Frame(self.root, padding=10)
        self.panel.pack(fill='both', expand=True, padx=20, pady=10)

    def _build_add_task_form(self):
        form = ttk.Labelframe(self.root, text="Add Task", padding=10)
        form.pack(fill='x', padx=10, pady=5)

        self.title_entry = ttk.Entry(form, width=30)
        self.title_entry.pack(side='left', padx=5)
        ttk.Button(form, text="Add", command=self._add_task, bootstyle="success").pack(side='left', padx=5)

    # ------------------------
    # Task Operations
    # ------------------------
    def add_task(self):
        try:
            title = self.title.get().strip()
            if not title:
                raise ValueError("Title required")
            pr = self.priority.get()
            if pr not in PRIORITY_STYLE:
                raise ValueError("Valid priority needed")
            start = self.get_datetime_from_fields(self.start_year, self.start_month, self.start_day, self.start_hour, self.start_min)
            dl = self.get_datetime_from_fields(self.end_year, self.end_month, self.end_day, self.end_hour, self.end_min)
            tags = [t.strip() for t in self.tags.get().split(",") if t.strip()]
            t = Task(title, "", start, dl, pr, tags, [])
            TASKS.add_task(t)
            self.refresh_tasks()
            self._clear_form()
        except Exception as e:
            messagebox.showerror("Oops!", str(e))

    def _add_task(self):
        from datetime import datetime, timedelta
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Title required")
            return
        # Dummy times for demo; replace with real form fields as needed
        start = datetime.now()
        deadline = start + timedelta(days=2)
        tags = ["todo"]
        # Use AI to set priority
        task = Task(title, "", start, deadline, "Low", tags, [])
        TASKS.add_task(task)
        self.refresh_tasks()
        self.title_entry.delete(0, 'end')

    def complete(self, idx):
        TASKS.mark_complete(idx)
        self.refresh_tasks()

    def delete(self, idx):
        TASKS.delete_task(idx)
        self.refresh_tasks()

    def get_datetime_from_fields(self, y, m, d, h, mi):
        values = [y.get(), m.get(), d.get(), h.get(), mi.get()]
        if any(v in ["", "DD", "MM", "YYYY", "HH"] for v in values):
            raise ValueError("Please select a complete valid date and time.")
        dt_str = f"{y.get()}-{m.get()}-{d.get()} {h.get()}:{mi.get()}"
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M")

    def _clear_form(self):
        self.title.delete(0, 'end')
        self.priority.set('')
        for field in [
            self.start_day, self.start_month, self.start_year,
            self.start_hour, self.start_min,
            self.end_day, self.end_month, self.end_year,
            self.end_hour, self.end_min
        ]:
            field.set('')
        self.tags.delete(0, 'end')

    # ------------------------
    # Task Display
    # ------------------------
    def _add_task_card(self, task, idx):
        card = ttk.Frame(self.panel, bootstyle=PRIORITY_STYLE[task.priority], padding=15)
        card.pack(fill='x', pady=6)

        # Countdown Label
        self.countdowns[idx] = ttk.Label(card, font=("Segoe UI", 10, "bold"))
        self.countdowns[idx].grid(row=1, column=1, padx=10, sticky='e')

        # Task Info
        ttk.Label(card, text=task.title, font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky='w')
        ttk.Label(card, text=f"{task.start_time.strftime('%Y-%m-%d %H:%M')} → {task.deadline.strftime('%Y-%m-%d %H:%M')}", font=("Segoe UI", 9)).grid(row=1, column=0, sticky='w')
        if task.tags:
            ttk.Label(card, text="Tags: " + ", ".join(task.tags), font=("Segoe UI", 9, "italic")).grid(row=2, column=0, sticky='w')

        # Actions
        ttk.Button(card, text="✔ Done", bootstyle="light-success", command=lambda i=idx: self.complete(i)).grid(row=0, column=1, padx=10)
        ttk.Button(card, text="🗑 Delete", bootstyle="light-danger", command=lambda i=idx: self.delete(i)).grid(row=0, column=2)

    def refresh_tasks(self):
        self.countdowns.clear()
        for widget in self.panel.winfo_children():
            widget.destroy()

        if self.view_mode == "completed":
            tasks = TASKS.get_completed_tasks()
        elif self.view_mode == "pending":
            tasks = TASKS.get_pending_tasks()
        else:
            tasks = TASKS.tasks

        for i, task in enumerate(tasks):
            self._add_task_card(task, i)

    # ------------------------
    # Countdown & Reminders
    # ------------------------
    def update_countdowns(self):
        while True:
            now = datetime.now()
            for i, task in enumerate(TASKS.get_pending_tasks()):
                if i in self.countdowns:
                    delta = task.deadline - now
                    if delta.total_seconds() > 0:
                        days = delta.days
                        hours, rem = divmod(delta.seconds, 3600)
                        mins, secs = divmod(rem, 60)
                        time_left = f"{days}d {hours}h {mins}m {secs}s"
                    else:
                        time_left = "⏰ Overdue"
                    self.countdowns[i].config(text=f"⏳ {time_left}")
            time.sleep(1)

    def reminders(self):
        alerted_starts = set()
        alerted_deadlines = set()
        while True:
            now = datetime.now()
            for t in TASKS.get_pending_tasks():
                # Starting soon alert
                if 0 < (t.start_time - now).total_seconds() < 60 and t.title not in alerted_starts:
                    self.root.after(0, lambda title=t.title: messagebox.showinfo("⌛ Starting Soon", f"Task '{title}' is about to start!"))
                    alerted_starts.add(t.title)

                # Deadline soon alert
                if 0 < (t.deadline - now).total_seconds() < 60 and t.title not in alerted_deadlines:
                    self.root.after(0, lambda title=t.title: messagebox.showwarning("⚠️ Deadline Approaching", f"Task '{title}' is nearing its deadline!"))
                    alerted_deadlines.add(t.title)
            time.sleep(30)


    # ------------------------
    # Theme Toggle
    # ------------------------
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.root.style.theme_use("darkly" if self.dark_mode else "flatly")
        self.refresh_tasks()
        
    # ------------------------
    # Theme Toggle
    # ------------------------
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.root.style.theme_use("darkly" if self.dark_mode else "flatly")
        self.refresh_tasks()

    # ------------------------
    # Calendar View Methods
    # ------------------------
    def show_calendar(self):
        import calendar
        from datetime import date

        for widget in self.panel.winfo_children():
            widget.destroy()

        today = date.today()
        year, month = today.year, today.month
        first_day, num_days = calendar.monthrange(year, month)

        calendar_frame = ttk.Labelframe(self.panel, text=f"📅 {today.strftime('%B %Y')}", padding=10)
        calendar_frame.pack(fill='both', expand=True)

        for day in range(1, num_days + 1):
            day_date = date(year, month, day)
            tasks_for_day = [
                task for task in TASKS.get_pending_tasks()
                if task.deadline.date() == day_date
            ]
            day_frame = ttk.Frame(calendar_frame, padding=5)
            day_frame.pack(fill='x', pady=2)

            label = f"{day:02d} - {day_date.strftime('%A')}"
            ttk.Label(day_frame, text=label, font=('Segoe UI', 10, 'bold')).pack(side='left')

            if tasks_for_day:
                ttk.Button(day_frame, text=f"{len(tasks_for_day)} Task(s)",
                           bootstyle="info-outline",
                           command=lambda d=day_date: self.show_tasks_for_day(d)).pack(side='right')

    def show_tasks_for_day(self, selected_date):
        for widget in self.panel.winfo_children():
            widget.destroy()

        tasks_for_day = [
            task for task in TASKS.get_pending_tasks()
            if task.deadline.date() == selected_date
        ]

        ttk.Label(self.panel, text=f"📅 Tasks on {selected_date.strftime('%A, %d %B %Y')}",
                  font=('Segoe UI', 14, 'bold')).pack(anchor='w', padx=10, pady=(5, 10))

        for i, task in enumerate(tasks_for_day):
            self._add_task_card(task, i)

    # ------------------------
    # Task Operations
    # ------------------------
    def add_task(self):
        try:
            title = self.title.get().strip()
            if not title:
                raise ValueError("Title required")
            pr = self.priority.get()
            if pr not in PRIORITY_STYLE:
                raise ValueError("Valid priority needed")
            start = self.get_datetime_from_fields(self.start_year, self.start_month, self.start_day, self.start_hour, self.start_min)
            dl = self.get_datetime_from_fields(self.end_year, self.end_month, self.end_day, self.end_hour, self.end_min)
            tags = [t.strip() for t in self.tags.get().split(",") if t.strip()]
            t = Task(title, "", start, dl, pr, tags, [])
            TASKS.add_task(t)
            self.refresh_tasks()
            self._clear_form()
        except Exception as e:
            messagebox.showerror("Oops!", str(e))

    def _add_task(self):
        from datetime import datetime, timedelta
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Title required")
            return
        # Dummy times for demo; replace with real form fields as needed
        start = datetime.now()
        deadline = start + timedelta(days=2)
        tags = ["todo"]
        # Use AI to set priority
        task = Task(title, "", start, deadline, "Low", tags, [])
        TASKS.add_task(task)
        self.refresh_tasks()
        self.title_entry.delete(0, 'end')

    def complete(self, idx):
        TASKS.mark_complete(idx)
        self.refresh_tasks()

    def delete(self, idx):
        TASKS.delete_task(idx)
        self.refresh_tasks()

    def get_datetime_from_fields(self, y, m, d, h, mi):
        values = [y.get(), m.get(), d.get(), h.get(), mi.get()]
        if any(v in ["", "DD", "MM", "YYYY", "HH"] for v in values):
            raise ValueError("Please select a complete valid date and time.")
        dt_str = f"{y.get()}-{m.get()}-{d.get()} {h.get()}:{mi.get()}"
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M")

    def _clear_form(self):
        self.title.delete(0, 'end')
        self.priority.set('')
        for field in [
            self.start_day, self.start_month, self.start_year,
            self.start_hour, self.start_min,
            self.end_day, self.end_month, self.end_year,
            self.end_hour, self.end_min
        ]:
            field.set('')
        self.tags.delete(0, 'end')

    # ------------------------
    # Task Display
    # ------------------------
    def _add_task_card(self, task, idx):
        card = ttk.Frame(self.panel, bootstyle=PRIORITY_STYLE[task.priority], padding=15)
        card.pack(fill='x', pady=6)

        # Countdown Label
        self.countdowns[idx] = ttk.Label(card, font=("Segoe UI", 10, "bold"))
        self.countdowns[idx].grid(row=1, column=1, padx=10, sticky='e')

        # Task Info
        ttk.Label(card, text=task.title, font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky='w')
        ttk.Label(card, text=f"{task.start_time.strftime('%Y-%m-%d %H:%M')} → {task.deadline.strftime('%Y-%m-%d %H:%M')}", font=("Segoe UI", 9)).grid(row=1, column=0, sticky='w')
        if task.tags:
            ttk.Label(card, text="Tags: " + ", ".join(task.tags), font=("Segoe UI", 9, "italic")).grid(row=2, column=0, sticky='w')

        # Actions
        ttk.Button(card, text="✔ Done", bootstyle="light-success", command=lambda i=idx: self.complete(i)).grid(row=0, column=1, padx=10)
        ttk.Button(card, text="🗑 Delete", bootstyle="light-danger", command=lambda i=idx: self.delete(i)).grid(row=0, column=2)

    def refresh_tasks(self):
        self.countdowns.clear()
        for widget in self.panel.winfo_children():
            widget.destroy()

        if self.view_mode == "completed":
            tasks = TASKS.get_completed_tasks()
        elif self.view_mode == "pending":
            tasks = TASKS.get_pending_tasks()
        else:
            tasks = TASKS.tasks

        for i, task in enumerate(tasks):
            self._add_task_card(task, i)

    # ------------------------
    # Countdown & Reminders
    # ------------------------
    def update_countdowns(self):
        while True:
            now = datetime.now()
            for i, task in enumerate(TASKS.get_pending_tasks()):
                if i in self.countdowns:
                    delta = task.deadline - now
                    if delta.total_seconds() > 0:
                        days = delta.days
                        hours, rem = divmod(delta.seconds, 3600)
                        mins, secs = divmod(rem, 60)
                        time_left = f"{days}d {hours}h {mins}m {secs}s"
                    else:
                        time_left = "⏰ Overdue"
                    self.countdowns[i].config(text=f"⏳ {time_left}")
            time.sleep(1)

    def reminders(self):
        alerted_starts = set()
        alerted_deadlines = set()
        while True:
            now = datetime.now()
            for t in TASKS.get_pending_tasks():
                # Starting soon alert
                if 0 < (t.start_time - now).total_seconds() < 60 and t.title not in alerted_starts:
                    self.root.after(0, lambda title=t.title: messagebox.showinfo("⌛ Starting Soon", f"Task '{title}' is about to start!"))
                    alerted_starts.add(t.title)

                # Deadline soon alert
                if 0 < (t.deadline - now).total_seconds() < 60 and t.title not in alerted_deadlines:
                    self.root.after(0, lambda title=t.title: messagebox.showwarning("⚠️ Deadline Approaching", f"Task '{title}' is nearing its deadline!"))
                    alerted_deadlines.add(t.title)
            time.sleep(30)

    # ------------------------
    # Theme Toggle
    # ------------------------
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.root.style.theme_use("darkly" if self.dark_mode else "flatly")
        self.refresh_tasks()

    def set_view(self, mode):
        self.view_mode = mode
        self.refresh_tasks()

# ----------------------------
# Main Application Runner
# ----------------------------
if __name__ == "__main__":
    app = ttk.Window(themename="flatly")
    ModernToDo(app)
    app.mainloop()
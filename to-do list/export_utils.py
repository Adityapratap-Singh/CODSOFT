# export_utils.py

import csv
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_to_csv(tasks, filename="tasks_export.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Description", "Start Time", "Deadline", "Priority", "Tags", "Recurring"])
        for t in tasks:
            writer.writerow([
                t.title,
                t.description,
                t.start_time.strftime("%Y-%m-%d %H:%M"),
                t.deadline.strftime("%Y-%m-%d %H:%M"),
                t.priority,
                ', '.join(t.tags),
                t.recurring or "None"
            ])
    print(f"✅ CSV Exported: {filename}")

def export_to_json(tasks, filename="tasks_export.json"):
    data = [t.to_dict() for t in tasks]
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"✅ JSON Exported: {filename}")

def export_to_pdf(tasks, filename="tasks_export.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "📋 Task Report")
    y -= 30

    c.setFont("Helvetica", 10)
    for t in tasks:
        lines = [
            f"Title: {t.title}",
            f"Desc: {t.description}",
            f"Start: {t.start_time.strftime('%Y-%m-%d %H:%M')}",
            f"Deadline: {t.deadline.strftime('%Y-%m-%d %H:%M')}",
            f"Priority: {t.priority} | Recurring: {t.recurring or 'None'}",
            f"Tags: {', '.join(t.tags)}",
            "-"*80
        ]
        for line in lines:
            c.drawString(40, y, line)
            y -= 15
            if y < 60:
                c.showPage()
                y = height - 40
                c.setFont("Helvetica", 10)
    c.save()
    print(f"✅ PDF Exported: {filename}")

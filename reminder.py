import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

class Reminder:
    def __init__(self, title, description, datetime):
        self.title = title
        self.description = description
        self.datetime = datetime
    
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'datetime': self.datetime.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @staticmethod
    def from_dict(data):
        return Reminder(
            title=data['title'],
            description=data['description'],
            datetime=datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S')
        )
    
    def __str__(self):
        return f"Reminder: {self.title}\nDescription: {self.description}\nTime: {self.datetime.strftime('%Y-%m-%d %H:%M:%S')}\n"


class Schedule:
    def __init__(self):
        self.reminders = []
        self.load_reminders()
    
    def add_reminder(self, reminder):
        self.reminders.append(reminder)
        self.save_reminders()
    
    def view_reminders(self):
        return "\n".join(str(reminder) for reminder in self.reminders) if self.reminders else "No reminders set."
    
    def delete_reminder(self, title):
        for reminder in self.reminders:
            if reminder.title == title:
                self.reminders.remove(reminder)
                self.save_reminders()
                return True
        return False
    
    def save_reminders(self):
        with open('reminders.json', 'w') as f:
            json.dump([reminder.to_dict() for reminder in self.reminders], f)
    
    def load_reminders(self):
        try:
            with open('reminders.json', 'r') as f:
                reminders_data = json.load(f)
                self.reminders = [Reminder.from_dict(data) for data in reminders_data]
        except FileNotFoundError:
            pass


class ReminderApp:
    def __init__(self, root):
        self.schedule = Schedule()
        self.root = root
        self.root.title("Schedule Reminder Program")

        self.add_frame = tk.Frame(root)
        self.view_frame = tk.Frame(root)
        self.delete_frame = tk.Frame(root)

        self.setup_add_frame()
        self.setup_view_frame()
        self.setup_delete_frame()

        self.add_frame.pack()
        self.view_frame.pack()
        self.delete_frame.pack()

    def setup_add_frame(self):
        tk.Label(self.add_frame, text="Add Reminder", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        self.title_entry = tk.Entry(self.add_frame, width=40)
        self.title_entry.insert(0, "Enter title")
        self.title_entry.pack(pady=5)
        
        self.description_entry = scrolledtext.ScrolledText(self.add_frame, width=40, height=4)
        self.description_entry.insert(tk.END, "Enter description")
        self.description_entry.pack(pady=5)
        
        self.datetime_entry = tk.Entry(self.add_frame, width=40)
        self.datetime_entry.insert(0, "Enter date and time (YYYY-MM-DD HH:MM:SS)")
        self.datetime_entry.pack(pady=5)
        
        tk.Button(self.add_frame, text="Add Reminder", command=self.add_reminder).pack(pady=10)

    def setup_view_frame(self):
        tk.Label(self.view_frame, text="View Reminders", font=('Helvetica', 14, 'bold')).pack(pady=10)
        self.reminders_text = scrolledtext.ScrolledText(self.view_frame, width=60, height=10)
        self.reminders_text.pack(pady=5)
        self.view_reminders()
    
    def setup_delete_frame(self):
        tk.Label(self.delete_frame, text="Delete Reminder", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        self.delete_title_entry = tk.Entry(self.delete_frame, width=40)
        self.delete_title_entry.insert(0, "Enter title to delete")
        self.delete_title_entry.pack(pady=5)
        
        tk.Button(self.delete_frame, text="Delete Reminder", command=self.delete_reminder).pack(pady=10)

    def add_reminder(self):
        title = self.title_entry.get()
        description = self.description_entry.get("1.0", tk.END).strip()
        date_str = self.datetime_entry.get()

        try:
            reminder_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            reminder = Reminder(title, description, reminder_datetime)
            self.schedule.add_reminder(reminder)
            messagebox.showinfo("Success", f"Added reminder: {title}")
            self.view_reminders()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD HH:MM:SS.")

    def view_reminders(self):
        self.reminders_text.delete("1.0", tk.END)
        reminders_str = self.schedule.view_reminders()
        self.reminders_text.insert(tk.END, reminders_str)

    def delete_reminder(self):
        title = self.delete_title_entry.get()
        if self.schedule.delete_reminder(title):
            messagebox.showinfo("Success", f"Deleted reminder: {title}")
            self.view_reminders()
        else:
            messagebox.showerror("Error", f"No reminder found with title: {title}")


def main():
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

# -----------------------------
# Student Class
# -----------------------------
class Student:
    def __init__(self, code, name, c1, c2, c3, exam):
        self.code = code.strip()
        self.name = name.strip()
        self.c1 = int(c1)
        self.c2 = int(c2)
        self.c3 = int(c3)
        self.exam = int(exam)

    def coursework_total(self):
        return self.c1 + self.c2 + self.c3

    def overall_percentage(self):
        return round(((self.coursework_total() + self.exam) / 160) * 100, 2)

    def grade(self):
        pct = self.overall_percentage()
        if pct >= 70: return "A"
        elif pct >= 60: return "B"
        elif pct >= 50: return "C"
        elif pct >= 40: return "D"
        else: return "F"

    def __str__(self):
        return (
            f"Name: {self.name}\n"
            f"Code: {self.code}\n"
            f"Coursework Total: {self.coursework_total()}/60\n"
            f"Exam Mark: {self.exam}/100\n"
            f"Overall Percentage: {self.overall_percentage()}%\n"
            f"Grade: {self.grade()}\n"
            "-----------------------------"
        )


# -----------------------------
# Main App
# -----------------------------
class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("1000x600")
        self.students = []

        self.file_path = r"Assessment 1 - Skills Portfolio\Exercise 3\studentMarks.txt"

        self.build_ui()
        self.load_data()

    # -----------------------------
    # UI Layout
    # -----------------------------
    def build_ui(self):

        # LEFT SIDEBAR
        sidebar = tk.Frame(self.root, bg="#1E1E1E", width=200)
        sidebar.pack(side="left", fill="y")

        title = tk.Label(sidebar, text="Student Manager",
                         font=("Arial", 16, "bold"), bg="#1E1E1E", fg="white")
        title.pack(pady=20)

        # BUTTONS IN SIDEBAR
        menu_buttons = [
            ("View All Records", self.view_all_records),
            ("View Individual", self.view_individual_record),
            ("Highest Score", self.highest_score),
            ("Lowest Score", self.lowest_score),
            ("Sort Records", self.sort_records),
            ("Add Student", self.add_student),
            ("Delete Student", self.delete_student),
            ("Update Student", self.update_student),
        ]

        for text, command in menu_buttons:
            btn = tk.Button(sidebar, text=text, command=command,
                            bg="#3A3A3A", fg="white", width=18, height=2,
                            font=("Arial", 10, "bold"))
            btn.pack(pady=5)

        # RIGHT OUTPUT PANEL
        output_frame = tk.Frame(self.root, bg="#2A2A2A")
        output_frame.pack(side="right", fill="both", expand=True)

        self.output_text = tk.Text(output_frame, font=("Courier", 12),
                                   bg="#2A2A2A", fg="white")
        self.output_text.pack(fill="both", expand=True, padx=10, pady=10)

    # -----------------------------
    # Utility
    # -----------------------------
    def output_message(self, msg):
        self.output_text.insert(tk.END, msg + "\n")
        self.output_text.see(tk.END)

    # -----------------------------
    # Load & Save Data
    # -----------------------------
    def load_data(self):
        if not os.path.exists(self.file_path):
            messagebox.showerror("Error", f"Cannot find file:\n{self.file_path}")
            return

        self.students.clear()

        with open(self.file_path, "r") as file:
            count = int(file.readline().strip())
            for _ in range(count):
                parts = file.readline().strip().split(",")
                if len(parts) == 6:
                    self.students.append(Student(*parts))

        self.output_message(f"Loaded {len(self.students)} student records.\n")

    def save_data(self):
        with open(self.file_path, "w") as f:
            f.write(str(len(self.students)) + "\n")
            for s in self.students:
                f.write(f"{s.code},{s.name},{s.c1},{s.c2},{s.c3},{s.exam}\n")

    # -----------------------------
    # MENU FUNCTIONS
    # -----------------------------
    def view_all_records(self):
        self.output_text.delete("1.0", tk.END)
        self.output_message("=== ALL STUDENT RECORDS ===\n")

        for s in self.students:
            self.output_message(str(s))

        avg = sum(s.overall_percentage() for s in self.students) / len(self.students)
        self.output_message(f"\nClass Average: {round(avg, 2)}%")

    def view_individual_record(self):
        search = simpledialog.askstring("Search", "Enter student NAME or CODE:")
        if not search: return

        for s in self.students:
            if s.code == search or s.name.lower() == search.lower():
                self.output_text.delete("1.0", tk.END)
                self.output_message(str(s))
                return

        messagebox.showerror("Not Found", "Student not found.")

    def highest_score(self):
        top = max(self.students, key=lambda s: s.overall_percentage())
        self.output_text.delete("1.0", tk.END)
        self.output_message("=== HIGHEST SCORE ===\n")
        self.output_message(str(top))

    def lowest_score(self):
        low = min(self.students, key=lambda s: s.overall_percentage())
        self.output_text.delete("1.0", tk.END)
        self.output_message("=== LOWEST SCORE ===\n")
        self.output_message(str(low))

    def sort_records(self):
        choice = messagebox.askquestion("Sort", "Sort ascending?\nClick 'No' for descending.")
        ascending = (choice == "yes")

        self.students.sort(key=lambda s: s.overall_percentage(), reverse=not ascending)
        self.save_data()

        self.output_text.delete("1.0", tk.END)
        self.output_message("✔ Records sorted and saved.\n")
        self.view_all_records()

    def add_student(self):
        code = simpledialog.askstring("Add", "Enter student code:")
        name = simpledialog.askstring("Add", "Enter student name:")
        c1 = simpledialog.askinteger("Add", "Coursework 1:")
        c2 = simpledialog.askinteger("Add", "Coursework 2:")
        c3 = simpledialog.askinteger("Add", "Coursework 3:")
        exam = simpledialog.askinteger("Add", "Exam mark:")

        self.students.append(Student(code, name, c1, c2, c3, exam))
        self.save_data()
        self.output_message("✔ Student added successfully.\n")

    def delete_student(self):
        search = simpledialog.askstring("Delete", "Enter NAME or CODE to delete:")
        if not search: return

        for s in self.students:
            if s.code == search or s.name.lower() == search.lower():
                self.students.remove(s)
                self.save_data()
                self.output_message("✔ Student deleted.\n")
                return

        messagebox.showerror("Not Found", "Student does not exist.")

    def update_student(self):
        search = simpledialog.askstring("Update", "Enter NAME or CODE to update:")
        if not search: return

        for s in self.students:
            if s.code == search or s.name.lower() == search.lower():

                new_name = simpledialog.askstring("Update", "New name:", initialvalue=s.name)
                new_c1 = simpledialog.askinteger("Update", "Coursework 1:", initialvalue=s.c1)
                new_c2 = simpledialog.askinteger("Update", "Coursework 2:", initialvalue=s.c2)
                new_c3 = simpledialog.askinteger("Update", "Coursework 3:", initialvalue=s.c3)
                new_exam = simpledialog.askinteger("Update", "Exam:", initialvalue=s.exam)

                s.name = new_name
                s.c1 = new_c1
                s.c2 = new_c2
                s.c3 = new_c3
                s.exam = new_exam

                self.save_data()
                self.output_message("✔ Student updated.\n")
                return

        messagebox.showerror("Not Found", "Student does not exist.")


# -----------------------------
# Run App
# -----------------------------
root = tk.Tk()
app = StudentManagerApp(root)
root.mainloop()

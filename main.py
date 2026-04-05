import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

FILE_NAME = "students.csv"

class Student:
   def __init__(self, name, student_id, physics, chemistry, biology, monthly_fee, fee_status):
       self.name = name
       self.student_id = student_id
       self.physics = physics
       self.chemistry = chemistry
       self.biology = biology
       self.monthly_fee = monthly_fee
       self.fee_status = fee_status

   def total_marks(self):
       return self.physics + self.chemistry + self.biology

   def average_marks(self):
       return self.total_marks() / 3

   def grade(self):
       avg = self.average_marks()
       if avg >= 75:
           return "A"
       elif avg >= 60:
           return "B"
       elif avg >= 45:
           return "C"
       elif avg >= 35:
           return "S"
       else:
           return "F"


def load_students():
   students = []
   if not os.path.exists(FILE_NAME):
       return students

   with open(FILE_NAME, "r") as file:
       reader = csv.DictReader(file)
       for row in reader:
           students.append(Student(
               row["name"],
               row["student_id"],
               int(row["physics"]),
               int(row["chemistry"]),
               int(row["biology"]),
               float(row["monthly_fee"]),
               row["fee_status"]
           ))
   return students


def save_students(students):
   with open(FILE_NAME, "w", newline="") as file:
       writer = csv.DictWriter(file, fieldnames=[
           "name", "student_id", "physics", "chemistry",
           "biology", "monthly_fee", "fee_status"
       ])
       writer.writeheader()
       for s in students:
           writer.writerow(vars(s))


students = load_students()


def clear_fields():
   entry_name.delete(0, tk.END)
   entry_id.delete(0, tk.END)
   entry_phy.delete(0, tk.END)
   entry_che.delete(0, tk.END)
   entry_bio.delete(0, tk.END)
   entry_fee.delete(0, tk.END)
   status_var.set("Paid")


def add_student():
   try:
       name = entry_name.get()
       sid = entry_id.get()

       if name == "" or sid == "":
           messagebox.showerror("Error", "Name and ID required")
           return

       for s in students:
           if s.student_id == sid:
               messagebox.showerror("Error", "Duplicate ID")
               return

       student = Student(
           name,
           sid,
           int(entry_phy.get()),
           int(entry_che.get()),
           int(entry_bio.get()),
           float(entry_fee.get()),
           status_var.get()
       )

       students.append(student)
       save_students(students)

       messagebox.showinfo("Success", "Student Added")
       clear_fields()

   except:
       messagebox.showerror("Error", "Invalid Input")


def view_students():
   for row in table.get_children():
       table.delete(row)

   for s in students:
       table.insert("", "end", values=(
           s.name,
           s.student_id,
           f"{s.average_marks():.2f}",
           s.grade(),
           s.monthly_fee,
           s.fee_status
       ))


def search_student():
   sid = entry_search.get()

   for row in table.get_children():
       table.delete(row)

   for s in students:
       if s.student_id == sid:
           table.insert("", "end", values=(
               s.name,
               s.student_id,
               f"{s.average_marks():.2f}",
               s.grade(),
               s.monthly_fee,
               s.fee_status
           ))
           return

   messagebox.showerror("Error", "Not Found")


def update_fee():
   sid = entry_search.get()

   for s in students:
       if s.student_id == sid:
           s.fee_status = status_var.get()
           save_students(students)
           messagebox.showinfo("Success", "Updated")
           return

   messagebox.showerror("Error", "Not Found")


def generate_report():
   sid = entry_search.get()

   for s in students:
       if s.student_id == sid:
           with open(f"report_{sid}.csv", "w", newline="") as f:
               writer = csv.writer(f)
               writer.writerow(["Field", "Value"])
               writer.writerow(["Name", s.name])
               writer.writerow(["ID", s.student_id])
               writer.writerow(["Average", s.average_marks()])
               writer.writerow(["Grade", s.grade()])
               writer.writerow(["Fee", s.monthly_fee])
               writer.writerow(["Status", s.fee_status])

           messagebox.showinfo("Success", "Report Created")
           return

   messagebox.showerror("Error", "Not Found")


root = tk.Tk()
root.title("Student Management System")
root.geometry("750x600")
root.configure(bg="#f5f7fa")


tk.Label(root, text="Student Management System",
        font=("Arial", 18, "bold"),
        bg="#f5f7fa").pack(pady=10)

# Input Frame
frame = tk.Frame(root, bg="white", bd=2, relief="groove")
frame.pack(pady=10, padx=10, fill="x")

def create_field(label):
   tk.Label(frame, text=label, bg="white").pack()
   entry = tk.Entry(frame)
   entry.pack(pady=2)
   return entry

entry_name = create_field("Name")
entry_id = create_field("Student ID")
entry_phy = create_field("Physics")
entry_che = create_field("Chemistry")
entry_bio = create_field("Biology")
entry_fee = create_field("Monthly Fee")

tk.Label(frame, text="Fee Status", bg="white").pack()
status_var = tk.StringVar(value="Paid")
dropdown = ttk.Combobox(frame, textvariable=status_var, values=["Paid", "Unpaid"], state="readonly")
dropdown.pack(pady=3)

btn_frame = tk.Frame(root, bg="#f5f7fa")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Student", command=add_student,
         width=18, bg="#4a90e2", fg="white").grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="View Students", command=view_students,
         width=18, bg="#4a90e2", fg="white").grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="Update Fee", command=update_fee,
         width=18, bg="#4a90e2", fg="white").grid(row=1, column=0, padx=5, pady=5)

tk.Button(btn_frame, text="Generate Report", command=generate_report,
         width=18, bg="#4a90e2", fg="white").grid(row=1, column=1, padx=5)

tk.Label(root, text="Search by ID", bg="#f5f7fa").pack()
entry_search = tk.Entry(root)
entry_search.pack()

tk.Button(root, text="Search Student", command=search_student,
         bg="#27ae60", fg="white", width=20).pack(pady=5)

columns = ("Name", "ID", "Average", "Grade", "Fee", "Status")
table = ttk.Treeview(root, columns=columns, show="headings", height=10)

for col in columns:
   table.heading(col, text=col)
   table.column(col, anchor="center")

table.pack(pady=10, fill="x")

root.mainloop()

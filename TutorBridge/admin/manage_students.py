import os
import sys
from tkinter import *
from tkinter import messagebox, ttk

# Resolve paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from TutorBridge.database import get_connection
except ImportError:
    from database import get_connection

class ManageStudentsFrame:
    def __init__(self, parent_frame, bg_color, text_color, accent_color, accent_hover, danger_color, danger_hover):
        self.parent = parent_frame
        self.bg_color = bg_color
        self.text_color = text_color
        self.accent_color = accent_color
        self.accent_hover = accent_hover
        self.danger_color = danger_color
        self.danger_hover = danger_hover
        
        self.draw_ui()
        
    def draw_ui(self):
        # Header
        header_frame = Frame(self.parent, bg=self.bg_color, padx=30, pady=25)
        header_frame.pack(fill="x")
        
        Label(header_frame, text="Manage Students", font=("Helvetica", 22, "bold"), fg=self.text_color, bg=self.bg_color).pack(side="left")
        
        # Search panel
        search_frame = Frame(self.parent, bg=self.bg_color, padx=30)
        search_frame.pack(fill="x", pady=(0, 15))
        
        Label(search_frame, text="Search Students:", font=("Helvetica", 10, "bold"), fg=self.text_color, bg=self.bg_color).pack(side="left", padx=(0, 10))
        
        self.search_val = StringVar()
        search_entry = Entry(
            search_frame, 
            textvariable=self.search_val, 
            font=("Helvetica", 11), 
            width=28, 
            bg="white", 
            fg="#3d200f", 
            insertbackground="#3d200f", 
            relief="flat", 
            highlightthickness=1, 
            highlightbackground="#bba690", 
            highlightcolor="#c69d77"
        )
        search_entry.pack(side="left", padx=5, ipady=3)
        search_entry.bind("<Return>", lambda e: self.search_students())
        
        Label(search_frame, text="Filter by:", font=("Helvetica", 10), fg=self.text_color, bg=self.bg_color).pack(side="left", padx=(15, 5))
        self.filter_col = StringVar(value="Name")
        filter_box = ttk.Combobox(search_frame, textvariable=self.filter_col, values=["Name", "City", "Email"], state="readonly", width=12, font=("Helvetica", 10))
        filter_box.pack(side="left", padx=5)
        
        btn_search = Button(search_frame, text="Search", bg=self.accent_color, fg="#3d200f", font=("Helvetica", 10, "bold"), bd=0, padx=15, cursor="hand2", command=self.search_students)
        btn_search.pack(side="left", padx=5, ipady=3)
        self.bind_hover(btn_search, self.accent_color, self.accent_hover)
        
        btn_clear = Button(search_frame, text="Reset", bg=self.danger_color, fg=self.text_color, font=("Helvetica", 10, "bold"), bd=0, padx=15, cursor="hand2", command=self.fetch_students)
        btn_clear.pack(side="left", padx=5, ipady=3)
        self.bind_hover(btn_clear, self.danger_color, self.danger_hover)
        
        # Table Container
        table_frame = Frame(self.parent, bg=self.bg_color, bd=0, padx=30)
        table_frame.pack(fill="both", expand=True, pady=10)
        
        # Scrollbars
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        
        # Treeview setup
        cols = ("Student ID", "Name", "Email", "Phone", "City")
        self.tree = ttk.Treeview(
            table_frame, 
            columns=cols, 
            show="headings", 
            yscrollcommand=scroll_y.set, 
            xscrollcommand=scroll_x.set
        )
        
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Headings and column widths
        widths = {
            "Student ID": 100, "Name": 200, "Email": 250, "Phone": 150, "City": 150
        }
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths.get(col, 150), anchor="center")
            
        self.tree.pack(fill="both", expand=True)
        
        # Actions Panel
        actions_frame = Frame(self.parent, bg=self.bg_color, padx=30, pady=20)
        actions_frame.pack(fill="x")
        
        btn_update = Button(actions_frame, text="✏️ Update Details", bg=self.accent_color, fg="#3d200f", font=("Helvetica", 11, "bold"), bd=0, padx=20, pady=8, cursor="hand2", command=self.update_student_dialog)
        btn_update.pack(side="left", padx=(0, 15))
        self.bind_hover(btn_update, self.accent_color, self.accent_hover)
        
        btn_delete = Button(actions_frame, text="🗑️ Delete Student", bg=self.danger_color, fg=self.text_color, font=("Helvetica", 11, "bold"), bd=0, padx=20, pady=8, cursor="hand2", command=self.delete_student)
        btn_delete.pack(side="left", padx=15)
        self.bind_hover(btn_delete, self.danger_color, self.danger_hover)
        
        # Load data
        self.fetch_students()
        
    def bind_hover(self, button, normal_color, hover_color):
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))

    def fetch_students(self):
        self.search_val.set("")
        self.tree.delete(*self.tree.get_children())
        
        conn = get_connection()
        if conn is None:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT student_id, name, email, phone, city FROM students ORDER BY student_id DESC")
            rows = cursor.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch students: {e}")

    def search_students(self):
        query_val = self.search_val.get().strip()
        filter_col = self.filter_col.get()
        
        if not query_val:
            self.fetch_students()
            return
            
        col_map = {
            "Name": "name",
            "City": "city",
            "Email": "email"
        }
        db_col = col_map.get(filter_col, "name")
        
        self.tree.delete(*self.tree.get_children())
        
        conn = get_connection()
        if conn is None:
            return
            
        try:
            cursor = conn.cursor()
            query = f"SELECT student_id, name, email, phone, city FROM students WHERE {db_col} LIKE %s ORDER BY student_id DESC"
            cursor.execute(query, (f"%{query_val}%",))
            rows = cursor.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a student profile to delete.")
            return
            
        data = self.tree.item(selected[0], "values")
        student_id = data[0]
        name = data[1]
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student {name}? This will also delete all their feedbacks.")
        if not confirm:
            return
            
        conn = get_connection()
        if conn is None:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            conn.commit()
            cursor.close()
            conn.close()
            
            messagebox.showinfo("Success", "Student profile deleted successfully.")
            self.fetch_students()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student: {e}")

    def update_student_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a student profile to update.")
            return
            
        data = self.tree.item(selected[0], "values")
        student_id = data[0]
        
        conn = get_connection()
        if conn is None:
            return
            
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        s = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not s:
            messagebox.showerror("Error", "Could not retrieve student details.")
            return
            
        # Dialog
        edit_win = Toplevel(self.parent)
        edit_win.title(f"Update Student - {s['name']}")
        edit_win.geometry("500x400")
        edit_win.resizable(False, False)
        edit_win.configure(bg="#3d200f")
        
        Label(edit_win, text=f"Update details for {s['name']}", font=("Helvetica", 16, "bold"), fg=self.accent_color, bg="#3d200f").pack(pady=20)
        
        form = Frame(edit_win, bg="#755e52", padx=25, pady=25)
        form.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Form Fields
        Label(form, text="Name", font=("Helvetica", 10, "bold"), fg=self.text_color, bg="#755e52").grid(row=0, column=0, sticky="w", pady=10, padx=(0, 15))
        name_entry = Entry(form, font=("Helvetica", 10), width=30, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
        name_entry.insert(0, s["name"])
        name_entry.grid(row=0, column=1, pady=10)
        
        Label(form, text="Phone", font=("Helvetica", 10, "bold"), fg=self.text_color, bg="#755e52").grid(row=1, column=0, sticky="w", pady=10, padx=(0, 15))
        phone_entry = Entry(form, font=("Helvetica", 10), width=30, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
        phone_entry.insert(0, s["phone"] if s["phone"] else "")
        phone_entry.grid(row=1, column=1, pady=10)
        
        Label(form, text="City", font=("Helvetica", 10, "bold"), fg=self.text_color, bg="#755e52").grid(row=2, column=0, sticky="w", pady=10, padx=(0, 15))
        city_entry = Entry(form, font=("Helvetica", 10), width=30, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
        city_entry.insert(0, s["city"] if s["city"] else "")
        city_entry.grid(row=2, column=1, pady=10)
        
        def save():
            name_val = name_entry.get().strip()
            phone_val = phone_entry.get().strip()
            city_val = city_entry.get().strip()
            
            if not name_val or not phone_val or not city_val:
                messagebox.showerror("Error", "All fields are required!", parent=edit_win)
                return
                
            db_conn = get_connection()
            if db_conn is None:
                return
                
            try:
                cursor_db = db_conn.cursor()
                cursor_db.execute(
                    "UPDATE students SET name=%s, phone=%s, city=%s WHERE student_id=%s",
                    (name_val, phone_val, city_val, student_id)
                )
                db_conn.commit()
                cursor_db.close()
                db_conn.close()
                
                messagebox.showinfo("Success", "Student details updated.", parent=edit_win)
                edit_win.destroy()
                self.fetch_students()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save changes: {e}", parent=edit_win)
                
        # Buttons
        btn_save = Button(form, text="Save Updates", font=("Helvetica", 11, "bold"), bg=self.accent_color, fg="#3d200f", bd=0, padx=20, pady=5, cursor="hand2", command=save)
        btn_save.grid(row=3, column=0, columnspan=2, pady=(20, 5), sticky="we")
        btn_save.bind("<Enter>", lambda e: btn_save.config(bg=self.accent_hover))
        btn_save.bind("<Leave>", lambda e: btn_save.config(bg=self.accent_color))
        
        btn_cancel = Button(form, text="Cancel", font=("Helvetica", 11, "bold"), bg=self.danger_color, fg=self.text_color, bd=0, padx=20, pady=5, cursor="hand2", command=edit_win.destroy)
        btn_cancel.grid(row=4, column=0, columnspan=2, pady=5, sticky="we")
        btn_cancel.bind("<Enter>", lambda e: btn_cancel.config(bg=self.danger_hover))
        btn_cancel.bind("<Leave>", lambda e: btn_cancel.config(bg=self.danger_color))

def load_students_frame(parent_frame, bg_color, text_color, accent_color, accent_hover, danger_color, danger_hover):
    ManageStudentsFrame(parent_frame, bg_color, text_color, accent_color, accent_hover, danger_color, danger_hover)

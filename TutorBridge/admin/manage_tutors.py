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

class AdminDashboard:
    def __init__(self, root, parent_root, username="admin"):
        self.root = root
        self.parent_root = parent_root
        self.username = username
        self.root.title("Admin Dashboard - TutorBridge")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)
        
        # Design Theme
        self.bg_color = "#3d200f"      
        self.sidebar_color = "#3d200f" 
        self.content_bg = "#c7b5a3"    
        self.text_dark = "#3d200f"     
        self.text_light = "#c7b5a3"    
        self.text_muted = "#bba690"    
        self.accent_color = "#c69d77"  
        self.accent_hover = "#b0977c"  
        self.danger_color = "#734022"  
        self.danger_hover = "#725237"  
        self.success_color = "#a87a64" 
        self.success_hover = "#8d7865" 
        
        self.root.configure(bg=self.content_bg)
        
        # Configure TTK style theme globally
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure Combobox Style
        style.configure("TCombobox", fieldbackground="#c7b5a3", background="#c69d77", foreground="#3d200f", selectbackground="#755e52")
        
        # Configure Treeview Style
        style.configure("Treeview", 
                        background="#c7b5a3", 
                        foreground="#3d200f", 
                        fieldbackground="#c7b5a3",
                        rowheight=25,
                        gridcolor="#bba690")
        style.map("Treeview", background=[("selected", "#755e52")], foreground=[("selected", "#c7b5a3")])
        style.configure("Treeview.Heading", 
                        background="#8d7865", 
                        foreground="#3d200f",
                        font=("Helvetica", 10, "bold"))
        
        # Set up cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self.logout)
        
        self.create_sidebar()
        
        # Main content area
        self.content_frame = Frame(self.root, bg=self.content_bg)
        self.content_frame.place(x=250, y=0, width=950, height=700)
        
        # Load Tutors screen as default
        self.load_manage_tutors()
        
    def create_sidebar(self):
        # Sidebar Container
        sidebar = Frame(self.root, bg=self.sidebar_color, width=250, height=700)
        sidebar.place(x=0, y=0, width=250, height=700)
        
        btn_back = Button(
            sidebar,
            text="← Back",
            font=("Helvetica", 11, "bold"),
            fg=self.text_light,
            bg=self.sidebar_color,
            bd=0,
            height=1,
            cursor="hand2",
            command=self.logout
        )
        btn_back.pack(pady=(20, 6), padx=10)
        btn_back.bind("<Enter>", lambda e: btn_back.config(bg=self.accent_color, fg="#3d200f"))
        btn_back.bind("<Leave>", lambda e: btn_back.config(bg=self.sidebar_color, fg=self.text_light))
        
        # Header / Title
        Label(
            sidebar, 
            text="TutorBridge", 
            font=("Helvetica", 20, "bold"), 
            fg=self.accent_color, 
            bg=self.sidebar_color
        ).pack(pady=(40, 5))
        
        Label(
            sidebar, 
            text="Admin Control Panel", 
            font=("Helvetica", 9, "italic"), 
            fg=self.text_muted, 
            bg=self.sidebar_color
        ).pack(pady=(0, 40))
        
        # Navigation Buttons
        btn_style = {
            "font": ("Helvetica", 11, "bold"),
            "fg": self.text_light,
            "bg": self.sidebar_color,
            "activebackground": self.accent_color,
            "activeforeground": "#3d200f",
            "bd": 0,
            "height": 2,
            "cursor": "hand2",
            "anchor": "w",
            "padx": 25
        }
        
        self.btn_tutors = Button(sidebar, text="👥  Manage Tutors", command=self.load_manage_tutors, **btn_style)
        self.btn_tutors.pack(fill="x", pady=2)
        
        self.btn_students = Button(sidebar, text="👨‍🎓  Manage Students", command=self.load_manage_students, **btn_style)
        self.btn_students.pack(fill="x", pady=2)
        
        self.btn_reports = Button(sidebar, text="📊  System Reports", command=self.load_reports, **btn_style)
        self.btn_reports.pack(fill="x", pady=2)
        
        self.btn_profile = Button(sidebar, text="👤  View Profile", command=self.load_profile, **btn_style)
        self.btn_profile.pack(fill="x", pady=2)
        
        # Bottom logout button
        btn_logout = Button(
            sidebar, 
            text="🚪  Sign Out", 
            command=self.logout, 
            font=("Helvetica", 11, "bold"),
            fg=self.text_light,
            bg=self.danger_color,
            activebackground=self.danger_hover,
            activeforeground=self.text_light,
            bd=0,
            height=2,
            cursor="hand2"
        )
        btn_logout.pack(side="bottom", fill="x", pady=30)
        btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg=self.danger_hover))
        btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg=self.danger_color))
        
        # Initial highlights
        self.highlight_nav(self.btn_tutors)
        
    def highlight_nav(self, active_btn):
        # Reset backgrounds
        for btn in [self.btn_tutors, self.btn_students, self.btn_reports, self.btn_profile]:
            btn.config(bg=self.sidebar_color, fg=self.text_light)
        active_btn.config(bg=self.accent_color, fg="#3d200f")
        
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def logout(self):
        self.root.destroy()
        self.parent_root.deiconify()

    # ------------------ MANAGE TUTORS VIEW ------------------
    def load_manage_tutors(self):
        self.highlight_nav(self.btn_tutors)
        self.clear_content()
        
        # Frame Title
        header_frame = Frame(self.content_frame, bg=self.content_bg, padx=30, pady=25)
        header_frame.pack(fill="x")
        
        Label(header_frame, text="Manage Tutors", font=("Helvetica", 22, "bold"), fg=self.text_dark, bg=self.content_bg).pack(side="left")
        
        # Search panel
        search_frame = Frame(self.content_frame, bg=self.content_bg, padx=30)
        search_frame.pack(fill="x", pady=(0, 15))
        
        Label(search_frame, text="Search Tutors:", font=("Helvetica", 10, "bold"), fg=self.text_dark, bg=self.content_bg).pack(side="left", padx=(0, 10))
        
        self.tutor_search_val = StringVar()
        search_entry = Entry(
            search_frame, 
            textvariable=self.tutor_search_val, 
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
        search_entry.bind("<Return>", lambda e: self.search_tutors())
        
        Label(search_frame, text="Filter by:", font=("Helvetica", 10), fg=self.text_dark, bg=self.content_bg).pack(side="left", padx=(15, 5))
        self.tutor_filter_col = StringVar(value="Name")
        filter_box = ttk.Combobox(search_frame, textvariable=self.tutor_filter_col, values=["Name", "City", "Subject", "Status"], state="readonly", width=12, font=("Helvetica", 10))
        filter_box.pack(side="left", padx=5)
        
        btn_search = Button(search_frame, text="Search", bg=self.accent_color, fg="#3d200f", font=("Helvetica", 10, "bold"), bd=0, padx=15, cursor="hand2", command=self.search_tutors)
        btn_search.pack(side="left", padx=5, ipady=3)
        self.bind_hover(btn_search, self.accent_color, self.accent_hover)
        
        btn_clear = Button(search_frame, text="Reset", bg=self.danger_color, fg=self.text_light, font=("Helvetica", 10, "bold"), bd=0, padx=15, cursor="hand2", command=self.fetch_tutors)
        btn_clear.pack(side="left", padx=5, ipady=3)
        self.bind_hover(btn_clear, self.danger_color, self.danger_hover)
        
        # Table Container
        table_frame = Frame(self.content_frame, bg=self.content_bg, bd=0, padx=30)
        table_frame.pack(fill="both", expand=True, pady=10)
        
        # Scrollbars
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        
        # Treeview setup
        cols = ("ID", "Name", "Email", "Phone", "City", "Subject", "Class", "Experience", "Fees", "Mode", "Rating", "Status")
        self.tutor_tree = ttk.Treeview(
            table_frame, 
            columns=cols, 
            show="headings", 
            yscrollcommand=scroll_y.set, 
            xscrollcommand=scroll_x.set
        )
        
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        scroll_y.config(command=self.tutor_tree.yview)
        scroll_x.config(command=self.tutor_tree.xview)
        
        # Headings and column widths
        widths = {
            "ID": 40, "Name": 120, "Email": 160, "Phone": 100, "City": 80, 
            "Subject": 100, "Class": 80, "Experience": 80, "Fees": 70, 
            "Mode": 80, "Rating": 60, "Status": 90
        }
        
        for col in cols:
            self.tutor_tree.heading(col, text=col)
            self.tutor_tree.column(col, width=widths.get(col, 100), anchor="center")
            
        self.tutor_tree.pack(fill="both", expand=True)
        
        # Style treeview a bit
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
        
        # Actions Panel
        actions_frame = Frame(self.content_frame, bg=self.content_bg, padx=30, pady=20)
        actions_frame.pack(fill="x")
        
        btn_action_style = {
            "font": ("Helvetica", 11, "bold"),
            "bd": 0,
            "padx": 20,
            "pady": 8,
            "cursor": "hand2"
        }
        
        btn_approve = Button(actions_frame, text="✓ Approve Tutor", bg=self.success_color, fg="#3d200f", command=self.approve_tutor, **btn_action_style)
        btn_approve.pack(side="left", padx=(0, 15))
        btn_approve.bind("<Enter>", lambda e: btn_approve.config(bg=self.success_hover))
        btn_approve.bind("<Leave>", lambda e: btn_approve.config(bg=self.success_color))
        
        btn_update = Button(actions_frame, text="✏️ Update Details", bg=self.accent_color, fg="#3d200f", command=self.update_tutor_dialog, **btn_action_style)
        btn_update.pack(side="left", padx=15)
        btn_update.bind("<Enter>", lambda e: btn_update.config(bg=self.accent_hover))
        btn_update.bind("<Leave>", lambda e: btn_update.config(bg=self.accent_color))
        
        btn_delete = Button(actions_frame, text="🗑️ Delete Profile", bg=self.danger_color, fg=self.text_light, command=self.delete_tutor, **btn_action_style)
        btn_delete.pack(side="left", padx=15)
        btn_delete.bind("<Enter>", lambda e: btn_delete.config(bg=self.danger_hover))
        btn_delete.bind("<Leave>", lambda e: btn_delete.config(bg=self.danger_color))
        
        btn_feedback = Button(actions_frame, text="💬 View Feedback", bg=self.accent_color, fg="#3d200f", command=self.view_tutor_feedback, **btn_action_style)
        btn_feedback.pack(side="left", padx=15)
        btn_feedback.bind("<Enter>", lambda e: btn_feedback.config(bg=self.accent_hover))
        btn_feedback.bind("<Leave>", lambda e: btn_feedback.config(bg=self.accent_color))
        
        # Load data
        self.fetch_tutors()

    def fetch_tutors(self):
        self.tutor_search_val.set("")
        self.tutor_tree.delete(*self.tutor_tree.get_children())
        
        conn = get_connection()
        if conn is None:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT tutor_id, name, email, phone, city, subject_name, class_name, experience, fees, mode, rating, status FROM tutors ORDER BY tutor_id DESC")
            rows = cursor.fetchall()
            for row in rows:
                # Format Rating display
                row_list = list(row)
                row_list[10] = f"{row[10]:.1f} ⭐" if row[10] is not None else "0.0 ⭐"
                self.tutor_tree.insert("", "end", values=row_list)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch tutors: {e}")

    def search_tutors(self):
        query_val = self.tutor_search_val.get().strip()
        filter_col = self.tutor_filter_col.get()
        
        if not query_val:
            self.fetch_tutors()
            return
            
        # Map filter header to SQL column names
        col_map = {
            "Name": "name",
            "City": "city",
            "Subject": "subject_name",
            "Status": "status"
        }
        
        db_col = col_map.get(filter_col, "name")
        
        self.tutor_tree.delete(*self.tutor_tree.get_children())
        
        conn = get_connection()
        if conn is None:
            return
            
        try:
            cursor = conn.cursor()
            query = f"SELECT tutor_id, name, email, phone, city, subject_name, class_name, experience, fees, mode, rating, status FROM tutors WHERE {db_col} LIKE %s ORDER BY tutor_id DESC"
            cursor.execute(query, (f"%{query_val}%",))
            rows = cursor.fetchall()
            for row in rows:
                row_list = list(row)
                row_list[10] = f"{row[10]:.1f} ⭐" if row[10] is not None else "0.0 ⭐"
                self.tutor_tree.insert("", "end", values=row_list)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")

    def approve_tutor(self):
        selected = self.tutor_tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a tutor profile to approve.")
            return
            
        tutor_data = self.tutor_tree.item(selected[0], "values")
        tutor_id = tutor_data[0]
        tutor_name = tutor_data[1]
        
        conn = get_connection()
        if conn is None:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE tutors SET status = 'Approved' WHERE tutor_id = %s", (tutor_id,))
            conn.commit()
            cursor.close()
            conn.close()
            
            messagebox.showinfo("Success", f"Tutor {tutor_name} approved successfully.")
            self.fetch_tutors()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to approve tutor: {e}")

    def delete_tutor(self):
        selected = self.tutor_tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a tutor profile to delete.")
            return
            
        tutor_data = self.tutor_tree.item(selected[0], "values")
        tutor_id = tutor_data[0]
        tutor_name = tutor_data[1]
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to permanently delete tutor {tutor_name}?")
        if not confirm:
            return
            
        conn = get_connection()
        if conn is None:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tutors WHERE tutor_id = %s", (tutor_id,))
            conn.commit()
            cursor.close()
            conn.close()
            
            messagebox.showinfo("Success", "Tutor profile deleted.")
            self.fetch_tutors()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete tutor: {e}")

    def update_tutor_dialog(self):
        selected = self.tutor_tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a tutor profile to update.")
            return
            
        tutor_data = self.tutor_tree.item(selected[0], "values")
        tutor_id = tutor_data[0]
        
        # Fetch current details from DB to make sure we have accurate, up-to-date values
        conn = get_connection()
        if conn is None:
            return
            
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tutors WHERE tutor_id = %s", (tutor_id,))
        t = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not t:
            messagebox.showerror("Error", "Could not retrieve tutor details.")
            return
            
        # Open Toplevel Update Window
        edit_win = Toplevel(self.root)
        edit_win.title(f"Update Tutor - {t['name']}")
        edit_win.geometry("550x600")
        edit_win.resizable(False, False)
        edit_win.configure(bg="#3d200f")
        
        Label(edit_win, text=f"Update profile for {t['name']}", font=("Helvetica", 16, "bold"), fg=self.accent_color, bg="#3d200f").pack(pady=20)
        
        form_frame = Frame(edit_win, bg="#755e52", padx=25, pady=25)
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Grid fields
        labels = [
            ("Phone", "phone"), ("City", "city"), ("Qualification", "qualification"),
            ("Experience (yrs)", "experience"), ("Subject", "subject_name"),
            ("Class", "class_name"), ("Mode (Online/Offline)", "mode"), ("Fees ($)", "fees")
        ]
        
        entries = {}
        for idx, (label_text, db_key) in enumerate(labels):
            Label(form_frame, text=label_text, font=("Helvetica", 10, "bold"), fg=self.text_light, bg="#755e52").grid(row=idx, column=0, sticky="w", pady=6, padx=(0, 15))
            val = t[db_key] if t[db_key] is not None else ""
            ent = Entry(form_frame, font=("Helvetica", 10), width=30, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
            ent.insert(0, str(val))
            ent.grid(row=idx, column=1, pady=6)
            entries[db_key] = ent
            
        def save_changes():
            # Basic validation
            phone_val = entries["phone"].get().strip()
            city_val = entries["city"].get().strip()
            qual_val = entries["qualification"].get().strip()
            exp_val = entries["experience"].get().strip()
            sub_val = entries["subject_name"].get().strip()
            cls_val = entries["class_name"].get().strip()
            mode_val = entries["mode"].get().strip()
            fees_val = entries["fees"].get().strip()
            
            if not phone_val or not city_val or not qual_val or not exp_val or not sub_val or not cls_val or not mode_val or not fees_val:
                messagebox.showerror("Error", "All fields are required!", parent=edit_win)
                return
                
            try:
                exp_int = int(exp_val)
                fees_float = float(fees_val)
            except ValueError:
                messagebox.showerror("Error", "Experience must be integer & Fees must be numeric!", parent=edit_win)
                return
                
            db_conn = get_connection()
            if db_conn is None:
                return
                
            try:
                db_cursor = db_conn.cursor()
                query = """
                UPDATE tutors 
                SET phone=%s, city=%s, qualification=%s, experience=%s, subject_name=%s, class_name=%s, mode=%s, fees=%s 
                WHERE tutor_id=%s
                """
                db_cursor.execute(query, (phone_val, city_val, qual_val, exp_int, sub_val, cls_val, mode_val, fees_float, tutor_id))
                db_conn.commit()
                db_cursor.close()
                db_conn.close()
                
                messagebox.showinfo("Success", "Tutor profile updated successfully.", parent=edit_win)
                edit_win.destroy()
                self.fetch_tutors()
            except Exception as ex:
                messagebox.showerror("Error", f"Failed to save changes: {ex}", parent=edit_win)
                
        # Save & Cancel Buttons
        btn_save = Button(form_frame, text="Save Updates", font=("Helvetica", 11, "bold"), bg=self.success_color, fg="#3d200f", bd=0, padx=20, pady=5, cursor="hand2", command=save_changes)
        btn_save.grid(row=len(labels), column=0, columnspan=2, pady=(20, 5), sticky="we")
        btn_save.bind("<Enter>", lambda e: btn_save.config(bg=self.success_hover))
        btn_save.bind("<Leave>", lambda e: btn_save.config(bg=self.success_color))
        
        btn_cancel = Button(form_frame, text="Cancel", font=("Helvetica", 11, "bold"), bg=self.danger_color, fg=self.text_light, bd=0, padx=20, pady=5, cursor="hand2", command=edit_win.destroy)
        btn_cancel.grid(row=len(labels)+1, column=0, columnspan=2, pady=5, sticky="we")
        btn_cancel.bind("<Enter>", lambda e: btn_cancel.config(bg=self.danger_hover))
        btn_cancel.bind("<Leave>", lambda e: btn_cancel.config(bg=self.danger_color))

    # ------------------ MANAGE STUDENTS NAVIGATION ------------------
    def load_manage_students(self):
        self.highlight_nav(self.btn_students)
        self.clear_content()
        
        # Load from manage_students module dynamically
        try:
            from TutorBridge.admin.manage_students import load_students_frame
            load_students_frame(self.content_frame, self.content_bg, self.text_dark, self.accent_color, self.accent_hover, self.danger_color, self.danger_hover)
        except ImportError:
            from admin.manage_students import load_students_frame
            load_students_frame(self.content_frame, self.content_bg, self.text_dark, self.accent_color, self.accent_hover, self.danger_color, self.danger_hover)

    # ------------------ REPORTS NAVIGATION ------------------
    def load_reports(self):
        self.highlight_nav(self.btn_reports)
        self.clear_content()
        
        # Load from reports module dynamically
        try:
            from TutorBridge.admin.reports import load_reports_frame
            load_reports_frame(self.content_frame, self.content_bg, self.text_dark, self.accent_color, self.accent_hover)
        except ImportError:
            from admin.reports import load_reports_frame
            load_reports_frame(self.content_frame, self.content_bg, self.text_dark, self.accent_color, self.accent_hover)

    def load_profile(self):
        self.highlight_nav(self.btn_profile)
        self.clear_content()
        
        # Header
        header_frame = Frame(self.content_frame, bg=self.content_bg, padx=30, pady=25)
        header_frame.pack(fill="x")
        Label(header_frame, text="My Profile", font=("Helvetica", 22, "bold"), fg=self.text_dark, bg=self.content_bg).pack(side="left")
        
        # Details container
        details_frame = Frame(self.content_frame, bg=self.content_bg, padx=30)
        details_frame.pack(fill="both", expand=True)
        
        card = Frame(details_frame, bg="#bba690", padx=30, pady=30)
        card.pack(anchor="nw", pady=(10, 0))
        
        Label(card, text="ADMIN INFORMATION", font=("Helvetica", 12, "bold"), fg=self.text_dark, bg="#bba690").pack(anchor="w", pady=(0, 20))
        
        # Username Detail
        user_detail_frame = Frame(card, bg="#bba690")
        user_detail_frame.pack(fill="x", pady=5)
        Label(user_detail_frame, text="Username:", font=("Helvetica", 10, "bold"), fg=self.text_dark, bg="#bba690").pack(side="left")
        Label(user_detail_frame, text=self.username, font=("Helvetica", 10), fg=self.text_dark, bg="#bba690").pack(side="left", padx=10)
        
        # Role Detail
        role_detail_frame = Frame(card, bg="#bba690")
        role_detail_frame.pack(fill="x", pady=5)
        Label(role_detail_frame, text="Role Status:", font=("Helvetica", 10, "bold"), fg=self.text_dark, bg="#bba690").pack(side="left")
        Label(role_detail_frame, text="System Administrator", font=("Helvetica", 10), fg=self.text_dark, bg="#bba690").pack(side="left", padx=10)
        
        # Update Profile Button
        btn_update = Button(
            card,
            text="Update Profile",
            font=("Helvetica", 10, "bold"),
            bg=self.accent_color,
            fg="#3d200f",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.load_update_profile
        )
        btn_update.pack(anchor="w", pady=(30, 0))
        self.bind_hover(btn_update, self.accent_color, self.accent_hover)

    def load_update_profile(self):
        self.clear_content()
        
        # Header
        header_frame = Frame(self.content_frame, bg=self.content_bg, padx=30, pady=25)
        header_frame.pack(fill="x")
        Label(header_frame, text="Update Profile", font=("Helvetica", 22, "bold"), fg=self.text_dark, bg=self.content_bg).pack(side="left")
        
        # Form Container
        form_frame = Frame(self.content_frame, bg=self.content_bg, padx=30)
        form_frame.pack(fill="both", expand=True)
        
        card = Frame(form_frame, bg="#bba690", padx=30, pady=25)
        card.pack(anchor="nw", pady=(10, 0))
        
        Label(card, text="CHANGE ADMIN PASSWORD", font=("Helvetica", 11, "bold"), fg=self.text_dark, bg="#bba690").pack(anchor="w", pady=(0, 15))
        
        Label(card, text="Current Password", font=("Helvetica", 10, "bold"), fg=self.text_dark, bg="#bba690").pack(anchor="w", pady=(0, 2))
        old_pass_ent = Entry(card, show="*", font=("Helvetica", 10), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
        old_pass_ent.pack(fill="x", ipady=4, pady=(0, 12))
        old_pass_ent.focus()
        
        Label(card, text="New Password", font=("Helvetica", 10, "bold"), fg=self.text_dark, bg="#bba690").pack(anchor="w", pady=(0, 2))
        new_pass_ent = Entry(card, show="*", font=("Helvetica", 10), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
        new_pass_ent.pack(fill="x", ipady=4, pady=(0, 12))
        
        Label(card, text="Confirm New Password", font=("Helvetica", 10, "bold"), fg=self.text_dark, bg="#bba690").pack(anchor="w", pady=(0, 2))
        conf_pass_ent = Entry(card, show="*", font=("Helvetica", 10), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
        conf_pass_ent.pack(fill="x", ipady=4, pady=(0, 15))
        
        # Action Buttons
        btn_frame = Frame(card, bg="#bba690")
        btn_frame.pack(fill="x", pady=(15, 0))
        
        def submit_admin_password():
            old_p = old_pass_ent.get().strip()
            new_p = new_pass_ent.get().strip()
            conf_p = conf_pass_ent.get().strip()
            
            if not (old_p and new_p and conf_p):
                messagebox.showerror("Validation Error", "All fields are required!", parent=self.root)
                return
                
            conn = get_connection()
            if conn is None:
                messagebox.showerror("Database Error", "Failed to connect to database.", parent=self.root)
                return
                
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT password FROM admin WHERE username = %s", (self.username,))
                res = cursor.fetchone()
                
                if not res or old_p != res[0]:
                    messagebox.showerror("Error", "Incorrect current password.", parent=self.root)
                    cursor.close()
                    conn.close()
                    return
                    
                if new_p != conf_p:
                    messagebox.showerror("Validation Error", "New passwords do not match.", parent=self.root)
                    cursor.close()
                    conn.close()
                    return
                    
                # Update in DB
                cursor.execute("UPDATE admin SET password = %s WHERE username = %s", (new_p, self.username))
                conn.commit()
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Success", "Admin password updated successfully!", parent=self.root)
                self.load_profile()
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to update password: {e}", parent=self.root)
                
        btn_submit = Button(
            btn_frame,
            text="Submit",
            font=("Helvetica", 10, "bold"),
            bg=self.success_color,
            fg="#3d200f",
            bd=0,
            padx=10,
            pady=6,
            cursor="hand2",
            command=submit_admin_password
        )
        btn_submit.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.bind_hover(btn_submit, self.success_color, self.success_hover)
        
        btn_cancel = Button(
            btn_frame,
            text="Cancel",
            font=("Helvetica", 10, "bold"),
            bg=self.danger_color,
            fg=self.text_light,
            bd=0,
            padx=10,
            pady=6,
            cursor="hand2",
            command=self.load_profile
        )
        btn_cancel.pack(side="right", fill="x", expand=True, padx=(5, 0))
        self.bind_hover(btn_cancel, self.danger_color, self.danger_hover)

    def view_tutor_feedback(self):
        import re
        selected = self.tutor_tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a tutor profile to view feedback.")
            return
            
        tutor_data = self.tutor_tree.item(selected[0], "values")
        tutor_id = tutor_data[0]
        tutor_name = tutor_data[1]
        
        view_win = Toplevel(self.root)
        view_win.title(f"Feedback Reviews - Tutor {tutor_name}")
        view_win.geometry("820x450")
        view_win.configure(bg=self.bg_color)
        view_win.grab_set()
        
        Label(view_win, text=f"FEEDBACK REVIEWS FOR TUTOR: {tutor_name} (ID: {tutor_id})", font=("Helvetica", 13, "bold"), fg=self.accent_color, bg=self.bg_color).pack(pady=15)
        
        table_frame = Frame(view_win, bg=self.bg_color, bd=0, padx=20)
        table_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        
        cols = ("Student Name", "Rating Given", "Course Duration", "Feedback Comment", "Date")
        fb_tree = ttk.Treeview(
            table_frame,
            columns=cols,
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        scroll_y.config(command=fb_tree.yview)
        scroll_x.config(command=fb_tree.xview)
        
        widths = {"Student Name": 120, "Rating Given": 100, "Course Duration": 200, "Feedback Comment": 250, "Date": 100}
        for col in cols:
            fb_tree.heading(col, text=col)
            fb_tree.column(col, width=widths.get(col, 150), anchor="center")
        fb_tree.pack(fill="both", expand=True)
        
        conn = get_connection()
        if conn is None:
            messagebox.showerror("Error", "Database connection failed.", parent=view_win)
            return
        try:
            cursor = conn.cursor()
            query = """
            SELECT s.name, f.rating, f.feedback, DATE_FORMAT(f.feedback_date, '%Y-%m-%d') 
            FROM feedback f 
            JOIN students s ON f.student_id = s.student_id 
            WHERE f.tutor_id = %s 
            ORDER BY f.feedback_date DESC
            """
            cursor.execute(query, (tutor_id,))
            rows = cursor.fetchall()
            for row in rows:
                rating_str = f"{row[1]} ⭐"
                feedback_text = row[2] if row[2] else ""
                
                # Parse course duration
                match = re.match(r"^\[Course Duration:\s*(.*?)\]\s*(.*)$", feedback_text)
                if match:
                    duration_str = match.group(1).strip()
                    comment_str = match.group(2).strip()
                else:
                    duration_str = "N/A"
                    comment_str = feedback_text
                
                fb_tree.insert("", "end", values=(row[0], rating_str, duration_str, comment_str, row[3]))
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to retrieve feedback: {e}", parent=view_win)
            
        btn_close = Button(
            view_win, 
            text="Close Window", 
            font=("Helvetica", 10, "bold"), 
            bg=self.danger_color, 
            fg=self.text_light, 
            bd=0, 
            padx=20, 
            pady=6, 
            cursor="hand2", 
            command=view_win.destroy
        )
        btn_close.pack(pady=(0, 15))
        btn_close.bind("<Enter>", lambda e: btn_close.config(bg=self.danger_hover))
        btn_close.bind("<Leave>", lambda e: btn_close.config(bg=self.danger_color))

    def bind_hover(self, button, normal_color, hover_color):
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))


def admin_dashboard(parent_root, username="admin"):
    root = Toplevel()
    root.resizable(False, False)
    AdminDashboard(root, parent_root, username)

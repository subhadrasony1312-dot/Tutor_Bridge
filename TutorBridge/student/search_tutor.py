import os
import sys
from tkinter import *
from tkinter import messagebox, ttk, simpledialog

# Resolve paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from TutorBridge.database import get_connection
    from TutorBridge.images_helper import load_and_resize
except ImportError:
    from database import get_connection
    from images_helper import load_and_resize

class StudentSearchDashboard:
    def __init__(self, root, parent_root, student_id):
        self.root = root
        self.parent_root = parent_root
        self.student_id = student_id
        
        self.root.title("Find Tutors - TutorBridge")
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
        self.root.protocol("WM_DELETE_WINDOW", self.logout)
        
        # Configure TTK style theme globally
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground="#c7b5a3", background="#c69d77", foreground="#3d200f", selectbackground="#755e52")
        
        self.fetch_student_name()
        self.create_sidebar_filters()
        
        # Right Side Content Container
        self.content_frame = Frame(self.root, bg=self.content_bg)
        self.content_frame.place(x=280, y=0, width=920, height=700)
        
        self.create_results_panel()
        self.search_tutors()  # Default search loads all approved tutors
        
    def fetch_student_name(self):
        self.student_name = "Student"
        conn = get_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM students WHERE student_id = %s", (self.student_id,))
                res = cursor.fetchone()
                if res:
                    self.student_name = res[0]
                cursor.close()
                conn.close()
            except Exception as e:
                print("Failed to fetch student name:", e)

    def logout(self):
        self.root.destroy()
        self.parent_root.deiconify()

    def create_sidebar_filters(self):
        sidebar = Frame(self.root, bg=self.sidebar_color, width=280, height=700)
        sidebar.place(x=0, y=0, width=280, height=700)
        
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
        btn_back.pack(pady=(12, 0), padx=10)
        btn_back.bind("<Enter>", lambda e: btn_back.config(bg=self.accent_color, fg="#3d200f"))
        btn_back.bind("<Leave>", lambda e: btn_back.config(bg=self.sidebar_color, fg=self.text_light))
        
        Label(
            sidebar, 
            text="TutorBridge", 
            font=("Helvetica", 20, "bold"), 
            fg=self.accent_color, 
            bg=self.sidebar_color
        ).pack(pady=(30, 5))
        
        Label(
            sidebar, 
            text="Student Dashboard", 
            font=("Helvetica", 9, "italic"), 
            fg=self.text_muted, 
            bg=self.sidebar_color
        ).pack(pady=(0, 30))
        
        # Filters Form Frame
        form_frame = Frame(sidebar, bg=self.sidebar_color, padx=20)
        form_frame.pack(fill="x")
        
        lbl_style = {"font": ("Helvetica", 10, "bold"), "fg": self.text_light, "bg": self.sidebar_color}
        ent_style = {"font": ("Helvetica", 10), "bg": "#c7b5a3", "fg": "#3d200f", "insertbackground": "#3d200f", "bd": 0}
        
        # City Filter
        Label(form_frame, text="City Location", **lbl_style).pack(anchor="w", pady=(0, 4))
        cities_list = ["All Cities", "Bhubaneswar", "Cuttack", "Rourkela", "Sambalpur", "Puri", "Balasore", "Berhampur", "Baripada", "Bhadrak", "Jharsuguda"]
        self.city_filter = ttk.Combobox(form_frame, values=cities_list, state="readonly", font=("Helvetica", 10))
        self.city_filter.set("All Cities")
        self.city_filter.pack(fill="x", ipady=2, pady=(0, 15))
        
        # Subject Filter
        Label(form_frame, text="Subject Name", **lbl_style).pack(anchor="w", pady=(0, 4))
        subjects_list = [
            "All Subjects", "Mathematics", "English", "Odia", "Political Science", "Physics", 
            "Chemistry", "Biology", "History", "Geography", "Computer Science", 
            "Economics", "Sanskrit", "Hindi", "Accountancy", "Business Studies"
        ]
        self.subject_filter = ttk.Combobox(form_frame, values=subjects_list, state="readonly", font=("Helvetica", 10))
        self.subject_filter.set("All Subjects")
        self.subject_filter.pack(fill="x", ipady=2, pady=(0, 15))
        
        # Class Filter
        Label(form_frame, text="Class / Grade", **lbl_style).pack(anchor="w", pady=(0, 4))
        classes_list = [
            "All Classes", "1st Class", "2nd Class", "3rd Class", "4th Class", "5th Class", 
            "6th Class", "7th Class", "8th Class", "9th Class", "10th Class", "11th Class", 
            "12th Class", "B.Sc", "B.A", "B.Com", "B.Tech", "BCA", "BBA", "B.Ed"
        ]
        self.class_filter = ttk.Combobox(form_frame, values=classes_list, state="readonly", font=("Helvetica", 10))
        self.class_filter.set("All Classes")
        self.class_filter.pack(fill="x", ipady=2, pady=(0, 15))
        
        # Mode Filter
        Label(form_frame, text="Teaching Mode", **lbl_style).pack(anchor="w", pady=(0, 4))
        self.mode_filter_var = StringVar(value="All Modes")
        mode_box = ttk.Combobox(
            form_frame, 
            textvariable=self.mode_filter_var, 
            values=["All Modes", "Online", "Offline", "Hybrid"], 
            state="readonly", 
            font=("Helvetica", 10)
        )
        mode_box.pack(fill="x", ipady=2, pady=(0, 20))
        
        # Filter Buttons
        btn_search = Button(
            sidebar, 
            text="🔍  Search Tutors", 
            font=("Helvetica", 11, "bold"),
            fg="#3d200f",
            bg=self.accent_color,
            bd=0,
            height=2,
            cursor="hand2",
            command=self.search_tutors
        )
        btn_search.pack(fill="x", padx=20, pady=10)
        btn_search.bind("<Enter>", lambda e: btn_search.config(bg=self.accent_hover))
        btn_search.bind("<Leave>", lambda e: btn_search.config(bg=self.accent_color))
        
        # Feedback Button
        btn_feedback = Button(
            sidebar, 
            text="📝  Submit Feedback", 
            font=("Helvetica", 11, "bold"),
            fg="#3d200f",
            bg=self.accent_color,
            bd=0,
            height=2,
            cursor="hand2",
            command=self.submit_feedback_clicked
        )
        btn_feedback.pack(fill="x", padx=20, pady=10)
        btn_feedback.bind("<Enter>", lambda e: btn_feedback.config(bg=self.accent_hover))
        btn_feedback.bind("<Leave>", lambda e: btn_feedback.config(bg=self.accent_color))
        
        # View Profile Button
        btn_profile = Button(
            sidebar, 
            text="👤  View Profile", 
            font=("Helvetica", 11, "bold"),
            fg="#3d200f",
            bg=self.accent_color,
            bd=0,
            height=2,
            cursor="hand2",
            command=self.view_profile_clicked
        )
        btn_profile.pack(fill="x", padx=20, pady=10)
        btn_profile.bind("<Enter>", lambda e: btn_profile.config(bg=self.accent_hover))
        btn_profile.bind("<Leave>", lambda e: btn_profile.config(bg=self.accent_color))
        
        btn_reset = Button(
            sidebar, 
            text="🔄  Reset Filters", 
            font=("Helvetica", 11, "bold"),
            fg=self.text_light,
            bg=self.danger_color,
            bd=0,
            height=2,
            cursor="hand2",
            command=self.reset_filters
        )
        btn_reset.pack(fill="x", padx=20, pady=5)
        btn_reset.bind("<Enter>", lambda e: btn_reset.config(bg=self.danger_hover))
        btn_reset.bind("<Leave>", lambda e: btn_reset.config(bg=self.danger_color))
        
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
        btn_logout.pack(side="bottom", fill="x", pady=25)
        btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg=self.danger_hover))
        btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg=self.danger_color))

    def reset_filters(self):
        self.city_filter.set("All Cities")
        self.subject_filter.set("All Subjects")
        self.class_filter.set("All Classes")
        self.mode_filter_var.set("All Modes")
        self.search_tutors()

    def create_results_panel(self):
        # Top welcome text
        welcome_frame = Frame(self.content_frame, bg=self.content_bg, padx=30, pady=20)
        welcome_frame.pack(fill="x")
        
        Label(
            welcome_frame, 
            text=f"Welcome, {self.student_name} 👋", 
            font=("Helvetica", 20, "bold"), 
            fg=self.text_dark, 
            bg=self.content_bg
        ).pack(anchor="w")
        
        Label(
            welcome_frame, 
            text="Find and connect with verified, expert tutors in your new city.", 
            font=("Helvetica", 10), 
            fg="#755e52", 
            bg=self.content_bg
        ).pack(anchor="w", pady=(3, 0))
        
        # Scrollable container for cards
        self.results_container = Frame(self.content_frame, bg=self.content_bg)
        self.results_container.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        self.canvas = Canvas(self.results_container, bg=self.content_bg, highlightthickness=0, bd=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.scrollbar = Scrollbar(self.results_container, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollable_frame = Frame(self.canvas, bg=self.content_bg)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        def _configure_window(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
            
        self.canvas.bind("<Configure>", _configure_window)
        
        # Bind mousewheel scrolling only when hovering the results list
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            
        def _bind_wheel(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
        def _unbind_wheel(event):
            self.canvas.unbind_all("<MouseWheel>")
            
        self.canvas.bind("<Enter>", _bind_wheel)
        self.canvas.bind("<Leave>", _unbind_wheel)

    def search_tutors(self):
        # Fetch filter arguments
        city = self.city_filter.get().strip()
        subject = self.subject_filter.get().strip()
        cls_val = self.class_filter.get().strip()
        mode = self.mode_filter_var.get()
        
        # Clear old card widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        conn = get_connection()
        if conn is None:
            return
            
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Construct dynamic query
            # We ONLY search for APPROVED tutors
            query = """
            SELECT tutor_id, name, subject_name, city, experience, fees, mode, rating, profile_pic, class_name 
            FROM tutors 
            WHERE status = 'Approved'
            """
            params = []
            
            if city and city != "All Cities":
                query += " AND city LIKE %s"
                params.append(f"%{city}%")
            if subject and subject != "All Subjects":
                query += " AND subject_name LIKE %s"
                params.append(f"%{subject}%")
            if cls_val and cls_val != "All Classes":
                query += " AND class_name LIKE %s"
                params.append(f"%{cls_val}%")
            if mode != "All Modes":
                query += " AND mode = %s"
                params.append(mode)
                
            query += " ORDER BY rating DESC, tutor_id DESC"
            
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            
            if not rows:
                lbl_no_results = Label(self.scrollable_frame, text="No approved tutors found matching filters.", font=("Helvetica", 12, "italic"), fg="#755e52", bg=self.content_bg)
                lbl_no_results.pack(pady=40)
                cursor.close()
                conn.close()
                return

            self.image_refs = []
            
            for row in rows:
                tutor_id = row['tutor_id']
                name = row['name']
                subject = row['subject_name']
                class_name = row['class_name']
                city = row['city']
                experience = row['experience']
                fees = row['fees']
                mode = row['mode']
                rating = row['rating']
                profile_pic = row['profile_pic'] if row['profile_pic'] else 'tutor1pic.jpeg'
                
                # Card frame
                card = Frame(self.scrollable_frame, bg="#bba690", bd=0)
                card.pack(fill="x", pady=8, padx=15)
                
                card_inner = Frame(card, bg="#bba690", padx=15, pady=15)
                card_inner.pack(fill="both", expand=True)
                
                # Left image (tutor profile picture instead of tutor id)
                pic_frame = Frame(card_inner, bg="#bba690")
                pic_frame.pack(side="left", padx=(0, 20))
                
                img_ref = load_and_resize(profile_pic, 90, 90)
                if not img_ref:
                    img_ref = load_and_resize("tutor1pic.jpeg", 90, 90)
                    
                if img_ref:
                    self.image_refs.append(img_ref)
                    lbl_pic = Label(pic_frame, image=img_ref, bg="#bba690")
                    lbl_pic.image = img_ref
                    lbl_pic.pack()
                else:
                    lbl_pic = Label(pic_frame, text="No Pic", font=("Helvetica", 9), bg="#8d7865", fg="#c7b5a3", width=12, height=6)
                    lbl_pic.pack()
                    
                # Center details
                details_frame = Frame(card_inner, bg="#bba690")
                details_frame.pack(side="left", fill="both", expand=True)
                
                lbl_name = Label(details_frame, text=f"{name} (ID: {tutor_id})", font=("Helvetica", 13, "bold"), fg=self.text_dark, bg="#bba690")
                lbl_name.pack(anchor="w", pady=(0, 2))
                
                lbl_sub = Label(details_frame, text=f"{subject} classes ({class_name})", font=("Helvetica", 10, "bold"), fg=self.text_dark, bg="#bba690")
                lbl_sub.pack(anchor="w", pady=(0, 4))
                
                # Rating stars display
                rating_val = rating if rating is not None else 0.0
                stars_count = int(round(rating_val))
                stars_str = "⭐" * stars_count + "☆" * (5 - stars_count)
                lbl_rating = Label(details_frame, text=f"{stars_str}  ({rating_val:.1f} rating)", font=("Helvetica", 10), fg=self.text_dark, bg="#bba690")
                lbl_rating.pack(anchor="w", pady=(0, 6))
                
                lbl_info = Label(
                    details_frame, 
                    text=f"📍 {city}   •   💼 {experience} Years Exp   •   💻 {mode} Mode   •   💵 ${fees:.2f}/mo", 
                    font=("Helvetica", 9), 
                    fg="#3d200f", 
                    bg="#bba690"
                )
                lbl_info.pack(anchor="w")
                
                # Right action button
                action_frame = Frame(card_inner, bg="#bba690")
                action_frame.pack(side="right", padx=(10, 0), fill="y")
                
                lbl_spacer = Label(action_frame, text="", bg="#bba690")
                lbl_spacer.pack(pady=4)
                
                btn_view = Button(
                    action_frame,
                    text="View Profile / Review",
                    font=("Helvetica", 9, "bold"),
                    bg=self.success_color,
                    fg="#3d200f",
                    bd=0,
                    padx=12,
                    pady=6,
                    cursor="hand2",
                    command=lambda tid=tutor_id: self.view_tutor_profile(tid)
                )
                btn_view.pack()
                
                def _make_hover(b, nc, hc):
                    b.bind("<Enter>", lambda e, button=b, color=hc: button.config(bg=color))
                    b.bind("<Leave>", lambda e, button=b, color=nc: button.config(bg=color))
                    
                _make_hover(btn_view, self.success_color, self.success_hover)
                
            cursor.close()
            conn.close()
            
            # Reset canvas scrolling region to include new contents
            self.canvas.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to execute tutor search: {e}", parent=self.root)

    def view_tutor_profile(self, tutor_id):
        # Open view tutor profile window
        try:
            from TutorBridge.student.view_tutor import view_tutor_details_dialog
            view_tutor_details_dialog(self.root, tutor_id, self.student_id, self.search_tutors)
        except ImportError:
            from student.view_tutor import view_tutor_details_dialog
            view_tutor_details_dialog(self.root, tutor_id, self.student_id, self.search_tutors)

    def view_profile_clicked(self):
        # Fetch student info from database
        conn = get_connection()
        if conn is None:
            messagebox.showerror("Error", "Database connection failed.", parent=self.root)
            return
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT name, email, phone, city, password FROM students WHERE student_id = %s", (self.student_id,))
            student_info = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if not student_info:
                messagebox.showerror("Error", "Student profile not found.", parent=self.root)
                return
                
            self.show_profile_dialog(student_info)
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}", parent=self.root)

    def show_profile_dialog(self, student_info):
        dialog = Toplevel(self.root)
        dialog.title("My Profile - TutorBridge")
        dialog.geometry("450x450")
        dialog.resizable(False, False)
        dialog.configure(bg=self.bg_color)
        dialog.grab_set()
        
        # Design Palette matching the dashboard
        card_color = "#755e52"
        text_color = "#c7b5a3"
        accent_color = "#c69d77"
        accent_hover = "#b0977c"
        success_color = "#a87a64"
        success_hover = "#8d7865"
        danger_color = "#734022"
        danger_hover = "#725237"
        
        main_frame = Frame(dialog, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True)
        
        def render_view_state():
            # Clear main_frame
            for w in main_frame.winfo_children():
                w.destroy()
                
            Label(main_frame, text="STUDENT PROFILE", font=("Helvetica", 16, "bold"), fg=accent_color, bg=self.bg_color).pack(pady=(20, 10))
            
            card = Frame(main_frame, bg=card_color, padx=20, pady=20)
            card.pack(fill="both", expand=True, padx=25, pady=(0, 20))
            
            # Helper to draw fields
            def draw_field(lbl, val):
                f_frame = Frame(card, bg=card_color)
                f_frame.pack(fill="x", pady=6)
                Label(f_frame, text=lbl, font=("Helvetica", 10, "bold"), fg=accent_color, bg=card_color).pack(side="left")
                Label(f_frame, text=val, font=("Helvetica", 11), fg=text_color, bg=card_color).pack(side="left", padx=10)
                
            draw_field("Full Name:", student_info["name"])
            draw_field("Email ID:", student_info["email"])
            draw_field("Phone No:", student_info["phone"])
            draw_field("City Location:", student_info["city"])
            
            # Action Buttons
            btn_frame = Frame(card, bg=card_color)
            btn_frame.pack(fill="x", side="bottom", pady=(15, 0))
            
            def bind_hover(button, normal_color, hover_color):
                button.bind("<Enter>", lambda e: button.config(bg=hover_color))
                button.bind("<Leave>", lambda e: button.config(bg=normal_color))
                
            btn_update = Button(
                btn_frame,
                text="Update Profile",
                font=("Helvetica", 10, "bold"),
                bg=success_color,
                fg="#3d200f",
                bd=0,
                padx=10,
                pady=6,
                cursor="hand2",
                command=render_update_state
            )
            btn_update.pack(side="left", fill="x", expand=True, padx=(0, 5))
            bind_hover(btn_update, success_color, success_hover)
            
            btn_close = Button(
                btn_frame,
                text="Close",
                font=("Helvetica", 10, "bold"),
                bg=danger_color,
                fg=text_color,
                bd=0,
                padx=10,
                pady=6,
                cursor="hand2",
                command=dialog.destroy
            )
            btn_close.pack(side="right", fill="x", expand=True, padx=(5, 0))
            bind_hover(btn_close, danger_color, danger_hover)
            
        def render_update_state():
            # Clear main_frame
            for w in main_frame.winfo_children():
                w.destroy()
                
            Label(main_frame, text="CHANGE PASSWORD", font=("Helvetica", 16, "bold"), fg=accent_color, bg=self.bg_color).pack(pady=(20, 10))
            
            card = Frame(main_frame, bg=card_color, padx=20, pady=15)
            card.pack(fill="both", expand=True, padx=25, pady=(0, 20))
            
            # Entry widgets for password change
            Label(card, text="Current Password", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 2))
            old_pass_ent = Entry(card, show="*", font=("Helvetica", 11), bg="#c7b5a3", fg="#3d200f", bd=0)
            old_pass_ent.pack(fill="x", ipady=4, pady=(0, 12))
            old_pass_ent.focus()
            
            Label(card, text="New Password", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 2))
            new_pass_ent = Entry(card, show="*", font=("Helvetica", 11), bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
            new_pass_ent.pack(fill="x", ipady=4, pady=(0, 12))
            
            Label(card, text="Confirm New Password", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 2))
            conf_pass_ent = Entry(card, show="*", font=("Helvetica", 11), bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
            conf_pass_ent.pack(fill="x", ipady=4, pady=(0, 15))
            
            # Action Buttons
            btn_frame = Frame(card, bg=card_color)
            btn_frame.pack(fill="x", side="bottom")
            
            def bind_hover(button, normal_color, hover_color):
                button.bind("<Enter>", lambda e: button.config(bg=hover_color))
                button.bind("<Leave>", lambda e: button.config(bg=normal_color))
                
            def submit_update():
                old_p = old_pass_ent.get().strip()
                new_p = new_pass_ent.get().strip()
                conf_p = conf_pass_ent.get().strip()
                
                if not (old_p and new_p and conf_p):
                    messagebox.showerror("Validation Error", "All fields are required!", parent=dialog)
                    return
                    
                if old_p != student_info["password"]:
                    messagebox.showerror("Error", "Incorrect current password.", parent=dialog)
                    return
                    
                if new_p != conf_p:
                    messagebox.showerror("Validation Error", "New passwords do not match.", parent=dialog)
                    return
                    
                # Update in DB
                conn = get_connection()
                if conn is None:
                    messagebox.showerror("Database Error", "Failed to connect to database.", parent=dialog)
                    return
                    
                try:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE students SET password = %s WHERE student_id = %s", (new_p, self.student_id))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
                    student_info["password"] = new_p  # update in memory info
                    messagebox.showinfo("Success", "Password updated successfully!", parent=dialog)
                    render_view_state()  # Go back to profile view screen
                except Exception as e:
                    messagebox.showerror("Database Error", f"Failed to update password: {e}", parent=dialog)
                    
            btn_submit = Button(
                btn_frame,
                text="Submit",
                font=("Helvetica", 10, "bold"),
                bg=success_color,
                fg="#3d200f",
                bd=0,
                padx=10,
                pady=6,
                cursor="hand2",
                command=submit_update
            )
            btn_submit.pack(side="left", fill="x", expand=True, padx=(0, 5))
            bind_hover(btn_submit, success_color, success_hover)
            
            btn_cancel = Button(
                btn_frame,
                text="Cancel",
                font=("Helvetica", 10, "bold"),
                bg=danger_color,
                fg=text_color,
                bd=0,
                padx=10,
                pady=6,
                cursor="hand2",
                command=render_view_state
            )
            btn_cancel.pack(side="right", fill="x", expand=True, padx=(5, 0))
            bind_hover(btn_cancel, danger_color, danger_hover)
            
        render_view_state()

    def submit_feedback_clicked(self):
        tutor_id = simpledialog.askinteger("Submit Feedback", "Enter Tutor ID:", parent=self.root)
        if tutor_id is None:
            return
            
        conn = get_connection()
        if conn is None:
            messagebox.showerror("Error", "Database connection failed.", parent=self.root)
            return
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT name, status FROM tutors WHERE tutor_id = %s", (tutor_id,))
            tutor = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if not tutor:
                messagebox.showerror("Invalid Tutor ID", f"No tutor found with ID: {tutor_id}", parent=self.root)
                return
            if tutor['status'] != 'Approved':
                messagebox.showerror("Not Approved", f"Tutor with ID {tutor_id} is not approved yet.", parent=self.root)
                return
                
            self.open_custom_feedback_dialog(tutor_id, tutor['name'])
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}", parent=self.root)

    def open_custom_feedback_dialog(self, tutor_id, tutor_name):
        dialog = Toplevel(self.root)
        dialog.title("Submit Feedback - TutorBridge")
        dialog.geometry("460x650")
        dialog.resizable(False, False)
        dialog.configure(bg=self.bg_color)
        dialog.grab_set()
        
        # Theme Palette
        card_color = "#755e52"
        text_color = "#2f1b07"
        accent_color = "#c69d77"
        accent_hover = "#b0977c"
        success_color = "#a87a64"
        success_hover = "#8d7865"
        danger_color = "#734022"
        danger_hover = "#725237"
        
        Label(dialog, text="SUBMIT TUTOR FEEDBACK", font=("Helvetica", 15, "bold"), fg=accent_color, bg=self.bg_color).pack(pady=20)
        
        form = Frame(dialog, bg=card_color, padx=20, pady=20)
        form.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        Label(form, text=f"Tutor Name: {tutor_name} (ID: {tutor_id})", font=("Helvetica", 11, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 10))
        
        # Course Completion Check
        Label(form, text="Have you completed this tutor's course?", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(5, 3))
        completed_var = StringVar(value="No")
        completed_box = ttk.Combobox(form, textvariable=completed_var, values=["Yes", "No"], state="readonly", font=("Helvetica", 10))
        completed_box.pack(fill="x", pady=(0, 10))
        
        # Dates frame (initially hidden, shown if "Yes" is selected)
        dates_frame = Frame(form, bg=card_color)
        
        Label(dates_frame, text="Course Start Date (dd-mm-yy)", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(5, 2))
        start_date_ent = Entry(dates_frame, font=("Helvetica", 11), bg="#c7b5a3", fg="#3d200f", bd=0)
        start_date_ent.pack(fill="x", ipady=4, pady=(0, 5))
        
        Label(dates_frame, text="Course End Date (dd-mm-yy)", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(5, 2))
        end_date_ent = Entry(dates_frame, font=("Helvetica", 11), bg="#c7b5a3", fg="#3d200f", bd=0)
        end_date_ent.pack(fill="x", ipady=4, pady=(0, 5))

        # We'll pack these elements in a specific order:
        Label(form, text="Select Feedback Level", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(5, 3))
        feedback_options = ["Excellent", "Very Good", "Good", "Poor"]
        feedback_var = StringVar(value=feedback_options[0])
        feedback_box = ttk.Combobox(form, textvariable=feedback_var, values=feedback_options, state="readonly", font=("Helvetica", 10))
        feedback_box.pack(fill="x", pady=(0, 10))
        
        Label(form, text="Write Additional Comments (Optional)", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(5, 3))
        feedback_text = Text(form, font=("Helvetica", 10), height=3, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0, wrap="word")
        feedback_text.pack(fill="both", expand=True, pady=(0, 15))
        feedback_text.focus()
        
        def on_completed_change(event):
            if completed_var.get() == "Yes":
                # Show dates frame right after completed_box
                dates_frame.pack(fill="x", after=completed_box, pady=(0, 10))
            else:
                # Hide dates frame
                dates_frame.pack_forget()
                
        completed_box.bind("<<ComboboxSelected>>", on_completed_change)

        def submit_feedback():
            import datetime
            
            if completed_var.get() == "No":
                messagebox.showerror("Validation Error", "You can only submit feedback if you have completed the tutor's course.", parent=dialog)
                return
                
            start_str = start_date_ent.get().strip()
            end_str = end_date_ent.get().strip()
            
            if not start_str or not end_str:
                messagebox.showerror("Validation Error", "Please enter start and end dates.", parent=dialog)
                return
                
            try:
                start_date = datetime.datetime.strptime(start_str, "%d-%m-%y").date()
                end_date = datetime.datetime.strptime(end_str, "%d-%m-%y").date()
            except ValueError:
                messagebox.showerror("Validation Error", "Dates must be in dd-mm-yy format (e.g. 15-02-26).", parent=dialog)
                return
                
            if end_date < start_date:
                messagebox.showerror("Validation Error", "End date cannot be before start date.", parent=dialog)
                return
                
            months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
            if end_date.day < start_date.day:
                months -= 1
            days = (end_date - start_date).days
            
            if months < 2 and days < 59:
                messagebox.showerror("Validation Error", "The course duration must be at least 2 months to submit feedback.", parent=dialog)
                return
                
            comment_val = feedback_text.get("1.0", "end-1c").strip()
            selected_feedback = feedback_var.get()
            
            rating_map = {
                "Excellent": 5,
                "Very Good": 4,
                "Good": 3,
                "Poor": 1
            }
            rating_val = rating_map.get(selected_feedback, 5)
            
            duration_str = f"[Course Duration: {start_str} to {end_str} ({months} months)]"
            if comment_val:
                db_feedback_text = f"{duration_str} {selected_feedback}: {comment_val}"
            else:
                db_feedback_text = f"{duration_str} {selected_feedback}"
                
            conn = get_connection()
            if conn is None:
                messagebox.showerror("Database Error", "Failed to connect to database.", parent=dialog)
                return
                
            try:
                cursor = conn.cursor()
                insert_query = """
                INSERT INTO feedback (student_id, tutor_id, rating, feedback) 
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (self.student_id, tutor_id, rating_val, db_feedback_text))
                conn.commit()
                
                cursor.execute("SELECT AVG(rating) FROM feedback WHERE tutor_id = %s", (tutor_id,))
                avg_rating = cursor.fetchone()[0]
                if avg_rating is not None:
                    cursor.execute("UPDATE tutors SET rating = %s WHERE tutor_id = %s", (avg_rating, tutor_id))
                    conn.commit()
                    
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Success", "Feedback submitted successfully!", parent=dialog)
                dialog.destroy()
                self.search_tutors()
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to submit feedback: {e}", parent=dialog)
                
        def bind_hover(button, normal_color, hover_color):
            button.bind("<Enter>", lambda e: button.config(bg=hover_color))
            button.bind("<Leave>", lambda e: button.config(bg=normal_color))
 
        btn_frame = Frame(form, bg=card_color)
        btn_frame.pack(fill="x", side="bottom")
        
        btn_submit = Button(
            btn_frame, 
            text="Submit Feedback", 
            font=("Helvetica", 11, "bold"), 
            bg=success_color, 
            fg="#3d200f", 
            bd=0, 
            width=18, 
            cursor="hand2", 
            command=submit_feedback
        )
        btn_submit.pack(side="left", padx=(0, 10))
        bind_hover(btn_submit, success_color, success_hover)
        
        btn_cancel = Button(
            btn_frame, 
            text="Cancel", 
            font=("Helvetica", 11, "bold"), 
            bg=danger_color, 
            fg=text_color, 
            bd=0, 
            width=12, 
            cursor="hand2", 
            command=dialog.destroy
        )
        btn_cancel.pack(side="right")
        bind_hover(btn_cancel, danger_color, danger_hover)

def student_dashboard(parent_root, student_id):
    root = Toplevel()
    StudentSearchDashboard(root, parent_root, student_id)

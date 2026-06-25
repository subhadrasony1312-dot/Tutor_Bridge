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
    from TutorBridge.images_helper import load_and_resize
except ImportError:
    from database import get_connection
    from images_helper import load_and_resize

class TutorDashboard:
    def __init__(self, root, parent_root, tutor_id):
        self.root = root
        self.parent_root = parent_root
        self.tutor_id = tutor_id
        
        self.root.title("Tutor Dashboard - TutorBridge")
        self.root.geometry("1100x650")
        self.root.resizable(False, False)
        
        # Design Theme
        self.bg_color = "#3d200f"      # Darkest chocolate brown
        self.card_color = "#755e52"    # Deep warm brown
        self.content_bg = "#c7b5a3"    # Very light grayish tan
        self.text_dark = "#3d200f"     # Darkest chocolate brown
        self.text_light = "#c7b5a3"    # Very light grayish tan
        self.text_muted = "#bba690"    # Soft grayish tan
        self.accent_color = "#c69d77"  # Light warm tan / accent
        self.accent_hover = "#b0977c"  # Light grayish tan
        self.success_color = "#a87a64" # Medium warm brown
        self.success_hover = "#8d7865" # Medium grayish brown
        self.danger_color = "#734022"  # Reddish brown
        self.danger_hover = "#725237"  # Rich brown
        
        self.root.configure(bg=self.content_bg)
        self.root.protocol("WM_DELETE_WINDOW", self.logout)
        
        # Configure TTK style theme globally
        style = ttk.Style()
        style.theme_use("clam")
        
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
        
        # Title Frame / Navbar
        self.create_navbar()
        
        # Main split container
        self.main_container = Frame(self.root, bg=self.content_bg)
        self.main_container.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Left Panel (Profile details)
        self.profile_frame = Frame(self.main_container, bg="#bba690", bd=0, padx=20, pady=10)
        self.profile_frame.place(x=0, y=0, width=450, height=525)
        
        # Right Panel (Feedbacks)
        self.feedback_frame = Frame(self.main_container, bg="#bba690", bd=0, padx=20, pady=10)
        self.feedback_frame.place(x=480, y=0, width=570, height=525)
        
        self.load_profile_details()
        self.load_feedbacks()
        
    def create_navbar(self):
        navbar = Frame(self.root, bg=self.bg_color, height=80)
        navbar.pack(fill="x")
        btn_back = Button(
            navbar,
            text="← Back",
            font=("Helvetica", 10, "bold"),
            bg=self.bg_color,
            fg=self.text_light,
            bd=0,
            padx=10,
            cursor="hand2",
            command=self.logout
        )
        btn_back.pack(side="left", padx=10, pady=20)
        btn_back.bind("<Enter>", lambda e: btn_back.config(bg=self.accent_color, fg="#3d200f"))
        btn_back.bind("<Leave>", lambda e: btn_back.config(bg=self.bg_color, fg=self.text_light))

        self.welcome_lbl = Label(
            navbar, 
            text="Tutor Dashboard", 
            font=("Helvetica", 18, "bold"), 
            fg=self.accent_color, 
            bg=self.bg_color
        )
        self.welcome_lbl.pack(side="left", padx=25, pady=20)
        
        btn_logout = Button(
            navbar, 
            text="Sign Out", 
            font=("Helvetica", 10, "bold"),
            bg=self.danger_color, 
            fg=self.text_light, 
            bd=0, 
            padx=15, 
            cursor="hand2", 
            command=self.logout
        )
        btn_logout.pack(side="right", padx=25, pady=20)
        btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg=self.danger_hover))
        btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg=self.danger_color))

    def logout(self):
        self.root.destroy()
        self.parent_root.deiconify()
        
    def load_profile_details(self):
        # Clear profile frame
        for widget in self.profile_frame.winfo_children():
            widget.destroy()
            
        conn = get_connection()
        if conn is None:
            return
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tutors WHERE tutor_id = %s", (self.tutor_id,))
            t = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if not t:
                messagebox.showerror("Error", "Failed to retrieve profile data.")
                return
                
            self.welcome_lbl.config(text=f"Welcome back, {t['name']}")
                       # Header
            header_lbl = Label(self.profile_frame, text="My Profile Information", font=("Helvetica", 15, "bold"), fg=self.text_dark, bg="#bba690")
            header_lbl.pack(anchor="w", pady=(0, 10))
            
            # Display Profile Image
            pic_name = t.get("profile_pic", "tutor1pic.jpeg")
            if not pic_name:
                pic_name = "tutor1pic.jpeg"
                
            img_ref = load_and_resize(pic_name, 80, 80)
            if not img_ref:
                img_ref = load_and_resize("tutor1pic.jpeg", 80, 80)
                
            if img_ref:
                img_frame = Frame(self.profile_frame, bg="#bba690")
                img_frame.pack(anchor="w", pady=(0, 15))
                
                lbl_img = Label(img_frame, image=img_ref, bg="#bba690")
                lbl_img.image = img_ref  # Keep reference
                lbl_img.pack()
            
            # Info Grid
            grid_frame = Frame(self.profile_frame, bg="#bba690")
            grid_frame.pack(fill="x", anchor="w")
            
            fields = [
                ("Tutor ID:", str(t.get('tutor_id', ''))),
                ("Name:", t['name']),
                ("Email:", t['email']),
                ("Phone:", t['phone']),
                ("City Location:", t['city']),
                ("Qualification:", t['qualification']),
                ("Experience:", f"{t['experience']} Years" if t['experience'] else "Not Specified"),
                ("Teaching Subject:", t['subject_name']),
                ("Target Class:", t['class_name']),
                ("Teaching Mode:", t['mode']),
                ("Monthly Fees:", f"${t['fees']:.2f}" if t['fees'] is not None else "$0.00"),
                ("Rating Status:", f"{t['rating']:.1f} ⭐" if t['rating'] is not None else "0.0 ⭐")
            ]
            
            for idx, (label, val) in enumerate(fields):
                Label(grid_frame, text=label, font=("Helvetica", 10, "bold"), fg="#3d200f", bg="#bba690").grid(row=idx, column=0, sticky="w", pady=2)
                Label(grid_frame, text=val, font=("Helvetica", 10), fg=self.text_dark, bg="#bba690").grid(row=idx, column=1, sticky="w", padx=15, pady=2)
                
            # Update Button
            btn_frame = Frame(self.profile_frame, bg="#bba690")
            btn_frame.pack(fill="x", side="bottom", pady=(15, 0))
            
            btn_update = Button(
                btn_frame, 
                text="✏️ Edit Details", 
                font=("Helvetica", 10, "bold"), 
                bg=self.accent_color, 
                fg="#3d200f", 
                bd=0, 
                pady=8, 
                cursor="hand2", 
                command=self.open_update_dialog
            )
            btn_update.pack(side="left", fill="x", expand=True, padx=(0, 4))
            btn_update.bind("<Enter>", lambda e: btn_update.config(bg=self.accent_hover))
            btn_update.bind("<Leave>", lambda e: btn_update.config(bg=self.accent_color))
            
            btn_password = Button(
                btn_frame, 
                text="Update Profile", 
                font=("Helvetica", 10, "bold"), 
                bg=self.accent_color, 
                fg="#3d200f", 
                bd=0, 
                pady=8, 
                cursor="hand2", 
                command=self.open_password_dialog
            )
            btn_password.pack(side="right", fill="x", expand=True, padx=(4, 0))
            btn_password.bind("<Enter>", lambda e: btn_password.config(bg=self.accent_hover))
            btn_password.bind("<Leave>", lambda e: btn_password.config(bg=self.accent_color))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load profile details: {e}")
 
    def load_feedbacks(self):
        import re
        # Clear feedback frame
        for widget in self.feedback_frame.winfo_children():
            widget.destroy()
        Label(self.feedback_frame, text="Parent & Student Feedback", font=("Helvetica", 15, "bold"), fg=self.text_dark, bg="#bba690").pack(anchor="w", pady=(0, 15))
        
        # Scrollbars
        scroll_y = Scrollbar(self.feedback_frame, orient=VERTICAL)
        scroll_x = Scrollbar(self.feedback_frame, orient=HORIZONTAL)
        
        cols = ("Student Name", "Rating Given", "Course Duration", "Feedback Comment", "Submission Date")
        tree = ttk.Treeview(
            self.feedback_frame, 
            columns=cols, 
            show="headings", 
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)
        
        widths = {"Student Name": 100, "Rating Given": 90, "Course Duration": 150, "Feedback Comment": 140, "Submission Date": 100}
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=widths.get(col, 100), anchor="center")
            
        tree.pack(fill="both", expand=True)
        
        conn = get_connection()
        if conn is None:
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
            cursor.execute(query, (self.tutor_id,))
            rows = cursor.fetchall()
            for r in rows:
                rating_str = f"{r[1]} ⭐"
                feedback_text = r[2] if r[2] else ""
                
                # Parse course duration
                match = re.match(r"^\[Course Duration:\s*(.*?)\]\s*(.*)$", feedback_text)
                if match:
                    duration_str = match.group(1).strip()
                    comment_str = match.group(2).strip()
                else:
                    duration_str = "N/A"
                    comment_str = feedback_text
                
                tree.insert("", "end", values=(r[0], rating_str, duration_str, comment_str, r[3]))
            cursor.close()
            conn.close()
        except Exception as e:
            print("Failed to load tutor feedback reviews:", e)

    def open_update_dialog(self):
        # Open update_profile dynamically
        try:
            from TutorBridge.tutor.update_profile import update_profile_dialog
            update_profile_dialog(self.root, self.tutor_id, self.load_profile_details)
        except ImportError:
            from tutor.update_profile import update_profile_dialog
            update_profile_dialog(self.root, self.tutor_id, self.load_profile_details)

    def open_password_dialog(self):
        # Open change password dialog modal
        dialog = Toplevel(self.root)
        dialog.title("Change Password - TutorBridge")
        dialog.geometry("450x420")
        dialog.resizable(False, False)
        dialog.configure(bg=self.bg_color)
        dialog.grab_set()
        
        # Theme Palette
        card_color = "#755e52"
        text_color = "#c7b5a3"
        accent_color = "#c69d77"
        accent_hover = "#b0977c"
        success_color = "#a87a64"
        success_hover = "#8d7865"
        danger_color = "#734022"
        danger_hover = "#725237"
        
        Label(dialog, text="CHANGE TUTOR PASSWORD", font=("Helvetica", 15, "bold"), fg=accent_color, bg=self.bg_color).pack(pady=20)
        
        form = Frame(dialog, bg=card_color, padx=20, pady=20)
        form.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        Label(form, text="Current Password", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 2))
        old_pass_ent = Entry(form, show="*", font=("Helvetica", 11), bg="#c7b5a3", fg="#3d200f", bd=0)
        old_pass_ent.pack(fill="x", ipady=4, pady=(0, 12))
        old_pass_ent.focus()
        
        Label(form, text="New Password", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 2))
        new_pass_ent = Entry(form, show="*", font=("Helvetica", 11), bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
        new_pass_ent.pack(fill="x", ipady=4, pady=(0, 12))
        
        Label(form, text="Confirm New Password", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 2))
        conf_pass_ent = Entry(form, show="*", font=("Helvetica", 11), bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
        conf_pass_ent.pack(fill="x", ipady=4, pady=(0, 20))
        
        def submit_update():
            old_p = old_pass_ent.get().strip()
            new_p = new_pass_ent.get().strip()
            conf_p = conf_pass_ent.get().strip()
            
            if not (old_p and new_p and conf_p):
                messagebox.showerror("Validation Error", "All fields are required!", parent=dialog)
                return
                
            conn = get_connection()
            if conn is None:
                messagebox.showerror("Database Error", "Failed to connect to database.", parent=dialog)
                return
                
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT password FROM tutors WHERE tutor_id = %s", (self.tutor_id,))
                res = cursor.fetchone()
                
                if not res or old_p != res[0]:
                    messagebox.showerror("Error", "Incorrect current password.", parent=dialog)
                    cursor.close()
                    conn.close()
                    return
                    
                if new_p != conf_p:
                    messagebox.showerror("Validation Error", "New passwords do not match.", parent=dialog)
                    cursor.close()
                    conn.close()
                    return
                    
                # Update in DB
                cursor.execute("UPDATE tutors SET password = %s WHERE tutor_id = %s", (new_p, self.tutor_id))
                conn.commit()
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Success", "Password updated successfully!", parent=dialog)
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to update password: {e}", parent=dialog)
                
        def bind_hover(button, normal_color, hover_color):
            button.bind("<Enter>", lambda e: button.config(bg=hover_color))
            button.bind("<Leave>", lambda e: button.config(bg=normal_color))
            
        btn_frame = Frame(form, bg=card_color)
        btn_frame.pack(fill="x", side="bottom")
        
        btn_submit = Button(
            btn_frame, 
            text="Submit", 
            font=("Helvetica", 11, "bold"), 
            bg=success_color, 
            fg="#3d200f", 
            bd=0, 
            width=18, 
            cursor="hand2", 
            command=submit_update
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

def tutor_dashboard(parent_root, tutor_id):
    root = Toplevel()
    TutorDashboard(root, parent_root, tutor_id)

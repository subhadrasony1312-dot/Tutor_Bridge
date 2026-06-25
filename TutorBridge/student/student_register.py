import os
import sys
import re
from tkinter import *
from tkinter import messagebox

# Resolve paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from TutorBridge.images_helper import setup_canvas_bg, load_and_resize
    from TutorBridge.database import get_connection
except ImportError:
    from images_helper import setup_canvas_bg, load_and_resize
    from database import get_connection

def student_register_window(parent_root):
    win = Toplevel()
    win.title("Student Registration - TutorBridge")
    win.geometry("1200x700")
    win.resizable(False, False)
    
    # Theme Palette
    bg_color = "#3d200f"      
    card_color = "#552a13"    
    text_color = "#c7b5a3"    
    text_muted = "#bba690"    # Soft grayish tan
    accent_color = "#c69d77"  # Light warm tan / accent
    accent_hover = "#b0977c"  # Light grayish tan
    success_color = "#a87a64" # Medium warm brown
    success_hover = "#8d7865" # Medium grayish brown
    danger_color = "#734022"  # Reddish brown
    danger_hover = "#725237"  # Rich brown
    
    # Background Canvas
    canvas = Canvas(win, width=1200, height=700, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    setup_canvas_bg(canvas, "student_reg_background.jpg", "#755e52", "#3d200f")
    
    def on_close():
        win.destroy()
        parent_root.deiconify()
        
    win.protocol("WM_DELETE_WINDOW", on_close)
    
    # Centered Card Frame
    card = Frame(canvas, bg=card_color, padx=40, pady=40)
    canvas.create_window(600, 350, window=card, anchor="center")
    
    # Logo inside card
    logo_ref = load_and_resize("logo.png", 60, 60)
    if logo_ref:
        lbl_logo = Label(card, image=logo_ref, bg=card_color)
        lbl_logo.image = logo_ref
        lbl_logo.pack(pady=(0, 10))
        
    # Title
    Label(card, text="STUDENT REGISTRATION", font=("Helvetica", 18, "bold"), fg=accent_color, bg=card_color).pack(pady=(0, 3))
    Label(card, text="Create a parent/student search profile", font=("Helvetica", 9), fg=text_muted, bg=card_color).pack(pady=(0, 12))
    
    # Fields
    Label(card, text="Full Name", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 2))
    name_ent = Entry(card, font=("Helvetica", 11), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    name_ent.pack(ipady=4, pady=(0, 8))
    name_ent.focus()
    
    Label(card, text="Email Id", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 2))
    email_ent = Entry(card, font=("Helvetica", 11), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    email_ent.pack(ipady=4, pady=(0, 8))
    
    Label(card, text="Password", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 2))
    pass_ent = Entry(card, show="*", font=("Helvetica", 11), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    pass_ent.pack(ipady=4, pady=(0, 8))
    
    Label(card, text="Confirm Password", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 2))
    confirm_pass_ent = Entry(card, show="*", font=("Helvetica", 11), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    confirm_pass_ent.pack(ipady=4, pady=(0, 8))
    
    Label(card, text="Phone Number", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 2))
    phone_ent = Entry(card, font=("Helvetica", 11), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    phone_ent.pack(ipady=4, pady=(0, 8))
    
    Label(card, text="Address", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 2))
    city_ent = Entry(card, font=("Helvetica", 11), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    city_ent.pack(ipady=4, pady=(0, 10))
    
    def clear_fields():
        name_ent.delete(0, END)
        email_ent.delete(0, END)
        pass_ent.delete(0, END)
        confirm_pass_ent.delete(0, END)
        phone_ent.delete(0, END)
        city_ent.delete(0, END)
        
    def register():
        name = name_ent.get().strip()
        email = email_ent.get().strip()
        password = pass_ent.get().strip()
        confirm_password = confirm_pass_ent.get().strip()
        phone = phone_ent.get().strip()
        city = city_ent.get().strip()
        
        if not (name and email and password and confirm_password and phone and city):
            messagebox.showerror("Validation Error", "All fields are required!", parent=win)
            return
            
        if password != confirm_password:
            messagebox.showerror("Validation Error", "Passwords do not match.", parent=win)
            return
            
        if email.startswith("@"):
            messagebox.showerror("Validation Error", "username cant be start with@", parent=win)
            return
            
        if not re.match(r"^[a-zA-Z0-9._%+-]{3,}@[a-zA-Z0-9.-]{3,}\.[a-zA-Z]{2,}$", email):
            messagebox.showerror("Validation Error", "Please enter a valid email address (e.g., username12@gmail.com).", parent=win)
            return
            
        if not phone.isdigit() or not (10 <= len(phone) <= 15):
            messagebox.showerror("Validation Error", "Phone number must be numeric (10-15 digits).", parent=win)
            return
            
        conn = get_connection()
        if conn is None:
            messagebox.showerror("Database Error", "Unable to connect to database.", parent=win)
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM students WHERE email=%s", (email,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Validation Error", "An account with this email already exists.", parent=win)
                cursor.close()
                conn.close()
                return
                
            query = "INSERT INTO students (name, email, password, phone, city) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (name, email, password, phone, city))
            conn.commit()
            cursor.close()
            conn.close()
            
            messagebox.showinfo("Success", "Student registration successful! You can now log in.", parent=win)
            win.destroy()
            from TutorBridge.student.student_login import student_login_window
            student_login_window(parent_root)
        except Exception as e:
            messagebox.showerror("Database Error", f"Registration failed: {e}", parent=win)
            
    # Buttons Panel
    btn_frame = Frame(card, bg=card_color)
    btn_frame.pack(fill="x", pady=(10, 0))
    
    # Hover Helper
    def bind_hover(button, normal_color, hover_color):
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))

    btn_style = {
        "font": ("Helvetica", 10, "bold"),
        "bd": 0,
        "padx": 10,
        "pady": 5,
        "width": 11,
        "cursor": "hand2"
    }
    
    btn_reg = Button(btn_frame, text="Register", bg=success_color, fg="#3d200f", command=register, **btn_style)
    btn_reg.pack(side="left", padx=2)
    bind_hover(btn_reg, success_color, success_hover)
    
    btn_clr = Button(btn_frame, text="Clear", bg="#725237", fg=text_color, command=clear_fields, **btn_style)
    btn_clr.pack(side="left", padx=2)
    bind_hover(btn_clr, "#725237", "#3d200f")
    
    btn_back = Button(btn_frame, text="Cancel", bg=danger_color, fg=text_color, command=on_close, **btn_style)
    btn_back.pack(side="right", padx=2)
    bind_hover(btn_back, danger_color, danger_hover)

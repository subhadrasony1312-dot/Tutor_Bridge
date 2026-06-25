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

def tutor_login_window(parent_root):
    win = Toplevel()
    win.title("Tutor Login - TutorBridge")
    win.geometry("1200x700")
    win.resizable(False, False)
    
    # Theme Palette
    bg_color = "#A0897B"     
    card_color = "#491903"   
    text_color = "#c7b5a3"    
    text_muted = "#bba690"    
    accent_color = "#c69d77"  
    accent_hover = "#b0977c"  
    danger_color = "#734022"  
    danger_hover = "#725237"  
    
    # Background Canvas
    canvas = Canvas(win, width=1200, height=700, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    setup_canvas_bg(canvas, "tutor_reg_background.jpg", "#755e52", "#3d200f")
    
    def on_close():
        win.destroy()
        parent_root.deiconify()
        
    win.protocol("WM_DELETE_WINDOW", on_close)
    
    # Card Frame centered on canvas
    card = Frame(canvas, bg=card_color, padx=40, pady=40)
    canvas.create_window(600, 350, window=card, anchor="center")
    
    # Logo inside card
    logo_ref = load_and_resize("logo.png", 60, 60)
    if logo_ref:
        lbl_logo = Label(card, image=logo_ref, bg=card_color)
        lbl_logo.image = logo_ref
        lbl_logo.pack(pady=(0, 10))
        
    # Title Layout
    Label(card, text="TUTOR PORTAL LOGIN", font=("Helvetica", 20, "bold"), fg=accent_color, bg=card_color).pack(pady=(0, 5))
    Label(card, text="Log in to manage your profile details", font=("Helvetica", 10), fg=text_muted, bg=card_color).pack(pady=(0, 20))
    
    # Email Field
    Label(card, text="Email ID", font=("Helvetica", 11, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 5))
    email_entry = Entry(card, font=("Helvetica", 12), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    email_entry.pack(ipady=6, pady=(0, 15))
    email_entry.focus()
    
    # Password Field
    Label(card, text="Password", font=("Helvetica", 11, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 5))
    password_entry = Entry(card, show="*", font=("Helvetica", 12), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    password_entry.pack(ipady=6, pady=(0, 20))
    
    def login():
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Validation Error", "All fields are required!", parent=win)
            return
            
        if email.startswith("@"):
            messagebox.showerror("Validation Error", "username cant be start with@", parent=win)
            return
            
        if not re.match(r"^[a-zA-Z0-9._%+-]{3,}@[a-zA-Z0-9.-]{3,}\.[a-zA-Z]{2,}$", email):
            messagebox.showerror("Validation Error", "Please enter a valid email address (e.g., username12@gmail.com).", parent=win)
            return
            
        conn = get_connection()
        if conn is None:
            messagebox.showerror("Database Error", "Unable to connect to database.", parent=win)
            return
            
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM tutors WHERE email=%s AND password=%s"
            cursor.execute(query, (email, password))
            tutor = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if tutor:
                # Check status approval
                if tutor.get("status") != "Approved":
                    messagebox.showwarning(
                        "Approval Pending", 
                        "Your tutor profile is pending Admin approval.", 
                        parent=win
                    )
                    return
                
                messagebox.showinfo("Success", f"Welcome back, {tutor['name']}!", parent=win)
                win.destroy()
                
                # Launch Tutor Dashboard
                from TutorBridge.tutor.tutor_profile import tutor_dashboard
                tutor_dashboard(parent_root, tutor["tutor_id"])
            else:
                messagebox.showerror("Error", "Invalid Email or Password.", parent=win)
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}", parent=win)
            
    # Hover Helper
    def bind_hover(button, normal_color, hover_color):
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))

    # Buttons
    btn_login = Button(
        card, 
        text="Login", 
        font=("Helvetica", 11, "bold"), 
        bg=accent_color, 
        fg="#3d200f", 
        bd=0, 
        width=35, 
        cursor="hand2",
        command=login
    )
    btn_login.pack(pady=10, ipady=4)
    bind_hover(btn_login, accent_color, accent_hover)
    
    btn_close = Button(
        card, 
        text="Cancel", 
        font=("Helvetica", 11, "bold"), 
        bg=danger_color, 
        fg=text_color, 
        bd=0, 
        width=35, 
        cursor="hand2",
        command=on_close
    )
    btn_close.pack(pady=(5, 0), ipady=4)
    bind_hover(btn_close, danger_color, danger_hover)

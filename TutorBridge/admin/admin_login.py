import os
import sys
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
    from TutorBridge.admin.admin_register import admin_register_window
except ImportError:
    from images_helper import setup_canvas_bg, load_and_resize
    from database import get_connection
    from admin.admin_register import admin_register_window

def admin_login_window(parent_root):
    win = Toplevel()
    win.title("Admin Login - TutorBridge")
    win.geometry("1200x700")
    win.resizable(False, False)
    
    # Theme Palette
    bg_color = "#3d200f"      # Darkest chocolate brown
    card_color = "#755e52"    # Deep warm brown
    text_color = "#c7b5a3"    # Very light grayish tan
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
    setup_canvas_bg(canvas, "admin_background.jpg", "#755e52", "#3d200f")
    
    def on_close():
        win.destroy()
        parent_root.deiconify()
        
    win.protocol("WM_DELETE_WINDOW", on_close)
    
    # Card / Form Container centered on canvas
    card = Frame(canvas, bg=card_color, padx=40, pady=40)
    canvas.create_window(600, 350, window=card, anchor="center")
    
    # Logo inside card or on canvas
    logo_ref = load_and_resize("logo.png", 60, 60)
    if logo_ref:
        lbl_logo = Label(card, image=logo_ref, bg=card_color)
        lbl_logo.image = logo_ref
        lbl_logo.pack(pady=(0, 10))
    
    # Title Layout
    Label(card, text="ADMIN PORTAL", font=("Helvetica", 20, "bold"), fg=accent_color, bg=card_color).pack(pady=(0, 5))
    Label(card, text="Sign in to manage database records", font=("Helvetica", 10), fg=text_muted, bg=card_color).pack(pady=(0, 20))
    
    # Username Field
    Label(card, text="Username", font=("Helvetica", 11, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 5))
    username_entry = Entry(card, font=("Helvetica", 12), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    username_entry.pack(ipady=6, pady=(0, 15))
    username_entry.focus()
    
    # Password Field
    Label(card, text="Password", font=("Helvetica", 11, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 5))
    password_entry = Entry(card, show="*", font=("Helvetica", 12), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    password_entry.pack(ipady=6, pady=(0, 20))
    
    def login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Validation Error", "All fields are required!", parent=win)
            return
            

            
        conn = get_connection()
        if conn is None:
            messagebox.showerror("Database Error", "Unable to connect to database.", parent=win)
            return
            
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM admin WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if result:
                win.destroy()
                # Open Admin Dashboard
                from TutorBridge.admin.manage_tutors import admin_dashboard
                admin_dashboard(parent_root, username)
            else:
                messagebox.showerror("Error", "Invalid Username or Password.", parent=win)
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
    
    btn_register = Button(
        card,
        text="Register New Admin",
        font=("Helvetica", 11, "bold"),
        bg=success_color,
        fg="#3d200f",
        bd=0,
        width=35,
        cursor="hand2",
        command=lambda: [win.destroy(), admin_register_window(parent_root)]
    )
    btn_register.pack(pady=(5, 0), ipady=4)
    bind_hover(btn_register, success_color, success_hover)

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

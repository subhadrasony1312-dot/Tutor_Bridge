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
except ImportError:
    from images_helper import setup_canvas_bg, load_and_resize
    from database import get_connection


def admin_register_window(parent_root):
    win = Toplevel()
    win.title("Admin Registration - TutorBridge")
    win.geometry("1200x700")
    win.resizable(False, False)

    bg_color = "#3d200f"
    card_color = "#755e52"
    text_color = "#c7b5a3"
    text_muted = "#bba690"
    accent_color = "#c69d77"
    accent_hover = "#b0977c"
    success_color = "#a87a64"
    success_hover = "#8d7865"
    danger_color = "#734022"
    danger_hover = "#725237"

    canvas = Canvas(win, width=1200, height=700, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    setup_canvas_bg(canvas, "admin_background.jpg", "#755e52", "#3d200f")

    def on_close():
        win.destroy()
        parent_root.deiconify()

    win.protocol("WM_DELETE_WINDOW", on_close)

    card = Frame(canvas, bg=card_color, padx=40, pady=40)
    canvas.create_window(600, 350, window=card, anchor="center")

    logo_ref = load_and_resize("logo.png", 60, 60)
    if logo_ref:
        lbl_logo = Label(card, image=logo_ref, bg=card_color)
        lbl_logo.image = logo_ref
        lbl_logo.pack(pady=(0, 10))

    Label(card, text="ADMIN REGISTRATION", font=("Helvetica", 20, "bold"), fg=success_color, bg=card_color).pack(pady=(0, 5))
    Label(card, text="Only approved admins may register.", font=("Helvetica", 10), fg=text_muted, bg=card_color).pack(pady=(0, 20))

    Label(card, text="Full Name", font=("Helvetica", 11, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 5))
    name_entry = Entry(card, font=("Helvetica", 12), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    name_entry.pack(ipady=6, pady=(0, 15))

    Label(card, text="Username", font=("Helvetica", 11, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 5))
    username_entry = Entry(card, font=("Helvetica", 12), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    username_entry.pack(ipady=6, pady=(0, 15))

    Label(card, text="Password", font=("Helvetica", 11, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 5))
    password_entry = Entry(card, show="*", font=("Helvetica", 12), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    password_entry.pack(ipady=6, pady=(0, 15))

    Label(card, text="Confirm Password", font=("Helvetica", 11, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 5))
    confirm_entry = Entry(card, show="*", font=("Helvetica", 12), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    confirm_entry.pack(ipady=6, pady=(0, 20))

 
   

    def register():
        name = name_entry.get().strip()
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        confirm = confirm_entry.get().strip()
       

        if not name or not username or not password or not confirm:
            messagebox.showerror("Validation Error", "All fields are required.", parent=win)
            return
        
        if password != confirm:
            messagebox.showerror("Validation Error", "Passwords do not match.", parent=win)
            return
    

        conn = get_connection()
        if conn is None:
            messagebox.showerror("Database Error", "Unable to connect to database.", parent=win)
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM admin WHERE username=%s", (username,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Duplicate Error", "This username is already taken.", parent=win)
                cursor.close()
                conn.close()
                return

            cursor.execute("INSERT INTO admin (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Admin registered successfully. You can now login.", parent=win)
            win.destroy()
            from TutorBridge.admin.admin_login import admin_login_window
            admin_login_window(parent_root)
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}", parent=win)

    def bind_hover(button, normal_color, hover_color):
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))

    btn_register = Button(
        card,
        text="Register Admin",
        font=("Helvetica", 11, "bold"),
        bg=success_color,
        fg="#3d200f",
        bd=0,
        width=35,
        cursor="hand2",
        command=register
    )
    btn_register.pack(pady=(0, 10), ipady=4)
    bind_hover(btn_register, success_color, success_hover)

    btn_cancel = Button(
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
    btn_cancel.pack(pady=(5, 0), ipady=4)
    bind_hover(btn_cancel, danger_color, danger_hover)

import os
import sys
import shutil
import time
from tkinter import *
from tkinter import messagebox, ttk, filedialog

# Resolve paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from TutorBridge.database import get_connection
except ImportError:
    from database import get_connection

def update_profile_dialog(parent_win, tutor_id, refresh_callback):
    # Fetch current values
    conn = get_connection()
    if conn is None:
        messagebox.showerror("Database Error", "Failed to connect to database.")
        return
        
    t = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tutors WHERE tutor_id = %s", (tutor_id,))
        t = cursor.fetchone()
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve profile data: {e}")
        conn.close()
        return
        
    if not t:
        messagebox.showerror("Error", "Could not find profile records.")
        return
        
    # Dialog Layout
    dialog = Toplevel(parent_win)
    dialog.title("Edit Profile - TutorBridge")
    dialog.geometry("520x650")
    dialog.resizable(False, False)
    dialog.configure(bg="#3d200f")
    dialog.grab_set()  # Modal window
    
    # Theme Styles
    card_color = "#755e52"
    text_color = "#c7b5a3"
    accent_color = "#c69d77"
    accent_hover = "#b0977c"
    success_color = "#a87a64"
    success_hover = "#8d7865"
    danger_color = "#734022"
    danger_hover = "#725237"
    
    Label(dialog, text="EDIT PROFILE DETAILS", font=("Helvetica", 16, "bold"), fg=accent_color, bg="#3d200f").pack(pady=10)
    
    form = Frame(dialog, bg=card_color, padx=20, pady=10)
    form.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    
    # Fields: Phone, City, Qualification, Experience, Fees, Mode
    # 1. Phone
    Label(form, text="Phone Number", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=0, column=0, sticky="w", pady=4)
    phone_ent = Entry(form, font=("Helvetica", 10), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    phone_ent.insert(0, t["phone"] if t["phone"] else "")
    phone_ent.grid(row=0, column=1, pady=4, padx=(15, 0))
    
    # 2. City
    Label(form, text="City Location", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=1, column=0, sticky="w", pady=4)
    city_ent = Entry(form, font=("Helvetica", 10), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    city_ent.insert(0, t["city"] if t["city"] else "")
    city_ent.grid(row=1, column=1, pady=4, padx=(15, 0))
    
    # 3. Qualification
    Label(form, text="Qualification", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=2, column=0, sticky="w", pady=4)
    qual_ent = Entry(form, font=("Helvetica", 10), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    qual_ent.insert(0, t["qualification"] if t["qualification"] else "")
    qual_ent.grid(row=2, column=1, pady=4, padx=(15, 0))
    
    # 4. Experience
    Label(form, text="Experience (Yrs)", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=3, column=0, sticky="w", pady=4)
    exp_ent = Entry(form, font=("Helvetica", 10), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    exp_ent.insert(0, str(t["experience"]) if t["experience"] is not None else "")
    exp_ent.grid(row=3, column=1, pady=4, padx=(15, 0))
    
    # 5. Teaching Mode
    Label(form, text="Teaching Mode", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=4, column=0, sticky="w", pady=4)
    mode_var = StringVar(value=t["mode"] if t["mode"] else "Online")
    mode_box = ttk.Combobox(form, textvariable=mode_var, values=["Online", "Offline", "Hybrid"], state="readonly", width=29, font=("Helvetica", 10))
    mode_box.grid(row=4, column=1, pady=4, padx=(15, 0))
    
    # 6. Fees
    Label(form, text="Monthly Fees ($)", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=5, column=0, sticky="w", pady=4)
    fees_ent = Entry(form, font=("Helvetica", 10), width=32, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    fees_ent.insert(0, f"{t['fees']:.2f}" if t["fees"] is not None else "")
    fees_ent.grid(row=5, column=1, pady=4, padx=(15, 0))
    
    # 7. Profile Picture
    Label(form, text="Profile Picture", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=6, column=0, sticky="w", pady=4)
    pic_frame = Frame(form, bg=card_color)
    pic_frame.grid(row=6, column=1, pady=4, padx=(15, 0), sticky="w")
    
    selected_pic_path = StringVar(value="")
    current_pic = t["profile_pic"] if t["profile_pic"] else "tutor1pic.jpeg"
    
    def browse_pic():
        path = filedialog.askopenfilename(
            title="Select Profile Picture",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp *.webp")]
        )
        if path:
            selected_pic_path.set(path)
            basename = os.path.basename(path)
            display_name = basename if len(basename) <= 18 else basename[:15] + "..."
            lbl_pic_name.config(text=display_name, fg=text_color)
            
    btn_browse = Button(pic_frame, text="Browse Image", font=("Helvetica", 9), bg=accent_color, fg="#3d200f", bd=0, padx=8, pady=2, cursor="hand2", command=browse_pic)
    btn_browse.pack(side="left")
    btn_browse.bind("<Enter>", lambda e: btn_browse.config(bg=accent_hover))
    btn_browse.bind("<Leave>", lambda e: btn_browse.config(bg=accent_color))
    
    lbl_pic_name = Label(pic_frame, text=current_pic if len(current_pic) <= 18 else current_pic[:15] + "...", font=("Helvetica", 9, "italic"), fg=text_color, bg=card_color)
    lbl_pic_name.pack(side="left", padx=8)
    
    def save():
        phone = phone_ent.get().strip()
        city = city_ent.get().strip()
        qual = qual_ent.get().strip()
        exp = exp_ent.get().strip()
        fees = fees_ent.get().strip()
        mode = mode_var.get()
        
        # Validations
        if not (phone and city and qual and exp and fees):
            messagebox.showerror("Error", "All fields are required!", parent=dialog)
            return
            
        if not phone.isdigit() or not (10 <= len(phone) <= 15):
            messagebox.showerror("Error", "Phone must be numeric (10-15 digits).", parent=dialog)
            return
            
        try:
            exp_int = int(exp)
            if exp_int < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Experience must be a positive integer.", parent=dialog)
            return
            
        try:
            fees_float = float(fees)
            if fees_float < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Fees must be a positive number.", parent=dialog)
            return
            
        # Copy file if a new one is selected
        pic_filename = t["profile_pic"]
        if selected_pic_path.get():
            images_dir = os.path.join(parent_dir, "images")
            os.makedirs(images_dir, exist_ok=True)
            ext = os.path.splitext(selected_pic_path.get())[1]
            pic_filename = f"tutor_{int(time.time())}{ext}"
            dest_path = os.path.join(images_dir, pic_filename)
            try:
                shutil.copy(selected_pic_path.get(), dest_path)
            except Exception as img_err:
                messagebox.showerror("Error", f"Failed to save profile picture: {img_err}", parent=dialog)
                return
                
        # Update database
        db_conn = get_connection()
        if db_conn is None:
            return
            
        try:
            cursor = db_conn.cursor()
            query = """
            UPDATE tutors 
            SET phone=%s, city=%s, qualification=%s, experience=%s, fees=%s, mode=%s, profile_pic=%s 
            WHERE tutor_id=%s
            """
            cursor.execute(query, (phone, city, qual, exp_int, fees_float, mode, pic_filename, tutor_id))
            db_conn.commit()
            cursor.close()
            db_conn.close()
            
            messagebox.showinfo("Success", "Profile updated successfully.", parent=dialog)
            dialog.destroy()
            refresh_callback()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save profile modifications: {e}", parent=dialog)
            
    # Hover Helper
    def bind_hover(button, normal_color, hover_color):
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))
 
    # Submit & Cancel Buttons
    btn_save = Button(form, text="Submit", font=("Helvetica", 11, "bold"), bg=success_color, fg="#3d200f", bd=0, cursor="hand2", command=save)
    btn_save.grid(row=7, column=0, columnspan=2, pady=(20, 5), ipady=4, sticky="we")
    bind_hover(btn_save, success_color, success_hover)
    
    btn_cancel = Button(form, text="Cancel Changes", font=("Helvetica", 11, "bold"), bg=danger_color, fg=text_color, bd=0, cursor="hand2", command=dialog.destroy)
    btn_cancel.grid(row=8, column=0, columnspan=2, pady=5, ipady=4, sticky="we")
    bind_hover(btn_cancel, danger_color, danger_hover)

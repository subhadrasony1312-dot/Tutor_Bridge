import os
import sys
import re
import time
import shutil
import random
from tkinter import *
from tkinter import messagebox, ttk, filedialog

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

def tutor_register_window(parent_root):
    win = Toplevel()
    win.title("Tutor Registration - TutorBridge")
    win.geometry("1200x700")
    win.resizable(False, False)
    
    # Configure TTK style theme globally
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox", fieldbackground="#c7b5a3", background="#c69d77", foreground="#3d200f", selectbackground="#755e52")
    
    # Theme Palette
    bg_color = "#3d200f"      
    card_color = "#361604"    
    text_color = "#c7b5a3"    # Very light grayish tan
    text_muted = "#bba690"    # Soft grayish tan
    accent_color = "#c69d77"  # Light warm tan / accent
    accent_hover = "#b0977c"  # Light grayish tan
    success_color = "#a87a64" # Medium warm brown
    success_hover = "#8d7865" # Medium grayish brown
    danger_color = "#734022"  # Reddish brown
    danger_hover = "#725237"  # Rich brown
    
    # Generate unique 4-digit Tutor ID
    tutor_id_val = random.randrange(1000, 5000)
    conn = get_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            while True:
                cursor.execute("SELECT COUNT(*) FROM tutors WHERE tutor_id=%s", (tutor_id_val,))
                if cursor.fetchone()[0] == 0:
                    break
                tutor_id_val = random.randrange(1000, 5000)
            cursor.close()
            conn.close()
        except Exception:
            pass

    # Background Canvas
    canvas = Canvas(win, width=1200, height=700, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    setup_canvas_bg(canvas, "tutor_reg_background.jpg", "#755e52", "#3d200f")
    
    def on_close():
        win.destroy()
        parent_root.deiconify()
        
    win.protocol("WM_DELETE_WINDOW", on_close)
    
    # Centered Card Frame (2 Columns layout)
    card = Frame(canvas, bg=card_color, padx=30, pady=30)
    canvas.create_window(600, 350, window=card, anchor="center")
    
    # Title
    Label(card, text="TUTOR REGISTRATION", font=("Helvetica", 18, "bold"), fg=accent_color, bg=card_color).grid(row=0, column=0, columnspan=2, pady=(0, 5))
    Label(card, text="Fill out credentials to create your teaching profile", font=("Helvetica", 10), fg=text_muted, bg=card_color).grid(row=1, column=0, columnspan=2, pady=(0, 20))
    
    # Column 0: Personal details (Left Frame)
    left_frame = Frame(card, bg=card_color)
    left_frame.grid(row=2, column=0, sticky="n", padx=(0, 20))
    
    # Column 1: Academic details (Right Frame)
    right_frame = Frame(card, bg=card_color)
    right_frame.grid(row=2, column=1, sticky="n")
    
    # Left Frame Contents
    Label(left_frame, text="Tutor ID (Generated)", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=0, column=0, sticky="w", pady=2)
    tutor_id_ent = Entry(left_frame, font=("Helvetica", 10), width=28, bg="#c7b5a3", fg="#3d200f", readonlybackground="#c7b5a3", disabledforeground="#3d200f", insertbackground="#3d200f", bd=0)
    tutor_id_ent.insert(0, str(tutor_id_val))
    tutor_id_ent.config(state="readonly")
    tutor_id_ent.grid(row=1, column=0, pady=(0, 10), sticky="w")

    Label(left_frame, text="Name", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=2, column=0, sticky="w", pady=2)
    name_ent = Entry(left_frame, font=("Helvetica", 10), width=28, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    name_ent.grid(row=3, column=0, pady=(0, 10), sticky="w")
    
    Label(left_frame, text="Email Address", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=4, column=0, sticky="w", pady=2)
    email_ent = Entry(left_frame, font=("Helvetica", 10), width=28, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    email_ent.grid(row=5, column=0, pady=(0, 10), sticky="w")
    
    Label(left_frame, text="Password", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=6, column=0, sticky="w", pady=2)
    pass_ent = Entry(left_frame, show="*", font=("Helvetica", 10), width=28, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    pass_ent.grid(row=7, column=0, pady=(0, 10), sticky="w")
    
    Label(left_frame, text="Confirm Password", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=8, column=0, sticky="w", pady=2)
    confirm_pass_ent = Entry(left_frame, show="*", font=("Helvetica", 10), width=28, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    confirm_pass_ent.grid(row=9, column=0, pady=(0, 10), sticky="w")

    Label(left_frame, text="Phone Number", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=10, column=0, sticky="w", pady=2)
    phone_ent = Entry(left_frame, font=("Helvetica", 10), width=28, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    phone_ent.grid(row=11, column=0, pady=(0, 10), sticky="w")
    
    Label(left_frame, text="City", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=12, column=0, sticky="w", pady=2)
    cities_list = ["Bhubaneswar", "Cuttack", "Rourkela", "Sambalpur", "Puri", "Balasore", "Berhampur", "Baripada", "Bhadrak", "Jharsuguda"]
    city_ent = ttk.Combobox(left_frame, values=cities_list, state="readonly", font=("Helvetica", 10), width=26)
    city_ent.grid(row=13, column=0, pady=(0, 10), sticky="w")
    
    Label(left_frame, text="Monthly Fees ($)", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=14, column=0, sticky="w", pady=2)
    fees_ent = Entry(left_frame, font=("Helvetica", 10), width=28, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    fees_ent.grid(row=15, column=0, pady=(0, 10), sticky="w")
    
    # Right Frame Contents
    Label(right_frame, text="Qualification", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=0, column=0, sticky="w", pady=2)
    qual_ent = Entry(right_frame, font=("Helvetica", 10), width=28, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    qual_ent.grid(row=1, column=0, pady=(0, 10), sticky="w")
    
    Label(right_frame, text="Experience (Years)", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=2, column=0, sticky="w", pady=2)
    exp_ent = Entry(right_frame, font=("Helvetica", 10), width=28, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0)
    exp_ent.grid(row=3, column=0, pady=(0, 10), sticky="w")
    
    # Dynamic Subjects (Max 5)
    Label(right_frame, text="Subject Specialist (Max 5)", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=4, column=0, sticky="w", pady=2)
    
    subject_container = Frame(right_frame, bg=card_color)
    subject_container.grid(row=5, column=0, pady=(0, 10), sticky="w")
    
    subject_entries = []
    subjects_list = [
        "Mathematics", "English", "Odia", "Political Science", "Physics", 
        "Chemistry", "Biology", "History", "Geography", "Computer Science", 
        "Economics", "Sanskrit", "Hindi", "Accountancy", "Business Studies"
    ]
    
    def add_subject_field():
        if len(subject_entries) >= 5:
            return
            
        ent = ttk.Combobox(subject_container, values=subjects_list, state="readonly", font=("Helvetica", 10), width=26)
        
        btn_add_subject.pack_forget()
        ent.pack(anchor="w", pady=(0, 5))
        subject_entries.append(ent)
        
        if len(subject_entries) < 5:
            btn_add_subject.pack(anchor="w", pady=(0, 2))
            
    btn_add_subject = Button(
        subject_container,
        text="+ Add Subject",
        font=("Helvetica", 8, "bold"),
        bg=accent_color,
        fg="#3d200f",
        bd=0,
        padx=8,
        pady=2,
        cursor="hand2",
        command=add_subject_field
    )
    add_subject_field()
    
    # Dynamic Classes (Max 5)
    Label(right_frame, text="Target Class / Grade (Max 5)", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=6, column=0, sticky="w", pady=2)
    
    class_container = Frame(right_frame, bg=card_color)
    class_container.grid(row=7, column=0, pady=(0, 10), sticky="w")
    
    class_entries = []
    classes_list = [
        "1st Class", "2nd Class", "3rd Class", "4th Class", "5th Class", 
        "6th Class", "7th Class", "8th Class", "9th Class", "10th Class", "11th Class", 
        "12th Class", "B.Sc", "B.A", "B.Com", "B.Tech", "BCA", "BBA", "B.Ed"
    ]

    def add_class_field():
        if len(class_entries) >= 5:
            return
            
        ent = ttk.Combobox(class_container, values=classes_list, state="readonly", font=("Helvetica", 10), width=26)
        
        btn_add_class.pack_forget()
        ent.pack(anchor="w", pady=(0, 5))
        class_entries.append(ent)
        
        if len(class_entries) < 5:
            btn_add_class.pack(anchor="w", pady=(0, 2))
            
    btn_add_class = Button(
        class_container,
        text="+ Add Class",
        font=("Helvetica", 8, "bold"),
        bg=accent_color,
        fg="#3d200f",
        bd=0,
        padx=8,
        pady=2,
        cursor="hand2",
        command=add_class_field
    )
    add_class_field()
    
    Label(right_frame, text="Teaching Mode", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=8, column=0, sticky="w", pady=2)
    mode_var = StringVar(value="Online")
    mode_box = ttk.Combobox(right_frame, textvariable=mode_var, values=["Online", "Offline", "Hybrid"], state="readonly", width=26, font=("Helvetica", 10))
    mode_box.grid(row=9, column=0, pady=(0, 10), sticky="w")
    
    # Profile Picture field
    Label(right_frame, text="Profile Picture", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).grid(row=10, column=0, sticky="w", pady=2)
    pic_frame = Frame(right_frame, bg=card_color)
    pic_frame.grid(row=11, column=0, pady=(0, 10), sticky="w")
    
    selected_pic_path = StringVar(value="")
    
    def browse_pic():
        path = filedialog.askopenfilename(
            title="Select Profile Picture",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg  *.bmp ")]
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
    
    lbl_pic_name = Label(pic_frame, text="No image selected", font=("Helvetica", 9, "italic"), fg=text_muted, bg=card_color)
    lbl_pic_name.pack(side="left", padx=8)
    
    def clear_fields():
        name_ent.delete(0, END)
        email_ent.delete(0, END)
        pass_ent.delete(0, END)
        confirm_pass_ent.delete(0, END)
        phone_ent.delete(0, END)
        city_ent.set("")
        qual_ent.delete(0, END)
        exp_ent.delete(0, END)
        
        # Reset Subjects
        for ent in subject_entries[1:]:
            ent.destroy()
        del subject_entries[1:]
        subject_entries[0].set("")
        btn_add_subject.pack(anchor="w", pady=(0, 2))
        
        # Reset Classes
        for ent in class_entries[1:]:
            ent.destroy()
        del class_entries[1:]
        class_entries[0].set("")
        btn_add_class.pack(anchor="w", pady=(0, 2))
        
        fees_ent.delete(0, END)
        mode_var.set("Online")
        selected_pic_path.set("")
        lbl_pic_name.config(text="No image selected", fg=text_muted)
        
    def validate_and_register():
        name = name_ent.get().strip()
        email = email_ent.get().strip()
        password = pass_ent.get().strip()
        confirm_password = confirm_pass_ent.get().strip()
        phone = phone_ent.get().strip()
        city = city_ent.get().strip()
        qual = qual_ent.get().strip()
        exp = exp_ent.get().strip()
        
        target_subjects = [ent.get().strip() for ent in subject_entries if ent.get().strip()]
        target_subject_str = ", ".join(target_subjects)
        
        target_classes = [ent.get().strip() for ent in class_entries if ent.get().strip()]
        target_class_str = ", ".join(target_classes)
        
        fees = fees_ent.get().strip()
        teaching_mode = mode_var.get()
        
        if not (name and email and password and confirm_password and phone and city and qual and exp and target_subject_str and target_class_str and fees):
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
            
        if not phone.isdigit() or not (10 <= len(phone) <= 10):
            messagebox.showerror("Validation Error", "Phone number must contain 10 digits only.", parent=win)
            return
            
        try:
            exp_int = int(exp)
            if exp_int < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Experience must be a positive integer.", parent=win)
            return
            
        try:
            fees_float = float(fees)
            if fees_float < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Fees must be a positive number.", parent=win)
            return
            
        conn = get_connection()
        if conn is None:
            messagebox.showerror("Database Error", "Unable to connect to database.", parent=win)
            return
            
        try:
            # Handle copying of the profile picture
            pic_filename = 'tutor1pic.jpeg'
            if selected_pic_path.get():
                images_dir = os.path.join(parent_dir, "images")
                os.makedirs(images_dir, exist_ok=True)
                ext = os.path.splitext(selected_pic_path.get())[1]
                pic_filename = f"tutor_{int(time.time())}{ext}"
                dest_path = os.path.join(images_dir, pic_filename)
                try:
                    shutil.copy(selected_pic_path.get(), dest_path)
                except Exception as img_err:
                    messagebox.showerror("Error", f"Failed to save profile picture: {img_err}", parent=win)
                    return
            
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM tutors WHERE email=%s", (email,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Validation Error", "An account with this email already exists.", parent=win)
                cursor.close()
                conn.close()
                return
                
            query = """
            INSERT INTO tutors (
                tutor_id, name, email, password, phone, city, qualification, experience, subject_name, class_name, mode, fees, rating, status, profile_pic
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0.0, 'Pending', %s)
            """
            cursor.execute(query, (tutor_id_val, name, email, password, phone, city, qual, exp_int, target_subject_str, target_class_str, teaching_mode, fees_float, pic_filename))
            conn.commit()
            cursor.close()
            conn.close()
            
            messagebox.showinfo("Success", "Registration successful! Log in once approved by Admin.", parent=win)
            win.destroy()
            from TutorBridge.tutor.tutor_login import tutor_login_window
            tutor_login_window(parent_root)
        except Exception as e:
            messagebox.showerror("Database Error", f"Already Exist tutorId {e}", parent=win)
            
    # Buttons Frame
    btn_frame = Frame(card, bg=card_color)
    btn_frame.grid(row=3, column=0, columnspan=2, pady=(15, 0), sticky="we")
    
    btn_style = {
        "font": ("Helvetica", 10, "bold"),
        "bd": 0,
        "padx": 15,
        "pady": 5,
        "width": 16,
        "cursor": "hand2"
    }
    
    btn_reg = Button(btn_frame, text="Register Profile", bg=success_color, fg="#3d200f", command=validate_and_register, **btn_style)
    btn_reg.pack(side="left", padx=5)
    btn_reg.bind("<Enter>", lambda e: btn_reg.config(bg=success_hover))
    btn_reg.bind("<Leave>", lambda e: btn_reg.config(bg=success_color))
    
    btn_clr = Button(btn_frame, text="Clear Fields", bg="#725237", fg=text_color, command=clear_fields, **btn_style)
    btn_clr.pack(side="left", padx=5)
    btn_clr.bind("<Enter>", lambda e: btn_clr.config(bg="#3d200f"))
    btn_clr.bind("<Leave>", lambda e: btn_clr.config(bg="#725237"))
    
    btn_back = Button(btn_frame, text="Cancel / Back", bg=danger_color, fg=text_color, command=on_close, **btn_style)
    btn_back.pack(side="right", padx=5)
    btn_back.bind("<Enter>", lambda e: btn_back.config(bg=danger_hover))
    btn_back.bind("<Leave>", lambda e: btn_back.config(bg=danger_color))

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

def feedback_submission_dialog(parent_dialog, tutor_id, student_id, completion_callback):
    dialog = Toplevel(parent_dialog)
    dialog.title("Leave Review - TutorBridge")
    dialog.geometry("450x420")
    dialog.resizable(False, False)
    dialog.configure(bg="#3d200f")
    dialog.grab_set()  # Modal window
    
    # Theme Palette
    card_color = "#755e52"
    text_color = "#c7b5a3"
    accent_color = "#c69d77"
    accent_hover = "#b0977c"
    success_color = "#a87a64"
    success_hover = "#8d7865"
    danger_color = "#734022"
    danger_hover = "#725237"
    
    Label(dialog, text="RATE & REVIEW TUTOR", font=("Helvetica", 15, "bold"), fg=accent_color, bg="#3d200f").pack(pady=20)
    
    form = Frame(dialog, bg=card_color, padx=20, pady=20)
    form.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    # 1. Rating Combobox
    Label(form, text="Select Rating", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 5))
    rating_options = [
        "5 ⭐  Excellent",
        "4 ⭐  Very Good",
        "3 ⭐  Good / Average",
        "2 ⭐  Fair / Poor",
        "1 ⭐  Terrible"
    ]
    rating_var = StringVar(value=rating_options[0])
    rating_box = ttk.Combobox(form, textvariable=rating_var, values=rating_options, state="readonly", font=("Helvetica", 10))
    rating_box.pack(fill="x", pady=(0, 15))
    
    # 2. Feedback Comment Textarea
    Label(form, text="Write Feedback Review", font=("Helvetica", 10, "bold"), fg=text_color, bg=card_color).pack(anchor="w", pady=(0, 5))
    feedback_text = Text(form, font=("Helvetica", 10), height=5, bg="#c7b5a3", fg="#3d200f", insertbackground="#3d200f", bd=0, wrap="word")
    feedback_text.pack(fill="both", expand=True, pady=(0, 20))
    feedback_text.focus()
    
    def submit_feedback():
        feedback_val = feedback_text.get("1.0", "end-1c").strip()
        
        # Rating string to integer
        selected_rating = rating_var.get()
        rating_val = int(selected_rating[0])  # Take first char e.g., '5'
        
        if not feedback_val:
            messagebox.showerror("Validation Error", "Please write a comment feedback review.", parent=dialog)
            return
            
        conn = get_connection()
        if conn is None:
            messagebox.showerror("Database Error", "Failed to connect to database.", parent=dialog)
            return
            
        try:
            cursor = conn.cursor()
            
            # 1. Insert feedback record
            insert_query = """
            INSERT INTO feedback (student_id, tutor_id, rating, feedback) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (student_id, tutor_id, rating_val, feedback_val))
            conn.commit()
            
            # 2. Recalculate average rating of this tutor
            cursor.execute("SELECT AVG(rating) FROM feedback WHERE tutor_id = %s", (tutor_id,))
            avg_rating = cursor.fetchone()[0]
            
            if avg_rating is not None:
                # Update tutors table rating
                cursor.execute("UPDATE tutors SET rating = %s WHERE tutor_id = %s", (avg_rating, tutor_id))
                conn.commit()
                
            cursor.close()
            conn.close()
            
            messagebox.showinfo("Success", "Thank you! Your feedback has been successfully submitted.", parent=dialog)
            dialog.destroy()
            completion_callback()
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to submit feedback: {e}", parent=dialog)
            
    # Hover Helper
    def bind_hover(button, normal_color, hover_color):
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))

    # Buttons Frame
    btn_frame = Frame(form, bg=card_color)
    btn_frame.pack(fill="x", side="bottom")
    
    btn_submit = Button(
        btn_frame, 
        text="Submit Review", 
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

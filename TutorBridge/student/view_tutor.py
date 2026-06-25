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
    from TutorBridge.database import get_connection
    from TutorBridge.images_helper import load_and_resize
except ImportError:
    from database import get_connection
    from images_helper import load_and_resize

class ViewTutorDetailsDialog:
    def __init__(self, parent_win, tutor_id, student_id, refresh_search_callback):
        self.parent = parent_win
        self.tutor_id = tutor_id
        self.student_id = student_id
        self.refresh_search = refresh_search_callback
        
        self.dialog = Toplevel(parent_win)
        self.dialog.title("Tutor Credentials - TutorBridge")
        self.dialog.geometry("520x680")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg="#3d200f")
        self.dialog.grab_set()  # Modal dialog
        
        # Design Theme Styles
        self.card_color = "#755e52"
        self.text_color = "#570707"
        self.accent_color = "#c69d77"
        self.accent_hover = "#b0977c"
        self.success_color = "#a87a64"
        self.success_hover = "#8d7865"
        self.danger_color = "#734022"
        self.danger_hover = "#725237"
        
        self.load_tutor_details()
        
    def load_tutor_details(self):
        # Clear dialog
        for widget in self.dialog.winfo_children():
            widget.destroy()
            
        conn = get_connection()
        if conn is None:
            messagebox.showerror("Error", "Unable to connect to database.", parent=self.dialog)
            self.dialog.destroy()
            return
            
        t = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tutors WHERE tutor_id = %s", (self.tutor_id,))
            t = cursor.fetchone()
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve data: {e}", parent=self.dialog)
            self.dialog.destroy()
            return
            
        if not t:
            messagebox.showerror("Error", "Tutor profile records not found.", parent=self.dialog)
            self.dialog.destroy()
            return
            
        # Top Heading
        Label(self.dialog, text="TUTOR PROFILE DETAILS", font=("Helvetica", 16, "bold"), fg=self.accent_color, bg="#3d200f").pack(pady=(15, 5))
        
        # Display Profile Image
        pic_name = t.get("profile_pic", "tutor1pic.jpeg")
        if not pic_name:
            pic_name = "tutor1pic.jpeg"
            
        img_ref = load_and_resize(pic_name, 95, 95)
        if not img_ref:
            img_ref = load_and_resize("tutor1pic.jpeg", 95, 95)
            
        if img_ref:
            lbl_pic = Label(self.dialog, image=img_ref, bg="#3d200f")
            lbl_pic.image = img_ref  # Keep reference
            lbl_pic.pack(pady=(0, 10))
            
        # Details Frame
        card = Frame(self.dialog, bg=self.card_color, padx=25, pady=20)
        card.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Profile Fields Grid
        fields = [
            ("Tutor ID:", str(t.get('tutor_id', ''))),
            ("Tutor Name:", t['name']),
            ("Email Address:", t['email']),
            ("Contact Number:", t['phone']),
            ("City Location:", t['city']),
            ("Qualification:", t['qualification']),
            ("Years of Experience:", f"{t['experience']} Years" if t['experience'] else "Not Specified"),
            ("Specialist Subject:", t['subject_name']),
            ("Target Class:", t['class_name']),
            ("Teaching Mode:", t['mode']),
            ("Monthly Tuition Fees:", f"${t['fees']:.2f}" if t['fees'] is not None else "$0.00"),
            ("System Rating status:", f"{t['rating']:.1f} ⭐" if t['rating'] is not None else "0.0 ⭐")
        ]
        
        for idx, (label_text, value_text) in enumerate(fields):
            Label(card, text=label_text, font=("Helvetica", 10, "bold"), fg="#bba690", bg=self.card_color).grid(row=idx, column=0, sticky="w", pady=4)
            Label(card, text=value_text, font=("Helvetica", 10, "bold"), fg=self.text_color, bg=self.card_color).grid(row=idx, column=1, sticky="w", padx=15, pady=4)
            
        # Hover Helper
        def bind_hover(button, normal_color, hover_color):
            button.bind("<Enter>", lambda e: button.config(bg=hover_color))
            button.bind("<Leave>", lambda e: button.config(bg=normal_color))
 
        # Bottom buttons
        btn_rate = Button(
            card, 
            text="⭐  Leave a Rating & Feedback", 
            font=("Helvetica", 11, "bold"), 
            bg=self.success_color, 
            fg="#3d200f", 
            bd=0, 
            ipady=5, 
            cursor="hand2", 
            command=self.open_feedback_dialog
        )
        btn_rate.grid(row=len(fields), column=0, columnspan=2, pady=(20, 5), sticky="we")
        bind_hover(btn_rate, self.success_color, self.success_hover)
        
        btn_close = Button(
            card, 
            text="Close Window", 
            font=("Helvetica", 11, "bold"), 
            bg=self.danger_color, 
            fg=self.text_color, 
            bd=0, 
            ipady=5, 
            cursor="hand2", 
            command=self.dialog.destroy
        )
        btn_close.grid(row=len(fields)+1, column=0, columnspan=2, pady=5, sticky="we")
        bind_hover(btn_close, self.danger_color, self.danger_hover)

    def open_feedback_dialog(self):
        try:
            from TutorBridge.student.rating_feedback import feedback_submission_dialog
            feedback_submission_dialog(self.dialog, self.tutor_id, self.student_id, self.refresh_details_and_search)
        except ImportError:
            from student.rating_feedback import feedback_submission_dialog
            feedback_submission_dialog(self.dialog, self.tutor_id, self.student_id, self.refresh_details_and_search)

    def refresh_details_and_search(self):
        # Refresh current window profile details to show new rating
        self.load_tutor_details()
        # Refresh student dashboard search view
        self.refresh_search()

def view_tutor_details_dialog(parent_win, tutor_id, student_id, refresh_search_callback):
    ViewTutorDetailsDialog(parent_win, tutor_id, student_id, refresh_search_callback)

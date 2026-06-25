import os
import sys
from tkinter import *
from tkinter import messagebox

# Add the parent directory to sys.path so we can run this file directly and resolve import paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


try:
    from TutorBridge.images_helper import setup_canvas_bg, load_and_resize
    from TutorBridge.admin.admin_login import admin_login_window
    from TutorBridge.tutor.tutor_login import tutor_login_window
    from TutorBridge.tutor.tutor_register import tutor_register_window
    from TutorBridge.student.student_login import student_login_window
    from TutorBridge.student.student_register import student_register_window
except ImportError:
    from images_helper import setup_canvas_bg, load_and_resize
    from admin.admin_login import admin_login_window
    from tutor.tutor_login import tutor_login_window
    from tutor.tutor_register import tutor_register_window
    from student.student_login import student_login_window
    from student.student_register import student_register_window

class TutorBridgeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TutorBridge - Find the Right Tutor")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)
        
        # Design Palette (Aesthetic Neutral Canva Theme)
        self.bg_color = "#3d200f"      
        self.card_color = "#755e52"    
        self.text_color = "#c7b5a3"    
        self.text_muted = "#bba690"    
        self.accent_color = "#c69d77"  
        self.accent_hover = "#b0977c"  
        self.success_color = "#a87a64" 
        self.success_hover = "#8d7865" 
        self.danger_color = "#734022"  
        self.danger_hover = "#725237"  
        
        self.setup_background()
        self.show_landing_screen()
        
    def setup_background(self):
        # Create background canvas
        self.bg_canvas = Canvas(self.root, width=1200, height=700, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        
        # Use the shipped first-page image for the welcome background.
        bg_img = load_and_resize("1stpage.jpeg", 1200, 700)
        if bg_img:
            self.bg_canvas.create_image(0, 0, image=bg_img, anchor="nw", tags="bg_image")
            self.bg_canvas.image_ref = bg_img
        else:
            setup_canvas_bg(self.bg_canvas, "background.png", "#c7b5a3", "#bba690")

    def set_background_image(self, image_name):
        # Replace the existing canvas background with a full-size local image
        self.bg_canvas.delete("bg_image")
        bg_img = load_and_resize(image_name, 1200, 700)
        if bg_img:
            self.bg_canvas.create_image(0, 0, image=bg_img, anchor="nw", tags="bg_image")
            self.bg_canvas.image_ref = bg_img
        else:
            setup_canvas_bg(self.bg_canvas, "background.png", "#c7b5a3", "#bba690")

    def show_landing_screen(self):
        # Clear any active widgets on canvas
        for widget in self.bg_canvas.winfo_children():
            widget.destroy()
            
        self.bg_canvas.delete("header")
        self.bg_canvas.delete("header_bg")
        self.draw_logo()


        # Legibility banner backing the title and subtitle
        self.bg_canvas.create_rectangle(300, 145, 900, 250, fill="#c7b5a3", outline="#3d200f", width=2, tags="header_bg")

        self.bg_canvas.create_text(600, 180, text="TutorBridge", font=("Helvetica", 38, "bold"), fill="#3d200f", tags="header")
        self.bg_canvas.create_text(600, 222, text="Bridging the Gap to Better Learning", font=("Helvetica", 14, "italic"), fill="#3d200f", tags="header")
        
        # Team Card (Frame)
        landing_card_color = "#bba690"
        landing_text_color = "#3d200f"
        landing_button_bg = "#a87a64"
        landing_button_hover = "#8d7865"
        card = Frame(self.bg_canvas, bg=landing_card_color, bd=0, padx=40, pady=30)
        self.bg_canvas.create_window(600, 450, window=card, anchor="center")
        
        # Subtitle inside the card
        Label(card, text="SYSTEM DEVELOPED BY", font=("Helvetica", 12, "bold"), fg="#734022", bg=landing_card_color).pack(pady=(0, 15))
        
        # Team Leader (Highlighted)
        Label(card, text="Subhadra Biswal", font=("Helvetica", 16, "bold"), fg=landing_text_color, bg=landing_card_color).pack(pady=2)
        Label(card, text="(Team Leader)", font=("Helvetica", 10, "italic"), fg="#734022", bg=landing_card_color).pack(pady=(0, 15))
        
        # Group Members
        Label(card, text="Subham Acharya", font=("Helvetica", 13, "bold"), fg=landing_text_color, bg=landing_card_color).pack(pady=2)
        Label(card, text="Bibhu Narayan Bhattacharya", font=("Helvetica", 13, "bold"), fg=landing_text_color, bg=landing_card_color).pack(pady=2)
        Label(card, text="Rohit Kumar Jena", font=("Helvetica", 13, "bold"), fg=landing_text_color, bg=landing_card_color).pack(pady=2)
        
        # Proceed Button
        btn_proceed = Button(
            card, 
            text="PROCEED →", 
            font=("Helvetica", 11, "bold"), 
            bg=landing_button_bg, 
            fg="#3d200f", 
            bd=0, 
            width=25, 
            height=2,
            cursor="hand2",
            command=self.show_welcome_screen
        )
        btn_proceed.pack(pady=(25, 0))
        self.bind_hover(btn_proceed, landing_button_bg, landing_button_hover)
        
        # Footer text
        self.bg_canvas.create_text(600, 670, text="TutorBridge © 2026 • Secure & Verified Connections", font=("Helvetica", 10), fill=self.text_muted)

    def show_welcome_screen(self):
        # Clear any active widgets on canvas
        for widget in self.bg_canvas.winfo_children():
            widget.destroy()
            
        self.bg_canvas.delete("header")
        self.bg_canvas.delete("header_bg")
        self.set_background_image("second__page.jpeg")
        self.draw_logo()

        # Legibility banner backing the title and subtitle
        self.bg_canvas.create_rectangle(300, 145, 900, 250, fill="#c7b5a3", outline="#3d200f", width=2, tags="header_bg")

        self.bg_canvas.create_text(600, 180, text="TutorBridge", font=("Helvetica", 38, "bold"), fill="#3d200f", tags="header")
        self.bg_canvas.create_text(600, 222, text="Find the Right Tutor in Your New City", font=("Helvetica", 15, "bold"), fill="#3d200f", tags="header")
        
        # Welcome Card (Frame)
        welcome_card_color = "#bba690"
        welcome_text_color = "#3d200f"
        welcome_button_bg = "#a87a64"
        welcome_button_hover = "#8d7865"
        card = Frame(self.bg_canvas, bg=welcome_card_color, bd=0, padx=30, pady=30)
        self.bg_canvas.create_window(600, 440, window=card, anchor="center")
        
        # Section Heading
        Label(card, text="Welcome to TutorBridge", font=("Helvetica", 20, "bold"), fg=welcome_text_color, bg=welcome_card_color).pack(pady=(0, 25))
        
        # Continue Buttons
        btn_config = {
            "font": ("Helvetica", 11, "bold"),
            "width": 32,
            "height": 2,
            "bd": 0,
            "cursor": "hand2",
            "activebackground": welcome_button_hover,
            "activeforeground": "#3d200f"
        }
        
        btn_admin = Button(card, text="Admin", bg=welcome_button_bg, fg="#3d200f", command=self.go_to_admin, **btn_config)
        btn_admin.pack(pady=8)
        self.bind_hover(btn_admin, welcome_button_bg, welcome_button_hover)
        
        btn_tutor = Button(card, text="Tutor", bg=welcome_button_bg, fg="#3d200f", command=self.go_to_tutor_portal, **btn_config)
        btn_tutor.pack(pady=8)
        self.bind_hover(btn_tutor, welcome_button_bg, welcome_button_hover)
        
        btn_student = Button(card, text="Student / Parent", bg=welcome_button_bg, fg="#3d200f", command=self.go_to_student_portal, **btn_config)
        btn_student.pack(pady=8)
        self.bind_hover(btn_student, welcome_button_bg, welcome_button_hover)
        
        btn_exit = Button(card, text="Exit Application", bg="#734022", fg="#c7b5a3", command=self.root.destroy, **btn_config)
        btn_exit.pack(pady=(12, 0))
        self.bind_hover(btn_exit, "#734022", "#725237")
        
        # Footer text
        self.bg_canvas.create_text(600, 670, text="TutorBridge © 2026 • Secure & Verified Connections", font=("Helvetica", 10), fill=self.text_muted)

    def draw_logo(self):
        # Try loading online/cached school logo, otherwise draw vector fallback
        logo_ref = load_and_resize("logo.png", 80, 80)
        if logo_ref:
            self.bg_canvas.create_image(600, 100, image=logo_ref, anchor="center", tags="logo")
            self.bg_canvas.logo_ref = logo_ref
        else:
            # Fallback vector representation (graduation cap)
            self.bg_canvas.create_oval(560, 50, 640, 130, fill="#755e52", outline="#c69d77", width=3, tags="logo")
            self.bg_canvas.create_text(600, 90, text="TB", font=("Helvetica", 24, "bold"), fill="#c69d77", tags="logo")
            # Trigger download
            setup_canvas_bg(self.bg_canvas, "logo.png", width=80, height=80)

    def bind_hover(self, button, normal_color, hover_color):
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))

    def go_to_admin(self):
        self.root.withdraw()
        admin_login_window(self.root)
        
    def go_to_tutor_portal(self):
        self.show_portal_screen("TUTOR PORTAL", self.go_to_tutor_login, self.go_to_tutor_register)

    def go_to_student_portal(self):
        self.show_portal_screen("STUDENT & PARENT PORTAL", self.go_to_student_login, self.go_to_student_register)

    def show_portal_screen(self, title_text, login_cmd, register_cmd):
        for widget in self.bg_canvas.winfo_children():
            widget.destroy()
            
        self.bg_canvas.delete("header")
        self.bg_canvas.delete("header_bg")
        self.draw_logo()
        
        # Legibility banner backing the title and subtitle
        self.bg_canvas.create_rectangle(300, 145, 900, 250, fill=self.card_color, outline=self.accent_color, width=2, tags="header_bg")

        self.bg_canvas.create_text(600, 180, text="TutorBridge", font=("Helvetica", 38, "bold"), fill=self.accent_color, tags="header")
        self.bg_canvas.create_text(600, 222, text=title_text, font=("Helvetica", 14, "bold"), fill=self.text_color, tags="header")
        
        card = Frame(self.bg_canvas, bg=self.card_color, bd=0, padx=40, pady=35)
        self.bg_canvas.create_window(600, 440, window=card, anchor="center")
        
        Label(card, text="Please select an option to continue", font=("Helvetica", 13), fg=self.text_color, bg=self.card_color).pack(pady=(0, 20))
        
        btn_config = {
            "font": ("Helvetica", 11, "bold"),
            "width": 30,
            "height": 2,
            "bd": 0,
            "cursor": "hand2"
        }
        
        btn_login = Button(card, text="Log In to My Account", bg=self.accent_color, fg="#3d200f", command=login_cmd, **btn_config)
        btn_login.pack(pady=8)
        self.bind_hover(btn_login, self.accent_color, self.accent_hover)
        
        btn_register = Button(card, text="Register New Account", bg=self.success_color, fg="#3d200f", command=register_cmd, **btn_config)
        btn_register.pack(pady=8)
        self.bind_hover(btn_register, self.success_color, self.success_hover)
        
        btn_back = Button(card, text="← Back to Welcome Screen", bg=self.danger_color, fg=self.text_color, command=self.show_welcome_screen, **btn_config)
        btn_back.pack(pady=(12, 0))
        self.bind_hover(btn_back, self.danger_color, self.danger_hover)
        
        self.bg_canvas.create_text(600, 670, text="TutorBridge © 2026 • Secure & Verified Connections", font=("Helvetica", 10), fill=self.text_muted)

    def go_to_tutor_login(self):
        self.root.withdraw()
        tutor_login_window(self.root)
        
    def go_to_tutor_register(self):
        self.root.withdraw()
        tutor_register_window(self.root)
        
    def go_to_student_login(self):
        self.root.withdraw()
        student_login_window(self.root)
        
    def go_to_student_register(self):
        self.root.withdraw()
        student_register_window(self.root)

if __name__ == "__main__":
    root = Tk()
    app = TutorBridgeApp(root)
    root.mainloop()
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

class ReportsFrame:
    def __init__(self, parent_frame, bg_color, text_color, accent_color, accent_hover):
        self.parent = parent_frame
        self.bg_color = bg_color
        self.text_color = text_color
        self.accent_color = accent_color
        self.accent_hover = accent_hover
        
        self.draw_ui()
        
    def draw_ui(self):
        # Header
        header_frame = Frame(self.parent, bg=self.bg_color, padx=30, pady=25)
        header_frame.pack(fill="x")
        
        Label(header_frame, text="System Statistics & Reports", font=("Helvetica", 22, "bold"), fg=self.text_color, bg=self.bg_color).pack(side="left")
        
        # Core Metrics Cards Frame
        cards_frame = Frame(self.parent, bg=self.bg_color, padx=30)
        cards_frame.pack(fill="x", pady=(0, 20))
        
        # Setup 3 cards
        self.total_tutors_lbl = StringVar(value="0")
        self.total_students_lbl = StringVar(value="0")
        self.avg_rating_lbl = StringVar(value="0.0")
        
        card_style = {"bg": "#755e52", "padx": 20, "pady": 15, "bd": 0}
        
        # Card 1: Tutors
        card_t = Frame(cards_frame, **card_style)
        card_t.pack(side="left", fill="both", expand=True, padx=(0, 10))
        Label(card_t, text="Total Tutors", font=("Helvetica", 11, "bold"), fg="#bba690", bg="#755e52").pack(anchor="w")
        Label(card_t, textvariable=self.total_tutors_lbl, font=("Helvetica", 24, "bold"), fg="#c69d77", bg="#755e52").pack(anchor="w", pady=(5, 0))
        
        # Card 2: Students
        card_s = Frame(cards_frame, **card_style)
        card_s.pack(side="left", fill="both", expand=True, padx=10)
        Label(card_s, text="Total Students", font=("Helvetica", 11, "bold"), fg="#bba690", bg="#755e52").pack(anchor="w")
        Label(card_s, textvariable=self.total_students_lbl, font=("Helvetica", 24, "bold"), fg="#c69d77", bg="#755e52").pack(anchor="w", pady=(5, 0))
        
        # Card 3: Avg Rating
        card_r = Frame(cards_frame, **card_style)
        card_r.pack(side="left", fill="both", expand=True, padx=(10, 0))
        Label(card_r, text="Average Tutor Rating", font=("Helvetica", 11, "bold"), fg="#bba690", bg="#755e52").pack(anchor="w")
        Label(card_r, textvariable=self.avg_rating_lbl, font=("Helvetica", 24, "bold"), fg="#c69d77", bg="#755e52").pack(anchor="w", pady=(5, 0))
        
        # Breakdown Control Panel
        control_frame = Frame(self.parent, bg=self.bg_color, padx=30)
        control_frame.pack(fill="x", pady=(10, 10))
        
        Label(control_frame, text="Detailed Breakdown Report:", font=("Helvetica", 11, "bold"), fg=self.text_color, bg=self.bg_color).pack(side="left", padx=(0, 10))
        
        self.report_type = StringVar(value="Subject-Wise Tutors")
        report_select = ttk.Combobox(
            control_frame, 
            textvariable=self.report_type, 
            values=["Subject-Wise Tutors", "City-Wise Tutors", "Top Rated Tutors"], 
            state="readonly", 
            width=25, 
            font=("Helvetica", 10)
        )
        report_select.pack(side="left", padx=5)
        report_select.bind("<<ComboboxSelected>>", lambda e: self.load_report_breakdown())
        
        btn_refresh = Button(
            control_frame, 
            text="🔄 Refresh Metrics", 
            bg=self.accent_color, 
            fg="#3d200f", 
            font=("Helvetica", 10, "bold"), 
            bd=0, 
            padx=15, 
            cursor="hand2", 
            command=self.refresh_all
        )
        btn_refresh.pack(side="right", padx=5, ipady=3)
        btn_refresh.bind("<Enter>", lambda e: btn_refresh.config(bg=self.accent_hover))
        btn_refresh.bind("<Leave>", lambda e: btn_refresh.config(bg=self.accent_color))
        
        # Table Frame
        self.table_frame = Frame(self.parent, bg=self.bg_color, bd=0, padx=30)
        self.table_frame.pack(fill="both", expand=True, pady=10)
        
        self.tree = None
        self.scroll_y = None
        self.scroll_x = None
        
        # Initial population
        self.refresh_all()

    def refresh_all(self):
        self.fetch_card_metrics()
        self.load_report_breakdown()

    def fetch_card_metrics(self):
        conn = get_connection()
        if conn is None:
            return
            
        try:
            cursor = conn.cursor()
            
            # Tutors count
            cursor.execute("SELECT COUNT(*) FROM tutors")
            self.total_tutors_lbl.set(str(cursor.fetchone()[0]))
            
            # Students count
            cursor.execute("SELECT COUNT(*) FROM students")
            self.total_students_lbl.set(str(cursor.fetchone()[0]))
            
            # Avg Rating
            cursor.execute("SELECT AVG(rating) FROM tutors WHERE rating IS NOT NULL AND rating > 0")
            val = cursor.fetchone()[0]
            if val is not None:
                self.avg_rating_lbl.set(f"{val:.2f} ⭐")
            else:
                self.avg_rating_lbl.set("0.0 ⭐")
                
            cursor.close()
            conn.close()
        except Exception as e:
            print("Failed to load reports card metrics:", e)

    def load_report_breakdown(self):
        # Clear existing Treeview
        if self.tree:
            self.tree.destroy()
        if self.scroll_y:
            self.scroll_y.destroy()
        if self.scroll_x:
            self.scroll_x.destroy()
            
        self.scroll_y = Scrollbar(self.table_frame, orient=VERTICAL)
        self.scroll_x = Scrollbar(self.table_frame, orient=HORIZONTAL)
        
        report = self.report_type.get()
        
        conn = get_connection()
        if conn is None:
            return
            
        cursor = conn.cursor()
        
        try:
            if report == "Subject-Wise Tutors":
                cols = ("Subject Name", "Total Tutors Available", "Avg Fees", "Avg Rating")
                self.tree = ttk.Treeview(self.table_frame, columns=cols, show="headings", yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
                
                for col in cols:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=200, anchor="center")
                    
                cursor.execute("""
                    SELECT subject_name, COUNT(*), AVG(fees), AVG(rating) 
                    FROM tutors 
                    GROUP BY subject_name 
                    ORDER BY COUNT(*) DESC
                """)
                rows = cursor.fetchall()
                for r in rows:
                    avg_fees = f"${r[2]:.2f}" if r[2] is not None else "$0.00"
                    avg_rating = f"{r[3]:.1f} ⭐" if r[3] is not None else "0.0 ⭐"
                    self.tree.insert("", "end", values=(r[0] if r[0] else "Unspecified", r[1], avg_fees, avg_rating))
                    
            elif report == "City-Wise Tutors":
                cols = ("City", "Total Tutors", "Avg Fees", "Avg Rating")
                self.tree = ttk.Treeview(self.table_frame, columns=cols, show="headings", yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
                
                for col in cols:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=200, anchor="center")
                    
                cursor.execute("""
                    SELECT city, COUNT(*), AVG(fees), AVG(rating) 
                    FROM tutors 
                    GROUP BY city 
                    ORDER BY COUNT(*) DESC
                """)
                rows = cursor.fetchall()
                for r in rows:
                    avg_fees = f"${r[2]:.2f}" if r[2] is not None else "$0.00"
                    avg_rating = f"{r[3]:.1f} ⭐" if r[3] is not None else "0.0 ⭐"
                    self.tree.insert("", "end", values=(r[0] if r[0] else "Unspecified", r[1], avg_fees, avg_rating))
                    
            else: # Top Rated Tutors
                cols = ("Tutor ID", "Name", "Subject", "City", "Rating Status")
                self.tree = ttk.Treeview(self.table_frame, columns=cols, show="headings", yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
                
                widths = {"Tutor ID": 100, "Name": 200, "Subject": 200, "City": 150, "Rating Status": 150}
                for col in cols:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=widths.get(col, 150), anchor="center")
                    
                cursor.execute("""
                    SELECT tutor_id, name, subject_name, city, rating 
                    FROM tutors 
                    WHERE rating IS NOT NULL AND rating > 0
                    ORDER BY rating DESC 
                    LIMIT 15
                """)
                rows = cursor.fetchall()
                for r in rows:
                    rating_str = f"{r[4]:.1f} ⭐"
                    self.tree.insert("", "end", values=(r[0], r[1], r[2], r[3], rating_str))
                    
            self.scroll_y.pack(side="right", fill="y")
            self.scroll_x.pack(side="bottom", fill="x")
            self.scroll_y.config(command=self.tree.yview)
            self.scroll_x.config(command=self.tree.xview)
            
            self.tree.pack(fill="both", expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate breakdown report: {e}")
        finally:
            cursor.close()
            conn.close()

def load_reports_frame(parent_frame, bg_color, text_color, accent_color, accent_hover):
    ReportsFrame(parent_frame, bg_color, text_color, accent_color, accent_hover)

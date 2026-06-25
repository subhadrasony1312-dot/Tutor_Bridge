import mysql.connector

def get_connection():
    # Primary connection details
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "Subham@2006",
    }
    
    # Try connecting without database first to ensure it exists
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS tutorbridge")
        conn.close()
    except Exception as e:
        print("Initial MySQL Connection Error:", e)
        # We will try connecting directly anyway, in case permissions are weird
    
    try:
        conn = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database="tutorbridge"
        )
        
        # Verify and initialize tables if they don't exist
        cursor = conn.cursor()
        
        # Create admin table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            admin_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(50) NOT NULL
        )
        """)
        
        # Insert default admin if not exists
        cursor.execute("SELECT COUNT(*) FROM admin WHERE username='@admin'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO admin (username, password) VALUES ('@admin', 'admin123')")
            conn.commit()
            
        # Create tutors table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tutors (
            tutor_id INT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(100),
            phone VARCHAR(10),
            city VARCHAR(50),
            qualification VARCHAR(100),
            experience INT,
            subject_name VARCHAR(50),
            class_name VARCHAR(50),
            mode VARCHAR(20),
            fees DECIMAL(10,2),
            rating FLOAT DEFAULT 0,
            status VARCHAR(20) DEFAULT 'Pending',
            profile_pic VARCHAR(255) DEFAULT 'tutor1pic.jpeg'
        )
        """)
        
        # Check if status column exists in tutors (just in case)
        try:
            cursor.execute("SELECT status FROM tutors LIMIT 1")
            cursor.fetchall()
        except mysql.connector.Error:
            cursor.execute("ALTER TABLE tutors ADD COLUMN status VARCHAR(20) DEFAULT 'Pending'")
            conn.commit()
            
        # Check if profile_pic column exists in tutors
        try:
            cursor.execute("SELECT profile_pic FROM tutors LIMIT 1")
            cursor.fetchall()
        except mysql.connector.Error:
            cursor.execute("ALTER TABLE tutors ADD COLUMN profile_pic VARCHAR(255) DEFAULT 'tutor1pic.jpeg'")
            conn.commit()
            
        # Create students table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(100),
            phone VARCHAR(15),
            city VARCHAR(50)
        )
        """)
        
        # Create feedback table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            tutor_id INT,
            rating INT,
            feedback TEXT,
            feedback_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY(tutor_id) REFERENCES tutors(tutor_id) ON DELETE CASCADE
        )
        """)
        
        cursor.close()
        return conn

    except Exception as e:
        print("Database Error :", e)
        return None

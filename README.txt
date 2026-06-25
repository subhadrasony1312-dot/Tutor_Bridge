========================================================================
                       TUTORBRIDGE - PROJECT MANUAL
========================================================================

PROJECT TITLE:
TutorBridge - Find the Right Tutor in Your New City

OBJECTIVE:
Moving to a new city can be challenging for families seeking high-quality,
verified education. TutorBridge bridges this gap by offering a desktop 
platform where parents and students can search for qualified tutors by 
city, class, subject, and mode of instruction, while allowing tutors to 
register profiles, list qualifications, and receive rating feedback. 
Admin users can manage the platform, approve tutors, delete profiles, 
and view analytics reports.

========================================================================
MODULES DESCRIPTION
========================================================================

1. Welcome Portal (main.py):
   - Entry point of the application with sleek Dark Slate graphics.
   - Allows users to choose paths: Admin, Tutor, or Student/Parent.

2. Admin Module (admin/):
   - admin_login.py: Validates admin credentials.
   - manage_tutors.py: Dashboard providing Tutor CRUD operations and approval toggles.
   - manage_students.py: Student CRUD management.
   - reports.py: Aggregate statistics and breakdowns (Subject/City/Rating).

3. Tutor Module (tutor/):
   - tutor_register.py: Registration form with strict regex validations.
   - tutor_login.py: Authenticates approved tutors only.
   - tutor_profile.py: Dashboard showing tutor stats and student reviews.
   - update_profile.py: Allows updating tutoring rates and credentials.

4. Student Module (student/):
   - student_register.py: Standard student signup.
   - student_login.py: Student sign-in.
   - search_tutor.py: Search portal filtering approved tutors by City/Subject/Class.
   - view_tutor.py: Displays detailed credentials of selected tutors.
   - rating_feedback.py: Rating (1-5 stars) and feedback reviews. Recalculates averages.

========================================================================
SYSTEM REQUIREMENTS
========================================================================

SOFTWARE REQUIREMENTS:
- Operating System: Windows 10/11, macOS, or Linux
- Python Version: Python 3.8 or higher
- Database: MySQL Server 5.7 or higher
- Python Packages: 
  * mysql-connector-python (Required for DB connectivity)
  * Pillow (Optional: For JPG background image support)

HARDWARE REQUIREMENTS:
- Processor: Dual Core 2.0 GHz or higher
- RAM: 4 GB minimum (8 GB recommended)
- Storage: 100 MB free space (excluding DB storage)
- Display: 1280x720 minimum resolution screen

========================================================================
DATABASE SETUP
========================================================================

1. Ensure MySQL Server is running locally.
2. The schema script is located at: `sql/tutorbridge.sql`.
3. To manually run the database script, execute via MySQL Command Line Client:
   mysql -u root -p < sql/tutorbridge.sql
4. Note: The application has a self-healing initializer. When run, 
   `database.py` will attempt to auto-create the database 'tutorbridge', 
   generate all required tables (admin, tutors, students, feedback), 
   and insert the default administrator credentials if they do not exist.
5. Default Database Connection:
   * Host: localhost
   * User: root
   * Password: (Set inside database.py)

DEFAULT ADMIN CREDENTIALS:
- Username: admin
- Password: admin123

========================================================================
HOW TO RUN THE APPLICATION
========================================================================

1. Open your terminal/command prompt and navigate to the project directory:
   cd "c:\Users\subha\OneDrive\Desktop\Tutor Bridge"

2. Run the main script:
   python TutorBridge/main.py

========================================================================
FUTURE SCOPE & ENHANCEMENTS
========================================================================
- Online Chat/Messaging System between tutors and students.
- Integrated Payment Gateway for processing monthly tuition fees securely.
- Document/Certificate verification upload and OCR scanning for tutors.
- GPS/Map-based radius searching for local offline tutors.
- Calendar scheduling for booking tuition trial classes.
========================================================================

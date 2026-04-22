# from https://www.py4e.com/html3/15-database
import sqlite3

connection = sqlite3.connect('registration.sqlite')
cursor = connection.cursor()

# ── Create tables ──────────────────────────────────────────────────────────────

cursor.execute('''CREATE TABLE IF NOT EXISTS Faculty
    (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Course
    (id INTEGER PRIMARY KEY AUTOINCREMENT, Department TEXT, Number TEXT, Credits INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Student
    (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Section
    (id INTEGER PRIMARY KEY AUTOINCREMENT, Course_ID INTEGER, Faculty_ID INTEGER,
     Semester TEXT, Year INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Enrollment
    (id INTEGER PRIMARY KEY AUTOINCREMENT, Student_ID INTEGER, Section_ID INTEGER,
     Grade TEXT)''')

connection.commit()

# ── Helpers ────────────────────────────────────────────────────────────────────

def list_faculty():
    cursor.execute('SELECT * FROM Faculty')
    rows = cursor.fetchall()
    if not rows:
        print("No faculty found.")
        return
    print("\nid  | name                 | email")
    print("-" * 50)
    for row in rows:
        print(f"{row[0]:<4}| {row[1]:<21}| {row[2]}")

def list_courses():
    cursor.execute('SELECT * FROM Course')
    rows = cursor.fetchall()
    if not rows:
        print("No courses found.")
        return
    print("\nid  | dept | number | credits")
    print("-" * 40)
    for row in rows:
        print(f"{row[0]:<4}| {row[1]:<5}| {row[2]:<7}| {row[3]}")

def list_students():
    cursor.execute('SELECT * FROM Student')
    rows = cursor.fetchall()
    if not rows:
        print("No students found.")
        return
    print("\nid  | name                 | email")
    print("-" * 50)
    for row in rows:
        print(f"{row[0]:<4}| {row[1]:<21}| {row[2]}")

def list_sections():
    cursor.execute('''SELECT Section.id, Course.Department, Course.Number,
                             Faculty.name, Section.Semester, Section.Year
                      FROM Section
                      INNER JOIN Course ON Course.id = Section.Course_ID
                      INNER JOIN Faculty ON Faculty.id = Section.Faculty_ID''')
    rows = cursor.fetchall()
    if not rows:
        print("No sections found.")
        return
    print("\nid  | dept | number | faculty              | semester | year")
    print("-" * 70)
    for row in rows:
        print(f"{row[0]:<4}| {row[1]:<5}| {row[2]:<7}| {row[3]:<21}| {row[4]:<9}| {row[5]}")

def list_enrollments():
    cursor.execute('''SELECT Enrollment.id, Student.name, Course.Department,
                             Course.Number, Section.Semester, Section.Year, Enrollment.Grade
                      FROM Enrollment
                      INNER JOIN Student ON Student.id = Enrollment.Student_ID
                      INNER JOIN Section ON Section.id = Enrollment.Section_ID
                      INNER JOIN Course ON Course.id = Section.Course_ID''')
    rows = cursor.fetchall()
    if not rows:
        print("No enrollments found.")
        return
    print("\nid  | student              | dept | number | semester | year | grade")
    print("-" * 75)
    for row in rows:
        grade = row[6] if row[6] else "--"
        print(f"{row[0]:<4}| {row[1]:<21}| {row[2]:<5}| {row[3]:<7}| {row[4]:<9}| {row[5]:<5}| {grade}")

# ── Main loop ──────────────────────────────────────────────────────────────────

choice = ""
while choice != "QUIT":
    print("\n==== Registration System ====")
    print("1 - Manage Faculty")
    print("2 - Manage Courses")
    print("3 - Manage Students")
    print("4 - Manage Sections")
    print("5 - Manage Enrollments")
    print("6 - Show Student Transcript")
    print("QUIT - Exit")
    choice = input("Enter a choice: ")

    # ── Faculty ────────────────────────────────────────────────────────────────
    if choice == "1":
        action = input("Enter 1 for List Faculty, 2 for Add Faculty, 3 for Update Faculty: ")
        if action == "1":
            list_faculty()
        elif action == "2":
            name = input("Enter name: ")
            email = input("Enter email: ")
            cursor.execute('INSERT INTO Faculty (name, email) VALUES (?, ?)', (name, email))
            connection.commit()
            print("Faculty added.")
        elif action == "3":
            list_faculty()
            id = int(input("Enter the ID to update: "))
            name = input("Enter name: ")
            email = input("Enter email: ")
            cursor.execute('UPDATE Faculty SET name = ?, email = ? WHERE id = ?', (name, email, id))
            connection.commit()
            print("Faculty updated.")

    # ── Courses ────────────────────────────────────────────────────────────────
    elif choice == "2":
        action = input("Enter 1 for List Courses, 2 for Add Course, 3 for Update Course: ")
        if action == "1":
            list_courses()
        elif action == "2":
            department = input("Enter department (e.g. CIS): ")
            number = input("Enter course number (e.g. 298): ")
            credits = int(input("Enter credits: "))
            cursor.execute('INSERT INTO Course (Department, Number, Credits) VALUES (?, ?, ?)',
                           (department, number, credits))
            connection.commit()
            print("Course added.")
        elif action == "3":
            list_courses()
            id = int(input("Enter the ID to update: "))
            department = input("Enter department: ")
            number = input("Enter course number: ")
            credits = int(input("Enter credits: "))
            cursor.execute('UPDATE Course SET Department = ?, Number = ?, Credits = ? WHERE id = ?',
                           (department, number, credits, id))
            connection.commit()
            print("Course updated.")

    # ── Students ───────────────────────────────────────────────────────────────
    elif choice == "3":
        action = input("Enter 1 for List Students, 2 for Add Student, 3 for Update Student: ")
        if action == "1":
            list_students()
        elif action == "2":
            name = input("Enter name: ")
            email = input("Enter email: ")
            cursor.execute('INSERT INTO Student (name, email) VALUES (?, ?)', (name, email))
            connection.commit()
            print("Student added.")
        elif action == "3":
            list_students()
            id = int(input("Enter the ID to update: "))
            name = input("Enter name: ")
            email = input("Enter email: ")
            cursor.execute('UPDATE Student SET name = ?, email = ? WHERE id = ?', (name, email, id))
            connection.commit()
            print("Student updated.")

    # ── Sections ───────────────────────────────────────────────────────────────
    elif choice == "4":
        action = input("Enter 1 for List Sections, 2 for Add Section, 3 for Update Section: ")
        if action == "1":
            list_sections()
        elif action == "2":
            list_courses()
            course_id = int(input("Enter Course ID: "))
            list_faculty()
            faculty_id = int(input("Enter Faculty ID: "))
            semester = input("Enter semester (Fall/Winter/Spring/Summer): ")
            year = int(input("Enter year: "))
            cursor.execute('INSERT INTO Section (Course_ID, Faculty_ID, Semester, Year) VALUES (?, ?, ?, ?)',
                           (course_id, faculty_id, semester, year))
            connection.commit()
            print("Section added.")
        elif action == "3":
            list_sections()
            id = int(input("Enter the ID to update: "))
            list_faculty()
            faculty_id = int(input("Enter new Faculty ID: "))
            semester = input("Enter semester: ")
            year = int(input("Enter year: "))
            cursor.execute('UPDATE Section SET Faculty_ID = ?, Semester = ?, Year = ? WHERE id = ?',
                           (faculty_id, semester, year, id))
            connection.commit()
            print("Section updated.")

    # ── Enrollments ────────────────────────────────────────────────────────────
    elif choice == "5":
        action = input("Enter 1 for List, 2 for Add, 3 for Update Grade, 4 for Delete: ")
        if action == "1":
            list_enrollments()
        elif action == "2":
            list_students()
            student_id = int(input("Enter Student ID: "))
            list_sections()
            section_id = int(input("Enter Section ID: "))
            grade = input("Enter grade (leave blank if not yet assigned): ")
            grade = grade if grade else None
            cursor.execute('INSERT INTO Enrollment (Student_ID, Section_ID, Grade) VALUES (?, ?, ?)',
                           (student_id, section_id, grade))
            connection.commit()
            print("Enrollment added.")
        elif action == "3":
            list_enrollments()
            id = int(input("Enter Enrollment ID to update grade: "))
            grade = input("Enter grade: ")
            cursor.execute('UPDATE Enrollment SET Grade = ? WHERE id = ?', (grade, id))
            connection.commit()
            print("Grade updated.")
        elif action == "4":
            list_enrollments()
            id = int(input("Enter Enrollment ID to delete: "))
            confirm = input(f"Delete enrollment {id}? (yes/no): ")
            if confirm.lower() == "yes":
                cursor.execute('DELETE FROM Enrollment WHERE id = ?', (id,))
                connection.commit()
                print("Enrollment deleted.")
            else:
                print("Cancelled.")

    # ── Transcript ─────────────────────────────────────────────────────────────
    elif choice == "6":
        list_students()
        student_id = int(input("Enter Student ID for transcript: "))

        cursor.execute('SELECT name, email FROM Student WHERE id = ?', (student_id,))
        student = cursor.fetchone()
        if not student:
            print("Student not found.")
        else:
            # transcript query with joins (from the comment in the starter code)
            cursor.execute('''SELECT Course.Department, Course.Number, Course.Credits, Enrollment.Grade
                              FROM Enrollment
                              INNER JOIN Student ON Student.id = Enrollment.Student_ID
                              INNER JOIN Section ON Section.id = Enrollment.Section_ID
                              INNER JOIN Course ON Course.id = Section.Course_ID
                              WHERE Student_ID = ?''', (student_id,))
            rows = cursor.fetchall()

            print("\n" + "=" * 50)
            print(f"  TRANSCRIPT")
            print(f"  Student: {student[0]}  |  {student[1]}")
            print("=" * 50)
            if not rows:
                print("  No enrollments on record.")
            else:
                print(f"\n  {'Dept':<6} {'Number':<8} {'Credits':<9} {'Grade'}")
                print("  " + "-" * 35)
                total_credits = 0
                grade_points = 0.0
                graded_credits = 0
                grade_map = {
                    "A+": 4.0, "A": 4.0, "A-": 3.7,
                    "B+": 3.3, "B": 3.0, "B-": 2.7,
                    "C+": 2.3, "C": 2.0, "C-": 1.7,
                    "D+": 1.3, "D": 1.0, "D-": 0.7,
                    "F": 0.0
                }
                for row in rows:
                    grade = row[3] if row[3] else "IP"
                    print(f"  {row[0]:<6} {row[1]:<8} {row[2]:<9} {grade}")
                    total_credits += row[2]
                    if row[3] and row[3].upper() in grade_map:
                        graded_credits += row[2]
                        grade_points += grade_map[row[3].upper()] * row[2]
                print("  " + "-" * 35)
                print(f"  Total Credits: {total_credits}")
                if graded_credits > 0:
                    print(f"  GPA: {grade_points / graded_credits:.2f}")
                else:
                    print("  GPA: N/A (no graded courses)")
            print("=" * 50)

connection.close()


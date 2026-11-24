
import sqlite3

DB_PATH = "university.db"


def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Students table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        name TEXT,
        branch TEXT,
        year INTEGER,
        gpa REAL
    )
    """)

    # Courses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_id INTEGER PRIMARY KEY,
        course_name TEXT,
        branch TEXT
    )
    """)

    # Enrollments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        course_id INTEGER,
        semester INTEGER,
        FOREIGN KEY(student_id) REFERENCES students(student_id),
        FOREIGN KEY(course_id) REFERENCES courses(course_id)
    )
    """)

    # Grants table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grants (
        grant_id INTEGER PRIMARY KEY,
        grant_name TEXT,
        minimum_gpa REAL,
        eligible_year INTEGER,
        deadline TEXT
    )
    """)

    students = [
        (1, "Aarav", "IT", 3, 8.7),
        (2, "Riya", "CS", 2, 9.1),
        (3, "Kabir", "IT", 3, 7.8),
        (4, "Neha", "CS", 4, 8.9),
        (5, "Ishaan", "IT", 2, 8.2),
        (6, "Ananya", "CS", 3, 9.3),
        (7, "Vihaan", "IT", 4, 8.5),
        (8, "Meera", "CS", 3, 7.9),
        (9, "Arjun", "IT", 3, 9.0),
        (10, "Sana", "CS", 2, 8.6),
        (11, "Dev", "IT", 1, 7.5),
        (12, "Ira", "CS", 4, 9.2),
        (13, "Reyansh", "IT", 2, 8.8),
        (14, "Aditi", "CS", 3, 8.4),
        (15, "Krish", "IT", 4, 7.7),
        (16, "Myra", "CS", 1, 8.9),
        (17, "Rohan", "IT", 3, 8.1),
        (18, "Diya", "CS", 2, 9.4),
        (19, "Atharv", "IT", 1, 8.0),
        (20, "Kiara", "CS", 3, 8.7)
    ]

    courses = [
        (101, "Data Structures", "IT"),
        (102, "Database Management", "CS"),
        (103, "Machine Learning", "IT"),
        (104, "Computer Networks", "CS"),
        (105, "Operating Systems", "IT")
    ]

    grants = [
        (1, "Research Excellence Grant", 8.0, 3, "2026-12-15"),
        (2, "Innovation Scholarship", 8.5, 2, "2026-12-20"),
        (3, "Academic Research Fellowship", 9.0, 4, "2027-01-10")
    ]

    enrollments = [
        (1, 101, 5), (1, 103, 5),
        (2, 102, 4), (3, 101, 5),
        (4, 104, 7), (5, 105, 4),
        (6, 103, 5), (7, 105, 7),
        (8, 102, 5), (9, 101, 5),
        (10, 104, 4), (11, 101, 2),
        (12, 102, 7), (13, 103, 4),
        (14, 104, 5), (15, 105, 7),
        (16, 102, 2), (17, 101, 5),
        (18, 103, 4), (19, 105, 2),
        (20, 104, 5)
    ]

    cursor.execute("DELETE FROM enrollments")
    
    cursor.executemany(
        "INSERT OR REPLACE INTO students VALUES (?, ?, ?, ?, ?)",
        students
    )

    cursor.executemany(
        "INSERT OR REPLACE INTO courses VALUES (?, ?, ?)",
        courses
    )

    cursor.executemany(
        """INSERT INTO enrollments
        (student_id, course_id, semester) VALUES (?, ?, ?)""",
        enrollments
    )

    cursor.executemany(
        "INSERT OR REPLACE INTO grants VALUES (?, ?, ?, ?, ?)",
        grants
    )

    conn.commit()
    conn.close()

    print("University database created successfully!")


if __name__ == "__main__":
    setup_database()

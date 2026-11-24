
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "university.db"


def execute_query(query, params=()):
    """Execute a read-only SQL query and return results."""

    if not query.strip().lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


# ---------------------------------
# INDIVIDUAL STUDENT INFORMATION
# ---------------------------------

def get_student(student_id):
    query = """
        SELECT student_id, name, branch, year, gpa
        FROM students
        WHERE student_id = ?
    """
    return execute_query(query, (student_id,))


# ---------------------------------
# STUDENT COUNTS
# ---------------------------------

def get_student_count():
    query = """
        SELECT COUNT(*) AS total_students
        FROM students
    """
    return execute_query(query)


def get_branch_student_count(branch=None):
    if branch:
        query = """
            SELECT COUNT(*) AS total
            FROM students
            WHERE UPPER(branch) = UPPER(?)
        """
        return execute_query(query, (branch,))

    query = """
        SELECT branch, COUNT(*) AS total
        FROM students
        GROUP BY branch
    """
    return execute_query(query)


# ---------------------------------
# STUDENT SEARCH AND FILTERING
# ---------------------------------

def get_students(branch=None, year=None, min_gpa=None):
    query = """
        SELECT student_id, name, branch, year, gpa
        FROM students
        WHERE 1=1
    """

    params = []

    if branch:
        query += " AND UPPER(branch) = UPPER(?)"
        params.append(branch)

    if year is not None:
        query += " AND year = ?"
        params.append(year)

    if min_gpa is not None:
        query += " AND gpa > ?"
        params.append(min_gpa)

    query += " ORDER BY student_id"

    return execute_query(query, tuple(params))


# ---------------------------------
# TOP-PERFORMING STUDENT
# ---------------------------------

def get_top_student(branch=None):
    query = """
        SELECT student_id, name, branch, year, gpa
        FROM students
    """

    params = []

    if branch:
        query += " WHERE UPPER(branch) = UPPER(?)"
        params.append(branch)

    query += " ORDER BY gpa DESC, student_id ASC LIMIT 1"

    return execute_query(query, tuple(params))


# ---------------------------------
# AVERAGE GPA
# ---------------------------------

def get_average_gpa(branch=None):
    query = """
        SELECT ROUND(AVG(gpa), 2) AS average_gpa
        FROM students
    """

    params = []

    if branch:
        query += " WHERE UPPER(branch) = UPPER(?)"
        params.append(branch)

    return execute_query(query, tuple(params))


# ---------------------------------
# GRANT INFORMATION
# ---------------------------------

def get_grants():
    query = """
        SELECT grant_id, grant_name, minimum_gpa,
               eligible_year, deadline
        FROM grants
    """
    return execute_query(query)


# ---------------------------------
# ENROLLMENT INFORMATION
# ---------------------------------

def get_enrollment_count():
    query = """
        SELECT COUNT(*) AS total_enrollments
        FROM enrollments
    """
    return execute_query(query)


# ---------------------------------
# TESTING
# ---------------------------------

if __name__ == "__main__":

    print("\n--- Student Details ---")
    print(get_student(1))

    print("\n--- Total Students ---")
    print(get_student_count())

    print("\n--- IT Students ---")
    print(get_students(branch="IT"))

    print("\n--- Third Year Students ---")
    print(get_students(year=3))

    print("\n--- Students with GPA Above 8.5 ---")
    print(get_students(min_gpa=8.5))

    print("\n--- Highest GPA Student ---")
    print(get_top_student())

    print("\n--- Highest GPA in IT ---")
    print(get_top_student(branch="IT"))

    print("\n--- Average GPA ---")
    print(get_average_gpa())

    print("\n--- Average IT GPA ---")
    print(get_average_gpa(branch="IT"))

    print("\n--- Available Grants ---")
    print(get_grants())

    print("\n--- Enrollment Count ---")
    print(get_enrollment_count())

    print("\n--- Students by Branch ---")
    print(get_branch_student_count())

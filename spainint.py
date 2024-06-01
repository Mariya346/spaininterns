import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Create and populate the database
def create_and_populate_db():
    conn = sqlite3.connect('student_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        student_id INTEGER PRIMARY KEY,
        name TEXT,
        dob DATE,
        gender TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Courses (
        course_id INTEGER PRIMARY KEY,
        course_name TEXT,
        credits INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Enrollments (
        enrollment_id INTEGER PRIMARY KEY,
        student_id INTEGER,
        course_id INTEGER,
        grade TEXT,
        semester TEXT,
        FOREIGN KEY(student_id) REFERENCES Students(student_id),
        FOREIGN KEY(course_id) REFERENCES Courses(course_id)
    )
    ''')

    cursor.execute("INSERT INTO Students (student_id, name, dob, gender) VALUES (1, 'John Doe', '2001-01-01', 'M')")
    cursor.execute("INSERT INTO Courses (course_id, course_name, credits) VALUES (101, 'Mathematics', 3)")
    cursor.execute("INSERT INTO Enrollments (enrollment_id, student_id, course_id, grade, semester) VALUES (1001, 1, 101, 'A', 'Fall 2023')")

    conn.commit()
    conn.close()

# Generate a report
def generate_report():
    conn = sqlite3.connect('student_data.db')
    cursor = conn.cursor()

    student_name = 'John Doe'
    cursor.execute('''
    SELECT Students.name, Courses.course_name, Enrollments.grade
    FROM Enrollments
    JOIN Students ON Enrollments.student_id = Students.student_id
    JOIN Courses ON Enrollments.course_id = Courses.course_id
    WHERE Students.name = ?
    ''', (student_name,))

    results = cursor.fetchall()
    for row in results:
        print(row)

    conn.close()

# Visualize data
def visualize_data():
    conn = sqlite3.connect('student_data.db')
    grades_df = pd.read_sql_query("SELECT grade, COUNT(*) as count FROM Enrollments GROUP BY grade", conn)

    plt.bar(grades_df['grade'], grades_df['count'])
    plt.xlabel('Grade')
    plt.ylabel('Number of Students')
    plt.title('Grade Distribution')
    plt.show()

    conn.close()

if __name__ == "__main__":
    create_and_populate_db()
    generate_report()
    visualize_data()

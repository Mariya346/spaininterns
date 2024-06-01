import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('student_data.db')
cursor = conn.cursor()

# Create Students table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
    student_id INTEGER PRIMARY KEY,
    name TEXT,
    dob DATE,
    gender TEXT
)
''')

# Create Courses table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Courses (
    course_id INTEGER PRIMARY KEY,
    course_name TEXT,
    credits INTEGER
)
''')

# Create Enrollments table
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

# Commit and close connection
conn.commit()
conn.close()
# Reconnect to SQLite database
conn = sqlite3.connect('student_data.db')
cursor = conn.cursor()

# Query to get grades of a specific student
student_name = 'John Doe'
cursor.execute('''
SELECT Students.name, Courses.course_name, Enrollments.grade
FROM Enrollments
JOIN Students ON Enrollments.student_id = Students.student_id
JOIN Courses ON Enrollments.course_id = Courses.course_id
WHERE Students.name = ?
''', (student_name,))

# Fetch and print results
results = cursor.fetchall()
for row in results:
    print(row)

# Close connection
conn.close()
import matplotlib.pyplot as plt
import pandas as pd

# Reconnect to SQLite database
conn = sqlite3.connect('student_data.db')

# Load data into DataFrame
grades_df = pd.read_sql_query("SELECT grade, COUNT(*) as count FROM Enrollments GROUP BY grade", conn)

# Create bar chart
plt.bar(grades_df['grade'], grades_df['count'])
plt.xlabel('Grade')
plt.ylabel('Number of Students')
plt.title('Grade Distribution')
plt.show()

# Close connection
conn.close()

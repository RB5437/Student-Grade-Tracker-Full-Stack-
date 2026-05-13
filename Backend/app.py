from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import os
import time

app = Flask(__name__)
CORS(app)

def get_db():
    retries = 5
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=os.environ.get("DB_HOST", "mysql"),
                user=os.environ.get("DB_USER", "root"),
                password=os.environ.get("DB_PASSWORD", "rootpass"),
                database=os.environ.get("DB_NAME", "gradesdb")
            )
            return conn
        except Exception as e:
            retries -= 1
            print(f"DB not ready, retrying... ({retries} left)")
            time.sleep(3)
    raise Exception("Could not connect to DB")

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            subject VARCHAR(100) NOT NULL,
            grade INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("DB initialized!")

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "grade-tracker-backend"})

@app.route("/api/students", methods=["GET"])
def get_students():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students ORDER BY created_at DESC")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(students)

@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, subject, grade) VALUES (%s, %s, %s)",
        (data["name"], data["subject"], data["grade"])
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"id": new_id, "message": "Student added!"}), 201

@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Deleted!"})

@app.route("/api/stats", methods=["GET"])
def get_stats():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total, AVG(grade) as avg_grade, MAX(grade) as top_grade FROM students")
    stats = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(stats)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)

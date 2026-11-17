from flask import Flask, render_template_string, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_NAME = os.environ.get("DATABASE_URL", "cloud_tasks.db")
APP_ENV = os.environ.get("APP_ENV", "Production")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT)''')
    conn.commit()
    conn.close()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Cloud Task Manager</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        input[type="text"] { width: 70%; padding: 10px; }
        button { padding: 10px 15px; background: #007bff; color: white; border: none; cursor: pointer; }
        ul { list-style: none; padding: 0; }
        li { background: #f4f4f4; margin: 5px 0; padding: 10px; border-radius: 4px; }
    </style>
</head>
<body>
    <h2>Cloud Task Manager ({{ env }})</h2>
    <form method="POST" action="/add">
        <input type="text" name="title" placeholder="Enter a new cloud task..." required>
        <button type="submit">Add Task</button>
    </form>
    <ul>
        {% for task in tasks %}
            <li>{{ task[1] }}</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, tasks=tasks, env=APP_ENV)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    if title:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        conn.commit()
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

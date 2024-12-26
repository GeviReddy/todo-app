from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace this with a random key

users = {"user": "password"}  # A simple user database
tasks = []

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('todos'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('todos'))
        else:
            return "Invalid username or password"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/todos', methods=['GET', 'POST'])
def todos():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        task = request.form['task']
        reminder_time = request.form['reminder']
        
        try:
            reminder_datetime = datetime.strptime(reminder_time, '%Y-%m-%d %H:%M')
            tasks.append((task, reminder_datetime))
        except ValueError:
            return "Invalid date/time format. Use YYYY-MM-DD HH:MM"
    
    return render_template('todos.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)

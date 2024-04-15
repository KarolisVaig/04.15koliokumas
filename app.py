from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# We will store tasks as a list of dictionaries
tasks = []

@app.route('/', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        session['user'] = request.form.get('user')
        return redirect(url_for('add_task'))
    return render_template('user.html')

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status')
        user = session.get('user', 'Anonymous')  # 'Anonymous' is a default value if 'user' isn't set
        tasks.append({'title': title, 'description': description, 'status': status, 'user': user})
        return redirect(url_for('view_tasks'))  # Redirect to view tasks
    return render_template('add_task.html')

@app.route('/tasks')
def view_tasks():  # Renamed function to avoid shadowing the 'tasks' list
    user = session.get('user')
    user_tasks = [task for task in tasks if task['user'] == user]
    return render_template('tasks.html', tasks=user_tasks, user=user)

@app.route('/update_status/<int:task_id>', methods=['POST'])
def update_status(task_id):
    new_status = request.form.get('status')
    if 0 <= task_id < len(tasks):
        tasks[task_id]['status'] = new_status
    return redirect(url_for('view_tasks'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for('view_tasks'))

if __name__ == '__main__':
    app.run(debug=True)

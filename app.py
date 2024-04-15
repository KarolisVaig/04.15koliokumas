from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for tasks
tasks = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Logic to add a new task
        title = request.form.get('title')
        description = request.form.get('description')
        tasks.append({'title': title, 'description': description, 'status': 'Not Completed', 'user': 'Anonymous'})
        return redirect(url_for('index'))
    return render_template('index.html', tasks=tasks)

@app.route('/update_status/<int:task_id>/<status>', methods=['POST'])
def update_status(task_id, status):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['status'] = status
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    state = db.Column(db.Boolean)
    description = db.Column(db.String(400))
    last_update = db.Column(db.DateTime)


@app.route('/', methods=['POST', 'GET'])
def index():
    tasks_done = Task.query.filter(Task.state == True). \
        order_by(Task.last_update.asc()).all()

    tasks_undone = Task.query.filter(Task.state == False). \
        order_by(Task.id.desc()).all()

    return render_template("index.html", tasks_done=tasks_done,
                           tasks_undone=tasks_undone)


@app.route('/update_task/<int:id>', methods=['POST'])
def update_task(id):
    task = Task.query.get(id)
    task.state = True if task.state==False else False
    task.last_update = datetime.now()
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/display_task/<int:id>', methods=['GET', 'POST'])
def display_task(id):
    task_to_display = Task.query.get(id)
    if not task_to_display:
        return "<h2>Task not found !</h2>"
    return render_template("display_task.html", task=task_to_display)


@app.route('/add_task', methods=['POST'])
def add_task():
    task_title = request.form['title']
    task_description = request.form['description']
    new_task = Task(title=task_title, description=task_description,
                    state=False, last_update=datetime.now())
    try:
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "Error while adding the new task!"


def prepopulate_db(db):
    if Task.query.first() is None:
        new_task1 = Task(title="Finish my todo list", state=True, last_update=datetime.now())
        new_task2 = Task(title="Call doctor", state=False, last_update=datetime.now(),
                         description="Make an appointment for next week")
        db.session.add_all([new_task1, new_task2])
        db.session.commit()
    pass
    return db


if __name__ == "__main__":
    db.create_all()
    db = prepopulate_db(db)
    app.run(debug=True)

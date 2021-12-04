
from flask import Flask, render_template
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

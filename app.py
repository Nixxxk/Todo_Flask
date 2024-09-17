from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key='WElldone'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICTIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
     serial_no = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(200), nullable=False)
     desc = db.Column(db.String(500), nullable=False)
     date_created = db.Column(db.DateTime, default = datetime.utcnow)

     def __repr__(self) -> str:
         return f'{self.serial_no} - {self.title}'
     


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        title= request.form["title"]
        desc= request.form["desc"]
        Made_it= Todo(title=title, desc=desc)
        db.session.add(Made_it)
        db.session.commit()

    allTodo=Todo.query.all()
    return render_template("index.html", allTodo=allTodo)

@app.route("/show")
def Products():
    allTodo=Todo.query.all()
    print(allTodo)
    return ("This is Products!")

@app.route("/update/<int:serial_no>", methods=['GET', 'POST'])
def update(serial_no):
    if request.method=='POST':
        title= request.form["title"]
        desc= request.form["desc"]
        todo=Todo.query.filter_by(serial_no= serial_no).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo=Todo.query.filter_by(serial_no= serial_no).first()
    return render_template("update.html", todo=todo)

@app.route("/delete/<int:serial_no>")
def delete(serial_no):
    todo=Todo.query.filter_by(serial_no= serial_no).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
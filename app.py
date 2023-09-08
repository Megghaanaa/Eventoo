from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Events.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    council = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(500), nullable=False)
    time = db.Column(db.String(500), nullable=False)
   


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        council = request.form['council']
        date = request.form['date']
        time = request.form['time']
        Events = Todo(title=title, desc=desc,council=council,date=date,time=time)
        db.session.add(Events)
        db.session.commit()
        
    allTodo = Todo.query.all() 
    return render_template('index.html', allTodo=allTodo)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        council = request.form['council']
        date = request.form['date']
        time = request.form['time']
        Events = Todo.query.filter_by(sno=sno).first()
        Events.title = title
        Events.desc = desc
        Events.council = council
        Events.date = date
        Events.time = time
        db.session.add(Events)
        db.session.commit()
        return redirect("/")
        
    Events = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', Events=Events)

@app.route('/delete/<int:sno>')
def delete(sno):
    Events = Todo.query.filter_by(sno=sno).first()
    db.session.delete(Events)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
from os import environ
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.secret_key = environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL').replace('postgres://', 'postgresql://', 1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=1)

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    list_id = db.Column("list_id", db.Integer)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route('/home')
def todo():
    incomplete = Todo.query.filter_by(complete=False, list_id=session["user_id"]).all()
    complete = Todo.query.filter_by(complete=True, list_id=session["user_id"]).all()

    return render_template('todo.html',
                           incomplete=incomplete,
                           complete=complete)


@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todoitem'],
                list_id=session["user_id"],
                complete=False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('todo'))


@app.route('/complete/<id>')
def complete(id):

    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()

    return redirect(url_for('todo'))


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        todo = Todo(list_id=None, text="", complete=True)
        db.session.add(todo)
        db.session.commit()
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(name=user).first()

        if found_user:
            session["email"] = found_user.email
            session["user_id"] = found_user._id
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()
            session["user_id"] = usr._id


        flash("You logged in successfully!")
        return redirect(url_for("profile"))
    else:
        if "user" in session:
            flash("Already logged in", "info")
            return redirect(url_for("profile"))
        return render_template("login.html")


@app.route("/profile", methods=["POST", "GET"])
def profile():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved.")
            return render_template("todo.html")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("profile.html", email=email)
    else:
        flash("You are not logged in.")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash("You have been logged out", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
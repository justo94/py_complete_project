from flask import Flask, render_template, request, flash, redirect, url_for, session
from config import *
from flask_bcrypt import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "154624"


@app.route('/home')
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("home.html")


@app.route('/users')
def users():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    users = User.select()
    return render_template("users.html", users=users)


@app.route('/delete/<int:id>')
def delete(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    User.delete().where(User.id == id).execute()
    flash('User deleted successfully')
    return redirect(url_for('users'))


@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    user = User.get(User.id == id)
    if request.method == "POST":
        updatedName = request.form["jina"]
        updatedEmail = request.form["arafa"]
        updatedPassword = request.form["siri"]
        user.name = updatedName
        user.email = updatedEmail
        user.password = updatedPassword
        user.password = generate_password_hash(updatedPassword)
        flash('Record updated successfully')
        return redirect(url_for('users'))
    return render_template("users.html",user=user)


@app.route('/', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["jina"]
        email = request.form["arafa"]
        password = request.form["siri"]
        password = generate_password_hash(password)
        User.create(name=name, email=email, password=password)
        flash("registration successful")
    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["arafa"]
        password = request.form["siri"]
        # Retrieve the user that matches the provided email
        try:
            user = User.get(User.email == email)
            hashedPassword = user.password
            if check_password_hash(hashedPassword, password):
                # Assign a session and redirect to home page
                session["email"] = email
                session["logged_in"] = True
                return redirect(url_for("index"))
            else:
                flash("Wrong email or password")
        except:
            flash("User does not exist")
    return render_template("login.html")


if __name__ == '__main__':
    app.run()
#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
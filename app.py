import os
from flask import (Flask, flash, render_template, 
        redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
if os.path.exists("env.py"):
    import env


# create instance of Flask
app = Flask(__name__)
# Setting environment variables
app.config["MONGO_DATABASE"] = os.environ.get("MONGO_DATABASE")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
# instance of mongo
mongo = PyMongo(app)


# ROUTES
# Tasks/ Home page (Both path points to same page)
@app.route('/')
@app.route('/get-tasks')
def get_tasks():
    tasks = list(mongo.db.tasks.find())
    return render_template("tasks.html", tasks=tasks)


# Register user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if the POST user exists in DB
        user_exists = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if user_exists:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("User Created!")
        return redirect(url_for('profile', username=session['user']))
    return render_template("register.html")


# Login
@app.route("/profile/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if the POST user exists in DB
        user_exists = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if user_exists:
            # ensure hashed password matches user input
            if check_password_hash(
                user_exists["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        'profile', username=session['user']))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


# user profile
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session['user'] or username == '':
        return render_template("profile.html", username=username)
    return redirect(url_for('login'))


# Logout
@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Add Task
@app.route("/add-task", methods=["GET", "POST"])
def add_task():
    if request.method == 'POST':
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        new_task = {
            "category_name": request.form.get("category_name"),
            "task_name": request.form.get("task_name"),
            "task_description": request.form.get("task_description"),
            "due_date": request.form.get("due_date"),
            "is_urgent": is_urgent,
            "created_by": session["user"],
            "created_at": datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        }
        mongo.db.tasks.insert_one(new_task)
        flash("New task added!")
        return redirect(url_for("get_tasks"))
    categories = mongo.db.categories.find().sort('category_name', 1)
    return render_template('add_task.html', categories=categories)


# Edit Task
@app.route("/edit-task/<task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    if request.method == 'POST':
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        task_to_update = {
            "category_name": request.form.get("category_name"),
            "task_name": request.form.get("task_name"),
            "task_description": request.form.get("task_description"),
            "due_date": request.form.get("due_date"),
            "is_urgent": is_urgent,
            "last_modified_by": session['user'],
            "last_modified_at": datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        }
        mongo.db.tasks.update(
            {"_id": ObjectId(task_id)}, {"$set": task_to_update})
        flash("Task Updated!")
        return redirect(url_for("get_tasks"))
    task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    categories = mongo.db.categories.find().sort('category_name', 1)
    return render_template('edit_task.html', task=task, categories=categories)


# Delete task
@app.route("/delete-task/<task_id>")
def delete_task(task_id):
    mongo.db.tasks.remove({"_id": ObjectId(task_id)})
    flash("Task Deleted!")
    return redirect(url_for("get_tasks"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)

import os
from flask import (Flask, flash, render_template, 
        redirect, request, session, url_for)
from flask_pymongo import PyMongo
if os.path.exists("env.py"):
    import env


# create instance of Flask
app = Flask(__name__)

app.config["MONGO_DATABASE"] = os.environ.get("MONGO_DATABASE")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.SECRET_KEY = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/get-tasks')
def get_tasks():
    tasks = mongo.db.tasks.find()
    return render_template("tasks.html", tasks=tasks)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)

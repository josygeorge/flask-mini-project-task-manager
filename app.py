import os
from flask import (Flask, flash, render_template, 
        redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


# create instance of Flask
app = Flask(__name__)
# Setting environment variables
app.config["MONGO_DATABASE"] = os.environ.get("MONGO_DATABASE")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.SECRET_KEY = os.environ.get("SECRET_KEY")
# instance of mongo
mongo = PyMongo(app)

# ROUTES
# Tasks/ Home page (Both path points to same page)
@app.route('/')
@app.route('/get-tasks')
def get_tasks():
    tasks = mongo.db.tasks.find()
    return render_template("tasks.html", tasks=tasks)


# Register
@app.route('/register', methods=['GET','POST'])
def register():
    return render_template('register.html')

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)

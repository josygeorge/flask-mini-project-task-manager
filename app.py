import os
from flask import Flask
if os.path.exists("env.py"):
    import env


# create instance of Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)

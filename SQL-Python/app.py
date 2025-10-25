from flask import Flask , render_template , Response, Request , globals

app = Flask(__name__)

app.route("/")
def home() -> Response:
    return "You Are On Home Page"
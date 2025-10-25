from flask import Flask , render_template , Response, Request , globals

app = Flask(__name__)

app.route("/", methods = ["GET", "POST"])
def home() -> Response:
    return "You are currently on home page"

app.route("/dashboard/student/information", methods = ["GET"])
def student_information() -> Response:
    return "This should display the student information"

app.route("/dashboard/teacher/information", methods = ["GET"])
def teacher_information() -> Response:
    return "This should display the teacher information"
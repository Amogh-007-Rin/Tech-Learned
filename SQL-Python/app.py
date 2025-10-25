from ast import main
from flask import Flask , render_template , Response, request , globals

app = Flask(__name__)

app.route("/")
def home() -> Response:
    return "You are currently on home page"

app.route("/dashboard/student/information")
def student_information() -> Response:
    return "This should display the student information"

app.route("/dashboard/teacher/information")
def teacher_information() -> Response:
    return "This should display the teacher information"

if __name__ == '__main__' :

    app.run(debug=True, host='0.0.0.0', port=5000)
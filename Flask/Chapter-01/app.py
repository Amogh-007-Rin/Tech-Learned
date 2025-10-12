# Importing flask library
from flask import Flask , Response

# Creating a flask object 
app = Flask(__name__)

# Creating a default home page route
@app.route("/") 
def home():
    return "Hello user! This is my first flask app"

# Creating a about page route
@app.route("/about")
def home():
    return "Hello user! This is my first flask app"

# Creating a contact page route
@app.route("/contact")
def home():
    return "Hello user! This is my first flask app"

# Creating a information page route
@app.route("/information")
def home():
    return "Hello user! This is my first flask app"


## IMPORTANT NOTES AND INSTRUCTIONS

# 01 : Always write the endpoints of route specific and complete use complete naming insted of using shortcut name.
# Example : Write /info is wrong convension insted use /information.

# 02 : Make your route end points uniques and dont repeat the same names for different endpoints.
# Example : @app.route("/user/information/one") function-01 and @app.router("/user/information") function-02 will hit same end point and backend my crash.

# 03 : Always remember to return a response even its nun or null. If you dont return a response the flask server may break.
# Example : @app.route("/admin") function-x is a bad code and the correct version of this is @app.route("/admin") function-x return "Admin is here".
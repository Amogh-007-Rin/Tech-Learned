# Importing flask library
from flask import Flask ,request, Response, globals, jsonify

# Creating a flask object 
app = Flask(__name__)

# Creating a default home page route
@app.route("/") 
def home():
    return "Hello user! This is my first flask app"

# Creating a about page route
@app.route("/about")
def about():
    return "Hello user! This is about page"

# Creating a contact page route
@app.route("/contact")
def contact():
    return "Hello user! This is contact page"

# Creating a information page route
@app.route("/information")
def information():
    return "Hello user! This is information page"

# Creating a route to get total request count
count = 0
@app.before_request
def request_count():
    global count
    count += 1

@app.route("/traffic/counter", methods=["GET"])
def request_counter() -> Response:
    return jsonify({
        "Total_Requests" : count
    })
    
## IMPORTANT NOTES AND INSTRUCTIONS

# 01 : Always write the endpoints of route specific and complete use complete naming insted of using shortcut name.
# Example : Write /info is wrong convension insted use /information.

# 02 : Make your route end points uniques and dont repeat the same names for different endpoints.
# Example : @app.route("/user/information/one") function-01 and @app.router("/user/information") function-02 will hit same end point and backend my crash.

# 03 : Always remember to return a response even its nun or null. If you dont return a response the flask server may break.
# Example : @app.route("/admin") function-x is a bad code and the correct version of this is @app.route("/admin") function-x return "Admin is here".

# 04 : By default the if methods are not mentioned the route requests will be considered as GET requests.
# Example : Given bellow :
# @app.route("/information")
# def information(): 
#     return "Hey coder you are on the information page"

# @app.route("/information", methods = ["GET"])
# def information() -> Response:
#     return "Hey coder you are on the information page"

# Both the routes are the same but the second one is mode detailed and more profassional way of writing the code. And its more preferable and industry standard to minimise errors and bugs.
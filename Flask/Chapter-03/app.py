from flask import Flask , Response , redirect , render_template, Request, globals

app = Flask(__name__)

valid_users = {
    "amogh" : "amoghdath233@gmail.com",
    "param" : "parampraman59@gmail.com",
    "akash" : "akashkr2005@gmail.com",
    "anupama" : "anupamamn1982@gmail.com"
}

@app.route("/login")
def login() -> Response :

    username = Request.form.get("username")
    password = Request.form.get("password")

    if(username in valid_users and password in valid_users["amogh"]):
        return render_template("index.html")
    else:
        return "Invalid Credentials"
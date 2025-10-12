from flask import Flask, request, Response, globals, jsonify, render_template

app = Flask(__name__)

@app.router("/Homepage", methods = ["GET"])
def home() -> Response:
    return render_template("index.html")
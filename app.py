#debug mode code: flask --debug run
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/page2")
def func1():
    return render_template("page2.html")
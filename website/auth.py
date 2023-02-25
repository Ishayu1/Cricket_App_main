from flask import Blueprint, render_template, redirect, url_for,request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail,Message

auth= Blueprint("auth",__name__)



@auth.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password is incorrect", category="error")
        else:
            flash("Email does not exist", category="error")
    return render_template("login.html")

@auth.route("/sign_up", methods=["GET","POST"])
def sign_up():
    if request.method == "POST": 
        #email = request.form.get("email")
        email = request.form["email"]
        password = request.form.get("password")
        password1 = request.form.get("password1")

        email_exists = User.query.filter_by(email=email).first()
        activate = []
        if email_exists:
            flash("Email is already in use", category="error")
            activate.append(0)
        if password != password1:
            flash("Passwords do not match", category="error")
            activate.append(0)
        if len(password) <8:
            flash("Password must be at least 8 characters", category="error")
            activate.append(0)
           
        if len(activate)==0:
            new_user = User(email=email, password= generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash("User created")
            login_user(new_user, remember=True)
            welcome_message = f'''
            <h3>Hello {email},welcome to the website</h3>
            '''
            mail.send(welcome_message)
        return redirect(url_for("views.home"))
        
        
    return render_template("sign_up.html")

@auth.route("/change_password")
def change_password():
    return render_template("change_password.html")
    

@auth.route("/sign_out")
@login_required 
def sign_out():
    logout_user()
    return redirect(url_for("views.home"))



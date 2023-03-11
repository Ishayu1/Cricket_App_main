from flask import Blueprint, render_template, redirect, url_for,request, flash
from . import db, mail
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from random import randint

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
            msg = Message("Registration", sender = "ishayu.ghosh@gmail.com", recipients=[email])
            msg.body = f'''
            <h3>Hello {email},welcome to the website</h3>
            '''
            try:
                mail.send(msg)
            except:
                flash("Email not sent, please check your settings", category="error")
            else:
                new_user = User(email=email, password= generate_password_hash(password, method="sha256"))
                db.session.add(new_user)
                db.session.commit()
                flash("User created")
                login_user(new_user, remember=True)
           
        return redirect(url_for("views.home"))
        
        
    return render_template("sign_up.html")

@auth.route("/change_password", methods=["GET","POST"])
def change_password():
    if request.method == "POST":
        email = request.form["email"]
        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            # add reset code for the user
            # the link will contain the reset code
            reset_code = randint(100000,1000000)
            email_exists.reset_code = reset_code
            db.session.commit()
            msg = Message("Change password", sender = "ishayu.ghosh@gmail.com", recipients=[email])
            msg.html = f'''
                <h3>Hello {email}, click the link to change password</h3>
                <a href="http://127.0.0.1:5000/reset_password/{reset_code}">Click here</a>
                ''' 
            
            try:
                mail.send(msg)
                flash("Email has been sent with a reset code", category="success")
            except:
                flash("Email not sent, please check your settings", category="error")
        else:
            flash("Email doesn't exist", category="error")

    return render_template("change_password.html")
    

@auth.route("/sign_out")
@login_required 
def sign_out():
    logout_user()
    return redirect(url_for("views.home"))

@auth.route("/reset_password/<int:reset_id>",  methods=["GET","POST"])
def reset_password(reset_id):
    reset_code_exists = User.query.filter_by(reset_code=reset_id).first()
    return render_template("reset_password.html",user=reset_code_exists)

@auth.route("/reset_password_confirm", methods = ["GET","POST"])
def reset_password_confirm():
    if request.method=="POST":
        password = request.form["password"]
        email = request.form["email"]
        password1 = request.form["password1"]
        activate = []
        if password != password1:
            flash("Passwords do not match", category="error")
            activate.append(0)
        if len(password) <8:
            flash("Password must be at least 8 characters", category="error")
            activate.append(0)
        if len(activate)==0:
            update_user = User.query.filter_by(email=email).first()
            update_user.password = generate_password_hash(password, method="sha256")
            update_user.reset_code = None
            db.session.commit()
            flash("Password has been reset",category="success")
            return render_template("login.html")
    else:
        return render_template("login.html")
            #update password in database and remove reset code


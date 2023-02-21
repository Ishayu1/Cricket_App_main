from flask import Blueprint, render_template, redirect, url_for

auth= Blueprint("auth",__name__)

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

@auth.route("/sign_out")
def sign_out():
    return redirect(url_for("views.home"))

# #
#  <nav class = "navbar navbar-expanded-lg navbar-dark bg-dark">
#     <div class ="container-fluid">
#       <button 
#       class="navbar-toggler"
#       type="button"
#       data-bs-toggle="collapse" 
#       data-bs-target="#navbar"
#       >
#         <span class="navbar-toggler-icon"></span>
#       </button>
#       <div class="collapse navbar-collapse" id="navbar">
#         <div class="navbar-nav">
#           <a class="nav-item nav-link" href="/home">Home</a>
#           <a class="nav-item nav-link" href="/login">Login</a>
#           <a class="nav-item nav-link" href="/sign_up">Sign Up</a>
#         </div>
#     </div>
#   </nav>

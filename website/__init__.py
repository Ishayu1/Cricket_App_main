from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail,Message
db = SQLAlchemy()     
DB_NAME = "database.db"
def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "210606"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = ''
    app.config['MAIL_PASSWORD'] = 'wpkgxtebqcfvcapu'
    app.config['MAIL_DEFAULT_SENDER'] = ''
    mail = Mail(app)
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    with app.app_context():
        db.create_all()



    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

        
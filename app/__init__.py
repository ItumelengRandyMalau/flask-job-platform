from flask import Flask
from flask_login import LoginManager
from mongoengine import connect

app = Flask(__name__)
app.secret_key = "supersecretkey"

# MongoDB connection
connect(
    db="jobhub_db",
    host="mongodb+srv://itumeleng:Itumeleng1.@cluster0.3klnl.mongodb.net/"
)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Import models
from .models import User


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


# Import routes
from app import routes
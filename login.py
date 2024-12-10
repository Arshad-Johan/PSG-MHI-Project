from flask import render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from passw import password

login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Hardcoded user (replace with database lookup for real applications)
users = {"admin": User(id=1, username="admin", password="password123")}

# Load user function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Function to initialize the login manager with the Flask app
def init_login(app):
    login_manager.init_app(app)

# Route for login page
def login_view():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users.get(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")
    
    return render_template("login.html")

# Route for dashboard (only accessible to authenticated users)
@login_required
def dashboard_view():
    return render_template("dashboard.html")

# Route for logging out
@login_required
def logout_view():
    logout_user()
    return redirect(url_for("login"))

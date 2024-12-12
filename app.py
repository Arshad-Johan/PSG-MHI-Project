from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from mailjet_rest import Client
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from pathlib import Path
import os
import re
import time
import threading
import random
import logging
from itsdangerous import URLSafeTimedSerializer

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(MONGO_URI)
    db = client["MACHINESDATA"]
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

users_collection = db["Users"]
data_collection = db["JabbalsMachine"]

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_view"

logging.basicConfig(level=logging.INFO)

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({"username": user_id})
    if user_data:
        return User(id=user_data["_id"], username=user_data["username"], password=user_data["password"])
    return None

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login_view():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard_view"))
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user_data = users_collection.find_one({"username": username})
        if user_data and check_password_hash(user_data["password"], password):
            user = User(id=user_data["_id"], username=user_data["username"], password=user_data["password"])
            login_user(user)
            return redirect(url_for("dashboard_view"))
        else:
            flash("Invalid username or password", "danger")
    
    return render_template("login.html")

serializer = URLSafeTimedSerializer(app.secret_key)

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["username"]
        user_data = users_collection.find_one({"username": email})
        
        if user_data:
            # Generate reset token
            token = serializer.dumps(email, salt="password-reset-salt")
            reset_url = url_for("reset_password", token=token, _external=True)

            # Send the reset link via email
            if send_reset_email(email, reset_url):
                flash("A password reset link has been sent to your email.", "info")
            else:
                flash("Failed to send reset email. Please try again.", "danger")
        else:
            flash("No account found with that email address.", "danger")
    
    return render_template("forgot_password.html")


@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = serializer.loads(token, salt="password-reset-salt", max_age=3600)  # Token expires in 1 hour
    except Exception:
        flash("The reset link is invalid or has expired.", "danger")
        return redirect(url_for("forgot_password"))
    
    if request.method == "POST":
        new_password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:
            flash("Passwords do not match.", "danger")
        else:
            hashed_password = generate_password_hash(new_password)
            users_collection.update_one({"username": email}, {"$set": {"password": hashed_password}})
            flash("Your password has been reset. You can now log in.", "success")
            return redirect(url_for("login_view"))

    return render_template("reset_password.html", token=token)

def send_reset_email(email, reset_url):
    """Function to send the password reset email."""
    try:
        mailjet = Client(auth=(os.getenv("MAILJET_API_KEY"), os.getenv("MAILJET_API_SECRET")), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {"Email": os.getenv("MAILJET_SENDER"), "Name": "MachineData"},
                    "To": [{"Email": email, "Name": "User"}],
                    "Subject": "Password Reset Request",
                    "TextPart": f"Click the link below to reset your password:\n{reset_url}\nThis link will expire in 1 hour.",
                }
            ]
        }
        result = mailjet.send.create(data=data)
        return result.status_code == 200
    except Exception as e:
        logging.error(f"Error sending reset email: {e}")
        return False

@app.route("/signup", methods=["GET", "POST"])
def signup_view():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not re.match(r"^[a-zA-Z0-9._%+-]+@psgtech\.ac\.in$", username):
            flash("Email must be a valid PSG Tech Email", "danger")
            return render_template("signup.html")

        if users_collection.find_one({"username": username}):
            flash("Email already registered. Please log in.", "danger")
            return render_template("signup.html")

        otp = random.randint(100000, 999999)
        session.update({"otp": otp, "temp_email": username, "temp_password": password})

        if send_otp(username, otp):
            flash("An OTP has been sent to your email. Please verify to complete signup.", "info")
            return redirect(url_for("verify_otp_view"))
        else:
            flash("Failed to send OTP. Please try again later.", "danger")
            return render_template("signup.html")

    return render_template("signup.html")

@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp_view():
    if request.method == "POST":
        entered_otp = request.form["otp"]

        if str(session.get("otp")) == entered_otp:
            hashed_password = generate_password_hash(session["temp_password"])
            new_user = {"username": session["temp_email"], "password": hashed_password}
            users_collection.insert_one(new_user)

            session.pop("otp", None)
            session.pop("temp_email", None)
            session.pop("temp_password", None)

            flash("Account verified and created successfully. Please log in.", "success")
            return redirect(url_for("login_view"))
        else:
            flash("Invalid OTP. Please try again.", "danger")

    return render_template("verify_otp.html")

@app.route("/dashboard")
@login_required
def dashboard_view():
    return render_template("dashboard.html")

@app.route("/logout")
@login_required
def logout_view():
    logout_user()
    return redirect(url_for("login_view"))

def send_otp(email, otp):
    try:
        mailjet = Client(auth=(os.getenv("MAILJET_API_KEY"), os.getenv("MAILJET_API_SECRET")), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {"Email": os.getenv("MAILJET_SENDER"), "Name": "MachineData"},
                    "To": [{"Email": email, "Name": "User"}],
                    "Subject": "Signup OTP Verification",
                    "TextPart": f"Your OTP for signup is: {otp}",
                }
            ]
        }
        result = mailjet.send.create(data=data)
        return result.status_code == 200
    except Exception as e:
        logging.error(f"Error sending email via Mailjet: {e}")
        return False

def parse_text_file(file_path):
    """Parse the given text file and return a list of dictionaries."""
    with open(file_path, "r") as file:
        lines = file.readlines()

    data_list = []
    for line in lines:
        values = re.split(r'\s*,\s*|\s+', line.strip())
        data_dict = {
            "serial number": values[0],
            "date": values[1],
            "surge error": values[2],
            "machine-model": values[3],
            "tests": []
        }
        current_test = []
        for value in values[4:]:
            if value.upper() == "N/A":
                continue
            current_test.append(value)
            if value.lower() in ["pass", "fail"]:
                data_dict["tests"].append(" ".join(current_test))
                current_test = []
        if current_test:
            data_dict["tests"].append(" ".join(current_test))
        data_list.append(data_dict)
    return data_list

def update_database(file_path):
    """Parse the file and update the database."""
    try:
        parsed_data_list = parse_text_file(file_path)
        for parsed_data in parsed_data_list:
            data_collection.update_one(
                {"serial number": parsed_data["serial number"]},
                {"$set": parsed_data},
                upsert=True
            )
        logging.info("Database updated successfully!")
    except Exception as e:
        logging.error(f"Error updating database: {e}")

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def on_modified(self, event):
        if Path(event.src_path) == self.file_path:
            logging.info(f"Detected changes in {self.file_path}. Updating database...")
            update_database(self.file_path)

def monitor_file(file_path):
    event_handler = FileChangeHandler(file_path)
    observer = Observer()
    observer.schedule(event_handler, path=str(file_path.parent), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    file_path = Path("data.txt")
    threading.Thread(target=monitor_file, args=(file_path,), daemon=True).start()
    app.run(port=5001, debug=True)
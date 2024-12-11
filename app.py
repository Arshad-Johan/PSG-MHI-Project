from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from passw import password, apikey, secretkey, gmail
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import threading
import random
from mailjet_rest import Client

# MongoDB connection setup
uri = f"mongodb+srv://chinnadeva46:{password()}@psg-mhi.zqbza.mongodb.net/?retryWrites=true&w=majority&appName=PSG-MHI"
client = MongoClient(uri)
db = client["MACHINESDATA"]
users_collection = db["Users"]  # This is where we will store users
data_collection = db["JabbalsMachine"]
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for session management

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    # Load the user from the Users collection using the user_id (which could be the username)
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

        # Retrieve user from MongoDB
        user_data = users_collection.find_one({"username": username})
        if user_data and user_data["password"] == password:
            user = User(id=user_data["_id"], username=user_data["username"], password=user_data["password"])
            login_user(user)
            return redirect(url_for("dashboard_view"))
        else:
            flash("Invalid username or password", "danger")
    
    return render_template("login.html")

# Mailjet API Configuration
MAILJET_API_KEY = apikey()  # Replace with your Mailjet API key
MAILJET_API_SECRET = secretkey()  # Replace with your Mailjet API secret
MAILJET_SENDER = gmail()  # Replace with your verified Mailjet sender email

def send_otp(email, otp):
    """Send OTP using Mailjet."""
    try:
        mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_API_SECRET), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": MAILJET_SENDER,
                        "Name": "MachineData"
                    },
                    "To": [
                        {
                            "Email": email,
                            "Name": "User"
                        }
                    ],
                    "Subject": "Signup OTP Verification",
                    "TextPart": f"Your OTP for signup is: {otp}",
                }
            ]
        }
        result = mailjet.send.create(data=data)
        if result.status_code == 200:
            return True
        else:
            print(f"Mailjet error: {result.status_code}, {result.json()}")
            return False
    except Exception as e:
        print(f"Error sending email via Mailjet: {e}")
        return False
    
@app.route("/signup", methods=["GET", "POST"])
def signup_view():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Step 1: Validate email format
        if not re.match(r"^[a-zA-Z0-9._%+-]+@psgtech\.ac\.in$", email):
            flash("Email must be a valid PSG Tech Email", "danger")
            return render_template("signup.html")

        # Step 2: Check if the email already exists in the database
        if users_collection.find_one({"email": email}):
            flash("Email already registered. Please log in.", "danger")
            return render_template("signup.html")

        # Step 3: Generate and send OTP
        otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
        session["otp"] = otp
        session["temp_email"] = email
        session["temp_password"] = password

        if send_otp(email, otp):
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

        # Check if OTP matches
        if "otp" in session and str(session["otp"]) == entered_otp:
            # Store the user in the MongoDB Users collection
            new_user = {
                "email": session["temp_email"],
                "password": session["temp_password"]  # Store plain-text password (consider hashing)
            }
            users_collection.insert_one(new_user)

            # Clear the session data
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

def parse_text_file(file_path):
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

        tests_start_index = 4
        current_test = []
        i = tests_start_index

        while i < len(values):
            if values[i].upper() == "N/A":
                i += 1
                continue

            if values[i].lower() in ["pass", "fail"]:
                current_test.append(f"{values[i]}")

            else:
                current_test.append(values[i])

            if len(current_test) > 1 and (current_test[-1].lower() in ["pass", "fail"]):
                data_dict["tests"].append(" ".join(current_test))
                current_test = [] 

            i += 1

        if current_test:
            data_dict["tests"].append(" ".join(current_test))

        data_list.append(data_dict)

    return data_list

def update_database(file_path):
    parsed_data_list = parse_text_file(file_path)
    for parsed_data in parsed_data_list:
        data_collection.update_one(
            {"serial number": parsed_data["serial number"]},
            {"$set": parsed_data},
            upsert=True
        )
    print("Documents updated successfully!")

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = file_path

    def on_modified(self, event):
        if event.src_path.endswith(self.file_path):
            print(f"Detected changes in {self.file_path}. Updating database...")
            update_database(self.file_path)

def monitor_file(file_path):
    event_handler = FileChangeHandler(file_path)
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)  
    observer.start()

    print(f"Monitoring {file_path} for changes. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1) 
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def start_monitoring():
    file_path = "data.txt"
    update_database(file_path)
    monitor_thread = threading.Thread(target=monitor_file, args=(file_path,))
    monitor_thread.daemon = True
    monitor_thread.start()

start_monitoring()

if __name__ == '__main__':
    app.run(port=5001, debug=True)

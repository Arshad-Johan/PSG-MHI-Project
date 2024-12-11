from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from passw import password
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import threading

# MongoDB connection setup
uri = f"mongodb+srv://chinnadeva46:{password()}@psg-mhi.zqbza.mongodb.net/?retryWrites=true&w=majority&appName=PSG-MHI"
client = MongoClient(uri)
db = client["MACHINESDATA"]
collection = db["JabbalsMachine"]

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for session management

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Hardcoded user (replace with database lookup for real applications)
users = {"admin": User(id=1, username="admin", password="password123")}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route("/login", methods=["GET", "POST"])
def login_view():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard_view"))
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users.get(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("dashboard_view"))
        else:
            flash("Invalid username or password", "danger")
    
    return render_template("login.html")

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
        collection.update_one(
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

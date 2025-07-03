from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from bson import ObjectId
from app import app, login_manager, users_collection, data_collection
from app.utils import send_reset_email, send_otp, convert_objectid_to_str
from app.models import User
import re
import random

serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(id=str(user_data["_id"]), username=user_data["username"], password=user_data["password"])
    return None

@app.route("/", methods=["GET"])
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard_view"))
    return redirect(url_for("login_view"))

@app.route("/login", methods=["GET", "POST"])
def login_view():
    if current_user.is_authenticated:
        return redirect(url_for("mainpage"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_data = users_collection.find_one({"username": username})
        if user_data and check_password_hash(user_data["password"], password):
            user = User(
                id=str(user_data["_id"]),
                username=user_data["username"],
                password=user_data["password"],
            )
            login_user(user)
            return redirect(url_for("mainpage"))

    return render_template("index.html")


@app.route("/mainpage", methods=["GET"])
@login_required
def mainpage():
    # Perform any necessary actions after login here
    # For example, you can log the login event, update user status, etc.
    print(f"User {current_user.username} has logged in.")

    # Redirect to the dashboard
    return render_template("mainpage.html")

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        username = request.form["username"]
        user_data = users_collection.find_one({"username": username})
        
        if user_data:
            token = serializer.dumps(username, salt="password-reset-salt")
            reset_url = url_for("reset_password", token=token, _external=True)

            send_reset_email(username, reset_url)
    
    return render_template("forgot_password.html")

@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = serializer.loads(token, salt="password-reset-salt", max_age=3600) 
    except Exception:
        return redirect(url_for("forgot_password"))
    
    if request.method == "POST":
        new_password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if new_password == confirm_password:
            hashed_password = generate_password_hash(new_password)
            users_collection.update_one({"username": email}, {"$set": {"password": hashed_password}})
            return redirect(url_for("login_view"))

    return render_template("reset_password.html", token=token)

@app.route("/signup", methods=["GET", "POST"])
def signup_view():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]


        if not re.match(r"^[a-zA-Z0-9._%+-]+@psgtech\.ac\.in$", username):
            return render_template("signup.html", error="Invalid email format")

        if users_collection.find_one({"username": username}):
            return render_template("signup.html", error="User already exists")

        otp = random.randint(100000, 999999)
        session.update({"otp": otp, "temp_email": username, "temp_password": password})

        send_otp(username, otp)
        return redirect(url_for("verify_otp_view"))

    return render_template("signup.html")


@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp_view():
    if request.method == "POST":
        entered_otp = request.form["otp"]

        if str(session.get("otp")) == entered_otp:
            hashed_password = generate_password_hash(session["temp_password"])
            new_user = {
                "username": session["temp_email"],
                "password": hashed_password,
            }
            users_collection.insert_one(new_user)

            session.pop("otp", None)
            session.pop("temp_email", None)
            session.pop("temp_password", None)

            return redirect(url_for("login_view"))

    return render_template("verify_otp.html")


@app.route("/logout")
@login_required
def logout_view():
    logout_user()
    return redirect(url_for("login_view"))

@app.route("/dashboard")
@login_required
def dashboard_view():
    motor_data = list(data_collection.find())
    motor_data = [convert_objectid_to_str(doc) for doc in motor_data]
    return render_template(
        "dashboard.html", motor_data=motor_data, username=current_user.username
    )


@app.route("/machines_data", methods=["GET"])
@login_required
def machines_data():
    motor_data = list(data_collection.find())
    motor_data = [convert_objectid_to_str(doc) for doc in motor_data]
    return jsonify(motor_data)


@app.route("/armature_winding_data", methods=["GET"])
@login_required
def armature_winding_data():
    try:
        import pandas as pd
        import os
        
        # Read the CSV file
        csv_path = "Hot_Stacking_Data.csv"
        if not os.path.exists(csv_path):
            return jsonify({"error": "CSV file not found"}), 404
        
        # Read CSV with pandas
        df = pd.read_csv(csv_path, header=None)
        
        # Define column names based on the data structure
        columns = ['Timestamp', 'DataType', 'Value1', 'Value2', 'Value3', 'Value4', 'Value5', 'Value6', 'Value7', 'Value8', 'Value9', 'Value10', 'ArrayData']
        df.columns = columns[:len(df.columns)]
        
        # Convert DataFrame to list of dictionaries
        data = []
        for index, row in df.iterrows():
            row_dict = {}
            for col in df.columns:
                if pd.isna(row[col]):
                    row_dict[col] = None
                else:
                    row_dict[col] = str(row[col])
            data.append(row_dict)
        
        return render_template("armature_winding_data.html", data=data, username=current_user.username)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("login_view"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/admin-panel")
@login_required
@admin_required
def admin_panel():
    return render_template("admin_panel.html")

import os
import re
import time
import threading
import random
import logging
from mailjet_rest import Client
from itsdangerous import URLSafeTimedSerializer
from bson import ObjectId
from app import data_collection  # Ensure this import is correct
from pathlib import Path

def send_reset_email(email, reset_url):
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
        mailjet.send.create(data=data)
    except Exception as e:
        logging.error(f"Error sending reset email: {e}")

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
        mailjet.send.create(data=data)
    except Exception as e:
        logging.error(f"Error sending email via Mailjet: {e}")

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

def convert_objectid_to_str(data):
    if isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    return data

def monitor_file(file_path):
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class FileChangeHandler(FileSystemEventHandler):
        def __init__(self, file_path):
            self.file_path = Path(file_path)

        def on_modified(self, event):
            if Path(event.src_path) == self.file_path:
                logging.info(f"Detected changes in {self.file_path}. Updating database...")
                update_database(self.file_path)

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
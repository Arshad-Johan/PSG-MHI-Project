from flask import Flask
from pymongo import MongoClient
from passw import password
import pymongo
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import threading

uri = f"mongodb+srv://chinnadeva46:{password()}@psg-mhi.zqbza.mongodb.net/?retryWrites=true&w=majority&appName=PSG-MHI"
client = MongoClient(uri)
db = client["MACHINESDATA"]
collection = db["JabbalsMachine"]

app = Flask(__name__)

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
    monitor_thread = threading.Thread(target=monitor_file, args=("data.txt",))
    monitor_thread.daemon = True
    monitor_thread.start()

start_monitoring()

if __name__ == '__main__':
    app.run(port=5001, debug=True)

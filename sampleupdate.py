import pymongo
import re
from passw import password
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

# Connect to MongoDB
uri = f"mongodb+srv://chinnadeva46:{password()}@psg-mhi.zqbza.mongodb.net/?retryWrites=true&w=majority&appName=PSG-MHI"
client = pymongo.MongoClient(uri)
db = client["MACHINESDATA"]
collection = db["JabbalsMachine"]

# Function to read and parse the text file
def parse_text_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    data_list = []

    for line in lines:
        # Split values by comma, spaces, or both
        values = re.split(r'\s*,\s*|\s+', line.strip())
        
        # Base dictionary for fixed fields
        data_dict = {
            "serial number": values[0],
            "date": values[1],
            "surge error": values[2],
            "machine-model": values[3],
            "tests": []
        }

        # Start reading from the 4th index onwards for tests
        tests_start_index = 4
        current_test = []
        i = tests_start_index

        while i < len(values):
            # Skip `N/A` values
            if values[i].upper() == "N/A":
                i += 1
                continue

            # Check if current value is a pass/fail
            if values[i].lower() in ["pass", "fail"]:
                # Add pass/fail test result
                current_test.append(f"{values[i]}")

            else:
                # Add non-pass/fail value to test
                current_test.append(values[i])

            # If we have a completed test that ends with pass or fail
            if len(current_test) > 1 and (current_test[-1].lower() in ["pass", "fail"]):
                data_dict["tests"].append(" ".join(current_test))
                current_test = []  # Reset for the next test

            i += 1

        # Add any incomplete test that doesn't end with pass or fail (optional)
        if current_test:
            data_dict["tests"].append(" ".join(current_test))

        data_list.append(data_dict)

    return data_list

# Function to update MongoDB with parsed data
def update_database(file_path):
    parsed_data_list = parse_text_file(file_path)
    for parsed_data in parsed_data_list:
        collection.update_one(
            {"serial number": parsed_data["serial number"]},
            {"$set": parsed_data},
            upsert=True
        )
    print("Documents updated successfully!")

# File system event handler
class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = file_path

    def on_modified(self, event):
        if event.src_path.endswith(self.file_path):
            print(f"Detected changes in {self.file_path}. Updating database...")
            update_database(self.file_path)

# Monitor the file for changes
def monitor_file(file_path):
    event_handler = FileChangeHandler(file_path)
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)  # Monitor the current directory
    observer.start()

    print(f"Monitoring {file_path} for changes. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# File path to monitor
file_path = "data.txt"

# Perform the initial update before starting to monitor for changes
update_database(file_path)

# Now, monitor for changes
monitor_file(file_path)

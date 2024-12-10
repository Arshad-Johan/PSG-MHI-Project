import pymongo
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from passw import password
class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, collection):
        self.collection = collection

    def on_modified(self, event):
        if event.src_path == "data.txt":
            with open("data.txt", "r") as file:
                data = file.read()
            parsed_data = json.loads(data)
            self.collection.update_one(
                {"_id": parsed_data["id"]},
                {"$set": parsed_data}
            )
            print("Document updated successfully!")

def main():
    uri = f"mongodb+srv://chinnadeva46:{password()}@psg-mhi.zqbza.mongodb.net/?retryWrites=true&w=majority&appName=PSG-MHI"
    # Connect to MongoDB
    client = pymongo.MongoClient(uri)
    db = client["MACHINESDATA"]
    collection = db["JabbalsMachine"]
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    print("Connection successful!") if client else print("Connection failed!")

    # Set up the event handler and observer
    event_handler = FileChangeHandler(collection)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)

    # Start the observer
    observer.start()
    print("Monitoring changes to data.txt...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()

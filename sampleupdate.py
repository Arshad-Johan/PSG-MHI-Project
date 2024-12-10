import pymongo
import json
import re
from passw import password
# Connect to MongoDB
uri = f"mongodb+srv://chinnadeva46:{password()}@psg-mhi.zqbza.mongodb.net/?retryWrites=true&w=majority&appName=PSG-MHI"
# Connect to MongoDB
client = pymongo.MongoClient(uri)
db = client["MACHINESDATA"]
collection = db["JabbalsMachine"]

# Function to read and parse the text file
def parse_text_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Define the keys to update
    keys = ["serial number", "date", "surge error", "machine-model", "last tests"]
    data_list = []

    for line in lines:
        values = re.split(r',\s+|\s{2,}', line.strip())
        data_dict = {
            "serial number": values[0],
            "date": values[1],
            "surge error": values[2],
            "machine-model": values[3],
            "tests": []
        }

        tests_start_index = 4
        for i in range(tests_start_index, len(values), 2):
            if i + 1 < len(values):
                test_value = f"{values[i]} {values[i+1]}"
                data_dict["tests"].append(test_value)
            else:
                data_dict["tests"].append(values[i])

        data_list.append(data_dict)

    return data_list

# Read and parse the text file
file_path = "data.txt"
parsed_data_list = parse_text_file(file_path)

# Update the documents in MongoDB
for parsed_data in parsed_data_list:
    collection.update_one(
        {"serial number": parsed_data["serial number"]},
        {"$set": parsed_data},
        upsert=True
    )

print("Documents updated successfully!")

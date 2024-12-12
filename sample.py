from pymongo import MongoClient
import os
from dotenv import load_dotenv

MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(MONGO_URI)
    print("Connection successful")
except Exception as e:
    print(f"Connection failed: {e}")

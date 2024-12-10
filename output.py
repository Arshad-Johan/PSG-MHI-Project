from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps
from passw import password
app = Flask(__name__)
uri = f"mongodb+srv://chinnadeva46:{password()}@psg-mhi.zqbza.mongodb.net/?retryWrites=true&w=majority&appName=PSG-MHI"
client = MongoClient(uri)
db = client['MACHINESDATA']
collection = db['JabbalsMachine']
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

if __name__ == '__main__':
    app.run(port=5001, debug = True)
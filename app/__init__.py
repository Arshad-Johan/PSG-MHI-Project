from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_view"

client = MongoClient(app.config["MONGO_URI"])

db = client["MACHINESDATA"]
users_collection = db["Users"]
data_collection = db["JabbalsMachine"]



from app import routes
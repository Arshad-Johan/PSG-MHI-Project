from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps
from passw import password
app = Flask(__name__)
uri = f"mongodb+srv://chinnadeva46:{password()}@psg-mhi.zqbza.mongodb.net/?retryWrites=true&w=majority&appName=PSG-MHI"
client = MongoClient(uri)
db = client['sample_mflix']
collection = db['movies']
print("hi")
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        user = request.json
        insert_result = collection.insert_one(user) # Retrieve the newly inserted document
        new_user = collection.find_one({'_id': insert_result.inserted_id}) # Return the inserted document using bson.json_util.dumps for serialization
        return jsonify(dumps(new_user)), 201
    except Exception as e:
        return jsonify({"error": str(e)}),400

@app.route('/users', methods=['GET'])
def get_users():
    query = {
'fullplot':
"Julio Madariaga is the Argentine patriarch of a wealthy family. He has two daughters, the elder wed to a Frenchman and the other to a German. He prefers the Frenchman and his family, especially his grandson Julio, causing jealousy from the German and his three sons. When Madariaga dies, the family splits up, each son-in-law returning to his own country. The Frenchman and his own move to Paris, where Julio becomes an artist and has an affair with an unhappily married woman, the lovely Marguerite Laurier. Her husband finds out, but before he can finalize a divorce, World War One rears its head and both sides of the family will endure great suffering in the conflict, especially since they must fight one another on the battlefield."}
    users = list(collection.find(query, {'_id': 0}))
   
    return jsonify((users))


if __name__ == '__main__':
    app.run(port=5001, debug = True)
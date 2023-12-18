from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS from flask_cors
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Connect to MongoDB
client = MongoClient('mongodb+srv://chirazgouissem:password@cluster0.v10j47f.mongodb.net/')
db = client['iot']
collection = db['detection_collection']

@app.route('/detections', methods=['GET'])
def get_detections():
    # Retrieve data from MongoDB
    detections = list(collection.find({}, {'_id': 0}))

    return jsonify({'detections': detections})

@app.route('/last_detection', methods=['GET'])
def get_last_detection():
    # Retrieve the last saved data using the highest timestamp
    last_detection = collection.find_one(sort=[('timestamp', -1)], projection={'_id': 0})

    return jsonify({'last_detection': last_detection})

if __name__ == '__main__':
    app.run(debug=True)



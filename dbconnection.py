import json
import paho.mqtt.client as mqtt
from pymongo import MongoClient

# MQTT settings
mqtt_broker = "localhost"  # MQTT broker address
mqtt_topic = "yolo_detection"

# MongoDB settings
mongo_host = "mongodb+srv://chirazgouissem:password@cluster0.v10j47f.mongodb.net/"  # Replace with your MongoDB server address
mongo_port = 27017
mongo_database = "iot"
mongo_collection = "detection_collection"

# Connect to MongoDB
mongo_client = MongoClient(mongo_host, mongo_port)
mongo_db = mongo_client[mongo_database]
mongo_coll = mongo_db[mongo_collection]

try:
    # MQTT on_connect callback
    def on_connect(client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")
        client.subscribe(mqtt_topic)
        

    # MQTT on_message callback
    def on_message(client, userdata, msg):
        payload = json.loads(msg.payload.decode())
        print(f"Received MQTT message: {payload}")
        
        try:
            # Insert the payload into MongoDB
            mongo_coll.insert_one(payload)
            print(f"Inserted data into MongoDB: {payload}")
        
        except Exception as e:
            print(f"Error inserting data into MongoDB: {e}")

    # Create MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to MQTT broker
    client.connect(mqtt_broker, 1883, 60)

    # Start the MQTT loop
    #client.loop_forever()

    def save_to_mongodb(data):
        # Insert data into MongoDB collection
        mongo_coll.insert_one(data)


except Exception as e:
    print(f"Error: {e}")
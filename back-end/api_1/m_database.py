from pymongo import MongoClient
import pymongo
import urllib 
import os
from dotenv import load_dotenv
import certifi

load_dotenv()


# Get MongoDB URI components from the config file under the [mongodb] section
mongo_username = os.getenv('mongo_username')
mongo_password = os.getenv('mongo_password')
mongo_cluster = os.getenv('mongo_cluster')

# Construct MongoDB URI with proper escaping
mongo_url = f'mongodb+srv://{urllib.parse.quote_plus(mongo_username)}:{urllib.parse.quote_plus(mongo_password)}@{mongo_cluster}/?retryWrites=true&w=majority'

# Initialize the MongoClient with the MongoDB URI
client = pymongo.MongoClient(mongo_url,tlsCAFile=certifi.where())

try:
    conn = client.server_info()
    print(f'Connected to MongoDB {conn.get("version")}')
except Exception:
    print("Unable to connect to the MongoDB server.")

db = client['BigDataAssignment4']

User_token = db.user_tokens
User_token.create_index([("email", pymongo.ASCENDING)], unique=True)

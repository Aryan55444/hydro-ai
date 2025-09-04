from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/water_quality")
client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

db_name = 'project_history'
db = client[db_name]
history_collection = "query_history"

def log_query(query_type, query_params, user_id=None):
    log_entry = {
        "timestamp": datetime.utcnow(),
        "query_type": query_type,
        "query_params": query_params,
        "user_id": user_id
    }
    return db[history_collection].insert_one(log_entry).inserted_id

def get_recent_queries(user_id=None, limit=10):
    query = {"user_id": user_id} if user_id else {}
    return list(db[history_collection]
               .find(query)
               .sort("timestamp", -1)
               .limit(limit))

def clear_history(user_id=None):
    query = {"user_id": user_id} if user_id else {}
    return db[history_collection].delete_many(query)
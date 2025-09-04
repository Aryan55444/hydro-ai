from pymongo import MongoClient
from dotenv import load_dotenv
import os
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))

from app.database.db import client, db

load_dotenv()

client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
db = client.get_default_database()
print(f"✅ Connected to database: {db.name}")

try:
    client.admin.command('ismaster')
    print("✅ Database connection is working")
    
    print(f"\nCollections in {db.name}:")
    for collection in db.list_collection_names():
        print(f"- {collection}")
    
    print("\nAvailable databases:")
    for db_name in client.list_database_names():
        print(f"- {db_name}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    
finally:
    client.close()

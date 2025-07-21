from pymongo import MongoClient

MONGO_USERNAME = "mongoadmin"
MONGO_PASSWORD = "secret"
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB_NAME = "amazon_ratings"
MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}?authSource=admin"

def get_mongo_client():
    return MongoClient(MONGO_URI)

def get_mongo_db():
    client = get_mongo_client()
    return client[MONGO_DB_NAME] 
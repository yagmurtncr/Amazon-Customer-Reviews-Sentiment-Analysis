from pymongo import MongoClient

# MongoDB'ye bağlan
client = MongoClient("mongodb://mongoadmin:secret@localhost:27017/")
db = client["amazon_ratings"]  # Veritabanı adı
collection = db["reviews"]     # Koleksiyon adı

# Örnek veri ekle
collection.insert_one({"text": "Bu ürün harika!", "prediction": 5})

print("Veri eklendi!")
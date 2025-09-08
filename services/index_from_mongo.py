from embedding_utils import get_embedding
from elasticsearch import Elasticsearch
from db_config import get_mongo_db
from uuid import uuid4
from tqdm import tqdm  # ✅ İlerleme çubuğu

# Elasticsearch ve Mongo bağlantısı
es = Elasticsearch("http://localhost:9200", verify_certs=False)
db = get_mongo_db()
INDEX_NAME = "reviews_vector"

# Mongo'dan veriler çekiliyor
cursor = list(db["reviews"].find({}, {"_id": 0, "text": 1, "label": 1}))
print(f"Toplam Mongo verisi: {len(cursor)}\n")

# tqdm ile progress bar başlatılıyor
for doc in tqdm(cursor, desc="Veriler aktarılıyor", unit="adet"):
    text = doc.get("text", "").strip()
    rating = doc.get("label")

    if text and rating in [1, 2, 3, 4, 5]:
        embedding = get_embedding(text)
        es.index(index=INDEX_NAME, id=str(uuid4()), document={
            "review": text,
            "rating": rating,
            "embedding": embedding
        })

print("\n✅ Aktarım tamamlandı.")

# FastAPI'nin gerekli modülleri
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Model tahmini için fonksiyon (DistilBERT)
from postprocess import predict_sentiment

# Kafka ile mesaj kuyruğu kullanımı
from kafka import KafkaProducer
import json

# Elasticsearch vektör arama için gerekli modüller
from services.embedding_utils import get_embedding
from elasticsearch import Elasticsearch

# FastAPI uygulamasını başlat
app = FastAPI()

# Statik dosyalar ve template ayarları
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Elasticsearch bağlantısı
es = Elasticsearch("http://localhost:9200", verify_certs=False)
INDEX_NAME = "reviews_vector"

# ===============================================================
# Benzer yorumları Elasticsearch üzerinden getiren fonksiyon
# ===============================================================
def search_similar_sentences(text: str, top_k=3, target_rating=None):
    embedding = get_embedding(text)

    base_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                "params": {"query_vector": embedding}
            }
        }
    }

    if target_rating is not None:
        query = {
            "bool": {
                "must": base_query,
                "filter": {
                    "term": {"rating": target_rating}
                }
            }
        }
    else:
        query = base_query

    script_query = {
        "size": top_k,
        "query": query
    }

    try:
        results = es.search(index=INDEX_NAME, query=script_query["query"])
        return [
            {
                "review": hit["_source"]["review"],
                "rating": hit["_source"].get("rating", "-"),
                "score": round((hit["_score"] - 1.0) * 100)  # % skor
            }
            for hit in results["hits"]["hits"]
        ]
    except Exception as e:
        return [{"review": f"Benzer cümleler alınamadı: {e}", "rating": "-", "score": 0}]

# ===============================================================
# Ana sayfa (GET)
# ===============================================================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ===============================================================
# Tahmin ve benzer yorumlar işlemi (POST)
# ===============================================================
@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, text: str = Form(...)):
    try:
        # Kafka'ya yorum gönder
        producer.send('reviews', {'text': text})
        producer.flush()

        # Modelden duygu tahmini (örneğin 4 ya da "★★★★☆")
        distilbert_prediction = predict_sentiment(text).get("distilbert", None)

        # Tahmin edilen yıldız sayısını belirle
        if isinstance(distilbert_prediction, str):
            predicted_star = distilbert_prediction.count('★')
        else:
            predicted_star = distilbert_prediction

        # Benzer yorumları rating'e göre getir
        similar_sentences = search_similar_sentences(text, top_k=3, target_rating=predicted_star)

    except Exception as e:
        distilbert_prediction = f"Kafka veya Elasticsearch hatası: {e}"
        similar_sentences = []

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "distilbert_prediction": distilbert_prediction,
            "input_text": text,
            "similar_sentences": similar_sentences
        }
    )

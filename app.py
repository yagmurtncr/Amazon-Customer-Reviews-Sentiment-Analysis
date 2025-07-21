from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse  # HTML sayfası döndürmek için
from fastapi.staticfiles import StaticFiles  # CSS, JS gibi statik dosyaları sunmak için
from fastapi.templating import Jinja2Templates  # HTML şablonlarını (template) yönetmek için
from postprocess import predict_sentiment  # Model tahmini için fonksiyon

# Kafka producer için ekleme
from kafka import KafkaProducer
import json

app = FastAPI()  # FastAPI uygulaması başlatılır

# Statik dosyalar (CSS, JS) ve şablonlar için ayarlar
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Kafka'ya mesaj göndermek için producer oluşturuluyor
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Mesajları JSON olarak gönder
)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Ana sayfa (form) render edilir
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, text: str = Form(...)):
    try:
        # Kullanıcıdan gelen yorumu Kafka'ya gönder
        producer.send('reviews', {'text': text})
        producer.flush()
        # Aynı anda model ile tahmin yap ve sonucu ekranda göster
        distilbert_prediction = predict_sentiment(text).get("distilbert", None)
    except Exception as e:
        # Hata olursa kullanıcıya mesaj göster
        distilbert_prediction = f"Kafka'ya gönderilemedi: {e}"

    # Sonucu ve girilen metni şablona gönder
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "distilbert_prediction": distilbert_prediction,
            "input_text": text
        }
    )




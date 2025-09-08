from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Kendi eğittiğin modelin yolu
model_path = "./final_model"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.eval()  #Model tahmin yapmak için çalışır
#Koymazsak; Model, tahmin (inference) sırasında bile hala eğitimdeymiş gibi davranır.

def predict_sentiment(text: str):
    encoded = tokenizer(text, return_tensors="pt", truncation=True, padding=True)  #Sonuçları PyTorch tensörü olarak döndür
    with torch.no_grad():  #Bellek ve hız için gradyan takibini kapatır
        output = model(**encoded)  #Encode edilmiş girdiye göre modelden tahmin alınır
    probs = torch.softmax(output.logits, dim=1)[0]  # Modelin her sınıf için hesapladığı skorlar (ham değerler)
    #Bu skorları 0-1 arası olasılıklara çevirir
    #Çünkü çıktı batch (küme) boyutunda gelir. Biz tek bir örnek verdiğimiz için sadece ilk sonucu alırız.
    pred_class= torch.argmax(probs).item()  # en olası sınıf indexi(0-4)
    stars = pred_class + 1  # 1-5 arası puan
    return {"distilbert": stars}

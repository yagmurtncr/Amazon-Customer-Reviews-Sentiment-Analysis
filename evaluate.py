import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import classification_report, confusion_matrix
import torch
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
import json
import os
from db_config import get_mongo_db

def get_mongo_df(collection_name):
    db = get_mongo_db()
    collection = db[collection_name]
    df = pd.DataFrame(list(collection.find({}, {'_id': 0})))
    return df

# Model yolu ve cihaz ayarı
model_path = "./final_model"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Model ve tokenizer yükle
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.to(device)
model.eval()

# Veri yükle
df = get_mongo_df("test_reviews")

# Her sınıftan eşit örnek sayısı al (örnek: 1000)
sample_size_per_class = 1000
df_balanced = df.groupby('label').apply(lambda x: x.sample(n=sample_size_per_class, random_state=42)).reset_index(drop=True)

texts = df_balanced["text"].tolist()
true_labels = (df_balanced["label"] - 1).tolist()

predicted_labels = []

print("📊 Model tahminleri alınıyor...")
for text in tqdm(texts, desc="Tahmin Ediliyor"):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
        predicted_labels.append(predicted_class)

# Label isimleri (0-4 için)
label_names = {
    0: "1 yıldız",
    1: "2 yıldız",
    2: "3 yıldız",
    3: "4 yıldız",
    4: "5 yıldız"
}

y_true_named = [label_names[l] for l in true_labels]
y_pred_named = [label_names[l] for l in predicted_labels]

os.makedirs("results", exist_ok=True)

cm = confusion_matrix(y_true_named, y_pred_named, labels=list(label_names.values()))
plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=list(label_names.values()), yticklabels=list(label_names.values()))
plt.title("Confusion Matrix")
plt.xlabel("Tahmin")
plt.ylabel("Gerçek")
plt.tight_layout()
cm_path = os.path.join("results", "confusion_matrix.png")
plt.savefig(cm_path)
plt.close()

report = classification_report(y_true_named, y_pred_named, output_dict=True)
json_path = os.path.join("results", "metrics.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=4, ensure_ascii=False)

print("\n🎯 Kısa Özet:")
print(classification_report(y_true_named, y_pred_named, digits=3))
print(f"✅ {cm_path} ve {json_path} dosyaları kaydedildi.")

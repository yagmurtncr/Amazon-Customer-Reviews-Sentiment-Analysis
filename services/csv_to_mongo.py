import pandas as pd
from pymongo import MongoClient
from tqdm import tqdm
import re

tqdm.pandas()

def clean_text(text):
    if not isinstance(text, str):
        return ''
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'@\w+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# CSV'yi oku ve temizle
df = pd.read_csv('./amazon_data/Reviews.csv')
df['Summary'] = df['Summary'].fillna('')
df['Text'] = df['Text'].fillna('')
df['text'] = (df['Summary'] + " " + df['Text']).progress_apply(clean_text)
df = df[df['Score'].isin([1, 2, 3, 4, 5])]
df = df[['Id', 'Score', 'text']].rename(columns={'Score': 'label'})

# MongoDB'ye bağlan ve reviews koleksiyonuna ekle
client = MongoClient("mongodb://mongoadmin:secret@localhost:27017/")
db = client["amazon_ratings"]
collection = db["reviews"]
collection.delete_many({})  # Koleksiyonu temizle (isteğe bağlı)
collection.insert_many(df.to_dict(orient="records"))

print("Reviews.csv verileri MongoDB'ye aktarıldı!")
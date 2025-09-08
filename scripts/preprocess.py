import pandas as pd
import re
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from db_config import get_mongo_db

# Temizleme fonksiyonu (preprocess.py'den alınmıştır)
def clean_text(text):
    if not isinstance(text, str):
        return ''
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'@\w+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def main():
    tqdm.pandas()
    # MongoDB bağlantısı
    db = get_mongo_db()
    reviews_col = db['reviews']

    print("Veritabanından veriler çekiliyor...")
    # reviews koleksiyonundan verileri DataFrame olarak çek
    cursor = reviews_col.find({}, {'_id': 0, 'Id': 1, 'label': 1, 'text': 1})
    df = pd.DataFrame(list(cursor))

    print("Geçersiz skorlar filtreleniyor...")
    df = df[df['label'].isin([1, 2, 3, 4, 5])]

    print("Eksik veriler dolduruluyor...")
    df['text'] = df['text'].fillna('')

    print("Metin temizleniyor...")
    df['text'] = df['text'].progress_apply(clean_text)

    print("Eğitim ve test verileri ayrılıyor (%80 / %20)...")
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])

    print(f"Eğitim verisi boyutu: {train_df.shape}")
    print(f"Test verisi boyutu:   {test_df.shape}")

    # Sonuçları iki ayrı koleksiyona ekle
    train_col = db['train_reviews']
    test_col = db['test_reviews']

    print("train_reviews koleksiyonu temizleniyor...")
    train_col.delete_many({})
    print("test_reviews koleksiyonu temizleniyor...")
    test_col.delete_many({})

    print("Eğitim verileri ekleniyor...")
    train_col.insert_many(train_df.to_dict('records'))
    print("Test verileri ekleniyor...")
    test_col.insert_many(test_df.to_dict('records'))
    print("İşlem tamamlandı.")

if __name__ == "__main__":
    main() 
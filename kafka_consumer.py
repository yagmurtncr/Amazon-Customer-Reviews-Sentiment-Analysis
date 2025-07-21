# kafka_consumer.py
# Bu script, Kafka'daki 'reviews' topic'inden gelen yorumları alır,
# model ile analiz eder ve sonucu 'predictions' topic'ine gönderir.

from kafka import KafkaConsumer, KafkaProducer  # Kafka ile iletişim için gerekli kütüphaneler
import json
from postprocess import predict_sentiment  # Model tahmin fonksiyonu

# Kafka'dan 'reviews' topic'ini dinleyen consumer oluşturuluyor
consumer = KafkaConsumer(
    'reviews',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Mesajları JSON olarak al
)
# Tahmin sonucunu başka bir topic'e göndermek için producer oluşturuluyor
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Mesajları JSON olarak gönder
)

# Sürekli olarak yeni mesajları dinle
for message in consumer:
    review = message.value['text']  # Gelen yorum metni
    result = predict_sentiment(review)  # Model ile tahmin yap
    # Sonucu 'predictions' topic'ine gönder
    producer.send('predictions', {'text': review, 'prediction': result})
    producer.flush()
    print(f"Processed: {review} -> {result}")  # Terminale sonucu yazdır
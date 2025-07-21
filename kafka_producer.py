from kafka import KafkaProducer  # Kafka ile iletişim için gerekli kütüphane
import json

# Kafka'ya mesaj göndermek için producer oluşturuluyor
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Mesajları JSON olarak gönder
)

def send_review(review_text):
    # Verilen yorumu 'reviews' topic'ine gönderir
    producer.send('reviews', {'text': review_text})
    producer.flush()
    print("Review sent to Kafka.")  # Terminale bilgi yazdır

if __name__ == "__main__":
    # Örnek bir yorum gönderimi
    send_review("This product is amazing!")
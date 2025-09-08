from kafka import KafkaProducer  # Kafka ile iletişim için gerekli kütüphane
import json

# Kafka'ya mesaj göndermek için producer oluşturuluyor
print(" Kafka producer oluşturuluyor...")
producer = KafkaProducer(
    bootstrap_servers='host.docker.internal:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Mesajları JSON olarak gönder
)
print(" Kafka producer hazır.")

def send_review(review_text):
    # Verilen yorumu 'reviews' topic'ine gönderir
    print(f" Gönderilecek yorum: '{review_text}'")
    producer.send('reviews', {'text': review_text})
    producer.flush()
    print(" Yorum Kafka'ya başarıyla gönderildi. (topic: 'reviews')\n")

if __name__ == "__main__":
    # Örnek bir yorum gönderimi
    print(" Örnek yorum gönderimi başlıyor...")
    send_review("This product is amazing!")
    print(" Gönderim işlemi tamamlandı.")

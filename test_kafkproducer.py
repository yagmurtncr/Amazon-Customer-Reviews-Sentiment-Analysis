from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='host.docker.internal:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

try:
    producer.send('reviews', {'text': 'test message from manual script'})
    producer.flush()
    print("Mesaj Kafka'ya başarıyla gönderildi!")
except Exception as e:
    print(f"Kafka Producer Hatası: {e}")

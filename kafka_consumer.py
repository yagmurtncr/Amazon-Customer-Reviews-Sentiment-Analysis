from kafka import KafkaConsumer, KafkaProducer
import json
from postprocess import predict_sentiment  # Model tahmin fonksiyonu

def main():
    # Kafka'dan 'reviews' adlı topic'i dinlemek için consumer oluşturuyoruz.
    # Burada kritik parametreleri belirtiyoruz:
    # - bootstrap_servers: Kafka broker adresi
    # - group_id: Consumer'ın ait olduğu grup, offset takibi için önemli
    # - auto_offset_reset: Eğer consumer'ın offset bilgisi yoksa en baştan mesajları okumaya başla
    # - enable_auto_commit: Offset bilgilerini Kafka'ya otomatik kaydet (offset commit)
    # - session_timeout_ms ve heartbeat_interval_ms: Consumer'ın Kafka ile bağlantısını sağlıklı tutmak için kalp atışı ayarları
    # - value_deserializer: Kafka'dan gelen mesaj JSON formatındaysa onu Python objesine çevirir
    print(" Kafka consumer başlatılıyor...")  # Başlangıç bildirimi
    consumer = KafkaConsumer(
        'reviews',
        bootstrap_servers='host.docker.internal:9092',
        group_id='my-consumer-group',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        session_timeout_ms=10000,
        heartbeat_interval_ms=3000,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    # Analiz sonucu tahminleri başka bir topic'e göndermek için producer oluşturuyoruz.
    # Burada mesajları JSON formatına çevirip Kafka'ya gönderiyoruz.
    producer = KafkaProducer(
        bootstrap_servers='host.docker.internal:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    print(" Kafka consumer hazır. 'reviews' konusunu dinlemeye başladı.")
    print(" Mesaj bekleniyor...\n")

    try:
        # Gelen mesajlar için sonsuz döngü ile bekleme ve işlem yapma
        for message in consumer:
            print(" Yeni mesaj alındı.")  # Yeni mesaj bildirimi

            # Mesajdan 'text' alanını alıyoruz (yorum metni)
            review = message.value.get('text', '')
            
            # Eğer 'text' alanı yoksa, uyarı verip atla
            if not review:
                print(" Uyarı: Mesajda 'text' alanı yok, atlanıyor.\n")
                continue

            # Yorum metni üzerinde duygu analizi ya da başka tahminler yap
            print(f" Yorum işleniyor: {review}")
            result = predict_sentiment(review)
            print(f" Tahmin sonucu: {result}")

            # Tahmin sonucunu 'predictions' topic'ine JSON olarak gönder
            producer.send('predictions', {'text': review, 'prediction': result})
            producer.flush()  # Mesajın hemen gönderilmesini sağlar

            # İşlenen veriyi konsola yazdır (debug ve takip için)
            print(" Tahmin sonucu 'predictions' konusuna gönderildi.\n")

    except Exception as e:
        # Herhangi bir hata durumunda hatayı yazdır ve döngüden çık
        print(f" Consumer hata aldı: {e}")
    finally:
        # Program kapanırken Kafka bağlantılarını düzgün kapat
        print(" Consumer kapanıyor, kaynaklar serbest bırakılıyor...")
        consumer.close()
        producer.close()
        print(" Tüm bağlantılar başarıyla kapatıldı.")

if __name__ == "__main__":
    main()

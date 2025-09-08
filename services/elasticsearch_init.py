from elasticsearch import Elasticsearch, exceptions

try:
    es = Elasticsearch("http://localhost:9200", verify_certs=False)
    
    info = es.info()  # Burada doğrudan HTTP GET ile info çekiyoruz
    print(" Elasticsearch bağlantısı başarılı!")
    print(f" Versiyon: {info['version']['number']}")
    print(f" Cluster adı: {info['cluster_name']}")
    
    # Index kontrol ve oluşturma
    index_name = "reviews_vector"
    if not es.indices.exists(index=index_name):
        es.indices.create(
    index=index_name,
    mappings={
        "properties": {
            "review": {"type": "text"},
            "rating": {"type": "integer"},
            "embedding": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "cosine"
            }
        }
    }
)

        print(f" Index oluşturuldu: `{index_name}`")
    else:
        print(f"ℹ Index zaten mevcut: `{index_name}`")

except exceptions.ConnectionError as e:
    print(" Elasticsearch'e bağlanırken bağlantı hatası:")
    print(e)

except Exception as e:
    print(" Beklenmeyen hata oluştu:")
    print(e)

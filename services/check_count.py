from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200", verify_certs=False)
count = es.count(index="reviews_vector")
print("Toplam doküman sayısı:", count["count"])

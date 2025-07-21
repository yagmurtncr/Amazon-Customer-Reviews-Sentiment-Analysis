import postprocess

# Olumlu örnek
result_pos = postprocess.predict_sentiment("This product is excellent and I love it.")
print("Olumlu örnek sonucu:", result_pos)

# Olumsuz örnek
result_neg = postprocess.predict_sentiment("This product is terrible and I hate it.")
print("Olumsuz örnek sonucu:", result_neg)

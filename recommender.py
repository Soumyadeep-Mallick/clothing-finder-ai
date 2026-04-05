from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def rank_products(products, query):
    if not products:
        return products

    # Combine product titles
    texts = [p["title"] for p in products]

    # Add query
    texts.append(query)

    # Vectorize
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)

    # Compute similarity
    query_vector = tfidf_matrix[-1]
    product_vectors = tfidf_matrix[:-1]

    similarities = cosine_similarity(query_vector, product_vectors)

    # Attach scores
    for i, product in enumerate(products):
        product["score"] = similarities[0][i]

    # Sort by score
    ranked = sorted(products, key=lambda x: x["score"], reverse=True)

    return ranked
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def rank_products(products, query):
    if not products:
        return products

    # Extract titles
    titles = [p["title"] for p in products]

    # Add query at first position
    corpus = [query] + titles

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Compute similarity
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Attach score
    for i, product in enumerate(products):
        product["score"] = similarity[i]

    # Sort by score (descending)
    products = sorted(products, key=lambda x: x["score"], reverse=True)

    return products
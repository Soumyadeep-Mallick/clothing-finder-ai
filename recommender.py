def extract_features(title):
    title = title.lower()

    return {
        "casual": int("casual" in title),
        "formal": int("formal" in title),
        "shirt": int("shirt" in title),
        "tshirt": int("tshirt" in title),
        "black": int("black" in title),
        "slim": int("slim" in title),
    }


def init_user_profile():
    return {
        "casual": 0,
        "formal": 0,
        "shirt": 0,
        "tshirt": 0,
        "black": 0,
        "slim": 0,
    }


def update_profile(profile, features, liked=True):
    for key in profile:
        if liked:
            profile[key] += features[key]
        else:
            profile[key] -= features[key]
    return profile


def score_product(product, profile):
    features = extract_features(product["title"])
    return sum(profile[k] * features[k] for k in profile)


def rank_products(products, profile):
    return sorted(products, key=lambda x: score_product(x, profile), reverse=True)
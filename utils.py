def clean_price(price):
    try:
        return int(price.replace("₹", "").replace(",", ""))
    except:
        return None


def filter_products(products, budget):
    return [
        p for p in products
        if clean_price(p["price"]) and clean_price(p["price"]) <= budget
    ]


def sort_by_price(products):
    return sorted(
        products,
        key=lambda x: clean_price(x["price"]) or 999999
    )
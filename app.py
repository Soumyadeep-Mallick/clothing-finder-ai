import streamlit as st
from flipkart import scrape_flipkart
from amazon import scrape_amazon
from concurrent.futures import ThreadPoolExecutor

st.set_page_config(layout="wide")

# ------------------ STYLING ------------------
st.markdown("""
<style>
.product-card {
    background: #161b22;
    padding: 12px;
    border-radius: 10px;
    transition: 0.3s;
}
.product-card:hover {
    transform: scale(1.03);
    box-shadow: 0 0 10px rgba(255,255,255,0.1);
}
.product-title {
    font-size: 14px;
    height: 40px;
    overflow: hidden;
}
.product-price {
    font-size: 16px;
    font-weight: bold;
}
.product-source {
    font-size: 12px;
    color: gray;
}
img {
    height: 250px !important;
    object-fit: cover;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.title("Filters")

gender = st.sidebar.selectbox("Gender", ["Male", "Female"])

dress = st.sidebar.selectbox(
    "Category",
    ["Shirt", "T-Shirt", "Jeans", "Dress", "Bra", "Kurti"]
)

color = st.sidebar.selectbox(
    "Color",
    ["Black", "Blue", "White", "Pink", "Red", "Green"]
)

style = st.sidebar.selectbox(
    "Style",
    ["Casual", "Formal", "Innerwear"]
)

# ------------------ CONDITIONAL FILTER ------------------
cup_size = None

if gender == "Female" and style == "Innerwear":
    cup_size = st.sidebar.selectbox(
        "Cup Size",
        ["32A", "32B", "34B", "34C", "36C", "36D", "38D"]
    )

# ------------------ BUDGET ------------------
budget = st.sidebar.slider("Max Budget", 100, 5000, 1500)

sort_price = st.sidebar.checkbox("Sort by Price")

search_btn = st.sidebar.button("Search")

# ------------------ HEADER ------------------
st.title("🛍️ Clothing Finder")

# ------------------ SEARCH ------------------
if search_btn:

    # BUILD QUERY
    query = f"{gender} {dress} {color} {style}"

    if cup_size:
        query += f" {cup_size}"

    with st.spinner("Fetching products..."):

        with ThreadPoolExecutor() as executor:
            flip = executor.submit(scrape_flipkart, query)
            amaz = executor.submit(scrape_amazon, query)

            flipkart_data = flip.result()
            amazon_data = amaz.result()

        products = flipkart_data + amazon_data

    # ------------------ CLEAN PRICE ------------------
    def clean_price(p):
        try:
            return int(p.replace("₹", "").replace(",", ""))
        except:
            return 999999

    filtered = []

    for p in products:
        price_val = clean_price(p["price"])
        if price_val <= budget:
            p["price_val"] = price_val
            filtered.append(p)

    # ------------------ SORT ------------------
    if sort_price:
        filtered = sorted(filtered, key=lambda x: x["price_val"])

    st.success(f"Found {len(filtered)} products")

    # ------------------ GRID ------------------
    cols = st.columns(4)

    for i, product in enumerate(filtered):
        with cols[i % 4]:

            st.markdown('<div class="product-card">', unsafe_allow_html=True)

            # IMAGE (clickable)
            st.markdown(f"""
            <a href="{product['link']}" target="_blank">
                <img src="{product['image']}" width="100%">
            </a>
            """, unsafe_allow_html=True)

            # TITLE
            st.markdown(f"""
            <div class="product-title"><b>{product['title']}</b></div>
            """, unsafe_allow_html=True)

            # PRICE
            st.markdown(f"""
            <div class="product-price">💰 {product['price']}</div>
            """, unsafe_allow_html=True)

            # SOURCE
            st.markdown(f"""
            <div class="product-source">🛒 {product['source']}</div>
            """, unsafe_allow_html=True)

            # BUTTON
            st.markdown(f"""
            <a href="{product['link']}" target="_blank">
                <button style="
                    background:#ff4b2b;
                    color:white;
                    padding:8px 12px;
                    border:none;
                    border-radius:6px;
                    cursor:pointer;
                    margin-top:8px;">
                    🔥 Buy Now
                </button>
            </a>
            """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
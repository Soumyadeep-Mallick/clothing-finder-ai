import streamlit as st
from flipkart import scrape_flipkart
from amazon import scrape_amazon
from recommender import rank_products

st.set_page_config(page_title="Clothing Finder AI", layout="wide")

# ---------------- HEADER ---------------- #
st.title("🛍️ Clothing Finder AI")

# ---------------- SIDEBAR ---------------- #
st.sidebar.header("Filters")

gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
dress = st.sidebar.text_input("Dress", "shirt")
color = st.sidebar.text_input("Color", "black")
style = st.sidebar.text_input("Style", "casual")

category = None
cup_size = None

if gender == "Female":
    category = st.sidebar.selectbox("Category", ["Normal Wear", "Innerwear"])

    if category == "Innerwear":
        cup_size = st.sidebar.selectbox(
            "Cup Size",
            ["30A", "32B", "34C", "36D", "38D", "40DD"]
        )

budget = st.sidebar.slider("Max Budget", 100, 5000, 1500)

search = st.sidebar.button("🔍 Search")

# ---------------- HELPER ---------------- #
def clean_price(price):
    try:
        return int(price.replace("₹", "").replace(",", ""))
    except:
        return 999999


# ---------------- SEARCH ---------------- #
if search:

    query = f"{gender} {dress} {color} {style}"

    if category:
        query += f" {category}"

    if cup_size:
        query += f" {cup_size}"

    with st.spinner("Fetching products..."):
        flipkart_data = scrape_flipkart(query)
        amazon_data = scrape_amazon(query)

        products = flipkart_data + amazon_data

        # AI ranking
        products = rank_products(products, query)

    # budget filter
    products = [p for p in products if clean_price(p["price"]) <= budget]

    st.success(f"Found {len(products)} products")

    # ---------------- CLEAN GRID ---------------- #
    cols = st.columns(4)

    for i, product in enumerate(products):
        with cols[i % 4]:

            # IMAGE
            if product.get("image"):
                st.image(product["image"], use_container_width=True)

            # TITLE
            st.markdown(f"**{product.get('title', 'No Title')[:60]}**")

            # PRICE
            st.write(f"💰 {product.get('price', 'N/A')}")

            # SOURCE
            st.caption(product.get("source", ""))

            # BUTTON
            if product.get("link"):
                st.link_button("Buy Now", product["link"])
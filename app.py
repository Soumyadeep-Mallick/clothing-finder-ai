import streamlit as st
from flipkart import scrape_flipkart
from amazon import scrape_amazon

st.set_page_config(page_title="Clothing Finder", layout="wide")

st.title("🛍️ Clothing Finder")

# ---------------- SESSION ---------------- #
if "products" not in st.session_state:
    st.session_state.products = []

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
            ["30A", "32A", "32B", "34B", "34C", "36C", "36D"]
        )

budget = st.sidebar.slider("Max Budget", 100, 5000, 1500)

# ---------------- SEARCH ---------------- #
if st.sidebar.button("Search"):

    query_parts = [color, style, dress, gender]

    if category:
        query_parts.append(category)

    if cup_size:
        query_parts.append(cup_size)

    query = " ".join(query_parts)

    with st.spinner("Fetching products..."):
        try:
            flipkart_data = scrape_flipkart(query)
        except:
            flipkart_data = []

        try:
            amazon_data = scrape_amazon(query)
        except:
            amazon_data = []

    products = flipkart_data + amazon_data

    # Fallback if scraper fails
    if not products:
        products = [
            {
                "title": "Demo Product",
                "price": "₹499",
                "image": "https://via.placeholder.com/200",
                "link": "https://www.amazon.in",
                "source": "Demo"
            }
        ]

    st.session_state.products = products

# ---------------- DISPLAY ---------------- #
if st.session_state.products:

    st.success(f"Found {len(st.session_state.products)} products")

    cols_per_row = 4

    for i in range(0, len(st.session_state.products), cols_per_row):
        cols = st.columns(cols_per_row)

        for j, col in enumerate(cols):
            if i + j < len(st.session_state.products):
                p = st.session_state.products[i + j]

                with col:
                    # ✅ IMAGE (SAFE)
                    st.image(
                        p.get("image", ""),
                        use_container_width=True
                    )

                    # ✅ TITLE
                    st.write(p["title"][:60])

                    # ✅ PRICE
                    st.markdown(f"**💰 {p['price']}**")

                    # ✅ SOURCE
                    st.caption(p["source"])

                    # ✅ CLICK BUTTON
                    st.link_button("🛒 Buy Now", p["link"])

                    st.markdown("---")
import streamlit as st

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="MiniStore",
    page_icon="🛍️",
    layout="wide"
)

# --------------------------------------------------
# PRODUCT DATA
# Shared knowledge for chatbot
# --------------------------------------------------
products = [
    {
        "name": "Wireless Bluetooth Headphones",
        "price": 2499,
        "category": "Electronics",
        "description": "Premium sound quality with active noise cancellation."
    },
    {
        "name": "Smart Fitness Watch",
        "price": 3999,
        "category": "Electronics",
        "description": "Track steps, heart rate, sleep, and workouts."
    },
    {
        "name": "Men's Casual Sneakers",
        "price": 1999,
        "category": "Fashion",
        "description": "Comfortable everyday sneakers with modern styling."
    },
    {
        "name": "Women's Tote Bag",
        "price": 1499,
        "category": "Fashion",
        "description": "Stylish and spacious tote bag for daily use."
    },
    {
        "name": "Coffee Maker",
        "price": 3499,
        "category": "Home & Kitchen",
        "description": "Brew fresh coffee quickly with one-touch operation."
    },
    {
        "name": "LED Desk Lamp",
        "price": 999,
        "category": "Home & Kitchen",
        "description": "Energy-efficient lamp with adjustable brightness."
    }
]

# Store products for chatbot access
st.session_state["products"] = products

# --------------------------------------------------
# CART STATE
# --------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

# --------------------------------------------------
# CSS
# --------------------------------------------------
st.markdown("""
<style>

.hero {
    background: linear-gradient(135deg,#2563eb,#7c3aed);
    padding:40px;
    border-radius:15px;
    text-align:center;
    color:white;
    margin-bottom:25px;
}

.product-card {
    background:white;
    padding:20px;
    border-radius:12px;
    box-shadow:0 3px 12px rgba(0,0,0,0.1);
    margin-bottom:20px;
    border:1px solid #e5e7eb;
    min-height:280px;
}

.product-title {
    font-size:20px;
    font-weight:bold;
}

.price {
    color:#16a34a;
    font-size:22px;
    font-weight:bold;
}

/* Floating Support Button */
.support-button {
    position: fixed;
    bottom: 25px;
    right: 25px;
    background: #2563eb;
    color: white;
    padding: 14px 18px;
    border-radius: 50px;
    text-decoration: none;
    font-weight: bold;
    z-index: 9999;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.25);
}

.support-button:hover{
    background:#1d4ed8;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("🛒 MiniStore")

categories = ["All"] + sorted(
    list(set(p["category"] for p in products))
)

selected_category = st.sidebar.selectbox(
    "Browse Categories",
    categories
)

st.sidebar.markdown("---")

st.sidebar.subheader("Cart Summary")

cart_count = len(st.session_state.cart)
cart_total = sum(item["price"] for item in st.session_state.cart)

st.sidebar.metric("Items", cart_count)
st.sidebar.metric("Total", f"₹{cart_total:,}")

# --------------------------------------------------
# HERO
# --------------------------------------------------
st.markdown("""
<div class="hero">
<h1>🛍️ MiniStore</h1>
<p>Your one-stop destination for quality products.</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# WELCOME
# --------------------------------------------------
st.header("Welcome to MiniStore")

st.write("""
Browse our latest products across Electronics,
Fashion, and Home & Kitchen categories.
""")

# --------------------------------------------------
# PRODUCT FILTER
# --------------------------------------------------
if selected_category == "All":
    filtered_products = products
else:
    filtered_products = [
        p for p in products
        if p["category"] == selected_category
    ]

# --------------------------------------------------
# PRODUCT GRID
# --------------------------------------------------
st.subheader("Featured Products")

cols = st.columns(3)

for idx, product in enumerate(filtered_products):

    with cols[idx % 3]:

        st.markdown(f"""
        <div class="product-card">
            <div class="product-title">
                {product["name"]}
            </div>
            <br>
            <b>{product["category"]}</b>
            <p>{product["description"]}</p>
            <div class="price">
                ₹{product["price"]:,}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Add to Cart",
            key=product["name"]
        ):
            st.session_state.cart.append(product)
            st.success("Added to cart!")

# --------------------------------------------------
# CART DETAILS
# --------------------------------------------------
st.divider()

st.subheader("Cart Items")

if st.session_state.cart:
    for item in st.session_state.cart:
        st.write(
            f"• {item['name']} - ₹{item['price']:,}"
        )
else:
    st.info("Your cart is empty.")

# --------------------------------------------------
# FLOATING SUPPORT BUTTON
# --------------------------------------------------
st.markdown("""
<a class="support-button" href="/Support_Chatbot" target="_self">
💬 Support
</a>
""", unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.caption("© 2026 MiniStore")
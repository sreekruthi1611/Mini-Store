import streamlit as st
from openai import OpenAI

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Support Chatbot",
    page_icon="💬",
    layout="wide"
)

# --------------------------------------------------
# OPENAI CLIENT
# --------------------------------------------------
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# --------------------------------------------------
# PRODUCT CATALOG
# --------------------------------------------------
products = st.session_state.get(
    "products",
    [
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
)

catalog_text = "\n".join([
    f"""
Product: {p['name']}
Category: {p['category']}
Price: ₹{p['price']}
Description: {p['description']}
"""
    for p in products
])

# --------------------------------------------------
# SYSTEM PROMPT
# --------------------------------------------------
SYSTEM_PROMPT = f"""
You are MiniStore's professional customer support assistant.

Your role:
- Help customers with product information.
- Help with delivery questions.
- Help with refunds.
- Help with returns.
- Help with payment methods.
- Help with order status inquiries.
- Provide friendly and professional support.

Store Catalog:

{catalog_text}

Important Rules:
1. Only answer questions related to MiniStore.
2. Supported topics:
   - Products
   - Orders
   - Delivery
   - Shipping
   - Refunds
   - Returns
   - Payments
   - Store policies

3. If a user asks unrelated questions
   (politics, coding, science, homework, math, celebrities, etc.),
   politely say:

   "I'm MiniStore's customer support assistant and can only help
   with store-related questions such as products, orders,
   delivery, refunds, returns, and payments."

4. Be concise, professional, and helpful.

5. If the user asks about products,
   use the catalog information provided.

6. Do not invent products that do not exist in the catalog.

7. If order-specific information is requested,
   explain that this demo store does not currently have
   real order tracking integrated.
"""

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------
st.title("💬 MiniStore Support Assistant")

st.write(
    "Ask questions about products, delivery, refunds, returns, payments, and orders."
)

# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! Welcome to MiniStore Support. "
                "How can I help you today?"
            )
        }
    ]

# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------------------------
# USER INPUT
# --------------------------------------------------
prompt = st.chat_input(
    "Ask a MiniStore support question..."
)

if prompt:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Build conversation
    conversation = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    conversation.extend(st.session_state.messages)

    try:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=conversation,
            temperature=0.3
        )

        assistant_reply = (
            response.choices[0]
            .message
            .content
        )

    except Exception as e:
        assistant_reply = (
            f"Error communicating with OpenAI API:\n\n{e}"
        )

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
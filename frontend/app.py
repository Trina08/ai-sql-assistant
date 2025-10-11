import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ✅ Connect to your Render backend
BACKEND_URL = "https://ai-sql-assistant-muem.onrender.com"

# 🎨 Streamlit Page Config
st.set_page_config(
    page_title="AI SQL Business Assistant",
    page_icon="🤖",
    layout="wide",
)

# 🏷️ Title
st.title("🤖 AI SQL Business Assistant")
st.markdown("### Manage your business with data-driven insights powered by Gemini AI")

# 🧭 Sidebar Navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to:", ["🏠 Dashboard", "📦 Products", "🧍 Customers", "🧾 Orders", "💬 Ask AI"])


# ✅ Helper to Fetch Data
def fetch_data(endpoint):
    try:
        res = requests.get(f"{BACKEND_URL}/{endpoint}")
        if res.status_code == 200:
            return res.json().get(endpoint, [])
        else:
            st.error(f"Error fetching {endpoint}: {res.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
        return []


# 🏠 Dashboard
if section == "🏠 Dashboard":
    st.header("📊 Business Overview")

    # Load all three data tables
    products = fetch_data("products")
    customers = fetch_data("customers")
    orders = fetch_data("orders")

    if products and customers and orders:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Products", len(products))
        col2.metric("Total Customers", len(customers))
        col3.metric("Total Orders", len(orders))

        df_orders = pd.DataFrame(orders)
        if not df_orders.empty:
            fig = px.bar(df_orders, x="customer", y="total_amount", color="customer",
                         title="💰 Orders by Customer", text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Loading data... or please ensure backend is active.")

# 📦 Products Section
elif section == "📦 Products":
    st.header("🛍️ Products Overview")
    products = fetch_data("products")
    if products:
        df = pd.DataFrame(products)
        st.dataframe(df, use_container_width=True)
        fig = px.pie(df, names="category", title="📈 Product Categories Distribution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No products found.")

# 🧍 Customers Section
elif section == "🧍 Customers":
    st.header("👥 Customers List")
    customers = fetch_data("customers")
    if customers:
        st.dataframe(pd.DataFrame(customers), use_container_width=True)
    else:
        st.warning("No customers found.")

# 🧾 Orders Section
elif section == "🧾 Orders":
    st.header("📦 Orders Summary")
    orders = fetch_data("orders")
    if orders:
        df = pd.DataFrame(orders)
        st.dataframe(df, use_container_width=True)
        fig = px.line(df, x="order_date", y="total_amount", markers=True, title="📊 Order Trends Over Time")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No orders data found.")

# 💬 Ask AI Section
elif section == "💬 Ask AI":
    st.header("💬 Ask Business AI Assistant")
    st.markdown("Type your business question below. The AI will generate SQL, run it, and show real results 👇")

    user_question = st.text_input("💭 Enter your question:", placeholder="E.g. Show me top 5 most expensive products")
    if st.button("Ask AI"):
        if not user_question:
            st.warning("Please enter a question first.")
        else:
            with st.spinner("🤖 Thinking... contacting Gemini AI..."):
                try:
                    res = requests.post(f"{BACKEND_URL}/ask", json={"question": user_question})
                    if res.status_code == 200:
                        data = res.json()
                        st.success(f"✅ Query generated: `{data.get('query', 'N/A')}`")

                        result = data.get("result", [])
                        if isinstance(result, list) and len(result) > 0:
                            st.dataframe(pd.DataFrame(result), use_container_width=True)
                        else:
                            st.info("No data found for this query.")
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

# 🦶 Footer
st.markdown("---")
st.caption("Built with ❤️ using FastAPI, PostgreSQL, Streamlit, and Gemini AI.")

# frontend/app.py
# frontend/app.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="AI SQL Assistant",
    page_icon="🤖",
    layout="wide"
)

# ================== CUSTOM CSS ==================
st.markdown("""
    <style>
    /* Background */
    .stApp {
        background: linear-gradient(120deg, #141E30, #243B55);
        color: white;
        font-family: 'Poppins', sans-serif;
    }

    /* Titles */
    h1, h2, h3, h4 {
        color: #00BFFF;
        text-align: center;
    }

    /* Chat Bubbles */
    .user-bubble {
        background: linear-gradient(135deg, #00BFFF, #0072ff);
        padding: 12px 16px;
        border-radius: 15px 15px 0px 15px;
        color: white;
        width: fit-content;
        max-width: 75%;
        margin-left: auto;
        margin-right: 10px;
        margin-bottom: 10px;
    }

    .ai-bubble {
        background: linear-gradient(135deg, #1e293b, #334155);
        padding: 12px 16px;
        border-radius: 15px 15px 15px 0px;
        color: #f5f6fa;
        width: fit-content;
        max-width: 75%;
        margin-left: 10px;
        margin-bottom: 10px;
    }

    /* Input box */
    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: white;
        border-radius: 10px;
        border: 1px solid #00BFFF;
        font-size: 15px;
        padding: 10px;
    }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #00BFFF, #0072ff);
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: 0.3s;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #63a4ff, #83eaf1);
        color: black;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: gray;
        margin-top: 2rem;
        font-size: 13px;
    }

    /* Scrollbar hidden for sleek look */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #00BFFF;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ================== SIDEBAR ==================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4712/4712100.png", width=80)
st.sidebar.markdown("<h2 style='color:#00BFFF;'>AI SQL Assistant</h2>", unsafe_allow_html=True)
st.sidebar.write("Built by **Anusha Nath** 💙")
st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Quick Prompts")
st.sidebar.write("- Show all customers")
st.sidebar.write("- Top 5 products by price")
st.sidebar.write("- Orders placed this month")
st.sidebar.write("- Total revenue per category")
st.sidebar.markdown("---")

# ================== MAIN HEADER ==================
st.markdown("<h1>💬 AI SQL Assistant Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Your intelligent data companion powered by <b>Gemini + FastAPI + PostgreSQL</b>.</p>", unsafe_allow_html=True)
st.markdown("---")

# ================== CHAT MEMORY ==================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_df" not in st.session_state:
    st.session_state.last_df = None

# ================== INPUT AREA ==================
question = st.text_input("🧠 Ask your question:", placeholder="e.g., Show me total revenue per category")

col1, col2 = st.columns([4, 1])
with col2:
    ask = st.button("Ask AI ✨")

# ================== PROCESS REQUEST ==================
if ask and question.strip():
    with st.spinner("Thinking... Analyzing your data..."):
        try:
            response = requests.post("http://127.0.0.1:8000/ask", json={"question": question})
            data = response.json()

            if "error" in data:
                ai_reply = f"❌ Error: {data['error']}"
            else:
                explanation = data.get("explanation", "No explanation provided.")
                sql_query = data.get("query", "No query generated.")
                ai_reply = f"**🧠 Explanation:** {explanation}\n\n**🧩 Query:**\n```sql\n{sql_query}\n```"

                result = data.get("result", [])
                st.session_state["last_df"] = pd.DataFrame(result) if result else None

            # Save chat
            st.session_state.chat_history.append({"user": question, "ai": ai_reply})
        except Exception as e:
            st.error(f"Backend error: {e}")

# ================== DISPLAY CHAT ==================
for chat in st.session_state.chat_history:
    st.markdown(f"<div class='user-bubble'>👩‍💻 {chat['user']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='ai-bubble'>{chat['ai']}</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ================== DISPLAY RESULTS ==================
if st.session_state["last_df"] is not None:
    df = st.session_state["last_df"]
    st.markdown("### 📊 Query Result")
    st.dataframe(df, use_container_width=True)

    # Generate charts dynamically
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    if len(numeric_cols) > 0:
        st.markdown("### 📈 Data Visualization")
        col_x = st.selectbox("Select X-axis:", options=df.columns)
        col_y = st.selectbox("Select Y-axis:", options=numeric_cols)
        chart_type = st.radio("Chart type:", ["Bar", "Line", "Pie"], horizontal=True)

        if chart_type == "Bar":
            fig = px.bar(df, x=col_x, y=col_y, color=col_x, title=f"{col_y} by {col_x}")
        elif chart_type == "Line":
            fig = px.line(df, x=col_x, y=col_y, title=f"{col_y} by {col_x}")
        else:
            fig = px.pie(df, names=col_x, values=col_y, title=f"{col_y} Distribution by {col_x}")

        st.plotly_chart(fig, use_container_width=True)

# ================== FOOTER ==================
st.markdown("<div class='footer'>© 2025 AI SQL Assistant | Crafted with 💙 by Anusha Nath</div>", unsafe_allow_html=True)

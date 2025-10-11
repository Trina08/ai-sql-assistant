import os
import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# ✅ Ensure Python can import local modules (for Render or local)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Local module imports
from chat_system import ask_ai
from sql_executor import SQLExecutor

# Initialize FastAPI app
app = FastAPI(title="AI E-Commerce Business Assistant", version="1.0")

# ✅ Enable CORS (allows Streamlit frontend to communicate with backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (you can restrict to your Streamlit URL later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root route - simple health check
@app.get("/")
def home():
    return {"message": "🚀 AI SQL Assistant Backend is Running Successfully!"}


# ✅ Route 1: Fetch all products
@app.get("/products")
def get_products():
    sql = "SELECT * FROM products"
    return {"products": SQLExecutor().execute(sql)}


# ✅ Route 2: Fetch all customers
@app.get("/customers")
def get_customers():
    sql = "SELECT * FROM customers"
    return {"customers": SQLExecutor().execute(sql)}


# ✅ Route 3: Fetch all orders
@app.get("/orders")
def get_orders():
    @app.get("/orders")
    def get_orders():
        sql = """
        SELECT 
            o.id, 
            c.name AS customer, 
            o.total_amount, 
            o.order_date
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        ORDER BY o.order_date DESC
        """
        return {"orders": SQLExecutor().execute(sql)}


# ✅ Route 4: Ask AI (Gemini-powered SQL generator)
@app.post("/ask")
async def ask_business_ai(request: Request):
    """
    Accepts a natural-language question, sends it to Gemini,
    converts it into SQL, executes the query, and returns results.
    """
    try:
        data = await request.json()
        question = data.get("question", "")
        if not question:
            return {"error": "No question provided."}

        result = ask_ai(question)
        return {"question": question, **result}
    except Exception as e:
        return {"error": str(e)}


# ✅ Start-up event for logging
@app.on_event("startup")
def startup_event():
    print("✅ Application startup complete. Backend is ready to serve requests.")


# ✅ Shutdown event
@app.on_event("shutdown")
def shutdown_event():
    print("🛑 Application shutdown complete.")

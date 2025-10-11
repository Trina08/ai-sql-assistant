from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from chat_system import ask_ai
from sql_executor import SQLExecutor

# Initialize FastAPI app
app = FastAPI(
    title="AI SQL Assistant API",
    description="An AI-powered FastAPI backend that converts natural language questions into SQL queries using Gemini and executes them on PostgreSQL.",
    version="1.0.0"
)

# Allow frontend access (Streamlit or React later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize SQL executor for API endpoints
executor = SQLExecutor()


@app.get("/")
def home():
    """
    Root endpoint for testing the API.
    """
    return {"message": "AI SQL Assistant Backend is Running 🚀"}


@app.get("/products")
def get_products():
    """
    Returns all products from the database.
    """
    sql = "SELECT * FROM products"
    return {"products": executor.execute(sql)}


@app.get("/customers")
def get_customers():
    """
    Returns all customers from the database.
    """
    sql = "SELECT * FROM customers"
    return {"customers": executor.execute(sql)}


@app.get("/orders")
def get_orders():
    """
    Returns all orders with customer names.
    """
    sql = """
    SELECT o.id, c.name AS customer, o.total_amount, o.order_date
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
    ORDER BY o.order_date DESC
    """
    return {"orders": executor.execute(sql)}


@app.post("/ask")
async def ask_business_ai(request: Request):
    """
    POST endpoint that accepts a JSON body:
    {
      "question": "Show me all products and their prices"
    }

    It sends the question to Gemini, gets an SQL query,
    executes it on PostgreSQL, and returns the result.
    """
    try:
        data = await request.json()
        question = data.get("question", "")

        if not question:
            return {"error": "Missing 'question' field in request body."}

        response = ask_ai(question)
        return response

    except Exception as e:
        print(f"❌ Error in /ask route: {e}")
        return {"error": str(e)}
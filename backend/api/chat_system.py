# backend/api/chat_system.py

import os
from dotenv import load_dotenv
import google.generativeai as genai
from sql_executor import SQLExecutor


# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("MODEL_NAME", "models/gemini-2.5-flash")

# Initialize SQL executor
executor = SQLExecutor()

def ask_ai(question: str):
    """
    Uses Gemini to:
      1. Generate SQL for the given natural language question.
      2. Explain what the query does in plain English.
      3. Execute it safely and return the results.
    """
    sql_prompt = f"""
    You are an expert data analyst. Convert this user question into
    a valid PostgreSQL SQL query based on the following database schema:

    - products(id, name, category, price)
    - customers(id, name, email)
    - orders(id, customer_id, total_amount, order_date)
    - order_items(id, order_id, product_id, quantity, unit_price)

    Question: "{question}"

    Rules:
    - Return only the SQL query (no explanations, no markdown)
    - It must start with SELECT
    """

    explain_prompt = f"""
    Explain in one short sentence what this SQL query does, in plain English:
    "{question}"
    """

    try:
        # Generate SQL
        model = genai.GenerativeModel(model_name=MODEL)
        sql_response = model.generate_content(sql_prompt)
        sql_query = sql_response.text.strip().replace("```sql", "").replace("```", "").strip()

        if not sql_query.lower().startswith("select"):
            raise ValueError(f"Invalid SQL generated: {sql_query}")

        # Generate explanation
        explain_response = model.generate_content(explain_prompt)
        explanation = explain_response.text.strip().replace("**", "")

        print("\n🤖 GEMINI GENERATED SQL:")
        print(sql_query)

        # Execute SQL
        result = executor.execute(sql_query)

        return {
            "question": question,
            "query": sql_query,
            "explanation": explanation,
            "result": result
        }

    except Exception as e:
        print(f"❌ Error in ask_ai: {e}")
        return {
            "error": str(e),
            "query": None,
            "explanation": None,
            "result": []
        }

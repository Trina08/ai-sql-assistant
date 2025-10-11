from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")
print("Using URL:", db_url)

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM products"))
        print("✅ Connected successfully! Products count:", list(result))
except Exception as e:
    print("❌ Database connection failed:", e)

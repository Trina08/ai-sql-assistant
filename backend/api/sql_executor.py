# sql_executor.py
# backend/api/sql_executor.py
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class SQLExecutor:
    def __init__(self):
        # Get database URL from .env
        db_url = os.getenv("DATABASE_URL")

        if not db_url:
            raise ValueError("DATABASE_URL is not set in the .env file.")

        # Initialize SQLAlchemy engine
        self.engine = create_engine(db_url)

    def validate_query(self, sql: str):
        """
        Validate the SQL query for safety.
        Only allow SELECT queries, and remove trailing semicolons.
        """
        sql = sql.strip().rstrip(";")  # Remove trailing semicolon if present

        # Ensure the query starts with SELECT
        if not sql.lower().startswith("select"):
            raise ValueError("Only SELECT queries are allowed for safety.")

        # Block potentially dangerous keywords
        banned = ["insert", "update", "delete", "drop", "alter", "create"]
        if any(keyword in sql.lower() for keyword in banned):
            raise ValueError("Unsafe SQL detected! Only SELECT queries are permitted.")

        return sql

    def execute(self, sql: str):
        """
        Safely execute a SQL query and return rows as list of dictionaries.
        """
        sql = self.validate_query(sql)

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql))
                # Convert SQLAlchemy Row objects to dictionaries
                rows = result.mappings().all()
                return [dict(row) for row in rows]

        except Exception as e:
            # Capture and return the full error message
            return {"error": str(e)}

from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://job_board_dev:123456@localhost:5432/job_board"

try:
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    print("✅ Connected successfully!")
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")

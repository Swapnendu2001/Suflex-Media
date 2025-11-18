import os
import asyncio
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("POSTGRES_CONNECTION_URL")

async def drop_all_tables():
    """
    Drop all tables from the database along with their data.
    This operation is irreversible and will delete all data.
    """
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        print("✓ Connected to database")
        
        tables = ['case_studies', 'blogs', 'admin_users']
        
        for table in tables:
            try:
                await conn.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                print(f"✓ Dropped table: {table}")
            except asyncpg.PostgresError as e:
                print(f"✗ Error dropping table {table}: {e}")
        
        print("\n✓ All tables dropped successfully")
        
        await conn.close()
        print("✓ Database connection closed")
        
    except asyncpg.PostgresError as e:
        print(f"✗ Database error: {e}")
        raise
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(drop_all_tables())
"""
Simple test to verify asyncpg implementation
"""
import os
import sys

# Add the Suflex-Media directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.path.abspath('../Suflex-Media'))

from data.db_handler_async import initialize_database
from data.db_handler_async.db_pool import close_db_pool
import asyncio


async def test_init():
    print("Testing database initialization...")
    try:
        await initialize_database()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False
    
    await close_db_pool()
    print("✓ Connection pool closed")
    return True


if __name__ == "__main__":
    if not os.getenv("POSTGRES_CONNECTION_URL"):
        print("Warning: POSTGRES_CONNECTION_URL environment variable not set.")
        print("Please set it before running the test.")
    else:
        success = asyncio.run(test_init())
        if success:
            print("\n✓ Basic asyncpg functionality test passed!")
        else:
            print("\n✗ Basic asyncpg functionality test failed!")
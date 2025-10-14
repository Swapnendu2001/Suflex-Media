"""
Test script to verify the asyncpg implementation works correctly
"""
import asyncio
import os
from data.db_handler_async import initialize_database, admin_login_db_check, get_blogs_list_db
from data.db_handler_async.db_pool import close_db_pool


async def test_database_connection():
    print("Testing asyncpg database implementation...")
    
    try:
        # Initialize the database
        print("1. Initializing database...")
        await initialize_database()
        print("   ✓ Database initialized successfully")
        
        # Test a simple query
        print("2. Testing basic query...")
        result, count = get_blogs_list_db()
        print(f"   ✓ Blog query successful, found {len(result)} blogs (count: {count})")
        
        # Test admin login function (should return appropriate response even if user doesn't exist)
        print("3. Testing admin login function...")
        login_result = admin_login_db_check("test@example.com", "wrongpassword")
        print(f"   ✓ Admin login test completed: {login_result['success']}")
        
        print("\n✓ All tests passed! Asyncpg implementation is working correctly.")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Close the database connection pool
        await close_db_pool()
        print("✓ Database connection pool closed")


if __name__ == "__main__":
    # Set the database URL from environment (you need to have this configured)
    if not os.getenv("POSTGRES_CONNECTION_URL"):
        print("Warning: POSTGRES_CONNECTION_URL environment variable not set.")
        print("Please set it before running the test.")
        exit(1)
    
    # Run the test
    asyncio.run(test_database_connection())
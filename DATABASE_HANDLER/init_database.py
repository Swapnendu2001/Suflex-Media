import os
import asyncpg
from dotenv import load_dotenv
from .utils import sha256_hash

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("POSTGRES_CONNECTION_URL")

async def ensure_admin_user(conn):
    try:
        # Check if admin user exists
        admin_exists = await conn.fetchval(
            "SELECT EXISTS(SELECT 1 FROM admin_users WHERE username = $1)",
            "admin"
        )
        
        if admin_exists:
            print("✓ Admin user already exists")
        else:
            # Create admin user
            await conn.execute(
                """
                INSERT INTO admin_users (email, username, password)
                VALUES ($1, $2, $3)
                """,
                sha256_hash("admin@gmail.com"),
                "admin",
                sha256_hash("admin")
            )
            print("✓ Default admin user created successfully")
            
    except asyncpg.PostgresError as e:
        print(f"✗ Error ensuring admin user: {e}")
        raise

async def initialize_database():
    """
    Initialize the database by running the SQL file.
    Creates tables if they don't exist.
    """
    try:
        # Connect to the database
        conn = await asyncpg.connect(DATABASE_URL)
        
        # Read the SQL file
        sql_file_path = os.path.join(os.path.dirname(__file__), 'init_db.sql')
        with open(sql_file_path, 'r') as f:
            sql_script = f.read()
        
        sql_script = sql_script.strip()
        if sql_script == "":
            print("No SQL commands found in init_db.sql")
            print("✓ Database tables initialized successfully (no changes made)")
        else:
            print("✓ SQL script loaded successfully")
            # Execute the SQL script
            await conn.execute(sql_script)
            print("✓ Database tables initialized successfully")

            # Ensure the default admin user exists
            await ensure_admin_user(conn)
            print("✓ Admin user check completed")
        
        # Close the connection
        await conn.close()
        
    except FileNotFoundError:
        print("✗ Error: init_db.sql file not found")
        raise
    except asyncpg.PostgresError as e:
        print(f"✗ Database error during initialization: {e}")
        raise
    except Exception as e:
        print(f"✗ Unexpected error during database initialization: {e}")
        raise
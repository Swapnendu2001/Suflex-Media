import asyncpg
import asyncio


async def main():
    """
    Connect to PostgreSQL database, list all tables, and drop them.
    """
    conn_url = "postgresql://postgres:xvUoelvuPpKpjuUqyoxnunZLwIKfHMay@caboose.proxy.rlwy.net:59811/railway"
    
    conn = await asyncpg.connect(conn_url)
    
    try:
        tables_query = """
        SELECT tablename 
        FROM pg_tables 
        WHERE schemaname = 'public'
        """
        
        tables = await conn.fetch(tables_query)
        
        print("Tables found:")
        table_names = []
        for table in tables:
            table_name = table['tablename']
            print(f"  - {table_name}")
            table_names.append(table_name)
        
        if table_names:
            print("\nDropping all tables...")
            
            for table_name in table_names:
                drop_query = f'DROP TABLE IF EXISTS "{table_name}" CASCADE'
                await conn.execute(drop_query)
                print(f"  Dropped: {table_name}")
            
            print("\nAll tables dropped successfully!")
        else:
            print("No tables found in the database.")
    
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())# PostgreSQL connection URL
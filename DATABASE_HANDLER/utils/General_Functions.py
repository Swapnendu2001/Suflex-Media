import hashlib

def sha256_hash(input_string):
    encoded_string = input_string.encode('utf-8')
    sha256_hash = hashlib.sha256(encoded_string)
    return sha256_hash.hexdigest()
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("POSTGRES_CONNECTION_URL")

async def store_pdf_download(first_name: str, last_name: str, email: str, company_name: str, mobile_number: str, pdf_link: str):
    """
    Store the details of a PDF download in the database.
    """
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute(
            """
            INSERT INTO pdf_downloads (first_name, last_name, email, company_name, mobile_number, pdf_link)
            VALUES ($1, $2, $3, $4, $5, $6)
            """,
            first_name,
            last_name,
            email,
            company_name,
            mobile_number,
            pdf_link,
        )
        await conn.close()
        return True
    except Exception as e:
        print(f"Error storing PDF download: {e}")
        return False

import os
import json
import asyncio
import logging
import asyncpg
from dotenv import load_dotenv
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

DATABASE_URL = os.getenv("POSTGRES_CONNECTION_URL")
JSON_FILE_PATH = r"D:\Programming\Projects\suhas_medam\Suflex-Media\debug_case_study.json"

async def create_case_studies_table(conn):
    """
    Creates the case_studies table if it doesn't exist
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS case_studies (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        slug TEXT UNIQUE,
        case_study JSONB NOT NULL,
        status VARCHAR(50) NOT NULL DEFAULT 'draft',
        type VARCHAR(50) NOT NULL DEFAULT 'CASE STUDY',
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        keyword JSONB,
        preview JSONB,
        editors_choice VARCHAR(1) DEFAULT 'N',
        redirect_url TEXT,
        pdf_url TEXT,
        isDeleted BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE INDEX IF NOT EXISTS idx_case_studies_status ON case_studies(status) WHERE isDeleted = FALSE;
    CREATE INDEX IF NOT EXISTS idx_case_studies_type ON case_studies(type) WHERE isDeleted = FALSE;
    CREATE INDEX IF NOT EXISTS idx_case_studies_date ON case_studies(date DESC) WHERE isDeleted = FALSE;
    CREATE INDEX IF NOT EXISTS idx_case_studies_slug ON case_studies(slug) WHERE isDeleted = FALSE;
    CREATE INDEX IF NOT EXISTS idx_case_studies_isDeleted ON case_studies(isDeleted);
    CREATE INDEX IF NOT EXISTS idx_case_studies_keyword ON case_studies USING GIN(keyword);
    CREATE INDEX IF NOT EXISTS idx_case_studies_preview ON case_studies USING GIN(preview);
    CREATE INDEX IF NOT EXISTS idx_case_studies_case_study ON case_studies USING GIN(case_study);
    """
    await conn.execute(create_table_query)
    logger.info("case_studies table created or already exists")

async def insert_case_study_data(conn, data):
    """
    Inserts case study data into the database
    """
    insert_query = """
    INSERT INTO case_studies 
    (id, slug, case_study, status, type, date, keyword, preview, editors_choice, redirect_url, pdf_url, isDeleted, created_at, updated_at)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
    ON CONFLICT (id) DO UPDATE SET
        slug = EXCLUDED.slug,
        case_study = EXCLUDED.case_study,
        status = EXCLUDED.status,
        type = EXCLUDED.type,
        date = EXCLUDED.date,
        keyword = EXCLUDED.keyword,
        preview = EXCLUDED.preview,
        editors_choice = EXCLUDED.editors_choice,
        redirect_url = EXCLUDED.redirect_url,
        pdf_url = EXCLUDED.pdf_url,
        isDeleted = EXCLUDED.isDeleted,
        updated_at = EXCLUDED.updated_at;
    """
    
    await conn.execute(
        insert_query,
        data['id'],
        data['slug'],
        data['case_study'],
        data['status'],
        data['type'],
        data['date'],
        data['keyword'],
        data['preview'],
        data['editors_choice'],
        data['redirect_url'],
        data['pdf_url'],
        data['isDeleted'],
        data['created_at'],
        data['updated_at']
    )
    logger.info(f"Inserted/Updated case study with id: {data['id']}")

async def load_case_study_from_json():
    """
    Loads case study data from JSON file and inserts into database
    """
    try:
        if not os.path.exists(JSON_FILE_PATH):
            logger.error(f"JSON file not found: {JSON_FILE_PATH}")
            return
        
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        logger.info(f"Successfully loaded JSON file: {JSON_FILE_PATH}")
        
        mapped_data = {
            'id': json_data['id'],
            'slug': json_data['slug'],
            'case_study': json_data['blog'],
            'status': json_data['status'],
            'type': json_data['type'],
            'date': datetime.fromisoformat(json_data['date']) if json_data['date'] else None,
            'keyword': json_data['keyword'],
            'preview': json_data['preview'],
            'editors_choice': json_data['editors_choice'],
            'redirect_url': json_data['redirect_url'],
            'pdf_url': json_data['pdf_url'],
            'isDeleted': json_data['isdeleted'],
            'created_at': datetime.fromisoformat(json_data['created_at']) if json_data['created_at'] else None,
            'updated_at': datetime.fromisoformat(json_data['updated_at']) if json_data['updated_at'] else None
        }
        
        conn = await asyncpg.connect(DATABASE_URL)
        
        await create_case_studies_table(conn)
        await insert_case_study_data(conn, mapped_data)
        
        await conn.close()
        
        logger.info("Successfully loaded case study data into database")
        
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON file: {e}")
        raise
    except asyncpg.PostgresError as e:
        logger.error(f"Database error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(load_case_study_from_json())
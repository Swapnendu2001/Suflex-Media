import uuid
from .db_sync_utils import execute_query, execute_mutation
from .files import delete_file_from_storage


def get_magazine_url(name):
    # In asyncpg implementation, we might need to construct URLs differently
    # depending on how the files are stored
    base_url = "http://localhost:8000" # This would be configured based on your setup
    return f"{base_url}/storage/magazine-pdfs/{name}"


def create_magazine_db(title, pdf_file, thumbnail_file, created_by):
    pdf_filename = None
    thumbnail_filename = None
    
    try:
        # In asyncpg implementation, we need to handle file uploads separately
        # For now, we'll simulate the file upload process and store URLs
        # This is a simplified version - in real implementation you'd handle file storage separately
        
        # Generate filenames
        if pdf_file:
            pdf_filename = f"{uuid.uuid4()}-{pdf_file.filename}"
            # In a real implementation, you would save the file to your storage system
            # and get a public URL back
            pdf_url = f"/static/magazine-pdfs/{pdf_filename}"
        else:
            return {"status": "error", "message": "PDF file is required"}
        
        # Handle thumbnail if provided
        if thumbnail_file:
            thumbnail_filename = f"{uuid.uuid4()}-{thumbnail_file.filename}"
            # In a real implementation, you would save the file to your storage system
            thumbnail_url = f"/static/magazine-thumbnails/{thumbnail_filename}"
        else:
            thumbnail_url = None

        # Insert record into the database
        magazine_id = str(uuid.uuid4())
        insert_query = """
            INSERT INTO magazine_details (id, title, pdf_url, thumbnail_url, created_by) 
            VALUES ($1, $2, $3, $4, $5) 
            RETURNING *
        """
        params = (magazine_id, title, pdf_url, thumbnail_url, created_by)
        
        result = execute_mutation(insert_query, params)
        
        if result:
            return {"status": "success", "data": result[0]}
        else:
            # This case might be hit if the insert fails for reasons other than an exception
            raise Exception("Failed to save magazine details to database.")

    except Exception as e:
        # In a real implementation, you would clean up uploaded files here
        if pdf_filename:
            # delete_file_from_storage(pdf_filename)  # This would delete the uploaded file
            pass
        if thumbnail_filename:
            # delete_file_from_storage(thumbnail_filename)  # This would delete the uploaded file
            pass
        
        print(f"Error creating magazine: {e}")
        return {"status": "error", "message": str(e)}


def get_recent_magazines_db(limit=9):
    print(f"Fetching recent magazines with limit: {limit}")
    query = """
        SELECT * 
        FROM magazine_details 
        ORDER BY created_at DESC 
        LIMIT $1
    """
    result = execute_query(query, (limit,))
    if result:
        return result
    return []


def get_magazine_details_db(magazine_id):
    print(f"Fetching magazine details for ID: {magazine_id}")
    query = "SELECT * FROM magazine_details WHERE id = $1"
    result = execute_query(query, (magazine_id,))
    if result:
        return result[0]
    return None


def delete_magazine_from_db(magazine_id):
    try:
        # 1. Get file URLs from the database record
        record_query = "SELECT pdf_url, thumbnail_url FROM magazine_details WHERE id = $1"
        record_result = execute_query(record_query, (magazine_id,))
        if not record_result:
            return {"status": "error", "message": "Magazine not found."}

        record = record_result[0]
        pdf_url = record.get("pdf_url")
        thumbnail_url = record.get("thumbnail_url")

        # 2. Delete the database record first
        delete_db_query = "DELETE FROM magazine_details WHERE id = $1 RETURNING *"
        delete_db_result = execute_mutation(delete_db_query, (magazine_id,))
        if not delete_db_result:
            raise Exception("Failed to delete magazine record from database.")

        # 3. Delete files from storage (in real implementation)
        # In asyncpg implementation, this would handle file deletion from actual storage
        if pdf_url:
            # Extract filename from URL and delete the file
            # delete_file_from_storage(pdf_url)  # This would delete the actual file
            pass

        if thumbnail_url:
            # Extract filename from URL and delete the file
            # delete_file_from_storage(thumbnail_url)  # This would delete the actual file
            pass

        return {"status": "success", "message": "Magazine deleted successfully."}
    except Exception as e:
        print(f"Error deleting magazine: {str(e)}")
        return {"status": "error", "message": str(e)}
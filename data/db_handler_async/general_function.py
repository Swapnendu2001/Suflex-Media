import hashlib
import random
from typing import List, Tuple, Optional
from .db_sync_utils import execute_query, execute_mutation


def sha256_hash(input_string):
    encoded_string = input_string.encode('utf-8')
    sha256_hash_obj = hashlib.sha256(encoded_string)
    return sha256_hash_obj.hexdigest()


def get_page_data(page_name: str):
    query = "SELECT * FROM main_pages WHERE page_name = $1"
    result = execute_query(query, (page_name,))
    return result[0] if result else None


def format_file_size(size_bytes):
    """Convert bytes to human readable format (B, KB, MB, GB, TB)"""
    if size_bytes is None:
        return "N/A"
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    try:
        size_bytes = float(size_bytes)
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"
    except (ValueError, TypeError):
        return "N/A"
    

def get_leadership_details():
    query = "SELECT * FROM leadership_table LIMIT 1"
    result = execute_query(query)
    return result[0] if result else None


def get_main_pages_db(search_keyword: Optional[str] = None, page: int = 1, per_page: int = 100, include_deleted: bool = False):
    print(
        f"Searching main pages with keyword: {search_keyword}, page: {page}, per_page: {per_page}"
    )

    offset = (page - 1) * per_page

    # Base query with count
    if search_keyword and search_keyword.strip():
        search_term = f'%{search_keyword.lower()}%'
        query = """
            SELECT *, COUNT(*) OVER() as total_count 
            FROM main_pages 
            WHERE (page_name ILIKE $1 OR page_data->>'status' ILIKE $1)
            AND (page_data->>'status' IS NULL OR page_data->>'status' != 'DELETED')
            ORDER BY updated_at DESC 
            LIMIT $2 OFFSET $3
        """
        params = (search_term, per_page, offset)
    else:
        query = """
            SELECT *, COUNT(*) OVER() as total_count 
            FROM main_pages 
            WHERE (page_data->>'status' IS NULL OR page_data->>'status' != 'DELETED')
            ORDER BY updated_at DESC 
            LIMIT $1 OFFSET $2
        """
        params = (per_page, offset)

    result = execute_query(query, params)
    
    # Extract total count from the first row if results exist
    total_count = 0
    if result:
        total_count = result[0].get('total_count', len(result))
        # Remove the total_count from each row since it was just for pagination info
        for row in result:
            if 'total_count' in row:
                del row['total_count']
    
    return result, total_count


def update_main_page_db(page_id: str, page_data):
    try:
        query = """
            UPDATE main_pages 
            SET page_data = $1, updated_at = NOW()
            WHERE page_id = $2
            RETURNING *
        """
        params = (page_data, page_id)
        
        result = execute_mutation(query, params)
        
        if result:
            return {"status": "success", "data": result[0]}
        else:
            return {"status": "error", "message": "Page not found or could not be updated."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def delete_main_page_db(page_id: str):
    try:
        # Get the current page_data
        select_query = "SELECT page_data FROM main_pages WHERE page_id = $1"
        page_result = execute_query(select_query, (page_id,))
        
        if not page_result:
            return {"status": "error", "message": "Page not found."}

        page_data = page_result[0].get("page_data", {})
        
        # Update the status to 'DELETED'
        page_data['status'] = 'DELETED'
        
        # Update the record in the database
        update_query = """
            UPDATE main_pages 
            SET page_data = $1, updated_at = NOW()
            WHERE page_id = $2
            RETURNING *
        """
        params = (page_data, page_id)
        
        result = execute_mutation(update_query, params)

        if result:
            return {"status": "success", "message": "Page status set to DELETED."}
        else:
            return {"status": "error", "message": "Page not found or could not be updated."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

def get_chosen_orgs(k: int = 1):
    """
    Choose one or more organizations based on their weights.
    
    :param k: Number of selections to make.
    :return: List of chosen organization names.
    """
    query = "SELECT organization, percentage FROM organization"
    data = execute_query(query)
    
    if not data:
        return []
    
    names = [item["organization"] for item in data]
    weights = [item["percentage"] for item in data]
    
    return random.choices(names, weights=weights, k=k)
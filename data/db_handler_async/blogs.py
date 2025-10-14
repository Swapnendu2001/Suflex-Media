from typing import List, Dict, Any, Optional
from .db_sync_utils import execute_query, execute_mutation
import uuid


def get_blogs_list_db(search_keyword: Optional[str] = None, page: int = 1, per_page: int = 100, include_deleted: bool = False):
    print(
        f"Searching blogs with keyword: {search_keyword}, page: {page}, per_page: {per_page}"
    )

    offset = (page - 1) * per_page

    # Base query with count
    if not include_deleted:
        if search_keyword and search_keyword.strip():
            search_term = f'%{search_keyword.replace(" ", "_").lower()}%'
            query = """
                SELECT *, COUNT(*) OVER() as total_count 
                FROM blogs 
                WHERE (id ILIKE $1 OR category ILIKE $1)
                AND status != 'deleted'
                ORDER BY created_at DESC 
                LIMIT $2 OFFSET $3
            """
            params = (search_term, per_page, offset)
        else:
            query = """
                SELECT *, COUNT(*) OVER() as total_count 
                FROM blogs 
                WHERE status != 'deleted'
                ORDER BY created_at DESC 
                LIMIT $1 OFFSET $2
            """
            params = (per_page, offset)
    else:
        if search_keyword and search_keyword.strip():
            search_term = f'%{search_keyword.replace(" ", "_").lower()}%'
            query = """
                SELECT *, COUNT(*) OVER() as total_count 
                FROM blogs 
                WHERE (id ILIKE $1 OR category ILIKE $1)
                ORDER BY created_at DESC 
                LIMIT $2 OFFSET $3
            """
            params = (search_term, per_page, offset)
        else:
            query = """
                SELECT *, COUNT(*) OVER() as total_count 
                FROM blogs 
                ORDER BY created_at DESC 
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


def get_blogs_by_category(category: str):
    query = "SELECT * FROM blogs WHERE category = $1 AND status != 'deleted' ORDER BY created_at DESC"
    result = execute_query(query, (category,))
    return result


def get_blog(blog_id: str, render: bool = False):
    query = "SELECT * FROM blogs WHERE id = $1"
    result = execute_query(query, (blog_id,))
    data = result[0] if result else None
    
    # Define template here if needed
    NEWSPAGE_BLANK_TEMPLATE = "<html><head>[[meta tags]]</head><body></body></html>"
    
    if render and data:
        NEWSPAGE_BLANK_TEMPLATE = NEWSPAGE_BLANK_TEMPLATE.replace(
            "[[meta tags]]", data["meta_tags"] or ""
        )
        return NEWSPAGE_BLANK_TEMPLATE
    return data


def handle_blog(
    blog_id: Optional[str] = None,
    insert_data: Optional[Dict] = None,
    update_data: Optional[Dict] = None,
    operation: Optional[str] = None,
):
    if operation == "insert":
        if insert_data is None:
            raise ValueError("insert_data must be provided for insert operation")
        # Insert a new blog
        columns = ", ".join(insert_data.keys())
        placeholders = ", ".join([f"${i+1}" for i in range(len(insert_data))])
        query = f"INSERT INTO blogs ({columns}) VALUES ({placeholders}) RETURNING *"
        params = list(insert_data.values())
        
        result = execute_mutation(query, params)
        return result

    if operation == "update":
        if blog_id is None or update_data is None:
            raise ValueError(
                "blog_id and update_data must be provided for update operation"
            )
        # Update an existing blog
        set_clause = ", ".join([f"{key} = ${i+1}" for i, key in enumerate(update_data.keys())])
        query = f"UPDATE blogs SET {set_clause} WHERE id = ${len(update_data)+1} RETURNING *"
        params = list(update_data.values()) + [blog_id]
        
        result = execute_mutation(query, params)
        return result

    if operation == "delete":
        if blog_id is None:
            raise ValueError("blog_id must be provided for delete operation")
        # Delete a blog (mark as deleted)
        query = "UPDATE blogs SET status = 'deleted' WHERE id = $1 RETURNING *"
        result = execute_mutation(query, (blog_id,))
        return result


def save_blogs_to_db(blog_data: Dict[str, Any]):
    modified_data = {}
    blog_id = blog_data.get("blogTitle", "").replace(" ", "_").lower()
    modified_data["id"] = blog_id
    modified_data["created_by"] = blog_data.get("admin_name", "")
    modified_data["status"] = blog_data.get("status", "draft")

    # Extract category and SEO information for separate storage if needed
    modified_data["category"] = blog_data.get("blogCategory", "")
    
    # Extract and store labels in JSON format
    labels_data = blog_data.get("labels", {})
    modified_data["labels"] = labels_data if isinstance(labels_data, dict) else {}

    # Generate meta tags from SEO data
    seo_title = blog_data.get("seoTitle", "") or blog_data.get("blogTitle", "")
    seo_description = blog_data.get("seoMetaDescription", "") or blog_data.get(
        "blogSummary", ""
    )
    seo_canonical = (
        blog_data.get("seoCanonicalUrl", "")
        or f"{blog_data.get('base_url', '')}/blog/{modified_data['id']}"
    )

    # Create meta tags HTML
    meta_tags = f"""<title>{seo_title}</title>
    <meta name="description" content="{seo_description}">
    <meta property="og:title" content="{seo_title}">
    <meta property="og:description" content="{seo_description}">
    <meta property="og:image" content="{blog_data.get('mainImageUrl', '')}">
    <meta property="og:url" content="{seo_canonical}">
    <meta property="og:type" content="article">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{seo_title}">
    <meta name="twitter:description" content="{seo_description}">
    <meta name="twitter:image" content="{blog_data.get('mainImageUrl', '')}">
    <link rel="canonical" href="{seo_canonical}">"""

    modified_data["meta_tags"] = meta_tags

    # Store the base_url before cleaning up for the return URL
    base_url = blog_data.get("base_url", "")

    # Clean up fields before storing in json_data
    fields_to_remove = ["admin_name", "status", "enc_email", "enc_pwd", "base_url", "labels"]
    for field in fields_to_remove:
        if field in blog_data:
            del blog_data[field]

    # Store the complete blog data including category and SEO information
    modified_data["json_data"] = blog_data
    
    # Check if a blog with the same ID exists and is in deleted state
    try:
        existing_blog_query = "SELECT * FROM blogs WHERE id = $1"
        existing_blog_result = execute_query(existing_blog_query, (blog_id,))
        existing_blog = existing_blog_result[0] if existing_blog_result else None
        
        if existing_blog and existing_blog.get("status") == "deleted":
            # Update the existing deleted blog instead of inserting
            print(f"Found existing deleted blog with ID: {blog_id}. Updating instead of inserting.")
            
            # Clear redirect URL when updating from deleted state
            modified_data["redirect_url"] = None
            
            # Get existing blog history and append to it
            if existing_blog and "history" in existing_blog:
                modified_data["history"] = existing_blog["history"]
                modified_data["history"].append(
                    {
                        "admin_name": modified_data["created_by"],
                        "date": blog_data.get("blogDate", ""),
                        "action": "restored_from_deleted",
                    }
                )
            else:
                modified_data["history"] = [
                    {
                        "admin_name": modified_data["created_by"],
                        "date": blog_data.get("blogDate", ""),
                        "action": "restored_from_deleted",
                    }
                ]
            
            # Update the existing blog
            set_clause = ", ".join([f"{key} = ${i+1}" for i, key in enumerate(modified_data.keys())])
            update_query = f"UPDATE blogs SET {set_clause} WHERE id = ${len(modified_data)+1} RETURNING *"
            params = list(modified_data.values()) + [blog_id]
            
            result = execute_mutation(update_query, params)
            
            if result:
                result[0]["url"] = f"{base_url}/blog/{modified_data['id']}"
                return result[0]
            else:
                return {
                    "status": "error",
                    "message": "Failed to update existing deleted blog.",
                }
        else:
            # Insert new blog (original logic)
            modified_data["history"] = [
                {
                    "admin_name": modified_data["created_by"],
                    "date": blog_data.get("blogDate", ""),
                }
            ]
            
            # Debug: Print what data is being stored
            print(f"Inserting new blog with data: {modified_data}")
            
            # Insert the blog
            columns = ", ".join(modified_data.keys())
            placeholders = ", ".join([f"${i+1}" for i in range(len(modified_data))])
            insert_query = f"INSERT INTO blogs ({columns}) VALUES ({placeholders}) RETURNING *"
            params = list(modified_data.values())
            
            result = execute_mutation(insert_query, params)
            
            # Use the stored base_url for the return URL
            result[0]["url"] = f"{base_url}/blog/{modified_data['id']}"
            return result[0]
            
    except Exception as e:
        print(f"Error saving blog to database: {e}")
        error_str = str(e)
        print(f"Error string: {error_str}")
        if (
            "23505" in error_str
            and "duplicate key value violates unique constraint" in error_str
        ):
            return {
                "status": "error",
                "message": "Blog with this title already exists.",
            }
        return {
            "status": "error",
            "message": f"Failed to save blog: {str(e)}",
        }


def update_blogs_to_db(blog_data: Dict[str, Any]):
    blog_id = blog_data.get("blog_id")
    if not blog_id:
        return {"status": "error", "message": "Blog ID is required for update."}

    # Prepare update data similar to save_blogs_to_db
    modified_data = {}
    modified_data["id"] = blog_data.get("blogTitle", "").replace(" ", "_").lower()
    modified_data["created_by"] = blog_data.get("admin_name", "")
    modified_data["status"] = blog_data.get("status", "draft")

    # Extract category and SEO information
    modified_data["category"] = blog_data.get("blogCategory", "")
    
    # Extract and store labels in JSON format
    labels_data = blog_data.get("labels", {})
    modified_data["labels"] = labels_data if isinstance(labels_data, dict) else {}

    # Generate meta tags from SEO data
    seo_title = blog_data.get("seoTitle", "") or blog_data.get("blogTitle", "")
    seo_description = blog_data.get("seoMetaDescription", "") or blog_data.get(
        "blogSummary", ""
    )
    seo_canonical = (
        blog_data.get("seoCanonicalUrl", "")
        or f"{blog_data.get('base_url', '')}/blog/{modified_data['id']}"
    )

    # Create meta tags HTML
    meta_tags = f"""<title>{seo_title}</title>
    <meta name="description" content="{seo_description}">
    <meta property="og:title" content="{seo_title}">
    <meta property="og:description" content="{seo_description}">
    <meta property="og:image" content="{blog_data.get('mainImageUrl', '')}">
    <meta property="og:url" content="{seo_canonical}">
    <meta property="og:type" content="article">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{seo_title}">
    <meta name="twitter:description" content="{seo_description}">
    <meta name="twitter:image" content="{blog_data.get('mainImageUrl', '')}">
    <link rel="canonical" href="{seo_canonical}">"""

    modified_data["meta_tags"] = meta_tags

    # Store the base_url before cleaning up
    base_url = blog_data.get("base_url", "")

    # Clean up fields before storing in json_data
    fields_to_remove = [
        "admin_name",
        "status",
        "enc_email",
        "enc_pwd",
        "base_url",
        "blog_id",
        "reason",
        "labels",
    ]
    for field in fields_to_remove:
        if field in blog_data:
            del blog_data[field]

    # Store the complete blog data
    modified_data["json_data"] = blog_data

    # Get existing blog history and append to it
    existing_blog = get_blog(blog_id)
    if existing_blog and "history" in existing_blog:
        modified_data["history"] = existing_blog["history"]
        modified_data["history"].append(
            {
                "admin_name": modified_data["created_by"],
                "date": blog_data.get("blogDate", ""),
                "action": "updated",
            }
        )
    else:
        modified_data["history"] = [
            {
                "admin_name": modified_data["created_by"],
                "date": blog_data.get("blogDate", ""),
                "action": "updated",
            }
        ]

    try:
        # Update the existing blog
        set_clause = ", ".join([f"{key} = ${i+1}" for i, key in enumerate(modified_data.keys())])
        update_query = f"UPDATE blogs SET {set_clause} WHERE id = ${len(modified_data)+1} RETURNING *"
        params = list(modified_data.values()) + [blog_id]
        
        result = execute_mutation(update_query, params)

        if result:
            result[0]["url"] = f"{base_url}/blog/{modified_data['id']}"
            return {
                "status": "success",
                "message": "Blog updated successfully.",
                "data": result[0],
            }
        else:
            return {
                "status": "error",
                "message": "Blog not found or could not be updated.",
            }

    except Exception as e:
        print(f"Error updating blog: {e}")
        return {"status": "error", "message": str(e)}


def delete_blog_from_db(blog_id: str, redirect_url: Optional[str] = None):
    print(f"Marking blog as deleted with ID: {blog_id}")
    
    # Prepare update data
    update_data = {
        "status": "deleted",
        "meta_tags": ""  # Clear meta tags when marking as deleted
    }
    
    # Add redirect URL if provided
    if redirect_url:
        update_data["redirect_url"] = redirect_url
    
    # Update the blog status instead of deleting
    set_clause = ", ".join([f"{key} = ${i+1}" for i, key in enumerate(update_data.keys())])
    query = f"UPDATE blogs SET {set_clause} WHERE id = ${len(update_data)+1} RETURNING *"
    params = list(update_data.values()) + [blog_id]
    
    result = execute_mutation(query, params)
    
    if result:
        return {"status": "success", "message": "Blog marked as deleted successfully."}
    return {"status": "error", "message": "Blog not found or could not be updated."}
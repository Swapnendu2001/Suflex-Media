import logging
from fastapi import APIRouter, HTTPException, Query, Request, Depends
from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional, Dict, Any, List
import asyncpg
import json
import re
from DATABASE_HANDLER.auth import require_admin
from DATABASE_HANDLER.utils.shared_utils import generate_slug, ensure_unique_slug
from config import config, StatusConstants, ContentTypeConstants

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Blogs Management"])

DATABASE_URL = config.DATABASE_URL

class CreateBlogRequest(BaseModel):
    blogContent: Dict[str, Any]
    status: str = StatusConstants.DRAFT
    keyword: Optional[Dict[str, Any]] = None
    editors_choice: Optional[str] = 'N'
    slug: Optional[str] = None
    redirect_url: Optional[str] = None

    @field_validator('blogContent')
    @classmethod
    def validate_blog_not_empty(cls, v):
        if not v or not isinstance(v, dict):
            raise ValueError('Blog content must be a non-empty dictionary')
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        valid_statuses = [StatusConstants.DRAFT, StatusConstants.PUBLISHED, StatusConstants.ARCHIVED]
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v

    @field_validator('editors_choice')
    @classmethod
    def validate_editors_choice(cls, v):
        if v is not None and v not in ['Y', 'N']:
            raise ValueError('editors_choice must be either "Y" or "N"')
        return v

    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v):
        if v is not None:
            if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', v):
                raise ValueError('Slug must be lowercase alphanumeric with hyphens only')
        return v

    @field_validator('redirect_url')
    @classmethod
    def validate_redirect_url(cls, v):
        if v is not None and v.strip():
            if not re.match(r'^https?://', v):
                raise ValueError('Redirect URL must start with http:// or https://')
        return v

class UpdateBlogRequest(BaseModel):
    blogContent: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    keyword: Optional[Dict[str, Any]] = None
    editors_choice: Optional[str] = None
    slug: Optional[str] = None
    redirect_url: Optional[str] = None

    @field_validator('blogContent')
    @classmethod
    def validate_blog_not_empty(cls, v):
        if v is not None and (not v or not isinstance(v, dict)):
            raise ValueError('Blog content must be a non-empty dictionary if provided')
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = [StatusConstants.DRAFT, StatusConstants.PUBLISHED, StatusConstants.ARCHIVED]
            if v not in valid_statuses:
                raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v

    @field_validator('editors_choice')
    @classmethod
    def validate_editors_choice(cls, v):
        if v is not None and v not in ['Y', 'N']:
            raise ValueError('editors_choice must be either "Y" or "N"')
        return v

    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v):
        if v is not None and v.strip():
            if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', v):
                raise ValueError('Slug must be lowercase alphanumeric with hyphens only')
        return v

    @field_validator('redirect_url')
    @classmethod
    def validate_redirect_url(cls, v):
        if v is not None and v.strip():
            if not re.match(r'^https?://', v):
                raise ValueError('Redirect URL must start with http:// or https://')
        return v

def _extract_blog_image(blog_content: Dict[str, Any]) -> Optional[str]:
    if not blog_content:
        return None
    
    if blog_content.get('mainImageUrl'):
        return blog_content['mainImageUrl']
    
    if blog_content.get('blogTitleImage'):
        return blog_content['blogTitleImage']
    
    if blog_content.get('blog_cover_image') and isinstance(blog_content['blog_cover_image'], dict):
        return blog_content['blog_cover_image'].get('url')
    
    if blog_content.get('blogcontent') and isinstance(blog_content['blogcontent'], dict):
        blocks = blog_content['blogcontent'].get('blocks', [])
        for block in blocks:
            if block.get('type') == 'image' and block.get('data', {}).get('file', {}).get('url'):
                return block['data']['file']['url']
    
    return None


def _parse_blog_content_from_db(blog_content_raw: Any, blog_id: str) -> Dict[str, Any]:
    parsed_content = {}
    if isinstance(blog_content_raw, str):
        try:
            parsed_content = json.loads(blog_content_raw)
        except json.JSONDecodeError:
            logger.error(f"Failed to decode blogcontent JSON for blog ID {blog_id}: {blog_content_raw}")
            return {}
    elif isinstance(blog_content_raw, dict):
        parsed_content = blog_content_raw
    else:
        logger.warning(f"Unexpected type for blogcontent for blog ID {blog_id}: {type(blog_content_raw)}. Expected str or dict.")
        return {}
    
    actual_blog_content = {}
    if 'blogcontent' in parsed_content and isinstance(parsed_content['blogcontent'], dict):
        actual_blog_content = parsed_content['blogcontent']
    elif 'blogContent' in parsed_content and isinstance(parsed_content['blogContent'], dict):
        logger.warning(f"Using camelCase 'blogContent' for blog ID {blog_id}. Consider updating data to use 'blogcontent'.")
        actual_blog_content = parsed_content['blogContent']
    else:
        actual_blog_content = parsed_content
    
    return actual_blog_content

def _format_blog_list(blogs_list_raw: List[asyncpg.Record]) -> List[Dict[str, Any]]:
    formatted_blogs = []
    for blog in blogs_list_raw:
        actual_blog_content = _parse_blog_content_from_db(blog['blogcontent'], str(blog['id']))
        
        keyword_dict = blog['keyword']
        if isinstance(keyword_dict, str):
            try:
                keyword_dict = json.loads(keyword_dict)
            except json.JSONDecodeError:
                logger.error(f"Failed to decode keyword for blog ID {blog['id']}: {keyword_dict}")
                keyword_dict = {}

        blog_category = blog.get('category', '')
        if not blog_category:
            blog_category = actual_blog_content.get('blogcategory') or actual_blog_content.get('blogCategory') or ''

        cover_image = _extract_blog_image(actual_blog_content)
        
        actual_blog_content['coverImage'] = cover_image

        formatted_blogs.append({
            "id": str(blog['id']),
            "blogContent": actual_blog_content,
            "status": blog['status'],
            "date": blog['date'].isoformat() if blog['date'] else None,
            "keyword": keyword_dict,
            "category": blog_category,
            "slug": blog['slug'],
            "type": blog['type'],
            "redirect_url": blog['redirect_url'],
            "isdeleted": blog['isdeleted'],
            "created_at": blog['created_at'].isoformat() if blog['created_at'] else None,
            "updated_at": blog['updated_at'].isoformat() if blog['updated_at'] else None,
            "editors_choice": blog.get('editors_choice', 'N'),
            "coverImage": cover_image
        })
    return formatted_blogs


@router.get("/blogs")
async def get_blogs(
    include_deleted: bool = Query(False, description="Include soft-deleted blogs"),
    purpose: Optional[str] = Query(None, description="Purpose of the request, e.g., 'landing_page'")
):
    """
    Get all blogs.
    - By default excludes soft-deleted entries. Set include_deleted=true to show all.
    - Use purpose=landing_page to get blogs structured for the landing page sections.
    """
    try:
        logger.debug(f"Attempting to connect to database with URL: {DATABASE_URL}")
        conn = await asyncpg.connect(DATABASE_URL)
        logger.debug("Successfully connected to database.")

        if purpose == 'landing_page':
            query = """
                SELECT id, blogContent, status, date, keyword, slug, type, redirect_url, category, isdeleted, created_at, updated_at, editors_choice
                FROM blogs
                WHERE isdeleted = FALSE AND status = 'published'
                ORDER BY date DESC
            """
            logger.debug(f"Executing query for landing_page: {query}")
            all_blogs = await conn.fetch(query)
            logger.debug(f"Fetched {len(all_blogs)} blogs for landing_page. Raw data: {all_blogs}")
            
            editors_choice_blogs = [b for b in all_blogs if b['editors_choice'] == 'Y']
            other_blogs = [b for b in all_blogs if b['editors_choice'] != 'Y']

            # The 3 most recent non-editor's-choice blogs for "Latest Gossip"
            latest_gossip_blogs = other_blogs[:3]
            # The rest for "Read More"
            read_more_blogs = other_blogs[3:]

            await conn.close()
            
            return {
                "status": "success",
                "sections": {
                    "editors_choice": _format_blog_list(editors_choice_blogs),
                    "latest_gossip": _format_blog_list(latest_gossip_blogs),
                    "read_more": _format_blog_list(read_more_blogs)
                }
            }
        
        else:
            if include_deleted:
                query = """
                    SELECT id, blogContent, status, date, keyword, slug, type, redirect_url, category, isdeleted, created_at, updated_at, editors_choice
                    FROM blogs
                    ORDER BY date DESC
                """
            else:
                query = """
                    SELECT id, blogContent, status, date, keyword, slug, type, redirect_url, category, isdeleted, created_at, updated_at, editors_choice
                    FROM blogs
                    WHERE isdeleted = FALSE
                    ORDER BY date DESC
                """
            
            logger.debug(f"Executing query for general blogs: {query}")
            blogs = await conn.fetch(query)
            logger.debug(f"Fetched {len(blogs)} general blogs. Raw data: {blogs}")
            await conn.close()
            
            blogs_list = _format_blog_list(blogs)
            
            return {"status": "success", "blogs": blogs_list, "count": len(blogs_list)}
            
    except asyncpg.PostgresError as e:
        logger.error(f"Database error in get_blogs: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in get_blogs: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/blogs", status_code=201)
async def create_blog(blog_data: CreateBlogRequest, current_user: Dict[str, Any] = Depends(require_admin)):
    """
    Create a new blog
    Requires blog content as JSONB
    Optional fields: status, keyword, redirect_url
    """
    logger.info(f"Creating new blog with status: {blog_data.status}")
    
    if not blog_data.blogContent:
        raise HTTPException(status_code=400, detail="Blog content is required")
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        # Extract the type from blog data if it exists
        blog_content = blog_data.blogContent.copy() if blog_data.blogContent else {}
        content_type = blog_content.get('contentType', ContentTypeConstants.BLOG)
        
        new_blog = await conn.fetchrow(
            """
            INSERT INTO blogs (blogContent, status, keyword, editors_choice, slug, type, redirect_url, isdeleted)
            VALUES ($1, $2, $3, $4, $5, $6, $7, FALSE)
            RETURNING id, blogContent, status, date, keyword, editors_choice, slug, type, redirect_url, isdeleted, created_at, updated_at
            """,
            json.dumps(blog_content),
            blog_data.status,
            json.dumps(blog_data.keyword),
            blog_data.editors_choice,
            blog_data.slug,
            content_type,
            blog_data.redirect_url
        )
        
        await conn.close()
        
        logger.info(f"Blog created successfully with ID: {new_blog['id']}")
        return {
            "status": "success",
            "message": "Blog created successfully",
            "blog": {
                "id": str(new_blog['id']),
                "blogContent": _parse_blog_content_from_db(new_blog['blogcontent'], str(new_blog['id'])),
                "status": new_blog['status'],
                "date": new_blog['date'].isoformat() if new_blog['date'] else None,
                "keyword": json.loads(new_blog['keyword']) if isinstance(new_blog['keyword'], str) else new_blog['keyword'],
                "category": _parse_blog_content_from_db(new_blog['blogcontent'], str(new_blog['id'])).get('blogcategory', 'General'),
                "slug": new_blog['slug'],
                "type": new_blog['type'],
                "redirect_url": new_blog['redirect_url'],
                "isdeleted": new_blog['isdeleted'],
                "created_at": new_blog['created_at'].isoformat() if new_blog['created_at'] else None,
                "updated_at": new_blog['updated_at'].isoformat() if new_blog['updated_at'] else None
            }
        }
        
    except asyncpg.PostgresError as e:
        logger.error(f"Database error in create_blog: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in create_blog: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/blogs/{blog_id}")
async def update_blog(blog_id: str, blog_data: UpdateBlogRequest, current_user: Dict[str, Any] = Depends(require_admin)):
    """
    Update an existing blog
    Only updates provided fields (partial update)
    Cannot update soft-deleted blogs
    """
    logger.info(f"Updating blog ID: {blog_id}")
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        existing_blog = await conn.fetchrow(
            "SELECT id, isdeleted FROM blogs WHERE id = $1",
            blog_id
        )
        
        if not existing_blog:
            await conn.close()
            raise HTTPException(status_code=404, detail="Blog not found")
        
        if existing_blog['isdeleted']:
            await conn.close()
            raise HTTPException(status_code=400, detail="Cannot update deleted blog")
        
        update_fields = []
        update_values = []
        param_count = 1
        
        if blog_data.blogContent is not None:
            update_fields.append(f"blogContent = ${param_count}")
            update_values.append(json.dumps(blog_data.blogContent))
            param_count += 1
        
        if blog_data.status is not None:
            update_fields.append(f"status = ${param_count}")
            update_values.append(blog_data.status)
            param_count += 1
        
        if blog_data.keyword is not None:
            update_fields.append(f"keyword = ${param_count}")
            update_values.append(json.dumps(blog_data.keyword))
            param_count += 1
        
        if blog_data.slug is not None:
            update_fields.append(f"slug = ${param_count}")
            update_values.append(blog_data.slug)
            param_count += 1
        
        if blog_data.editors_choice is not None:
            update_fields.append(f"editors_choice = ${param_count}")
            update_values.append(blog_data.editors_choice)
            param_count += 1
        
        if blog_data.redirect_url is not None:
            update_fields.append(f"redirect_url = ${param_count}")
            update_values.append(blog_data.redirect_url)
            param_count += 1
        
        if not update_fields:
            await conn.close()
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_fields.append(f"updated_at = CURRENT_TIMESTAMP")
        update_values.append(blog_id)
        
        query = f"""
            UPDATE blogs
            SET {', '.join(update_fields)}
            WHERE id = ${param_count}
            RETURNING id, blogContent, status, date, keyword, slug, type, redirect_url, isdeleted, created_at, updated_at
        """
        
        updated_blog = await conn.fetchrow(query, *update_values)
        await conn.close()
        
        logger.info(f"Blog updated successfully: {blog_id}")
        return {
            "status": "success",
            "message": "Blog updated successfully",
            "blog": {
                "id": str(updated_blog['id']),
                "blogContent": _parse_blog_content_from_db(updated_blog['blogcontent'], str(updated_blog['id'])),
                "status": updated_blog['status'],
                "date": updated_blog['date'].isoformat() if updated_blog['date'] else None,
                "keyword": json.loads(updated_blog['keyword']) if isinstance(updated_blog['keyword'], str) else updated_blog['keyword'],
                "category": _parse_blog_content_from_db(updated_blog['blogcontent'], str(updated_blog['id'])).get('blogcategory', 'General'),
                "slug": updated_blog['slug'],
                "type": updated_blog['type'],
                "redirect_url": updated_blog['redirect_url'],
                "isdeleted": updated_blog['isdeleted'],
                "created_at": updated_blog['created_at'].isoformat() if updated_blog['created_at'] else None,
                "updated_at": updated_blog['updated_at'].isoformat() if updated_blog['updated_at'] else None
            }
        }
        
    except HTTPException:
        raise
    except asyncpg.PostgresError as e:
        logger.error(f"Database error in update_blog: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in update_blog: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.patch("/blogs/{blog_id}")
async def partial_update_blog(blog_id: str, blog_data: UpdateBlogRequest, current_user: Dict[str, Any] = Depends(require_admin)):
    """
    Partial update of an existing blog (alias for PUT endpoint)
    Only updates provided fields
    Cannot update soft-deleted blogs
    """
    return await update_blog(blog_id, blog_data)

@router.delete("/blogs/{blog_id}")
async def delete_blog(blog_id: str, current_user: Dict[str, Any] = Depends(require_admin)):
    """
    Permanently delete a blog from the database
    This action cannot be undone
    """
    logger.warning(f"Permanently deleting blog ID: {blog_id}")
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        blog = await conn.fetchrow(
            "SELECT id FROM blogs WHERE id = $1",
            blog_id
        )
        
        if not blog:
            await conn.close()
            raise HTTPException(status_code=404, detail="Blog not found")
        
        await conn.execute(
            "DELETE FROM blogs WHERE id = $1",
            blog_id
        )
        
        await conn.close()
        
        logger.info(f"Blog permanently deleted successfully: {blog_id}")
        return {
            "status": "success",
            "message": "Blog deleted successfully"
        }
        
    except HTTPException:
        raise
    except asyncpg.PostgresError as e:
        logger.error(f"Database error in delete_blog: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in delete_blog: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/blogs/{blog_id}/restore")
async def restore_blog(blog_id: str, current_user: Dict[str, Any] = Depends(require_admin)):
    """
    Restore a soft-deleted blog
    Sets isdeleted back to FALSE
    """
    logger.info(f"Restoring blog ID: {blog_id}")
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        blog = await conn.fetchrow(
            "SELECT id, isdeleted FROM blogs WHERE id = $1",
            blog_id
        )
        
        if not blog:
            await conn.close()
            raise HTTPException(status_code=404, detail="Blog not found")
        
        if not blog['isdeleted']:
            await conn.close()
            raise HTTPException(status_code=400, detail="Blog is not deleted")
        
        await conn.execute(
            """
            UPDATE blogs
            SET isdeleted = FALSE, updated_at = CURRENT_TIMESTAMP
            WHERE id = $1
            """,
            blog_id
        )
        
        await conn.close()
        
        logger.info(f"Blog restored successfully: {blog_id}")
        return {
            "status": "success",
            "message": "Blog restored successfully"
        }
        
    except HTTPException:
        raise
    except asyncpg.PostgresError as e:
        logger.error(f"Database error in restore_blog: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in restore_blog: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
@router.post("/blogs/{blog_id}/toggle-editors-choice")
async def toggle_editors_choice(blog_id: str, current_user: Dict[str, Any] = Depends(require_admin)):
    """
    Toggle editor's choice status for a blog
    Validates the 5-item maximum limit before setting to 'Y'
    """
    logger.info(f"Toggling editor's choice for blog ID: {blog_id}")
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        existing_blog = await conn.fetchrow(
            "SELECT id, editors_choice, isdeleted FROM blogs WHERE id = $1",
            blog_id
        )
        
        if not existing_blog:
            await conn.close()
            raise HTTPException(status_code=404, detail="Blog not found")
        
        if existing_blog['isdeleted']:
            await conn.close()
            raise HTTPException(status_code=400, detail="Cannot modify deleted blog")
        
        current_status = existing_blog['editors_choice']
        new_status = 'N' if current_status == 'Y' else 'Y'
        
        if new_status == 'Y':
            count_result = await conn.fetchval(
                """
                SELECT COUNT(*) FROM blogs
                WHERE editors_choice = 'Y' AND isdeleted = FALSE AND type = $1
                """,
                ContentTypeConstants.BLOG
            )
            
            if count_result >= 5:
                await conn.close()
                raise HTTPException(
                    status_code=400,
                    detail="Maximum of 5 blogs can be marked as Editor's Choice. Please remove one before adding another."
                )
        
        updated_blog = await conn.fetchrow(
            """
            UPDATE blogs
            SET editors_choice = $1, updated_at = CURRENT_TIMESTAMP
            WHERE id = $2
            RETURNING id, blogContent, status, date, keyword, editors_choice, slug, type, redirect_url, isdeleted, created_at, updated_at
            """,
            new_status,
            blog_id
        )
        
        await conn.close()
        
        logger.info(f"Editor's choice toggled successfully for blog: {blog_id} to {new_status}")
        return {
            "status": "success",
            "message": f"Editor's choice {'added' if new_status == 'Y' else 'removed'} successfully",
            "editors_choice": new_status,
            "blog": {
                "id": str(updated_blog['id']),
                "blogContent": updated_blog['blogcontent'],
                "status": updated_blog['status'],
                "date": updated_blog['date'].isoformat() if updated_blog['date'] else None,
                "keyword": updated_blog['keyword'],
                "editors_choice": updated_blog['editors_choice'],
                "slug": updated_blog['slug'],
                "type": updated_blog['type'],
                "redirect_url": updated_blog['redirect_url'],
                "isdeleted": updated_blog['isdeleted'],
                "created_at": updated_blog['created_at'].isoformat() if updated_blog['created_at'] else None,
                "updated_at": updated_blog['updated_at'].isoformat() if updated_blog['updated_at'] else None
            }
        }
        
    except HTTPException:
        raise
    except asyncpg.PostgresError as e:
        logger.error(f"Database error in toggle_editors_choice: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in toggle_editors_choice: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/blogs/type-counts")
async def get_blog_type_counts():
    """
    Get the current count of blogs for special types.
    """
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        type_counts = await conn.fetch(
            "SELECT type, COUNT(*) as count FROM blogs WHERE type IN ('EDITORS_CHOICE', 'BLOG_HERO', 'BLOG_HOME_PAGE') AND isdeleted = FALSE GROUP BY type"
        )
        
        await conn.close()
        
        counts = {
            "EDITORS_CHOICE": 0,
            "BLOG_HERO": 0,
            "BLOG_HOME_PAGE": 0
        }
        for record in type_counts:
            counts[record['type']] = record['count']

        return {
            "status": "success",
            "counts": counts,
            "limits": {
                "EDITORS_CHOICE": 3,
                "BLOG_HERO": 1,
                "BLOG_HOME_PAGE": 3
            }
        }
    except Exception as e:
        logger.error(f"Error getting blog type counts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/admin_save_blog")
async def admin_save_blog(request: Request, current_user: Dict[str, Any] = Depends(require_admin)):
    """
    Save blog from admin panel (Draft or Publish)
    Receives complete blog data from frontend and saves to database
    Preserves all original JSON key names
    Generates slug from title field
    """
    try:
        data = await request.json()
        
        logger.debug("=" * 80)
        logger.debug("RECEIVED BLOG DATA FROM FRONTEND:")
        logger.debug(json.dumps(data, indent=2))
        logger.debug("=" * 80)
        
        blog_title = data.get('blogTitle', '')
        if not blog_title:
            raise HTTPException(status_code=400, detail="Blog title is required")
        
        blog_id = data.get('blog_id')
        reason = data.get('reason', 'create')
        
        slug = generate_slug(blog_title)
        blog_status = data.get('blogStatus', StatusConstants.DRAFT)
        
        # Handle blog type and limits
        blog_type = data.get('blogType', 'GENERAL')
        editors_choice_val = 'Y' if blog_type == 'EDITORS_CHOICE' else 'N'

        conn = await asyncpg.connect(DATABASE_URL)
        
        try:
            # Check limits for special types
            type_limits = {"EDITORS_CHOICE": 3, "BLOG_HERO": 1, "BLOG_HOME_PAGE": 3}
            if blog_type in type_limits:
                query = "SELECT COUNT(*) FROM blogs WHERE type = $1 AND isdeleted = FALSE"
                params = [blog_type]
                if blog_id:
                    query += " AND id != $2"
                    params.append(blog_id)
                
                count = await conn.fetchval(query, *params)
                if count >= type_limits[blog_type]:
                    raise HTTPException(status_code=400, detail=f"Maximum of {type_limits[blog_type]} blogs can be marked as {blog_type.replace('_', ' ')}.")

            if reason == 'update' and blog_id:
                existing_blog = await conn.fetchrow("SELECT id, slug FROM blogs WHERE id = $1 AND isdeleted = FALSE", blog_id)
                if not existing_blog:
                    raise HTTPException(status_code=404, detail="Blog not found for update")
                
                if slug != existing_blog['slug']:
                    slug = await ensure_unique_slug(conn, slug, "blogs", blog_id)
                
                blog_category = data.get('blogCategory', '')
                
                updated_blog = await conn.fetchrow(
                    """
                    UPDATE blogs
                    SET blogContent = $1, status = $2, editors_choice = $3, slug = $4, type = $5, category = $6, updated_at = CURRENT_TIMESTAMP
                    WHERE id = $7
                    RETURNING id, slug
                    """,
                    json.dumps(data), blog_status, editors_choice_val, slug, blog_type, blog_category, blog_id
                )
                
                if not updated_blog:
                    raise HTTPException(status_code=404, detail="Blog not found for update")
                
                blog_url = f"{config.BACKEND_URL}/blog/{updated_blog['slug']}"
                logger.info(f"Blog updated successfully - ID: {blog_id}, slug: {updated_blog['slug']}, status: {blog_status}, type: {blog_type}")
                
                return {"status": "success", "message": "Blog updated successfully", "blog_id": blog_id, "slug": updated_blog['slug'], "url": blog_url}
            else:
                slug = await ensure_unique_slug(conn, slug, "blogs")
                blog_category = data.get('blogCategory', '')
                
                new_blog = await conn.fetchrow(
                    """
                    INSERT INTO blogs (blogContent, status, editors_choice, slug, type, category, isdeleted)
                    VALUES ($1, $2, $3, $4, $5, $6, FALSE)
                    RETURNING id, slug
                    """,
                    json.dumps(data), blog_status, editors_choice_val, slug, blog_type, blog_category
                )
                
                blog_id = str(new_blog['id'])
                blog_url = f"{config.BACKEND_URL}/blog/{new_blog['slug']}"
                logger.info(f"Blog saved successfully - ID: {blog_id}, slug: {new_blog['slug']}, status: {blog_status}, type: {blog_type}")
                
                return {"status": "success", "message": "Blog saved successfully", "blog_id": blog_id, "slug": new_blog['slug'], "url": blog_url}
            
        finally:
            await conn.close()
        
    except HTTPException:
        raise
    except asyncpg.UniqueViolationError:
        logger.warning("Slug already exists")
        raise HTTPException(status_code=400, detail="A blog with this title already exists")
    except asyncpg.PostgresError as e:
        logger.error(f"Database error in admin_save_blog: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in admin_save_blog: {e}")
        raise HTTPException(status_code=500, detail=str(e))


from DATABASE_HANDLER.utils.General_Functions import store_pdf_download
class PDFDownloadFormRequest(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    email: str
    company_name: Optional[str] = None
    mobile_number: Optional[str] = None
    pdf_link: str # For blogs, this will be the blog slug


@router.post("/pdf-download-form-blog")
async def save_pdf_download_form_blog(form_data: PDFDownloadFormRequest):
    """
    Save PDF download form submission to the database for a blog.
    """
    logger.info(f"Saving PDF download form for blog: {form_data.pdf_link}")
    
    success = await store_pdf_download(
        first_name=form_data.first_name,
        last_name=form_data.last_name,
        email=form_data.email,
        company_name=form_data.company_name,
        mobile_number=form_data.mobile_number,
        pdf_link=form_data.pdf_link
    )
    
    if success:
        logger.info(f"PDF download form saved successfully for blog: {form_data.pdf_link}")
        return {
            "status": "success",
            "message": "Form submitted successfully"
        }
    else:
        logger.error(f"Failed to save PDF download form for blog: {form_data.pdf_link}")
        raise HTTPException(status_code=500, detail="Failed to save form data.")

@router.get("/pdf-downloads")
async def get_pdf_downloads(
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page")
):
    """
    Get paginated PDF download records.
    """
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        offset = (page - 1) * per_page
        
        count_query = "SELECT COUNT(*) FROM pdf_downloads"
        total_count = await conn.fetchval(count_query)
        
        query = """
            SELECT timestamp, first_name, last_name, email, company_name, mobile_number, pdf_link
            FROM pdf_downloads
            ORDER BY timestamp DESC
            LIMIT $1 OFFSET $2
        """
        downloads = await conn.fetch(query, per_page, offset)
        
        await conn.close()
        
        downloads_list = [dict(record) for record in downloads]
        
        total_pages = (total_count + per_page - 1) // per_page
        
        return {
            "status": "success",
            "pdf_downloads": downloads_list,
            "page": page,
            "per_page": per_page,
            "total_count": total_count,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
        
    except asyncpg.PostgresError as e:
        logger.error(f"Database error in get_pdf_downloads: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in get_pdf_downloads: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/pdf-downloads-kpi")
async def get_pdf_downloads_kpi():
    """
    Get Key Performance Indicators for PDF downloads.
    """
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        # Total downloads this month
        monthly_downloads_query = """
            SELECT COUNT(*) FROM pdf_downloads
            WHERE timestamp >= date_trunc('month', CURRENT_DATE)
        """
        total_downloads_this_month = await conn.fetchval(monthly_downloads_query)
        
        # Most downloaded PDF
        most_downloaded_query = """
            SELECT pdf_link, COUNT(*) as download_count
            FROM pdf_downloads
            GROUP BY pdf_link
            ORDER BY download_count DESC
            LIMIT 1
        """
        most_downloaded_record = await conn.fetchrow(most_downloaded_query)
        most_downloaded_pdf = most_downloaded_record['pdf_link'] if most_downloaded_record else "-"
        
        # Total downloads
        total_downloads_query = "SELECT COUNT(*) FROM pdf_downloads"
        total_downloads = await conn.fetchval(total_downloads_query)
        
        await conn.close()
        
        return {
            "total_downloads_this_month": total_downloads_this_month,
            "most_downloaded_pdf": most_downloaded_pdf,
            "total_downloads": total_downloads,
        }
        
    except asyncpg.PostgresError as e:
        logger.error(f"Database error in get_pdf_downloads_kpi: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in get_pdf_downloads_kpi: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

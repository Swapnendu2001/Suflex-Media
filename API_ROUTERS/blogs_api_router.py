from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import asyncpg
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api", tags=["Blogs Management"])

DATABASE_URL = os.getenv("POSTGRES_CONNECTION_URL")

def generate_slug(title: str) -> str:
    """
    Generate a URL-friendly slug from a title
    """
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')

class CreateBlogRequest(BaseModel):
    blog: Dict[str, Any]
    status: str = "draft"
    keyword: Optional[Dict[str, Any]] = None
    category: Optional[str] = None
    slug: Optional[str] = None
    redirect_url: Optional[str] = None

class UpdateBlogRequest(BaseModel):
    blog: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    keyword: Optional[Dict[str, Any]] = None
    category: Optional[str] = None
    slug: Optional[str] = None
    redirect_url: Optional[str] = None

@router.get("/blogs")
async def get_blogs(include_deleted: bool = Query(False, description="Include soft-deleted blogs")):
    """
    Get all blogs
    By default excludes soft-deleted entries
    Set include_deleted=true to show all blogs including deleted ones
    """
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        if include_deleted:
            query = """
                SELECT id, blog, status, date, keyword, category, slug, redirect_url, isDeleted, created_at, updated_at
                FROM blogs
                ORDER BY date DESC
            """
        else:
            query = """
                SELECT id, blog, status, date, keyword, category, slug, redirect_url, isDeleted, created_at, updated_at
                FROM blogs
                WHERE isDeleted = FALSE
                ORDER BY date DESC
            """
        
        blogs = await conn.fetch(query)
        await conn.close()
        
        blogs_list = [
            {
                "id": str(blog['id']),
                "blog": blog['blog'],
                "status": blog['status'],
                "date": blog['date'].isoformat() if blog['date'] else None,
                "keyword": blog['keyword'],
                "category": blog['category'],
                "slug": blog['slug'],
                "redirect_url": blog['redirect_url'],
                "isDeleted": blog['isDeleted'],
                "created_at": blog['created_at'].isoformat() if blog['created_at'] else None,
                "updated_at": blog['updated_at'].isoformat() if blog['updated_at'] else None
            }
            for blog in blogs
        ]
        
        return {"status": "success", "blogs": blogs_list, "count": len(blogs_list)}
        
    except asyncpg.PostgresError as e:
        print(f"✗ Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/blogs", status_code=201)
async def create_blog(blog_data: CreateBlogRequest):
    """
    Create a new blog
    Requires blog content as JSONB
    Optional fields: status, keyword, category, redirect_url
    """
    print(f"Creating new blog with status: {blog_data.status}")
    
    if not blog_data.blog:
        raise HTTPException(status_code=400, detail="Blog content is required")
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        new_blog = await conn.fetchrow(
            """
            INSERT INTO blogs (blog, status, keyword, category, slug, redirect_url, isDeleted)
            VALUES ($1, $2, $3, $4, $5, $6, FALSE)
            RETURNING id, blog, status, date, keyword, category, slug, redirect_url, isDeleted, created_at, updated_at
            """,
            blog_data.blog,
            blog_data.status,
            blog_data.keyword,
            blog_data.category,
            blog_data.slug,
            blog_data.redirect_url
        )
        
        await conn.close()
        
        print(f"✓ Blog created successfully with ID: {new_blog['id']}")
        return {
            "status": "success",
            "message": "Blog created successfully",
            "blog": {
                "id": str(new_blog['id']),
                "blog": new_blog['blog'],
                "status": new_blog['status'],
                "date": new_blog['date'].isoformat() if new_blog['date'] else None,
                "keyword": new_blog['keyword'],
                "category": new_blog['category'],
                "slug": new_blog['slug'],
                "redirect_url": new_blog['redirect_url'],
                "isDeleted": new_blog['isDeleted'],
                "created_at": new_blog['created_at'].isoformat() if new_blog['created_at'] else None,
                "updated_at": new_blog['updated_at'].isoformat() if new_blog['updated_at'] else None
            }
        }
        
    except asyncpg.PostgresError as e:
        print(f"✗ Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/blogs/{blog_id}")
async def update_blog(blog_id: str, blog_data: UpdateBlogRequest):
    """
    Update an existing blog
    Only updates provided fields (partial update)
    Cannot update soft-deleted blogs
    """
    print(f"Updating blog ID: {blog_id}")
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        existing_blog = await conn.fetchrow(
            "SELECT id, isDeleted FROM blogs WHERE id = $1",
            blog_id
        )
        
        if not existing_blog:
            await conn.close()
            raise HTTPException(status_code=404, detail="Blog not found")
        
        if existing_blog['isDeleted']:
            await conn.close()
            raise HTTPException(status_code=400, detail="Cannot update deleted blog")
        
        update_fields = []
        update_values = []
        param_count = 1
        
        if blog_data.blog is not None:
            update_fields.append(f"blog = ${param_count}")
            update_values.append(blog_data.blog)
            param_count += 1
        
        if blog_data.status is not None:
            update_fields.append(f"status = ${param_count}")
            update_values.append(blog_data.status)
            param_count += 1
        
        if blog_data.keyword is not None:
            update_fields.append(f"keyword = ${param_count}")
            update_values.append(blog_data.keyword)
            param_count += 1
        
        if blog_data.category is not None:
            update_fields.append(f"category = ${param_count}")
            update_values.append(blog_data.category)
            param_count += 1
        
        if blog_data.slug is not None:
            update_fields.append(f"slug = ${param_count}")
            update_values.append(blog_data.slug)
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
            RETURNING id, blog, status, date, keyword, category, slug, redirect_url, isDeleted, created_at, updated_at
        """
        
        updated_blog = await conn.fetchrow(query, *update_values)
        await conn.close()
        
        print(f"✓ Blog updated successfully: {blog_id}")
        return {
            "status": "success",
            "message": "Blog updated successfully",
            "blog": {
                "id": str(updated_blog['id']),
                "blog": updated_blog['blog'],
                "status": updated_blog['status'],
                "date": updated_blog['date'].isoformat() if updated_blog['date'] else None,
                "keyword": updated_blog['keyword'],
                "category": updated_blog['category'],
                "slug": updated_blog['slug'],
                "redirect_url": updated_blog['redirect_url'],
                "isDeleted": updated_blog['isDeleted'],
                "created_at": updated_blog['created_at'].isoformat() if updated_blog['created_at'] else None,
                "updated_at": updated_blog['updated_at'].isoformat() if updated_blog['updated_at'] else None
            }
        }
        
    except HTTPException:
        raise
    except asyncpg.PostgresError as e:
        print(f"✗ Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.patch("/blogs/{blog_id}")
async def partial_update_blog(blog_id: str, blog_data: UpdateBlogRequest):
    """
    Partial update of an existing blog (alias for PUT endpoint)
    Only updates provided fields
    Cannot update soft-deleted blogs
    """
    return await update_blog(blog_id, blog_data)

@router.delete("/blogs/{blog_id}")
async def delete_blog(blog_id: str):
    """
    Soft delete a blog
    Sets isDeleted to TRUE instead of removing from database
    Cannot delete already deleted blogs
    """
    print(f"Soft deleting blog ID: {blog_id}")
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        blog = await conn.fetchrow(
            "SELECT id, isDeleted FROM blogs WHERE id = $1",
            blog_id
        )
        
        if not blog:
            await conn.close()
            raise HTTPException(status_code=404, detail="Blog not found")
        
        if blog['isDeleted']:
            await conn.close()
            raise HTTPException(status_code=400, detail="Blog is already deleted")
        
        await conn.execute(
            """
            UPDATE blogs
            SET isDeleted = TRUE, updated_at = CURRENT_TIMESTAMP
            WHERE id = $1
            """,
            blog_id
        )
        
        await conn.close()
        
        print(f"✓ Blog soft deleted successfully: {blog_id}")
        return {
            "status": "success",
            "message": "Blog deleted successfully"
        }
        
    except HTTPException:
        raise
    except asyncpg.PostgresError as e:
        print(f"✗ Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/blogs/{blog_id}/restore")
async def restore_blog(blog_id: str):
    """
    Restore a soft-deleted blog
    Sets isDeleted back to FALSE
    """
    print(f"Restoring blog ID: {blog_id}")
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        blog = await conn.fetchrow(
            "SELECT id, isDeleted FROM blogs WHERE id = $1",
            blog_id
        )
        
        if not blog:
            await conn.close()
            raise HTTPException(status_code=404, detail="Blog not found")
        
        if not blog['isDeleted']:
            await conn.close()
            raise HTTPException(status_code=400, detail="Blog is not deleted")
        
        await conn.execute(
            """
            UPDATE blogs
            SET isDeleted = FALSE, updated_at = CURRENT_TIMESTAMP
            WHERE id = $1
            """,
            blog_id
        )
        
        await conn.close()
        
        print(f"✓ Blog restored successfully: {blog_id}")
        return {
            "status": "success",
            "message": "Blog restored successfully"
        }
        
    except HTTPException:
        raise
    except asyncpg.PostgresError as e:
        print(f"✗ Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/admin_save_blog")
async def admin_save_blog(request: Request):
    """
    Save blog from admin panel (Draft or Publish)
    Receives complete blog data from frontend and saves to database
    Preserves all original JSON key names
    Generates slug from title field
    """
    try:
        data = await request.json()
        
        print("=" * 80)
        print("RECEIVED BLOG DATA FROM FRONTEND:")
        print("=" * 80)
        print(json.dumps(data, indent=2))
        print("=" * 80)
        print(f"Data keys: {list(data.keys())}")
        print(f"Status field: {data.get('blogStatus', 'NOT FOUND')}")
        print("=" * 80)
        
        blog_title = data.get('blogTitle', '')
        if not blog_title:
            raise HTTPException(status_code=400, detail="Blog title is required")
        
        slug = generate_slug(blog_title)
        blog_status = data.get('blogStatus', 'draft')
        blog_category = data.get('blogCategory', None)
        
        conn = await asyncpg.connect(DATABASE_URL)
        
        try:
            existing_blog = await conn.fetchrow(
                "SELECT id FROM blogs WHERE slug = $1",
                slug
            )
            
            if existing_blog:
                original_slug = slug
                counter = 1
                while existing_blog:
                    slug = f"{original_slug}-{counter}"
                    existing_blog = await conn.fetchrow(
                        "SELECT id FROM blogs WHERE slug = $1",
                        slug
                    )
                    counter += 1
                print(f"✓ Generated unique slug: {slug}")
            
            new_blog = await conn.fetchrow(
                """
                INSERT INTO blogs (blog, status, category, slug, isDeleted)
                VALUES ($1, $2, $3, $4, FALSE)
                RETURNING id, blog, status, date, keyword, category, slug, redirect_url, isDeleted, created_at, updated_at
                """,
                json.dumps(data),
                blog_status,
                blog_category,
                slug
            )
            
            blog_id = str(new_blog['id'])
            blog_url = f"http://localhost:5000/blog/{slug}"
            
            print(f"✓ Blog saved successfully with ID: {blog_id}")
            print(f"✓ Blog slug: {slug}")
            print(f"✓ Blog status: {blog_status}")
            print(f"✓ Blog URL: {blog_url}")
            print("=" * 80)
            
            return {
                "status": "success",
                "message": f"Blog {'published' if blog_status == 'published' else 'saved as draft'} successfully",
                "blog_id": blog_id,
                "slug": slug,
                "url": blog_url
            }
            
        finally:
            await conn.close()
        
    except HTTPException:
        raise
    except asyncpg.UniqueViolationError:
        print(f"✗ Slug already exists")
        raise HTTPException(status_code=400, detail="A blog with this title already exists")
    except asyncpg.PostgresError as e:
        print(f"✗ Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        print(f"✗ Unexpected error in admin_save_blog: {e}")
        raise HTTPException(status_code=500, detail=str(e))


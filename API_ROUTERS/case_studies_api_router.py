from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import asyncpg
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api", tags=["Case Studies Management"])

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

class CreateCaseStudyRequest(BaseModel):
    case_study: Dict[str, Any]
    status: str = "draft"
    keyword: Optional[Dict[str, Any]] = None
    category: Optional[str] = None
    editors_choice: Optional[str] = 'N'
    slug: Optional[str] = None
    redirect_url: Optional[str] = None

class UpdateCaseStudyRequest(BaseModel):
    case_study: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    keyword: Optional[Dict[str, Any]] = None
    category: Optional[str] = None
    editors_choice: Optional[str] = None
    slug: Optional[str] = None
    redirect_url: Optional[str] = None

@router.get("/case_studies")
async def get_case_studies(include_deleted: bool = Query(False, description="Include soft-deleted case studies")):
    """
    Get all case studies
    """
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        if include_deleted:
            query = "SELECT * FROM case_studies ORDER BY date DESC"
        else:
            query = "SELECT * FROM case_studies WHERE isdeleted = FALSE ORDER BY date DESC"
        
        records = await conn.fetch(query)
        await conn.close()
        
        results = [dict(record) for record in records]
        
        return {"status": "success", "case_studies": results, "count": len(results)}
        
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/case_studies", status_code=201)
async def create_case_study(data: CreateCaseStudyRequest):
    """
    Create a new case study
    """
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        content_type = data.case_study.get('contentType', 'CASE STUDY')
        
        new_record = await conn.fetchrow(
            """
            INSERT INTO case_studies (blog, status, keyword, category, editors_choice, slug, type, redirect_url, isdeleted)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, FALSE)
            RETURNING *
            """,
            data.case_study,
            data.status,
            data.keyword,
            data.category,
            data.editors_choice,
            data.slug,
            content_type,
            data.redirect_url
        )
        
        await conn.close()
        
        return {
            "status": "success",
            "message": "Case study created successfully",
            "case_study": dict(new_record)
        }
        
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/case_studies/{case_study_id}")
async def update_case_study(case_study_id: str, data: UpdateCaseStudyRequest):
    """
    Update an existing case study
    """
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        existing_record = await conn.fetchrow(
            "SELECT id, isdeleted FROM case_studies WHERE id = $1",
            case_study_id
        )
        
        if not existing_record:
            await conn.close()
            raise HTTPException(status_code=404, detail="Case study not found")
        
        if existing_record['isdeleted']:
            await conn.close()
            raise HTTPException(status_code=400, detail="Cannot update deleted case study")
        
        update_fields = []
        update_values = []
        param_count = 1
        
        if data.case_study is not None:
            update_fields.append(f"blog = ${param_count}")
            update_values.append(data.case_study)
            param_count += 1
        
        if data.status is not None:
            update_fields.append(f"status = ${param_count}")
            update_values.append(data.status)
            param_count += 1
        
        if data.keyword is not None:
            update_fields.append(f"keyword = ${param_count}")
            update_values.append(data.keyword)
            param_count += 1
        
        if data.category is not None:
            update_fields.append(f"category = ${param_count}")
            update_values.append(data.category)
            param_count += 1
        
        if data.slug is not None:
            update_fields.append(f"slug = ${param_count}")
            update_values.append(data.slug)
            param_count += 1
        
        if data.editors_choice is not None:
            update_fields.append(f"editors_choice = ${param_count}")
            update_values.append(data.editors_choice)
            param_count += 1
        
        if data.redirect_url is not None:
            update_fields.append(f"redirect_url = ${param_count}")
            update_values.append(data.redirect_url)
            param_count += 1
        
        if not update_fields:
            await conn.close()
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_fields.append(f"updated_at = CURRENT_TIMESTAMP")
        update_values.append(case_study_id)
        
        query = f"""
            UPDATE case_studies
            SET {', '.join(update_fields)}
            WHERE id = ${param_count}
            RETURNING *
        """
        
        updated_record = await conn.fetchrow(query, *update_values)
        await conn.close()
        
        return {
            "status": "success",
            "message": "Case study updated successfully",
            "case_study": dict(updated_record)
        }
        
    except HTTPException:
        raise
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/case_studies/{case_study_id}")
async def delete_case_study(case_study_id: str):
    """
    Soft delete a case study
    """
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        record = await conn.fetchrow(
            "SELECT id, isdeleted FROM case_studies WHERE id = $1",
            case_study_id
        )
        
        if not record:
            await conn.close()
            raise HTTPException(status_code=404, detail="Case study not found")
        
        if record['isdeleted']:
            await conn.close()
            raise HTTPException(status_code=400, detail="Case study is already deleted")
        
        await conn.execute(
            """
            UPDATE case_studies
            SET isdeleted = TRUE, updated_at = CURRENT_TIMESTAMP
            WHERE id = $1
            """,
            case_study_id
        )
        
        await conn.close()
        
        return {
            "status": "success",
            "message": "Case study deleted successfully"
        }
        
    except HTTPException:
        raise
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/admin_save_case_study")
async def admin_save_case_study(request: Request):
    """
    Save case study from admin panel (Draft or Publish)
    """
    try:
        data = await request.json()
        
        title = data.get('blogTitle', '')
        if not title:
            raise HTTPException(status_code=400, detail="Case study title is required")
        
        case_study_id = data.get('blog_id')
        reason = data.get('reason', 'create')
        
        slug = generate_slug(title)
        status = data.get('blogStatus', 'draft')
        category = data.get('blogCategory', None)
        content_type = 'CASE STUDY'
        
        data['contentType'] = content_type
        
        conn = await asyncpg.connect(DATABASE_URL)
        
        try:
            if reason == 'update' and case_study_id:
                existing_record = await conn.fetchrow(
                    "SELECT id, slug FROM case_studies WHERE id = $1 AND isdeleted = FALSE",
                    case_study_id
                )
                
                if not existing_record:
                    raise HTTPException(status_code=404, detail="Case study not found for update")
                
                if slug != existing_record['slug']:
                    existing_slug_record = await conn.fetchrow(
                        "SELECT id FROM case_studies WHERE slug = $1 AND id != $2 AND isdeleted = FALSE",
                        slug,
                        case_study_id
                    )
                    
                    if existing_slug_record:
                        original_slug = slug
                        counter = 1
                        while existing_slug_record:
                            slug = f"{original_slug}-{counter}"
                            existing_slug_record = await conn.fetchrow(
                                "SELECT id FROM case_studies WHERE slug = $1 AND id != $2 AND isdeleted = FALSE",
                                slug,
                                case_study_id
                            )
                            counter += 1
                
                updated_record = await conn.fetchrow(
                    """
                    UPDATE case_studies
                    SET blog = $1, status = $2, category = $3, editors_choice = $4, slug = $5, type = $6, updated_at = CURRENT_TIMESTAMP
                    WHERE id = $7
                    RETURNING *
                    """,
                    json.dumps(data),
                    status,
                    category,
                    data.get('editors_choice', 'N'),
                    slug,
                    content_type,
                    case_study_id
                )
                
                if not updated_record:
                    raise HTTPException(status_code=404, detail="Case study not found for update")
                
                record_id = str(updated_record['id'])
                record_url = f"/case_study/{slug}"
                
                return {
                    "status": "success",
                    "message": f"Case study {'published' if status == 'published' else 'updated'} successfully",
                    "case_study_id": record_id,
                    "slug": slug,
                    "url": record_url
                }
            else:
                existing_record = await conn.fetchrow(
                    "SELECT id FROM case_studies WHERE slug = $1 AND isdeleted = FALSE",
                    slug
                )
                
                if existing_record:
                    original_slug = slug
                    counter = 1
                    while existing_record:
                        slug = f"{original_slug}-{counter}"
                        existing_record = await conn.fetchrow(
                            "SELECT id FROM case_studies WHERE slug = $1 AND isdeleted = FALSE",
                            slug
                        )
                        counter += 1
                
                new_record = await conn.fetchrow(
                    """
                    INSERT INTO case_studies (blog, status, category, editors_choice, slug, type, isdeleted)
                    VALUES ($1, $2, $3, $4, $5, $6, FALSE)
                    RETURNING *
                    """,
                    json.dumps(data),
                    status,
                    category,
                    data.get('editors_choice', 'N'),
                    slug,
                    content_type
                )
                
                record_id = str(new_record['id'])
                record_url = f"/case_study/{slug}"
                
                return {
                    "status": "success",
                    "message": f"Case study {'published' if status == 'published' else 'saved as draft'} successfully",
                    "case_study_id": record_id,
                    "slug": slug,
                    "url": record_url
                }
            
        finally:
            await conn.close()
        
    except HTTPException:
        raise
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=400, detail="A case study with this title already exists")
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
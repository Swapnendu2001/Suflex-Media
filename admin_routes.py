from fastapi import APIRouter, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from typing import Optional, List
import os
from pathlib import Path

# Import database handlers
from data.db_handler_async import (
    admin_login_db_check,
    get_blogs_list_db,
    save_blogs_to_db,
    update_blogs_to_db,
    delete_blog_from_db,
    get_blog,
    upload_file_to_storage,
    get_file_details_db,
    delete_file_from_storage,
    delete_file_from_storage_by_url,
    get_main_pages_db,
    update_main_page_db,
    delete_main_page_db,
    sha256_hash,
    create_admin_user,
    get_all_admin_users,
    delete_admin_user,
    update_admin_user,
    create_default_admin,
)

router = APIRouter()

# Get the templates directory
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates" / "admin"


# --------------------------------------------------------------------------------#
#                              ADMIN PAGE ROUTES                                 #
# --------------------------------------------------------------------------------#

@router.get("/admin_login", response_class=HTMLResponse)
async def admin_login():
    """Serve admin login page"""
    admin_html_path = TEMPLATES_DIR / "admin.html"
    with open(admin_html_path, "r", encoding="utf-8") as f:
        return f.read()


@router.post("/admin_auth")
async def admin_auth(request: Request):
    """Handle admin authentication"""
    data = await request.json()
    email = (
        sha256_hash(data.get("email"))
        if "@" in data.get("email", "a")
        else data.get("enc_email")
    )
    password = (
        sha256_hash(data.get("password"))
        if "@" in data.get("email", "a")
        else data.get("enc_pwd")
    )
    return admin_login_db_check(email, password)


# ------------------------------ ADMIN PAGE BLOG ------------------------------#

@router.get("/admin_blogs", response_class=HTMLResponse)
async def admin_blogs():
    """Serve admin blogs page"""
    blogs_html_path = TEMPLATES_DIR / "blogs" / "admin_blogs.html"
    with open(blogs_html_path, "r", encoding="utf-8") as f:
        return f.read()


@router.get("/get_blog_list")
async def get_blog_list(search_keyword: Optional[str] = None):
    """Get list of blogs"""
    list_of_blogs, _ = get_blogs_list_db(
        search_keyword=search_keyword, page=1, per_page=1000
    )
    return JSONResponse({"status": "success", "blogs": list_of_blogs})


@router.post("/admin_blog_preview")
async def admin_blog_preview(request: Request):
    """Preview blog before publishing"""
    from data.page_handler import get_blog_preview
    
    data = await request.json()
    blog_data = get_blog_preview(blog_data=data)
    
    if blog_data.get('status') == "not_found":
        return JSONResponse({"status": "error", "message": "Blog not found"}, status_code=404)
    
    if blog_data.get('status') == "error":
        return JSONResponse({"status": "error", "message": "Error generating preview"}, status_code=500)
    
    if blog_data.get('status') == "redirect":
        redirect_url = blog_data.get("redirect_url")
        if redirect_url:
            return JSONResponse({"status": "redirect", "url": redirect_url})
        else:
            return JSONResponse({"status": "error", "message": "Redirect URL not found"}, status_code=500)
    
    if blog_data.get("status") == "deleted":
        redirect_url = blog_data.get("redirect_url")
        if redirect_url:
            return JSONResponse({"status": "redirect", "url": redirect_url})
        else:
            return JSONResponse({"status": "error", "message": "Blog deleted"}, status_code=404)

    return JSONResponse({
        "status": "success",
        "data": blog_data['html']
    })


@router.post("/admin_save_blog")
async def admin_save_blog(request: Request):
    """Save or update a blog"""
    data = await request.json()
    minimum_required_keys = [
        "mainImageUrl",
        "mainImageAlt",
        "blogTitle",
        "blogAuthor",
        "blogDate",
        "blogSummary",
        "dynamicSections",
        "blogCategory",
    ]
    
    for key in minimum_required_keys:
        if not data.get(key):
            return JSONResponse(
                {"status": "error", "message": f"Missing required field: {key}"},
                status_code=400
            )
    
    # Check if labels are provided or if they are marked as not mandatory
    labels_data = data.get("labels", {})
    labels_not_mandatory = data.get("labelsNotMandatory", False)
    
    if not labels_not_mandatory and (not labels_data or not isinstance(labels_data, dict) or len(labels_data) == 0):
        return JSONResponse(
            {"status": "error", "message": "Labels are required unless marked as not mandatory"},
            status_code=400
        )

    verification_status = admin_login_db_check(
        email=data.get("enc_email", ""), password=data.get("enc_pwd", "")
    )
    if not verification_status["success"]:
        return JSONResponse(
            {"status": "error", "message": "Unauthorized"},
            status_code=401
        )

    data["admin_name"] = verification_status["name"]
    
    if data.get("reason", "insert") == "insert":
        result = save_blogs_to_db(data)
    else:
        result = update_blogs_to_db(data)
    
    if result.get("status") == "error":
        return JSONResponse(result, status_code=500)

    return JSONResponse({
        "status": "success",
        "message": "Blog saved successfully",
        "url": result.get("url", ""),
    })


@router.get("/blog/{blog_id}", response_class=HTMLResponse)
async def display_blog(blog_id: str):
    """Display a blog"""
    from data.page_handler import get_blog_page
    
    blog_data = get_blog_page(blog_id)
    
    if blog_data.get('status') == "not_found":
        return HTMLResponse(content="<h1>Blog not found</h1>", status_code=404)
    
    if blog_data.get('status') == "error":
        return HTMLResponse(content="<h1>Error loading blog</h1>", status_code=500)
    
    if blog_data.get('status') == "redirect":
        from fastapi.responses import RedirectResponse
        redirect_url = blog_data.get("redirect_url")
        if redirect_url:
            return RedirectResponse(url=redirect_url)
        else:
            return HTMLResponse(content="<h1>Blog not found</h1>", status_code=404)
    
    if blog_data.get("status") == "deleted":
        redirect_url = blog_data.get("redirect_url")
        if redirect_url:
            from fastapi.responses import RedirectResponse
            return RedirectResponse(url=redirect_url)
        else:
            return HTMLResponse(content="<h1>Blog has been deleted</h1>", status_code=404)

    return blog_data['html']


@router.post("/delete_blog")
async def delete_blog(request: Request):
    """Delete a blog"""
    data = await request.json()
    blog_id = data.get("blog_id")
    redirect_url = data.get("redirect_url")
    
    if not blog_id:
        return JSONResponse({"status": "error", "message": "Blog ID required"}, status_code=400)
    
    result = delete_blog_from_db(blog_id, redirect_url)
    
    if result.get("status") == "success":
        return JSONResponse({
            "status": "success",
            "message": "Blog deleted successfully"
        })
    else:
        return JSONResponse(result, status_code=500)


# --------------------------------------------------------------------------------#
#                           MAIN PAGES ROUTES                                    #
# --------------------------------------------------------------------------------#

@router.get("/page_updater", response_class=HTMLResponse)
async def page_updater():
    """Serve page updater admin interface"""
    page_updater_html_path = TEMPLATES_DIR / "page_updater.html"
    with open(page_updater_html_path, "r", encoding="utf-8") as f:
        return f.read()


@router.get("/get_main_pages")
async def get_main_pages(search_keyword: Optional[str] = None):
    """Get list of main pages"""
    list_of_pages, _ = get_main_pages_db(
        search_keyword=search_keyword, page=1, per_page=1000
    )
    return JSONResponse({"status": "success", "pages": list_of_pages})


@router.post("/update_main_page")
async def update_main_page(request: Request):
    """Update a main page"""
    data = await request.json()
    page_id = data.get("page_id")
    page_name = data.get("page_name")
    page_data = data.get("page_data")

    if not all([page_id, page_name, page_data]):
        return JSONResponse(
            {"status": "error", "message": "Missing required fields"},
            status_code=400
        )

    verification_status = admin_login_db_check(
        email=data.get("enc_email", ""), password=data.get("enc_pwd", "")
    )
    if not verification_status["success"]:
        return JSONResponse(
            {"status": "error", "message": "Unauthorized"},
            status_code=401
        )

    result = update_main_page_db(page_id, page_data)
    if result["status"] == "success":
        return JSONResponse(result)
    else:
        return JSONResponse(result, status_code=500)


@router.post("/delete_main_page")
async def delete_main_page(request: Request):
    """Delete a main page"""
    data = await request.json()
    page_id = data.get("page_id")

    if not page_id:
        return JSONResponse(
            {"status": "error", "message": "Page ID required"},
            status_code=400
        )

    verification_status = admin_login_db_check(
        email=data.get("enc_email", ""), password=data.get("enc_pwd", "")
    )
    if not verification_status["success"]:
        return JSONResponse(
            {"status": "error", "message": "Unauthorized"},
            status_code=401
        )

    result = delete_main_page_db(page_id)
    if result["status"] == "success":
        return JSONResponse(result)
    else:
        return JSONResponse(result, status_code=500)


@router.post("/preview_main_page")
async def preview_main_page(request: Request):
    """Preview main page"""
    from data.page_handler import get_homepage
    
    data = await request.json()
    page_data = data.get("page_data")
    page_id = data.get("page_id")

    if not page_data:
        return JSONResponse(
            {"status": "error", "message": "Page data required"},
            status_code=400
        )
    
    if data.get("page_name") == "homepage":
        html = get_homepage(page_data=page_data)
        return JSONResponse({"status": "success", "html": html})
    else:
        return JSONResponse(
            {"status": "error", "message": "Page type not supported for preview"},
            status_code=400
        )


# --------------------------------------------------------------------------------#
#                             UPLOAD FILES ROUTE                                 #
# --------------------------------------------------------------------------------#

@router.get("/manage_files", response_class=HTMLResponse)
async def manage_files():
    """Serve file management page"""
    manage_files_html_path = TEMPLATES_DIR / "manage_files.html"
    with open(manage_files_html_path, "r", encoding="utf-8") as f:
        return f.read()


@router.get("/get_file_details")
async def get_file_details(bucket_name: str, user_id: Optional[str] = None):
    """Get file details from storage bucket"""
    if not bucket_name:
        return JSONResponse(
            {"status": "error", "message": "Bucket name required"},
            status_code=400
        )
    
    file_details = get_file_details_db(bucket_name, user_id)
    
    if file_details["status"] == "error":
        return JSONResponse(file_details, status_code=500)
    
    return JSONResponse(file_details)


@router.post("/upload_file")
async def upload_file(
    file: UploadFile = File(...),
    bucket_name: str = Form(...)
):
    """Upload file to storage"""
    try:
        result = upload_file_to_storage(file, bucket_name)
        
        if result["status"] == "success":
            return JSONResponse({
                "status": "success",
                "url": result["url"],
                "message": "File uploaded successfully"
            })
        else:
            return JSONResponse(result, status_code=500)
    except Exception as e:
        return JSONResponse(
            {"status": "error", "message": str(e)},
            status_code=500
        )


@router.post("/delete_file")
async def delete_file(request: Request):
    """Delete file from storage"""
    data = await request.json()
    
    if "file_name" not in data:
        return JSONResponse(
            {"status": "error", "message": "File name required"},
            status_code=400
        )

    file_name = data["file_name"]
    result = delete_file_from_storage(file_name)

    if result["status"] == "success":
        return JSONResponse(result)
    else:
        return JSONResponse(result, status_code=500)






# --------------------------------------------------------------------------------#
#                           ADMIN USER MANAGEMENT ROUTES                           #
# --------------------------------------------------------------------------------#

@router.post("/api/admin_users")
async def create_admin(request: Request):
    """Create a new admin user"""
    try:
        data = await request.json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        
        if not all([username, email, password]):
            return JSONResponse(
                {"status": "error", "message": "Username, email, and password are required"},
                status_code=400
            )
        
        result = create_admin_user(username, email, password)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(
            {"status": "error", "message": str(e)},
            status_code=500
        )


@router.get("/api/admin_users")
async def get_admin_users():
    """Get all admin users"""
    try:
        result = get_all_admin_users()
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(
            {"status": "error", "message": str(e)},
            status_code=500
        )


@router.delete("/api/admin_users/{email}")
async def delete_admin(email: str):
    """Delete an admin user by email"""
    try:
        result = delete_admin_user(email)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(
            {"status": "error", "message": str(e)},
            status_code=500
        )


@router.put("/api/admin_users/{email}")
async def update_admin(email: str, request: Request):
    """Update an admin user's information"""
    try:
        data = await request.json()
        new_username = data.get("username")
        new_password = data.get("password")
        
        result = update_admin_user(email, new_username=new_username, new_password=new_password)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(
            {"status": "error", "message": str(e)},
            status_code=500
        )


@router.post("/api/create_default_admin")
async def create_default_admin_endpoint():
    """Create a default admin user if none exists"""
    try:
        result = create_default_admin()
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(
            {"status": "error", "message": str(e)},
            status_code=500
        )

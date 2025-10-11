# Admin Panel Integration Guide

This document outlines the integration of the admin panel from Brands_out_loud into the Suflex-Media workspace.

## What Has Been Integrated

### 1. Database Handlers (`data/db_handler/`)
All database handler modules have been ported from Brands_out_loud:

- **`auth.py`** - Admin and user authentication
- **`blogs.py`** - Blog management (CRUD operations)
- **`files.py`** - File upload/download to Supabase storage
- **`magazine.py`** - Magazine management
- **`ad_manager.py`** - Advertisement and organization management
- **`general_function.py`** - Utility functions (hashing, page data, etc.)
- **`__init__.py`** - Exports all database functions

### 2. Admin Templates (`templates/admin/`)
All admin HTML templates have been copied:

- `admin.html` - Main admin login page
- `admin_blogs.html` - Blog management interface
- `page_updater.html` - Page update interface
- `manage_files.html` - File management interface
- `ad_manager.html` - Ad and organization management interface

### 3. Admin Routes (`admin_routes.py`)
FastAPI router with all admin endpoints converted from Flask:

#### Authentication Routes
- `GET /admin_login` - Admin login page
- `POST /admin_auth` - Admin authentication endpoint

#### Blog Management Routes
- `GET /admin_blogs` - Blog management interface
- `GET /get_blog_list` - Get list of all blogs
- `POST /admin_blog_preview` - Preview blog before publishing
- `POST /admin_save_blog` - Save or update blog
- `GET /blog/{blog_id}` - Display a blog post
- `POST /delete_blog` - Delete a blog

#### Main Pages Routes
- `GET /page_updater` - Page updater interface
- `GET /get_main_pages` - Get list of main pages
- `POST /update_main_page` - Update a main page
- `POST /delete_main_page` - Delete a main page
- `POST /preview_main_page` - Preview main page

#### File Management Routes
- `GET /manage_files` - File management interface
- `GET /get_file_details` - Get file details from bucket
- `POST /upload_file` - Upload file to storage
- `POST /delete_file` - Delete file from storage

#### Magazine Management Routes
- `POST /create_magazine` - Create new magazine
- `POST /delete_magazine` - Delete magazine

#### Ad Manager Routes
- `GET /ad_manager` - Ad manager interface
- `GET /api/organizations` - Get all organizations
- `POST /api/organizations` - Add new organization
- `PUT /api/organizations/{org_id}` - Update organization
- `DELETE /api/organizations/{org_id}` - Delete organization
- `GET /api/ads` - Get all ads
- `POST /api/ads_post` - Add new ad
- `PUT /api/ads/{ad_id}` - Update ad
- `DELETE /api/ads/{ad_id}` - Delete ad

### 4. Dependencies Updated
Added to `requirements.txt`:
- `supabase == 2.15.1` - Supabase Python client
- `python-dotenv == 1.1.0` - Environment variable management
- `python-multipart == 0.0.9` - File upload handling for FastAPI

## Setup Instructions

### 1. Install Dependencies

```powershell
# Navigate to Suflex-Media directory
cd c:\Code\Freelance\Suflex-Media

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the root of Suflex-Media:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

You can find these values in your Supabase project settings.

### 3. Database Setup

Ensure your Supabase database has the following tables:

#### Required Tables:
1. **`admin users`** - Admin authentication
   - `id` (uuid, primary key)
   - `username` (text)
   - `email` (text, unique)
   - `password` (text, hashed)
   - `created_at` (timestamp)

2. **`blogs`** - Blog posts
   - `id` (text, primary key)
   - `created_by` (text)
   - `status` (text) - 'draft', 'published', 'deleted'
   - `category` (text)
   - `labels` (jsonb)
   - `meta_tags` (text)
   - `json_data` (jsonb)
   - `history` (jsonb)
   - `redirect_url` (text, nullable)
   - `created_at` (timestamp)
   - `updated_at` (timestamp)

3. **`organization`** - Organizations for ads
   - `id` (int, primary key, auto-increment)
   - `organization` (text, unique)
   - `logo` (text, url)
   - `percentage` (float)
   - `created_at` (timestamp)

4. **`ads`** - Advertisements
   - `id` (int, primary key, auto-increment)
   - `organization` (text, foreign key to organization.organization)
   - `aspect_ratio` (text)
   - `image` (text, url)
   - `created_at` (timestamp)

5. **`magazine_details`** - Magazine publications
   - `id` (uuid, primary key)
   - `title` (text)
   - `pdf_url` (text)
   - `thumbnail_url` (text, nullable)
   - `created_by` (text)
   - `created_at` (timestamp)

6. **`main_pages`** - Main website pages
   - `page_id` (uuid, primary key)
   - `page_name` (text, unique)
   - `page_data` (jsonb)
   - `created_at` (timestamp)
   - `updated_at` (timestamp)

7. **`users`** - User accounts (if implementing user features)
   - `id` (uuid, primary key)
   - `username` (text)
   - `email` (text, unique)
   - `password` (text, hashed)
   - `created_at` (timestamp)

#### Required Storage Buckets:
1. **`blog-images`** - Blog post images
2. **`ad-images`** - Advertisement images
3. **`organization-logos`** - Organization logos
4. **`magazine-pdfs`** - Magazine PDF files
5. **`magazine-thumbnails`** - Magazine thumbnail images

### 4. Run the Application

```powershell
# Run with uvicorn
python app.py

# Or use uvicorn directly
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The admin panel will be available at:
- Admin Login: `http://localhost:8000/admin_login`
- Admin Blogs: `http://localhost:8000/admin_blogs`
- Page Updater: `http://localhost:8000/page_updater`
- File Manager: `http://localhost:8000/manage_files`
- Ad Manager: `http://localhost:8000/ad_manager`

## Implementation Notes

### Key Differences from Brands_out_loud

1. **Framework**: Converted from Flask to FastAPI
   - `@app.route()` → `@router.get()` / `@router.post()`
   - `request.json` → `await request.json()`
   - `request.form` → Form parameters
   - `request.files` → UploadFile parameters
   - `jsonify()` → `JSONResponse()`
   - `render_template()` → Direct HTML file reading or HTMLResponse

2. **Static Files**: HTML templates are read directly in Suflex-Media instead of using a template engine

3. **File Uploads**: Uses FastAPI's `UploadFile` instead of Flask's `request.files`

### TODO: Complete Implementation

The following stubs need to be implemented in `data/page_handler.py`:

1. **`get_blog_preview(blog_data)`**
   - Should render blog preview HTML from provided data
   - You may want to copy the blog rendering logic from Brands_out_loud

2. **`get_blog_page(blog_id)`**
   - Should fetch blog from database and render full HTML page
   - Include header, footer, and blog content

3. **`get_homepage(page_data=None)`**
   - Should render homepage
   - If page_data is provided, use it for preview mode
   - Otherwise fetch from database

### Security Considerations

1. **Authentication**: The admin routes use SHA-256 hashed passwords. Consider using bcrypt or argon2 for production.

2. **CORS**: If your frontend is on a different domain, add CORS middleware:
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # Update with specific origins
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. **File Upload Validation**: Add file type and size validation for uploads

4. **Rate Limiting**: Consider adding rate limiting for admin endpoints

## Testing

To test the integration:

1. Create an admin user in Supabase `admin users` table (hash the password using SHA-256)
2. Access `http://localhost:8000/admin_login`
3. Log in with your admin credentials
4. Test each admin feature:
   - Create/edit/delete blogs
   - Upload/delete files
   - Manage organizations and ads
   - Create/delete magazines

## Troubleshooting

### Import Errors
If you see import errors for `supabase` or `dotenv`:
```powershell
pip install supabase python-dotenv
```

### Database Connection Errors
- Verify your `.env` file has correct `SUPABASE_URL` and `SUPABASE_KEY`
- Check that your Supabase project is active
- Ensure you're using the correct API key (anon key for client-side, service key for admin)

### Template Not Found Errors
- Ensure all admin templates were copied to `templates/admin/`
- Check file paths in `admin_routes.py` match your template structure

## Next Steps

1. Implement the page rendering functions in `data/page_handler.py`
2. Test all admin functionalities thoroughly
3. Set up proper authentication middleware for admin routes
4. Add error handling and logging
5. Configure production environment variables
6. Set up database migrations if needed

## Support

For questions or issues, refer to:
- FastAPI Documentation: https://fastapi.tiangolo.com/
- Supabase Python Client: https://supabase.com/docs/reference/python/
- Original Brands_out_loud implementation for reference

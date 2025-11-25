from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from minio import Minio
from minio.error import S3Error
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import uuid

load_dotenv()

router = APIRouter(prefix="/api", tags=["Images"])

MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_PUBLIC_ENDPOINT = os.getenv("MINIO_PUBLIC_ENDPOINT")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")

parsed_url = urlparse(MINIO_PUBLIC_ENDPOINT)
endpoint = parsed_url.netloc
secure = parsed_url.scheme == 'https'

minio_client = Minio(
    endpoint=endpoint,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=secure
)

try:
    minio_client.list_buckets()
    found = any(bucket.name == MINIO_BUCKET_NAME for bucket in minio_client.list_buckets())
    if not found:
        minio_client.make_bucket(MINIO_BUCKET_NAME)
except Exception as e:
    print(f"Warning: Could not check/create bucket: {e}")

class ImageUploadResponse(BaseModel):
    status: str
    message: str
    object_name: str
    file_name: str
    file_size: int
    public_url: str

class ImageDeleteResponse(BaseModel):
    status: str
    message: str
    object_name: str
class ImageListResponse(BaseModel):
    status: str
    message: str
    images: list

class FileUploadResponse(BaseModel):
    status: str
    message: str
    object_name: str
    file_name: str
    file_size: int
    public_url: str

@router.get("/list-images")
async def list_images():
    """
    API endpoint to list only image files from MinIO bucket (excludes PDFs)
    Returns list of image objects with their names and public URLs
    """
    print("Image list request received")
    
    try:
        objects = minio_client.list_objects(MINIO_BUCKET_NAME)
        
        images = []
        for obj in objects:
            if not obj.object_name.lower().endswith('.pdf'):
                public_url = f"{MINIO_PUBLIC_ENDPOINT}/{MINIO_BUCKET_NAME}/{obj.object_name}"
                images.append({
                    "object_name": obj.object_name,
                    "public_url": public_url,
                    "size": obj.size,
                    "last_modified": obj.last_modified.isoformat() if obj.last_modified else None
                })
        
        print(f"Found {len(images)} images in bucket (excluding PDFs)")
        
        return ImageListResponse(
            status="success",
            message=f"Found {len(images)} images",
            images=images
        )
            
    except S3Error as e:
        print(f"MinIO error: {e}")
        raise HTTPException(status_code=500, detail=f"MinIO error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/list-pdfs")
async def list_pdfs():
    """
    API endpoint to list all files from MinIO bucket (both images and PDFs)
    Returns list of file objects with their names and public URLs
    Frontend filters them by type
    """
    print("File list request received")
    
    try:
        objects = minio_client.list_objects(MINIO_BUCKET_NAME)
        
        files = []
        for obj in objects:
            public_url = f"{MINIO_PUBLIC_ENDPOINT}/{MINIO_BUCKET_NAME}/{obj.object_name}"
            files.append({
                "object_name": obj.object_name,
                "public_url": public_url,
                "size": obj.size,
                "last_modified": obj.last_modified.isoformat() if obj.last_modified else None
            })
        
        print(f"Found {len(files)} files in bucket")
        
        return ImageListResponse(
            status="success",
            message=f"Found {len(files)} files",
            images=files
        )
            
    except S3Error as e:
        print(f"MinIO error: {e}")
        raise HTTPException(status_code=500, detail=f"MinIO error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """
    API endpoint to upload images to MinIO bucket
    Accepts multipart/form-data with image file
    Stores file in MinIO with unique name
    Returns object name and public URL for direct access
    """
    print(f"Image upload request - Filename: {file.filename}")
    
    try:
        image_data = await file.read()
        image_size = len(image_data)
        
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
        object_name = f"{uuid.uuid4()}.{file_extension}" if file_extension else str(uuid.uuid4())
        
        print(f"Processing upload - Name: {file.filename}, Size: {image_size} bytes")
        
        from io import BytesIO
        minio_client.put_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=object_name,
            data=BytesIO(image_data),
            length=image_size,
            content_type=file.content_type or 'application/octet-stream'
        )
        
        public_url = f"{MINIO_PUBLIC_ENDPOINT}/{MINIO_BUCKET_NAME}/{object_name}"
        
        print(f"Image uploaded successfully - Object: {object_name}")
        
        return ImageUploadResponse(
            status="success",
            message="Image uploaded successfully",
            object_name=object_name,
            file_name=file.filename,
            file_size=image_size,
            public_url=public_url
        )
            
    except S3Error as e:
        print(f"MinIO error: {e}")
        raise HTTPException(status_code=500, detail=f"MinIO error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    """
    API endpoint to upload files (including PDFs) to MinIO bucket
    Accepts multipart/form-data with file
    Preserves original filename, checks for duplicates
    Returns object name and public URL for direct access
    No size limit enforced
    """
    print(f"File upload request - Filename: {file.filename}")
    
    try:
        file_data = await file.read()
        file_size = len(file_data)
        
        original_filename = file.filename
        object_name = original_filename
        is_duplicate = False
        
        try:
            minio_client.stat_object(MINIO_BUCKET_NAME, object_name)
            is_duplicate = True
            
            base_name = original_filename.rsplit('.', 1)[0] if '.' in original_filename else original_filename
            extension = original_filename.rsplit('.', 1)[1] if '.' in original_filename else ''
            
            counter = 1
            while True:
                object_name = f"{base_name}_{counter}.{extension}" if extension else f"{base_name}_{counter}"
                try:
                    minio_client.stat_object(MINIO_BUCKET_NAME, object_name)
                    counter += 1
                except S3Error as e:
                    if e.code == 'NoSuchKey':
                        break
                    raise
            
            print(f"Duplicate found, using name: {object_name}")
        except S3Error as e:
            if e.code != 'NoSuchKey':
                raise
        
        print(f"Processing upload - Name: {object_name}, Size: {file_size} bytes")
        
        from io import BytesIO
        minio_client.put_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=object_name,
            data=BytesIO(file_data),
            length=file_size,
            content_type=file.content_type or 'application/octet-stream'
        )
        
        public_url = f"{MINIO_PUBLIC_ENDPOINT}/{MINIO_BUCKET_NAME}/{object_name}"
        
        message = "File uploaded successfully"
        if is_duplicate:
            message = f"File uploaded as '{object_name}' (original name already exists)"
        
        print(f"File uploaded successfully - Object: {object_name}")
        
        return FileUploadResponse(
            status="success",
            message=message,
            object_name=object_name,
            file_name=original_filename,
            file_size=file_size,
            public_url=public_url
        )
            
    except S3Error as e:
        print(f"MinIO error: {e}")
        raise HTTPException(status_code=500, detail=f"MinIO error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/delete-image/{object_name}")
async def delete_image(object_name: str):
    """
    API endpoint to delete images from MinIO bucket
    Accepts object name as path parameter
    Removes the file from MinIO storage
    Returns success confirmation or error
    """
    print(f"Image delete request - Object: {object_name}")
    
    try:
        minio_client.remove_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=object_name
        )
        
        print(f"Image deleted successfully - Object: {object_name}")
        
        return ImageDeleteResponse(
            status="success",
            message="Image deleted successfully",
            object_name=object_name
        )
            
    except S3Error as e:
        print(f"MinIO error: {e}")
        if e.code == 'NoSuchKey':
            raise HTTPException(status_code=404, detail="Image not found")
        raise HTTPException(status_code=500, detail=f"MinIO error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
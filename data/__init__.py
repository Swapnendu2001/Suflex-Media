# Data module for Suflex-Media
# This module provides access to database handlers and page rendering functions

from .db_handler import *
from .page_handler import get_blog_preview, get_blog_page, get_homepage

__all__ = [
    # Auth functions
    'admin_login_db_check',
    'user_register_db',
    'user_login_db_check',
    
    # Blog functions
    'get_blogs_list_db',
    'get_blogs_by_category',
    'get_blog',
    'handle_blog',
    'save_blogs_to_db',
    'update_blogs_to_db',
    'delete_blog_from_db',
    
    # File functions
    'upload_file_to_storage',
    'get_file_details_db',
    'delete_file_from_storage_by_url',
    'delete_file_from_storage',
    
    # Magazine functions
    'get_magazine_url',
    'create_magazine_db',
    'get_recent_magazines_db',
    'get_magazine_details_db',
    'delete_magazine_from_db',
    
    # Ad manager functions
    'get_organizations_db',
    'add_organization_db',
    'update_organization_db',
    'delete_organization_db',
    'get_ads_db',
    'add_ad_db',
    'update_ad_db',
    'delete_ad_db',
    'get_orgs_db',
    
    # General functions
    'sha256_hash',
    'get_page_data',
    'format_file_size',
    'get_leadership_details',
    'update_main_page_db',
    'delete_main_page_db',
    'get_chosen_orgs',
    'get_main_pages_db',
    
    # Page handler functions
    'get_blog_preview',
    'get_blog_page',
    'get_homepage',
]

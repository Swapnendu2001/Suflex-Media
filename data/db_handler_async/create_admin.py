"""
Admin User Creation Module

This module provides functions for creating and managing admin users.
The functions are imported from the auth module to maintain compatibility
with existing imports.
"""

from .auth import (
    create_admin_user,
    get_all_admin_users,
    delete_admin_user,
    update_admin_user,
    create_default_admin
)

__all__ = [
    'create_admin_user',
    'get_all_admin_users', 
    'delete_admin_user',
    'update_admin_user',
    'create_default_admin'
]
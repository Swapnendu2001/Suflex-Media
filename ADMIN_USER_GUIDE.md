# Admin User Management Guide for Suflex Media

This document explains how to create and manage admin users in the Suflex Media application.

## Function Locations

The admin user management functions are located in:
- **Primary location**: `data/db_handler_async/auth.py`
- **Re-exported from**: `data/db_handler_async/create_admin.py` (for backward compatibility)

## Available Functions

The following functions are available for admin user management:

- `create_admin_user(username, email, password)` - Creates a new admin user with hashed password
- `get_all_admin_users()` - Retrieves all admin users from the database
- `delete_admin_user(email)` - Deletes an admin user by email
- `update_admin_user(email, new_username=None, new_password=None)` - Updates admin user information
- `create_default_admin()` - Creates a default admin user if none exists

## Available Endpoints

### Create Admin User
- **Endpoint**: `POST /api/admin_users`
- **Description**: Creates a new admin user
- **Request Body**:
  ```json
  {
    "username": "admin_username",
    "email": "admin@example.com",
    "password": "secure_password"
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "message": "Admin user created successfully.",
    "data": {
      "id": "uuid-string",
      "username": "admin_username",
      "email": "admin@example.com"
    }
  }
  ```

### Get All Admin Users
- **Endpoint**: `GET /api/admin_users`
- **Description**: Retrieves all admin users

### Update Admin User
- **Endpoint**: `PUT /api/admin_users/{email}`
- **Description**: Updates an existing admin user
- **Request Body**:
  ```json
  {
    "username": "new_username",
    "password": "new_password"
  }
  ```

### Delete Admin User
- **Endpoint**: `DELETE /api/admin_users/{email}`
- **Description**: Deletes an admin user by email

### Create Default Admin
- **Endpoint**: `POST /api/create_default_admin`
- **Description**: Creates a default admin user if none exists (username: "admin", email: "admin@example.com", password: "admin123")

## Using the Command Line Tool

You can also create admin users using the command line tool:

```bash
python create_admin_users.py
```

This will provide an interactive interface to create admin users or set up a default admin account.

## Database Schema

Admin users are stored in the `admin_users` table with the following columns:
- `id`: UUID (Primary Key, auto-generated)
- `created_at`: Timestamp with timezone (auto-generated)
- `email`: Text
- `username`: Text
- `password`: Text (hashed)

## Security Notes

- Passwords are automatically hashed using SHA256 before being stored in the database
- Always use strong passwords for admin accounts
- The default admin password should be changed immediately after creation
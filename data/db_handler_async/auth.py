from ..db_handler_async.db_sync_utils import execute_query, execute_mutation
from .general_function import sha256_hash


def admin_login_db_check(email, password):
    print(f"Attempting admin login with email: {email} and \n password: {password}")
    
    query = "SELECT * FROM admin_users WHERE email = $1 AND password = $2"
    params = (email, password)
    
    result = execute_query(query, params)
    
    if result:
        user_data = result[0]
        return {
            "success": True,
            "email": email,
            "name": user_data["username"],
            "enc_email": user_data["email"],
            "enc_pwd": user_data["password"],
        }
    return {"success": False, "email": email}


def user_register_db(username, email, password):
    try:
        # Check if user already exists
        check_query = "SELECT id FROM users WHERE email = $1"
        existing_users = execute_query(check_query, (email,))
        
        if existing_users:
            return {"status": "error", "message": "User with this email already exists."}

        # Insert new user
        insert_query = """
            INSERT INTO users (username, email, password) 
            VALUES ($1, $2, $3) 
            RETURNING *
        """
        params = (username, email, sha256_hash(password))
        
        result = execute_mutation(insert_query, params)

        if result:
            return {"status": "success", "message": "User registered successfully.", "data": result[0]}
        else:
            return {"status": "error", "message": "Failed to register user."}
    except Exception as e:
        print(f"Error registering user: {e}")
        return {"status": "error", "message": str(e)}


def user_login_db_check(email, password):
    try:
        hashed_password = sha256_hash(password)
        query = "SELECT * FROM users WHERE email = $1 AND password = $2"
        params = (email, hashed_password)
        
        result = execute_query(query, params)
        
        if result:
            user = result[0]
            return {
                "success": True,
                "username": user["username"],
                "email": user["email"],
            }
        return {"success": False, "message": "Invalid email or password."}
    except Exception as e:
        print(f"Error during user login check: {e}")


def create_admin_user(username, email, password):
    """
    Create a new admin user with the given credentials.
    The password will be hashed before storing in the database.
    """
    try:
        # Check if admin user already exists with this email
        check_query = "SELECT id FROM admin_users WHERE email = $1"
        existing_admins = execute_query(check_query, (email,))
        
        if existing_admins:
            return {"status": "error", "message": "Admin user with this email already exists."}

        # Hash the password
        hashed_password = sha256_hash(password)
        
        # Insert new admin user
        insert_query = """
            INSERT INTO admin_users (username, email, password) 
            VALUES ($1, $2, $3) 
            RETURNING *
        """
        params = (username, email, hashed_password)
        
        result = execute_mutation(insert_query, params)

        if result:
            return {
                "status": "success", 
                "message": "Admin user created successfully.", 
                "data": {
                    "id": result[0]["id"],
                    "username": result[0]["username"],
                    "email": result[0]["email"]
                }
            }
        else:
            return {"status": "error", "message": "Failed to create admin user."}
    except Exception as e:
        print(f"Error creating admin user: {e}")
        return {"status": "error", "message": str(e)}


def get_all_admin_users():
    """
    Retrieve all admin users from the database.
    """
    try:
        query = "SELECT id, username, email, created_at FROM admin_users ORDER BY created_at DESC"
        result = execute_query(query)
        
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        print(f"Error retrieving admin users: {e}")
        return {"status": "error", "message": str(e)}


def delete_admin_user(email):
    """
    Delete an admin user by email.
    """
    try:
        query = "DELETE FROM admin_users WHERE email = $1 RETURNING id, username, email"
        result = execute_mutation(query, (email,))
        
        if result:
            return {
                "status": "success", 
                "message": "Admin user deleted successfully.",
                "data": result[0]
            }
        else:
            return {"status": "error", "message": "Admin user not found."}
    except Exception as e:
        print(f"Error deleting admin user: {e}")
        return {"status": "error", "message": str(e)}


def update_admin_user(email, new_username=None, new_password=None):
    """
    Update an admin user's information.
    """
    try:
        # Build the update query dynamically based on provided parameters
        updates = []
        params = []
        param_index = 1
        
        if new_username:
            updates.append(f"username = ${param_index}")
            params.append(new_username)
            param_index += 1
            
        if new_password:
            hashed_password = sha256_hash(new_password)
            updates.append(f"password = ${param_index}")
            params.append(hashed_password)
            param_index += 1
        
        if not updates:
            return {"status": "error", "message": "No updates provided."}
        
        params.append(email)  # For the WHERE clause
        update_clause = ", ".join(updates)
        query = f"UPDATE admin_users SET {update_clause} WHERE email = ${param_index} RETURNING *"
        
        result = execute_mutation(query, tuple(params))
        
        if result:
            return {
                "status": "success", 
                "message": "Admin user updated successfully.",
                "data": result[0]
            }
        else:
            return {"status": "error", "message": "Admin user not found."}
    except Exception as e:
        print(f"Error updating admin user: {e}")
        return {"status": "error", "message": str(e)}


def create_default_admin():
    """
    Create a default admin user if no admin users exist.
    This is useful for setting up the initial admin account.
    """
    try:
        # Check if any admin users exist
        check_query = "SELECT COUNT(*) as count FROM admin_users"
        result = execute_query(check_query)
        
        if result and result[0]['count'] == 0:
            # No admin users exist, create default admin
            default_username = "admin"
            default_email = "admin@example.com"
            default_password = "admin123"
            
            return create_admin_user(default_username, default_email, default_password)
        else:
            return {"status": "info", "message": "Admin user(s) already exist, skipping default admin creation."}
    except Exception as e:
        print(f"Error checking for existing admin users: {e}")
        return {"status": "error", "message": str(e)}
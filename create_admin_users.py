#!/usr/bin/env python3
"""
Script to create admin users for the Suflex Media application.

This script provides functionality to create admin users in the database.
It can be used to set up initial admin accounts or add new administrators.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.db_handler_async.auth import create_admin_user, create_default_admin


def main():
    print("Suflex Media - Admin User Creation Tool")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Create a new admin user")
        print("2. Create default admin (if none exists)")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            print("\nCreating a new admin user...")
            username = input("Enter username: ").strip()
            email = input("Enter email: ").strip()
            password = input("Enter password: ").strip()
            
            if not all([username, email, password]):
                print("Error: All fields are required!")
                continue
            
            result = create_admin_user(username, email, password)
            if result["status"] == "success":
                print(f"✓ Admin user created successfully!")
                print(f"  - ID: {result['data']['id']}")
                print(f"  - Username: {result['data']['username']}")
                print(f"  - Email: {result['data']['email']}")
            else:
                print(f"✗ Error creating admin user: {result['message']}")
        
        elif choice == "2":
            print("\nCreating default admin user (if none exists)...")
            result = create_default_admin()
            print(f"Result: {result['message']}")
        
        elif choice == "3":
            print("\nGoodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Authentication Manager
Handles user authentication and session management for the web dashboard
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
from pathlib import Path
import secrets

class User(UserMixin):
    """User model for authentication"""
    
    def __init__(self, id, username, password_hash, email=None, created_at=None, is_admin=False):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.created_at = created_at or datetime.now().isoformat()
        self.is_admin = is_admin
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to dictionary for storage"""
        return {
            'id': self.id,
            'username': self.username,
            'password_hash': self.password_hash,
            'email': self.email,
            'created_at': self.created_at,
            'is_admin': self.is_admin
        }

class AuthManager:
    """Manages user authentication and storage"""
    
    def __init__(self, users_file='users.json'):
        self.users_file = Path(users_file)
        self.users = {}
        self._load_users()
    
    def _load_users(self):
        """Load users from file"""
        if self.users_file.exists():
            try:
                with open(self.users_file, 'r') as f:
                    data = json.load(f)
                    for user_data in data.get('users', []):
                        user = User(**user_data)
                        self.users[user.id] = user
            except Exception as e:
                print(f"Error loading users: {e}")
        
        # Create default admin if no users exist
        if not self.users:
            self._create_default_admin()
    
    def _save_users(self):
        """Save users to file"""
        data = {
            'users': [user.to_dict() for user in self.users.values()],
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.users_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _create_default_admin(self):
        """Create default admin user with a random temporary password.

        The setup wizard (first-run) forces the user to choose a real password
        before they can log in, so this temporary password is never usable in
        practice.
        """
        temp_password = secrets.token_urlsafe(24)
        admin_id = secrets.token_hex(8)
        admin = User(
            id=admin_id,
            username='admin',
            password_hash=generate_password_hash(temp_password),
            email='admin@localhost',
            is_admin=True
        )
        self.users[admin_id] = admin
        self._save_users()
        print("Default admin user created — password must be set via setup wizard.")
    
    def create_user(self, username, password, email=None, is_admin=False):
        """Create a new user"""
        # Check if username already exists
        if any(u.username == username for u in self.users.values()):
            return None, "Username already exists"
        
        user_id = secrets.token_hex(8)
        user = User(
            id=user_id,
            username=username,
            password_hash=generate_password_hash(password),
            email=email,
            is_admin=is_admin
        )
        
        self.users[user_id] = user
        self._save_users()
        
        return user, None
    
    def get_user(self, user_id):
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_user_by_username(self, username):
        """Get user by username"""
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    def authenticate(self, username, password):
        """Authenticate user with username and password"""
        user = self.get_user_by_username(username)
        if user and user.check_password(password):
            return user
        return None
    
    def change_password(self, user_id, old_password, new_password):
        """Change user password"""
        user = self.get_user(user_id)
        if not user:
            return False, "User not found"
        
        if not user.check_password(old_password):
            return False, "Incorrect current password"
        
        user.password_hash = generate_password_hash(new_password)
        self._save_users()
        
        return True, "Password changed successfully"
    
    def delete_user(self, user_id):
        """Delete a user"""
        if user_id in self.users:
            # Don't allow deleting the last admin
            if self.users[user_id].is_admin:
                admin_count = sum(1 for u in self.users.values() if u.is_admin)
                if admin_count <= 1:
                    return False, "Cannot delete the last admin user"
            
            del self.users[user_id]
            self._save_users()
            return True, "User deleted successfully"
        
        return False, "User not found"
    
    def list_users(self):
        """List all users (without password hashes)"""
        return [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at,
                'is_admin': user.is_admin
            }
            for user in self.users.values()
        ]

def setup_user_interactive():
    """Interactive user setup"""
    import getpass
    
    print("👤 User Setup")
    print("=" * 50)
    
    auth = AuthManager()
    
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    password_confirm = getpass.getpass("Confirm password: ")
    
    if password != password_confirm:
        print("❌ Passwords don't match")
        return
    
    email = input("Email (optional): ").strip() or None
    is_admin = input("Admin user? (y/N): ").lower().strip() == 'y'
    
    user, error = auth.create_user(username, password, email, is_admin)
    
    if error:
        print(f"❌ Error: {error}")
    else:
        print(f"✅ User '{username}' created successfully")
        if is_admin:
            print("🔑 User has admin privileges")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "add":
            setup_user_interactive()
        elif sys.argv[1] == "list":
            auth = AuthManager()
            users = auth.list_users()
            print("\n👥 Users:")
            print("=" * 50)
            for user in users:
                admin_badge = " [ADMIN]" if user['is_admin'] else ""
                print(f"• {user['username']}{admin_badge}")
                print(f"  Email: {user['email'] or 'N/A'}")
                print(f"  Created: {user['created_at']}")
                print()
        else:
            print("Usage: python auth_manager.py [add|list]")
    else:
        print("👤 Authentication Manager")
        print("Usage:")
        print("  python auth_manager.py add   - Add new user")
        print("  python auth_manager.py list  - List all users")
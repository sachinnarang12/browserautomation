#!/usr/bin/env python3
"""
Secure Credential Manager
Handles secure storage and retrieval of credentials using keyring
"""

import keyring
import json
from typing import Dict, Optional
from pathlib import Path
import getpass
from datetime import datetime

class CredentialManager:
    """Secure credential storage using system keyring"""
    
    SERVICE_NAME = "PortalAutomationAgent"
    
    def __init__(self):
        self.credentials_file = Path("credentials_index.json")
        self._load_index()
    
    def _load_index(self):
        """Load credential index (non-sensitive metadata only)"""
        if self.credentials_file.exists():
            with open(self.credentials_file, 'r') as f:
                self.index = json.load(f)
        else:
            self.index = {"credentials": {}}
    
    def _save_index(self):
        """Save credential index"""
        with open(self.credentials_file, 'w') as f:
            json.dump(self.index, f, indent=2)
    
    def store_credential(self, credential_id: str, username: str, password: str, 
                        description: str = "", url: str = ""):
        """
        Store credentials securely in system keyring
        
        Args:
            credential_id: Unique identifier for this credential
            username: Username/email
            password: Password (will be encrypted)
            description: Human-readable description
            url: Associated URL
        """
        # Store password in system keyring
        keyring.set_password(self.SERVICE_NAME, f"{credential_id}_password", password)
        
        # Store username in keyring too (for consistency)
        keyring.set_password(self.SERVICE_NAME, f"{credential_id}_username", username)
        
        # Store metadata in index (non-sensitive but include username for display)
        self.index["credentials"][credential_id] = {
            "username": username,
            "description": description,
            "url": url,
            "created_at": str(datetime.now())
        }
        
        self._save_index()
    
    def get_credential(self, credential_id: str) -> Optional[Dict[str, str]]:
        """
        Retrieve credentials from keyring
        
        Returns:
            Dict with 'username' and 'password' keys, or None if not found
        """
        if credential_id not in self.index["credentials"]:
            return None
        
        username = keyring.get_password(self.SERVICE_NAME, f"{credential_id}_username")
        password = keyring.get_password(self.SERVICE_NAME, f"{credential_id}_password")
        
        if username and password:
            return {
                "username": username,
                "password": password,
                "metadata": self.index["credentials"][credential_id]
            }
        
        return None
    
    def list_credentials(self) -> Dict[str, Dict]:
        """List all stored credentials (metadata only, no passwords)"""
        return self.index["credentials"]
    
    def delete_credential(self, credential_id: str) -> bool:
        """Delete credentials from keyring"""
        if credential_id not in self.index["credentials"]:
            return False
        
        try:
            keyring.delete_password(self.SERVICE_NAME, f"{credential_id}_username")
            keyring.delete_password(self.SERVICE_NAME, f"{credential_id}_password")
            del self.index["credentials"][credential_id]
            self._save_index()
            return True
        except:
            return False
    
    def update_credential(self, credential_id: str, username: str = None, 
                         password: str = None, description: str = None, url: str = None):
        """Update existing credentials"""
        if credential_id not in self.index["credentials"]:
            return False
        
        if username:
            keyring.set_password(self.SERVICE_NAME, f"{credential_id}_username", username)
        
        if password:
            keyring.set_password(self.SERVICE_NAME, f"{credential_id}_password", password)
        
        if description:
            self.index["credentials"][credential_id]["description"] = description
        
        if url:
            self.index["credentials"][credential_id]["url"] = url
        
        self._save_index()
        return True

def setup_credentials_interactive():
    """Interactive credential setup"""
    from datetime import datetime
    
    print("🔐 Secure Credential Setup")
    print("=" * 50)
    
    manager = CredentialManager()
    
    credential_id = input("Credential ID (e.g., 'utility_portal'): ").strip()
    
    if credential_id in manager.list_credentials():
        print(f"⚠️  Credential '{credential_id}' already exists")
        overwrite = input("Overwrite? (y/N): ").lower().strip()
        if overwrite != 'y':
            print("❌ Cancelled")
            return
    
    description = input("Description: ").strip()
    url = input("URL: ").strip()
    username = input("Username: ").strip()
    password = getpass.getpass("Password (hidden): ")
    
    manager.store_credential(credential_id, username, password, description, url)
    
    print(f"✅ Credentials stored securely for '{credential_id}'")
    print("🔒 Password encrypted in system keyring")

def list_credentials_interactive():
    """List all stored credentials"""
    manager = CredentialManager()
    credentials = manager.list_credentials()
    
    if not credentials:
        print("📋 No credentials stored")
        return
    
    print("\n🔐 Stored Credentials")
    print("=" * 50)
    
    for cred_id, metadata in credentials.items():
        print(f"\n📌 {cred_id}")
        print(f"   Description: {metadata.get('description', 'N/A')}")
        print(f"   URL: {metadata.get('url', 'N/A')}")
        print(f"   Created: {metadata.get('created_at', 'N/A')}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "add":
            setup_credentials_interactive()
        elif sys.argv[1] == "list":
            list_credentials_interactive()
        else:
            print("Usage: python credential_manager.py [add|list]")
    else:
        print("🔐 Credential Manager")
        print("Usage:")
        print("  python credential_manager.py add   - Add new credentials")
        print("  python credential_manager.py list  - List stored credentials")
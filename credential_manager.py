#!/usr/bin/env python3
"""
Secure Credential Manager
Handles secure storage and retrieval of credentials using keyring,
with an encrypted file fallback for headless Linux systems.
"""

import keyring
import json
import os
import sys
import base64
from typing import Dict, Optional
from pathlib import Path
import getpass
from datetime import datetime


def _init_keyring():
    """Initialize keyring with a working backend.

    On headless Linux (no D-Bus / DISPLAY), the default SecretService backend
    won't work.  Instead of falling back to PlaintextKeyring we use
    ``cryptography.Fernet`` with a key derived from a master password so that
    credentials are always encrypted at rest.
    """
    needs_fallback = (
        sys.platform == 'linux'
        and not os.environ.get('DBUS_SESSION_BUS_ADDRESS')
        and not os.environ.get('DISPLAY')
    )

    if needs_fallback:
        try:
            from keyrings.alt.file import EncryptedKeyring
            keyring.set_keyring(EncryptedKeyring())
        except (ImportError, Exception):
            # EncryptedKeyring may not be available; use our own Fernet backend
            keyring.set_keyring(_FernetFileKeyring())


class _FernetFileKeyring(keyring.backend.KeyringBackend):
    """Encrypted file-based keyring using Fernet (AES-128-CBC + HMAC).

    The encryption key is derived from the environment variable
    ``PORTAL_MASTER_KEY``.  If that is not set, a random key is generated
    on first use and written to ``data/.master_key`` (chmod 600).
    """

    priority = 1  # low priority so native backends win when available
    _VAULT_PATH = Path('data/credential_vault.enc')

    def __init__(self):
        self._fernet = None

    def _get_fernet(self):
        if self._fernet is not None:
            return self._fernet

        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.primitives import hashes

        master = os.environ.get('PORTAL_MASTER_KEY')
        key_file = Path('data/.master_key')

        if master:
            # Derive a Fernet key from the user-supplied master password
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                             salt=b'AutomatePortal_v2', iterations=480_000)
            raw = kdf.derive(master.encode())
            fernet_key = base64.urlsafe_b64encode(raw)
        elif key_file.exists():
            fernet_key = key_file.read_bytes().strip()
        else:
            # First run: generate and persist a random key
            fernet_key = Fernet.generate_key()
            key_file.parent.mkdir(parents=True, exist_ok=True)
            key_file.write_bytes(fernet_key)
            try:
                os.chmod(key_file, 0o600)
            except OSError:
                pass

        self._fernet = Fernet(fernet_key)
        return self._fernet

    # --- internal vault helpers -------------------------------------------

    def _load_vault(self) -> dict:
        if not self._VAULT_PATH.exists():
            return {}
        try:
            fernet = self._get_fernet()
            encrypted = self._VAULT_PATH.read_bytes()
            decrypted = fernet.decrypt(encrypted)
            return json.loads(decrypted)
        except Exception:
            return {}

    def _save_vault(self, vault: dict):
        fernet = self._get_fernet()
        plaintext = json.dumps(vault).encode()
        self._VAULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        self._VAULT_PATH.write_bytes(fernet.encrypt(plaintext))

    # --- KeyringBackend interface -----------------------------------------

    def set_password(self, service, username, password):
        vault = self._load_vault()
        vault.setdefault(service, {})[username] = password
        self._save_vault(vault)

    def get_password(self, service, username):
        vault = self._load_vault()
        return vault.get(service, {}).get(username)

    def delete_password(self, service, username):
        vault = self._load_vault()
        svc = vault.get(service, {})
        if username in svc:
            del svc[username]
            self._save_vault(vault)


_init_keyring()


class CredentialManager:
    """Secure credential storage using system keyring (or encrypted fallback)"""

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
        Store credentials securely in system keyring (or encrypted vault).

        Args:
            credential_id: Unique identifier for this credential
            username: Username/email
            password: Password (encrypted at rest)
            description: Human-readable description
            url: Associated URL
        """
        keyring.set_password(self.SERVICE_NAME, f"{credential_id}_password", password)
        keyring.set_password(self.SERVICE_NAME, f"{credential_id}_username", username)

        self.index["credentials"][credential_id] = {
            "username": username,
            "description": description,
            "url": url,
            "created_at": str(datetime.now())
        }
        self._save_index()

    def get_credential(self, credential_id: str) -> Optional[Dict[str, str]]:
        """
        Retrieve credentials from keyring / encrypted vault.

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
        """Delete credentials from keyring / vault"""
        if credential_id not in self.index["credentials"]:
            return False

        try:
            keyring.delete_password(self.SERVICE_NAME, f"{credential_id}_username")
            keyring.delete_password(self.SERVICE_NAME, f"{credential_id}_password")
            del self.index["credentials"][credential_id]
            self._save_index()
            return True
        except Exception:
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
#!/usr/bin/env python3
"""
Portal Automation Agent - V1 to V2 Migration Tool
Migrates tasks and credentials from V1 (JSON) to V2 (Database + Keyring)
"""

import json
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

from credential_manager import CredentialManager
from database import Database, Task, TaskStatus
from auth_manager import AuthManager

class MigrationTool:
    def __init__(self):
        self.credential_manager = CredentialManager()
        self.db = Database()
        self.auth_manager = AuthManager()
        
        self.v1_config_file = Path('agent_config.json')
        self.backup_dir = Path('v1_backup')
        
        self.stats = {
            'tasks_migrated': 0,
            'credentials_extracted': 0,
            'errors': []
        }
    
    def backup_v1_config(self) -> bool:
        """Backup V1 configuration files"""
        print("\n📦 Backing up V1 configuration...")
        
        try:
            # Create backup directory with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = self.backup_dir / f'backup_{timestamp}'
            backup_path.mkdir(parents=True, exist_ok=True)
            
            # Backup agent_config.json
            if self.v1_config_file.exists():
                shutil.copy2(self.v1_config_file, backup_path / 'agent_config.json')
                print(f"   ✅ Backed up: agent_config.json")
            
            # Backup other V1 files if they exist
            v1_files = ['portal_agent.log', 'users.json', 'credentials_index.json']
            for file in v1_files:
                file_path = Path(file)
                if file_path.exists():
                    shutil.copy2(file_path, backup_path / file)
                    print(f"   ✅ Backed up: {file}")
            
            print(f"\n✅ Backup created at: {backup_path}")
            return True
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            self.stats['errors'].append(f"Backup error: {e}")
            return False
    
    def extract_credentials_from_instructions(self, instructions: str) -> List[Dict]:
        """Extract username/password from task instructions"""
        credentials = []
        
        # Pattern 1: "username: X and password: Y"
        pattern1 = r'username[:\s]+([^\s]+).*?password[:\s]+([^\s]+)'
        matches = re.finditer(pattern1, instructions, re.IGNORECASE)
        
        for match in matches:
            username = match.group(1).strip()
            password = match.group(2).strip()
            credentials.append({
                'username': username,
                'password': password,
                'pattern': 'username_password'
            })
        
        # Pattern 2: "login with X / Y" or "X and Y"
        pattern2 = r'login.*?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}).*?([A-Za-z0-9!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]+)'
        matches = re.finditer(pattern2, instructions, re.IGNORECASE)
        
        for match in matches:
            username = match.group(1).strip()
            password = match.group(2).strip()
            if len(password) >= 6:  # Reasonable password length
                credentials.append({
                    'username': username,
                    'password': password,
                    'pattern': 'email_password'
                })
        
        return credentials

    def migrate_credentials(self, tasks: List[Dict]) -> Dict[str, str]:
        """Extract and migrate credentials from tasks"""
        print("\n🔐 Migrating credentials...")
        
        credential_map = {}  # Maps (username, password) -> credential_id
        
        for task in tasks:
            instructions = task.get('instructions', '')
            url = task.get('url', '')
            
            # Extract credentials from instructions
            found_creds = self.extract_credentials_from_instructions(instructions)
            
            for cred in found_creds:
                username = cred['username']
                password = cred['password']
                key = (username, password)
                
                # Skip if already processed
                if key in credential_map:
                    continue
                
                # Generate credential ID from URL or username
                if 'livingstonnj' in url.lower() or 'utility' in url.lower():
                    cred_id = 'utility_portal'
                elif 'demoqa' in url.lower():
                    cred_id = 'demoqa_test'
                else:
                    # Generate from username
                    cred_id = username.split('@')[0].replace('.', '_')
                
                # Make unique if needed
                base_cred_id = cred_id
                counter = 1
                while cred_id in [v for v in credential_map.values()]:
                    cred_id = f"{base_cred_id}_{counter}"
                    counter += 1
                
                # Store credential
                try:
                    description = f"Migrated from V1 - {url}"
                    self.credential_manager.store_credential(
                        cred_id, username, password, description, url
                    )
                    credential_map[key] = cred_id
                    self.stats['credentials_extracted'] += 1
                    print(f"   ✅ Stored credential: {cred_id} ({username})")
                    
                except Exception as e:
                    print(f"   ⚠️  Failed to store credential {cred_id}: {e}")
                    self.stats['errors'].append(f"Credential error: {e}")
        
        print(f"\n✅ Migrated {self.stats['credentials_extracted']} credential(s)")
        return credential_map
    
    def update_task_instructions(self, instructions: str, credential_map: Dict) -> str:
        """Replace plain-text credentials with template variables"""
        updated = instructions
        
        for (username, password), cred_id in credential_map.items():
            # Replace username
            updated = updated.replace(username, f"{{{{credential:{cred_id}:username}}}}")
            
            # Replace password
            updated = updated.replace(password, f"{{{{credential:{cred_id}:password}}}}")
        
        return updated
    
    def migrate_tasks(self) -> bool:
        """Migrate tasks from V1 JSON to V2 database"""
        print("\n📋 Migrating tasks...")
        
        if not self.v1_config_file.exists():
            print("❌ No V1 configuration found (agent_config.json)")
            return False
        
        try:
            # Load V1 tasks
            with open(self.v1_config_file, 'r') as f:
                v1_data = json.load(f)
            
            tasks = v1_data.get('tasks', [])
            
            if not tasks:
                print("⚠️  No tasks found in V1 configuration")
                return True
            
            print(f"   Found {len(tasks)} task(s) to migrate")
            
            # First, migrate credentials
            credential_map = self.migrate_credentials(tasks)
            
            # Get default user (admin)
            admin_user = self.auth_manager.get_user('admin')
            if not admin_user:
                print("❌ Admin user not found. Please run database initialization first.")
                return False
            
            # Migrate each task
            for v1_task in tasks:
                try:
                    # Update instructions with credential references
                    original_instructions = v1_task.get('instructions', '')
                    updated_instructions = self.update_task_instructions(
                        original_instructions, credential_map
                    )
                    
                    # Create V2 task
                    task = Task(
                        name=v1_task.get('name', 'Unnamed Task'),
                        url=v1_task.get('url', ''),
                        instructions=updated_instructions,
                        scheduled_time=v1_task.get('scheduled_time', ''),
                        enabled=v1_task.get('enabled', True),
                        user_id=admin_user.id,
                        status=TaskStatus.PENDING,
                        retry_count=v1_task.get('retry_count', 0),
                        max_retries=v1_task.get('max_retries', 3)
                    )
                    
                    # Add to database
                    session = self.db.get_session()
                    session.add(task)
                    session.commit()
                    
                    self.stats['tasks_migrated'] += 1
                    print(f"   ✅ Migrated task: {task.name}")
                    
                    # Show credential replacement if any
                    if updated_instructions != original_instructions:
                        print(f"      🔐 Updated instructions with credential references")
                    
                except Exception as e:
                    print(f"   ❌ Failed to migrate task '{v1_task.get('name')}': {e}")
                    self.stats['errors'].append(f"Task migration error: {e}")
            
            print(f"\n✅ Migrated {self.stats['tasks_migrated']} task(s)")
            return True
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            self.stats['errors'].append(f"Migration error: {e}")
            return False
    
    def verify_migration(self) -> bool:
        """Verify migration was successful"""
        print("\n🔍 Verifying migration...")
        
        try:
            # Check credentials
            creds = self.credential_manager.list_credentials()
            print(f"   ✅ Found {len(creds)} credential(s) in keyring")
            
            # Check tasks
            session = self.db.get_session()
            tasks = session.query(Task).all()
            print(f"   ✅ Found {len(tasks)} task(s) in database")
            
            # Check for credential references in tasks
            tasks_with_creds = sum(1 for t in tasks if '{{credential:' in t.instructions)
            print(f"   ✅ {tasks_with_creds} task(s) using secure credentials")
            
            return True
            
        except Exception as e:
            print(f"❌ Verification failed: {e}")
            return False
    
    def print_summary(self):
        """Print migration summary"""
        print("\n" + "=" * 60)
        print("📊 MIGRATION SUMMARY")
        print("=" * 60)
        print(f"✅ Tasks migrated: {self.stats['tasks_migrated']}")
        print(f"🔐 Credentials extracted: {self.stats['credentials_extracted']}")
        
        if self.stats['errors']:
            print(f"\n⚠️  Errors encountered: {len(self.stats['errors'])}")
            for error in self.stats['errors'][:5]:  # Show first 5
                print(f"   - {error}")
            if len(self.stats['errors']) > 5:
                print(f"   ... and {len(self.stats['errors']) - 5} more")
        else:
            print("\n✅ No errors encountered")
        
        print("=" * 60)
    
    def run(self):
        """Run the complete migration process"""
        print("\n" + "=" * 60)
        print("🚀 Portal Automation Agent - V1 to V2 Migration")
        print("=" * 60)
        
        # Step 1: Backup
        if not self.backup_v1_config():
            print("\n❌ Migration aborted due to backup failure")
            return False
        
        # Step 2: Migrate
        if not self.migrate_tasks():
            print("\n❌ Migration failed")
            self.print_summary()
            return False
        
        # Step 3: Verify
        if not self.verify_migration():
            print("\n⚠️  Migration completed but verification failed")
        
        # Step 4: Summary
        self.print_summary()
        
        print("\n✅ Migration completed successfully!")
        print("\n📝 Next steps:")
        print("   1. Review migrated tasks in the dashboard")
        print("   2. Test credential references")
        print("   3. Start the scheduler: python standalone_scheduler.py")
        print("   4. Monitor task execution")
        
        return True

def main():
    """Main entry point"""
    print("\n⚠️  WARNING: This will migrate your V1 configuration to V2")
    print("   - V1 files will be backed up")
    print("   - Credentials will be moved to Windows Credential Manager")
    print("   - Tasks will be moved to the database")
    
    response = input("\nContinue with migration? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("\n❌ Migration cancelled")
        return
    
    migrator = MigrationTool()
    migrator.run()

if __name__ == '__main__':
    main()

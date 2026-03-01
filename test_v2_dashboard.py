#!/usr/bin/env python3
"""
Quick test script for V2 Dashboard functionality
"""

from credential_manager import CredentialManager
from auth_manager import AuthManager
from database import Database

def test_credential_manager():
    """Test credential manager"""
    print("\n🔐 Testing Credential Manager...")
    cm = CredentialManager()
    
    # List credentials
    creds = cm.list_credentials()
    print(f"   Found {len(creds)} credential(s)")
    
    for cred_id, cred_data in creds.items():
        print(f"   - {cred_id}: {cred_data.get('username', 'N/A')}")
    
    return True

def test_auth_manager():
    """Test authentication manager"""
    print("\n👤 Testing Authentication Manager...")
    am = AuthManager()
    
    # Check admin user
    admin = am.get_user('admin')
    if admin:
        print(f"   ✅ Admin user exists: {admin.username}")
        print(f"   - Is admin: {admin.is_admin}")
        print(f"   - Created: {admin.created_at}")
    else:
        print("   ❌ Admin user not found")
        return False
    
    # List all users
    users = am.list_users()
    print(f"   Total users: {len(users)}")
    
    return True

def test_database():
    """Test database connection"""
    print("\n💾 Testing Database...")
    db = Database()
    
    try:
        session = db.get_session()
        from database import Task, User
        
        # Count tasks
        task_count = session.query(Task).count()
        print(f"   Tasks in database: {task_count}")
        
        # Count users
        user_count = session.query(User).count()
        print(f"   Users in database: {user_count}")
        
        return True
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False

def test_credential_list_format():
    """Test credential list format for template"""
    print("\n📋 Testing Credential List Format...")
    cm = CredentialManager()
    
    creds_dict = cm.list_credentials()
    creds = []
    for cred_id, cred_data in creds_dict.items():
        cred_item = {
            'credential_id': cred_id,
            'username': cred_data.get('username', ''),
            'description': cred_data.get('description', ''),
            'url': cred_data.get('url', ''),
            'created_at': cred_data.get('created_at', '')
        }
        creds.append(cred_item)
    
    print(f"   Converted {len(creds)} credential(s) to list format")
    for cred in creds:
        print(f"   - {cred['credential_id']}: {cred['username']}")
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 V2 Dashboard Component Tests")
    print("=" * 60)
    
    tests = [
        ("Credential Manager", test_credential_manager),
        ("Authentication Manager", test_auth_manager),
        ("Database", test_database),
        ("Credential List Format", test_credential_list_format),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ Test failed with exception: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! V2 Dashboard is ready.")
        print("\n📝 Next steps:")
        print("   1. Start dashboard: python agent_dashboard_v2.py")
        print("   2. Login at: http://localhost:5000")
        print("   3. Default credentials: admin / admin123")
        print("   4. Change password immediately!")
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
    
    print("=" * 60)

if __name__ == '__main__':
    main()

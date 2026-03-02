#!/usr/bin/env python3
"""
Test credential login functionality standalone
"""

from credential_manager import CredentialManager
from nova_act import NovaAct
import time

def test_login(credential_id):
    """Test login with stored credential"""
    
    manager = CredentialManager()
    
    # Get credential
    cred = manager.get_credential(credential_id)
    if not cred:
        print(f"Credential '{credential_id}' not found")
        return False
    
    print(f"Testing credential: {credential_id}")
    print(f"Username: {cred['username']}")
    print(f"URL: {cred['metadata'].get('url', 'N/A')}")
    
    try:
        # Initialize Nova Act
        print("\nInitializing browser...")
        nova = NovaAct(
            starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
            headless=True,
            tty=False,
            nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
        )
        
        nova.start()
        print("Browser started")
        
        # Attempt login
        print("\nAttempting login...")
        username = cred['username']
        password = cred['password']
        
        login_result = nova.act(f"""Login to the portal:
1. Enter username: {username}
2. Enter password: {password}
3. Click login button
4. Wait 10 seconds for the page to load
5. Check if login was successful by looking for dashboard or home page elements""")
        
        print(f"Login result: {login_result}")
        
        # Wait and verify
        time.sleep(3)
        
        verify_result = nova.act("Check if we are successfully logged in. Look for 'Active Home' dropdown or dashboard elements. Return 'SUCCESS' if logged in, 'FAILED' if still on login page or error page.")
        
        print(f"Verification result: {verify_result}")
        
        if 'SUCCESS' in str(verify_result).upper() or 'LOGGED IN' in str(verify_result).upper():
            print("\n✅ LOGIN TEST SUCCESSFUL!")
            success = True
        else:
            print("\n❌ LOGIN TEST FAILED")
            success = False
        
        # Keep browser open for inspection
        print("\nBrowser will stay open for 10 seconds for inspection...")
        time.sleep(10)
        
        nova.stop()
        print("Browser closed")
        
        return success
        
    except Exception as e:
        print(f"\n❌ Error during login test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        credential_id = sys.argv[1]
    else:
        # List available credentials
        manager = CredentialManager()
        creds = manager.list_credentials()
        
        if not creds:
            print("No credentials stored. Add one first:")
            print("  python credential_manager.py add")
            sys.exit(1)
        
        print("Available credentials:")
        for cred_id in creds.keys():
            print(f"  - {cred_id}")
        
        credential_id = input("\nEnter credential ID to test: ").strip()
    
    test_login(credential_id)

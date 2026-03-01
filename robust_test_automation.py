#!/usr/bin/env python3
"""
Robust Test Automation - Using Your Working Utility Portal
Test the automation with your proven working configuration
"""

from nova_act import NovaAct
import time
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def main():
    print("🚀 Robust Test Automation - Using Your Working Configuration")
    print("=" * 60)
    
    log_message("Using your proven working utility portal configuration...")
    
    # Use your exact working configuration from WORKING_simple_navigation_helper.py
    nova = NovaAct(
        starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
        headless=False,  # Keep browser visible
        tty=False,
        nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
    )
    
    try:
        log_message("🌐 Starting browser - you should see it open now...")
        nova.start()
        
        log_message("✅ Browser started successfully!")
        log_message("🔍 Browser window should be visible with the utility login page")
        
        # Test just the login part (don't do full automation to avoid account issues)
        log_message("🧪 Testing login page navigation...")
        
        result = nova.act("""Test navigation:
1. Wait for the login page to fully load (10 seconds)
2. Look for the username/email field on the page
3. Look for the password field on the page
4. Take a screenshot of the current page
5. Report what elements you can see on the page""")
        
        log_message("✅ Navigation test completed!")
        log_message(f"📋 Result: {result}")
        
        log_message("🔍 Keeping browser open for 30 seconds so you can see the result...")
        log_message("👀 Check the browser window - you should see the utility login page")
        
        # Keep browser open for inspection
        for i in range(30, 0, -1):
            print(f"\r⏳ Browser will close in {i} seconds... ", end="", flush=True)
            time.sleep(1)
        
        print("\n")
        log_message("🛑 Closing browser...")
        
    except Exception as e:
        log_message(f"❌ Error occurred: {e}")
        log_message("🔧 This might be a temporary network issue or site problem")
        
    finally:
        try:
            nova.stop()
            log_message("✅ Browser closed successfully")
        except:
            log_message("✅ Browser cleanup completed")
    
    log_message("🎉 Test completed!")
    log_message("💡 If this worked, your Nova Act setup is fine and the scheduler should work too")

if __name__ == "__main__":
    main()
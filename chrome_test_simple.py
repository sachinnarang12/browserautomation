#!/usr/bin/env python3
"""
Simple Chrome Test - Run Nova Act automation specifically on Chrome browser
"""

from nova_act import NovaAct
import time
from datetime import datetime
import os

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def main():
    print("🌐 Chrome Browser Test - Nova Act Automation")
    print("=" * 60)
    
    log_message("Initializing Nova Act with Chrome browser...")
    
    # Kill any existing Chrome processes first
    try:
        os.system("taskkill /f /im chrome.exe >nul 2>&1")
        os.system("taskkill /f /im chromedriver.exe >nul 2>&1")
        time.sleep(2)
        log_message("Cleaned up existing browser processes")
    except:
        pass
    
    # Create Nova Act instance with explicit Chrome configuration
    nova = NovaAct(
        starting_page="https://demoqa.com/login",
        headless=False,  # Keep browser visible
        tty=False,
        nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
    )
    
    try:
        log_message("🚀 Starting Chrome browser...")
        nova.start()
        
        log_message("✅ Chrome browser started successfully!")
        log_message("🔍 You should see a Chrome window open now")
        
        # Wait a moment for browser to fully load
        time.sleep(3)
        
        log_message("📋 Executing simple test automation...")
        
        # Simple, reliable test automation
        result = nova.act("""Simple Chrome test:
1. Wait for the page to fully load (5 seconds)
2. Look at the page title and confirm it contains 'ToolsQA'
3. Find the username input field
4. Click on the username field
5. Type 'testuser' slowly
6. Find the password input field  
7. Click on the password field
8. Type 'Test@123' slowly
9. Wait 2 seconds to see the filled form""")
        
        log_message("✅ Automation completed successfully!")
        log_message(f"📊 Result: {result}")
        
        log_message("🎯 Test completed! Browser will stay open for 15 seconds...")
        time.sleep(15)
        
    except Exception as e:
        log_message(f"❌ Error occurred: {str(e)}")
        log_message("🔧 This might be due to:")
        log_message("   - Chrome not installed or not in PATH")
        log_message("   - Antivirus blocking browser automation")
        log_message("   - Multiple browser instances running")
        log_message("   - Network connectivity issues")
        
    finally:
        try:
            log_message("🛑 Closing browser...")
            nova.stop()
            log_message("✅ Browser closed successfully")
        except Exception as e:
            log_message(f"⚠️ Browser cleanup: {e}")
    
    log_message("🎉 Chrome test completed!")

if __name__ == "__main__":
    main()
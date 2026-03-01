#!/usr/bin/env python3
"""
Run Task Immediately - Execute a Nova Act task right now without scheduling
"""

from nova_act import NovaAct
import time
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def main():
    print("🚀 Running Nova Act Task Immediately")
    print("=" * 50)
    
    log_message("Starting Nova Act browser automation...")
    
    # Create Nova Act instance (same config as your working script)
    nova = NovaAct(
        starting_page="https://demoqa.com/login",
        headless=False,  # Keep browser visible
        tty=False,
        nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
    )
    
    try:
        log_message("Starting browser...")
        nova.start()
        
        log_message("🌐 Browser should be visible now!")
        log_message("Executing automation instructions...")
        
        # Simple test automation
        result = nova.act("""Simple test automation:
1. Wait for the login page to fully load (5 seconds)
2. Look for the username field and click on it
3. Type 'testuser' in the username field
4. Look for the password field and click on it  
5. Type 'Test@123' in the password field
6. Take a screenshot of the current page
7. Wait 3 seconds so you can see the result""")
        
        log_message(f"✅ Automation completed successfully!")
        log_message(f"📋 Result: {result}")
        
        log_message("🔍 Browser will stay open for 30 seconds for you to see the result...")
        time.sleep(30)
        
    except Exception as e:
        log_message(f"❌ Error occurred: {e}")
        
    finally:
        try:
            nova.stop()
            log_message("🛑 Browser closed")
        except:
            log_message("🛑 Browser cleanup completed")
    
    log_message("✅ Test completed!")

if __name__ == "__main__":
    main()
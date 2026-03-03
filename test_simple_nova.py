#!/usr/bin/env python3
"""
Simple Nova Act Test - Test basic browser automation
"""

import os
from nova_act import NovaAct
import time

def test_simple_automation():
    print("🧪 Testing Simple Nova Act Automation")
    print("=" * 50)
    
    try:
        # Create Nova Act instance
        print("1. Creating Nova Act instance...")
        nova = NovaAct(
            starting_page="https://demoqa.com/login",
            headless=False,
            tty=False,
            nova_act_api_key=os.environ.get("NOVA_ACT_API_KEY", "")
        )
        
        print("2. Starting Nova Act...")
        nova.start()
        print("✅ Nova Act started successfully")
        
        print("3. Waiting 5 seconds for page to load...")
        time.sleep(5)
        
        print("4. Testing simple action...")
        result = nova.act("Take a screenshot of the current page")
        print(f"✅ Action completed: {result}")
        
        print("5. Keeping browser open for 10 seconds...")
        time.sleep(10)
        
        print("6. Stopping Nova Act...")
        nova.stop()
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        try:
            nova.stop()
        except:
            pass

if __name__ == "__main__":
    test_simple_automation()
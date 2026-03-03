#!/usr/bin/env python3
"""
Diagnose Nova Act Issues
Check system status and identify problems with Nova Act automation
"""

import os
import subprocess
import sys
import requests
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_internet_connectivity():
    """Check if we can reach the internet and test sites"""
    log_message("🌐 Checking internet connectivity...")
    
    test_sites = [
        "https://google.com",
        "https://demoqa.com",
        "https://demoqa.com/login"
    ]
    
    for site in test_sites:
        try:
            response = requests.get(site, timeout=10)
            log_message(f"✅ {site} - Status: {response.status_code}")
        except Exception as e:
            log_message(f"❌ {site} - Error: {e}")

def check_nova_act_installation():
    """Check Nova Act installation"""
    log_message("🔍 Checking Nova Act installation...")
    
    try:
        import nova_act
        log_message(f"✅ Nova Act imported successfully - Version: {nova_act.__version__ if hasattr(nova_act, '__version__') else 'Unknown'}")
    except ImportError as e:
        log_message(f"❌ Nova Act import failed: {e}")
        return False
    
    return True

def check_playwright_installation():
    """Check Playwright installation and browsers"""
    log_message("🎭 Checking Playwright installation...")
    
    try:
        import playwright
        log_message(f"✅ Playwright imported successfully")
        
        # Check if browsers are installed
        try:
            result = subprocess.run([sys.executable, "-m", "playwright", "install", "--help"], 
                                  capture_output=True, text=True, timeout=10)
            log_message("✅ Playwright CLI accessible")
        except Exception as e:
            log_message(f"⚠️ Playwright CLI issue: {e}")
            
    except ImportError as e:
        log_message(f"❌ Playwright import failed: {e}")
        return False
    
    return True

def check_chrome_processes():
    """Check for running Chrome processes"""
    log_message("🌐 Checking Chrome processes...")
    
    try:
        if sys.platform == "win32":
            result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq chrome.exe"], 
                                  capture_output=True, text=True)
            if "chrome.exe" in result.stdout:
                log_message("⚠️ Chrome processes found running")
                print(result.stdout)
            else:
                log_message("✅ No Chrome processes found")
        else:
            log_message("ℹ️ Chrome process check not implemented for this OS")
    except Exception as e:
        log_message(f"❌ Error checking Chrome processes: {e}")

def test_simple_nova_act():
    """Test basic Nova Act functionality"""
    log_message("🧪 Testing basic Nova Act functionality...")
    
    try:
        from nova_act import NovaAct
        
        # Test with a reliable site
        nova = NovaAct(
            starting_page="https://google.com",
            headless=True,  # Use headless for testing
            tty=False,
            nova_act_api_key=os.environ.get("NOVA_ACT_API_KEY", "")
        )
        
        log_message("🚀 Starting Nova Act test...")
        nova.start()
        
        log_message("✅ Nova Act started successfully")
        
        # Simple test action
        result = nova.act("Wait for the page to load and take a screenshot")
        log_message(f"✅ Test action completed: {result}")
        
        nova.stop()
        log_message("✅ Nova Act stopped successfully")
        
        return True
        
    except Exception as e:
        log_message(f"❌ Nova Act test failed: {e}")
        return False

def main():
    log_message("🔧 Starting Nova Act Diagnostics")
    log_message("=" * 50)
    
    # Run all checks
    check_internet_connectivity()
    print()
    
    nova_ok = check_nova_act_installation()
    print()
    
    playwright_ok = check_playwright_installation()
    print()
    
    check_chrome_processes()
    print()
    
    if nova_ok and playwright_ok:
        log_message("🧪 Running Nova Act functionality test...")
        test_result = test_simple_nova_act()
        print()
        
        if test_result:
            log_message("🎉 All tests passed! Nova Act should be working.")
        else:
            log_message("❌ Nova Act test failed. See errors above.")
    else:
        log_message("❌ Basic dependencies missing. Install Nova Act and Playwright first.")
    
    log_message("🔧 Diagnostics completed")
    
    # Recommendations
    print("\n" + "=" * 50)
    log_message("💡 RECOMMENDATIONS:")
    log_message("1. If Playwright failed: pip install playwright && playwright install")
    log_message("2. If Nova Act failed: pip install nova-act")
    log_message("3. If Chrome processes found: Close all Chrome windows and try again")
    log_message("4. If network issues: Check your internet connection")
    log_message("5. Try using your working utility portal URL instead of demo sites")

if __name__ == "__main__":
    main()
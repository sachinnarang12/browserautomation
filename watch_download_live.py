from nova_act import NovaAct
import os
import time
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_downloads():
    """Check Downloads folder for recent files"""
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    recent_files = []
    
    if os.path.exists(downloads_path):
        try:
            for file in os.listdir(downloads_path):
                file_path = os.path.join(downloads_path, file)
                if os.path.isfile(file_path):
                    mod_time = os.path.getmtime(file_path)
                    if time.time() - mod_time < 600:  # Last 10 minutes
                        recent_files.append({
                            'name': file,
                            'path': file_path,
                            'size': os.path.getsize(file_path),
                            'modified': datetime.fromtimestamp(mod_time)
                        })
        except Exception as e:
            log_message(f"Error checking downloads: {e}")
    
    return recent_files

log_message("🎬 LIVE DOWNLOAD WATCH - You'll see everything happen!")
log_message("The browser will stay open and visible throughout the process")

# Check initial state
initial_downloads = check_downloads()
log_message(f"📁 Initial downloads in folder: {len(initial_downloads)}")

# Initialize Nova Act with visible browser
log_message("🚀 Starting Nova Act with visible browser...")
nova = NovaAct(
    starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
    headless=False,  # Keep browser visible
    tty=False,
    nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
)

nova.start()
log_message("✅ Browser opened - you should see it now!")

try:
    # Step 1: Login (you'll see this happen)
    log_message("🔐 Step 1: Logging in... (watch the browser)")
    login_result = nova.act("Login with username narang.sachin@gmail.com and password Testing1234!12")
    log_message("✅ Login completed!")
    time.sleep(2)

    # Step 2: Select Active Home (you'll see this happen)
    log_message("🏠 Step 2: Selecting Active Home... (watch the dropdown)")
    home_result = nova.act("Find and click the Active Home dropdown, then select 103892 0")
    log_message("✅ Active Home selected!")
    time.sleep(2)

    # Step 3: Navigate to Usage (you'll see this happen)
    log_message("📊 Step 3: Going to Usage section... (watch the navigation)")
    usage_result = nova.act("Click on Usage in the left menu to go to the Usage section")
    log_message("✅ Usage section opened!")
    time.sleep(2)

    # Step 4: Export (you'll see this happen)
    log_message("📥 Step 4: Clicking Export... (watch for download)")
    log_message("👀 WATCH THE BROWSER - download should start now!")
    export_result = nova.act("Click the Export button to download the usage data")
    log_message("✅ Export button clicked!")
    
    # Give time for download to start
    log_message("⏳ Waiting 15 seconds for download to complete...")
    for i in range(15):
        time.sleep(1)
        log_message(f"   Waiting... {15-i} seconds remaining")

    # Check what happened
    log_message("🔍 Checking for downloaded files...")
    current_downloads = check_downloads()
    
    new_files = []
    for current in current_downloads:
        is_new = True
        for initial in initial_downloads:
            if current['path'] == initial['path']:
                is_new = False
                break
        if is_new:
            new_files.append(current)

    if new_files:
        log_message(f"🎉 SUCCESS! Found {len(new_files)} new file(s):")
        
        for file_info in new_files:
            log_message(f"\n📄 File: {file_info['name']}")
            log_message(f"   📏 Size: {file_info['size']:,} bytes")
            log_message(f"   🕒 Modified: {file_info['modified']}")
            log_message(f"   📂 Path: {file_info['path']}")
            
            # Open the file automatically
            log_message(f"🔍 Opening {file_info['name']}...")
            try:
                os.startfile(file_info['path'])
                log_message(f"✅ File opened successfully!")
            except Exception as e:
                log_message(f"❌ Error opening file: {e}")

    else:
        log_message("❌ No new downloads found automatically")
        log_message("🔍 Let's check the browser downloads manually...")
        
        # Ask Nova Act to check downloads
        browser_check = nova.act("Press Ctrl+J to open the browser downloads and tell me what you see")
        log_message(f"Browser downloads check: {browser_check}")

except Exception as e:
    log_message(f"❌ Error during automation: {e}")
    log_message("But don't worry - the browser is still open!")

# Final status
log_message("\n" + "="*60)
log_message("🎬 LIVE DOWNLOAD WATCH COMPLETE!")
log_message("="*60)

if new_files:
    log_message("✅ SUCCESS - Files were downloaded and opened!")
else:
    log_message("⚠️  No automatic downloads detected")
    log_message("📂 Please check your Downloads folder manually:")
    log_message(f"   Location: {os.path.join(os.path.expanduser('~'), 'Downloads')}")
    log_message("   Look for files modified in the last few minutes")

log_message("\n🔄 KEEPING SESSION ALIVE")
log_message("The browser will stay open so you can:")
log_message("1. See what happened during the automation")
log_message("2. Manually complete any remaining steps")
log_message("3. Check downloads in the browser (Ctrl+J)")
log_message("4. Navigate and explore as needed")
log_message("\nPress Ctrl+C when you're done to close everything")

# Keep session alive with periodic monitoring
try:
    while True:
        time.sleep(30)
        
        # Check for very recent downloads
        very_recent = check_downloads()
        for file_info in very_recent:
            if time.time() - file_info['modified'].timestamp() < 60:
                log_message(f"🆕 NEW FILE DETECTED: {file_info['name']}")
                try:
                    os.startfile(file_info['path'])
                    log_message(f"✅ Automatically opened: {file_info['name']}")
                except:
                    pass
        
        log_message("🔄 Session active - browser still open - Press Ctrl+C to stop")
        
except KeyboardInterrupt:
    log_message("\n🛑 Stopping session...")
    nova.stop()
    log_message("✅ Session stopped - browser closed")
    log_message("🎯 All done!")
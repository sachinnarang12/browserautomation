from nova_act import NovaAct
import os
import time
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_downloads():
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    recent_files = []
    
    if os.path.exists(downloads_path):
        try:
            for file in os.listdir(downloads_path):
                file_path = os.path.join(downloads_path, file)
                if os.path.isfile(file_path):
                    mod_time = os.path.getmtime(file_path)
                    if time.time() - mod_time < 300:  # Last 5 minutes
                        recent_files.append({
                            'name': file,
                            'path': file_path,
                            'size': os.path.getsize(file_path),
                            'modified': datetime.fromtimestamp(mod_time)
                        })
        except:
            pass
    
    return recent_files

print("🔄 ROBUST NOVA DOWNLOAD - Handling login redirects better")

initial_downloads = check_downloads()
log_message(f"Starting with {len(initial_downloads)} recent files")

# Start directly at the dashboard to avoid login redirect issues
nova = NovaAct(
    starting_page="https://livingstonnj.my360-app.com/dashboard",
    headless=False,
    tty=False,
    nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
)

nova.start()
log_message("✅ Browser opened - should redirect to login automatically")

try:
    # Step 1: Handle login (it should redirect to login page)
    log_message("🔐 Step 1: Handling login...")
    login_result = nova.act("""If you see a login page, login with:
    - Username: narang.sachin@gmail.com
    - Password: Testing1234!12
    
    If you're already logged in, describe what you see on the page.""")
    
    log_message("✅ Login step completed")
    time.sleep(5)  # Wait for any redirects
    
    # Step 2: Navigate to usage
    log_message("📊 Step 2: Finding usage section...")
    usage_result = nova.act("""Look for and navigate to the Usage section:
    1. If you see an Active Home dropdown, select "103892 0"
    2. Look for "Usage" in the menu and click it
    3. Describe what you see on the page""")
    
    log_message("✅ Usage navigation completed")
    time.sleep(3)
    
    # Step 3: Simple export
    log_message("📥 Step 3: Attempting export...")
    export_result = nova.act("""Look for an Export button or link and click it.
    If you see format options, choose Excel or XLSX.
    Describe what happens when you click it.""")
    
    log_message("✅ Export attempted")
    
    # Wait for potential download
    log_message("⏳ Waiting for download...")
    time.sleep(15)
    
    # Check for downloads
    current_downloads = check_downloads()
    new_files = [f for f in current_downloads if f not in initial_downloads]
    
    if new_files:
        log_message(f"🎉 SUCCESS! Found {len(new_files)} new file(s):")
        for file_info in new_files:
            log_message(f"📄 {file_info['name']} ({file_info['size']:,} bytes)")
            log_message(f"   📂 {file_info['path']}")
            
            # Open the file
            try:
                os.startfile(file_info['path'])
                log_message(f"✅ Opened: {file_info['name']}")
            except Exception as e:
                log_message(f"Error opening file: {e}")
    else:
        log_message("❌ No new downloads detected")
        
        # Manual check
        log_message("🔍 Let's check browser downloads...")
        browser_result = nova.act("Press Ctrl+J to open downloads and describe what you see")
        log_message(f"Browser downloads: {browser_result}")

except Exception as e:
    log_message(f"❌ Error during automation: {e}")

# Keep session alive for manual inspection
log_message("\n🔄 SESSION STAYING ALIVE")
log_message("Browser will remain open for manual inspection")
log_message("You can now manually navigate and complete any remaining steps")
log_message("Press Ctrl+C to stop when done")

try:
    while True:
        time.sleep(30)
        
        # Check for very recent downloads
        current = check_downloads()
        very_new = [f for f in current if time.time() - f['modified'].timestamp() < 60]
        
        if very_new:
            for file_info in very_new:
                log_message(f"🆕 NEW FILE: {file_info['name']}")
                try:
                    os.startfile(file_info['path'])
                    log_message(f"✅ Auto-opened: {file_info['name']}")
                except:
                    pass
        
        log_message("🔄 Monitoring... Press Ctrl+C to stop")
        
except KeyboardInterrupt:
    log_message("\n🛑 Stopping session...")
    nova.stop()
    log_message("✅ Session stopped!")
    log_message("Check your Downloads folder for any files that were downloaded")
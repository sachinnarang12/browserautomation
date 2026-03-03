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

print("="*60)
log_message("🎬 FRESH LIVE DOWNLOAD SESSION")
log_message("You'll watch the entire process happen step by step!")
print("="*60)

# Check what we start with
initial_downloads = check_downloads()
log_message(f"📁 Starting with {len(initial_downloads)} recent files in Downloads")

# Create fresh Nova Act session
log_message("🚀 Creating fresh Nova Act session...")
nova = NovaAct(
    starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
    headless=False,
    tty=False,
    nova_act_api_key=os.environ.get("NOVA_ACT_API_KEY", "")
)

log_message("🌐 Starting browser session...")
nova.start()
log_message("✅ Browser is now open and visible!")

try:
    # Complete process in steps you can watch
    log_message("\n🔐 STEP 1: LOGIN")
    log_message("👀 Watch the browser - entering credentials...")
    
    step1 = nova.act("Login using {{credential:utility_portal:username}} and {{credential:utility_portal:password}}")
    log_message("✅ Login step completed!")
    time.sleep(3)
    
    log_message("\n🏠 STEP 2: SELECT ACTIVE HOME")
    log_message("👀 Watch the browser - selecting Active Home...")
    
    step2 = nova.act("Select Active Home dropdown and choose 103892 0")
    log_message("✅ Active Home selected!")
    time.sleep(3)
    
    log_message("\n📊 STEP 3: NAVIGATE TO USAGE")
    log_message("👀 Watch the browser - going to Usage section...")
    
    step3 = nova.act("Click on Usage in the menu to go to Usage section")
    log_message("✅ Usage section opened!")
    time.sleep(3)
    
    log_message("\n📥 STEP 4: EXPORT DATA")
    log_message("👀 WATCH CAREFULLY - clicking Export button now...")
    log_message("🚨 DOWNLOAD SHOULD START - watch for browser download indicator!")
    
    step4 = nova.act("Click Export button to download the data")
    log_message("✅ Export button clicked!")
    
    # Monitor for download
    log_message("\n⏳ MONITORING FOR DOWNLOAD...")
    for i in range(20):
        time.sleep(1)
        current_downloads = check_downloads()
        new_files = [f for f in current_downloads if f not in initial_downloads]
        
        if new_files:
            log_message(f"🎉 DOWNLOAD DETECTED after {i+1} seconds!")
            break
        
        if i % 5 == 0:
            log_message(f"   Still waiting... {20-i} seconds remaining")
    
    # Final check
    final_downloads = check_downloads()
    new_files = [f for f in final_downloads if f not in initial_downloads]
    
    if new_files:
        log_message(f"\n🎉 SUCCESS! Downloaded {len(new_files)} file(s):")
        for file_info in new_files:
            log_message(f"📄 {file_info['name']} ({file_info['size']:,} bytes)")
            log_message(f"   📂 {file_info['path']}")
            
            # Open file
            try:
                os.startfile(file_info['path'])
                log_message(f"✅ Opened {file_info['name']}")
            except Exception as e:
                log_message(f"❌ Error opening: {e}")
    else:
        log_message("\n⚠️ No automatic download detected")
        log_message("Let's check browser downloads...")
        
        browser_check = nova.act("Press Ctrl+J to show downloads")
        log_message(f"Browser check: {browser_check}")

except Exception as e:
    log_message(f"❌ Error: {e}")

# Keep session alive
log_message("\n" + "="*60)
log_message("🔄 SESSION STAYING ALIVE")
log_message("Browser remains open for manual inspection")
log_message("Press Ctrl+C to stop when done")
log_message("="*60)

try:
    while True:
        time.sleep(30)
        
        # Check for new downloads
        current = check_downloads()
        very_new = [f for f in current if time.time() - f['modified'].timestamp() < 60]
        
        if very_new:
            for file_info in very_new:
                log_message(f"🆕 NEW: {file_info['name']}")
        
        log_message("🔄 Monitoring... Press Ctrl+C to stop")
        
except KeyboardInterrupt:
    log_message("\n🛑 Stopping...")
    nova.stop()
    log_message("✅ Done!")
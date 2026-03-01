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

print("🎯 SIMPLE DIRECT DOWNLOAD")
print("This will do the basic steps and monitor for downloads")

initial_downloads = check_downloads()
log_message(f"Starting with {len(initial_downloads)} recent files")

nova = NovaAct(
    starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
    headless=False,
    tty=False,
    nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
)

nova.start()

try:
    # Simple direct approach
    log_message("Executing direct download...")
    result = nova.act("Login with narang.sachin@gmail.com and Testing1234!1, select Active Home 103892 0, go to Usage, click Export")
    
    log_message("Waiting for download...")
    time.sleep(10)
    
    # Check for downloads
    current_downloads = check_downloads()
    new_files = [f for f in current_downloads if f not in initial_downloads]
    
    if new_files:
        log_message(f"✅ Found {len(new_files)} new file(s):")
        for file_info in new_files:
            log_message(f"📄 {file_info['name']} ({file_info['size']:,} bytes)")
            try:
                os.startfile(file_info['path'])
                log_message(f"✅ Opened {file_info['name']}")
            except:
                pass
    else:
        log_message("❌ No downloads detected")

except Exception as e:
    log_message(f"Error: {e}")

log_message("Session staying open - Press Ctrl+C to stop")
try:
    while True:
        time.sleep(60)
        log_message("Monitoring...")
except KeyboardInterrupt:
    nova.stop()
    log_message("Done!")
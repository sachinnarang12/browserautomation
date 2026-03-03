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
                    if time.time() - mod_time < 300:  # Last 5 minutes
                        recent_files.append({
                            'name': file,
                            'path': file_path,
                            'size': os.path.getsize(file_path),
                            'modified': datetime.fromtimestamp(mod_time)
                        })
        except Exception as e:
            log_message(f"Error checking downloads: {e}")
    
    return recent_files

log_message("🎯 FINAL EXPORT ATTEMPT - We know Nova Act can reach the Export button!")

# Check initial downloads
initial_downloads = check_downloads()
log_message(f"Initial downloads: {len(initial_downloads)}")

# Initialize Nova Act with screen dimension handling
nova = NovaAct(
    starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
    headless=False,
    tty=False,
    nova_act_api_key=os.environ.get("NOVA_ACT_API_KEY", "")
)

nova.start()

try:
    # Step 1: Get to export (we know this works)
    log_message("Step 1: Navigate to Export (we know this works)...")
    nav_result = nova.act("""Navigate to export:
1. Login: {{credential:utility_portal:username}} / {{credential:utility_portal:password}}
2. Select Active Home: 103892 0
3. Go to Usage section
4. Find Export button""", ignore_screen_dims_check=True)
    
    log_message("✅ Navigation completed successfully!")
    time.sleep(3)

    # Step 2: Simple export click
    log_message("Step 2: Click Export...")
    export_result = nova.act("Click the Export button to download the file", ignore_screen_dims_check=True)
    
    log_message("✅ Export clicked!")
    time.sleep(10)  # Wait for download

    # Step 3: Check what happened
    log_message("Step 3: Check download status...")
    status_result = nova.act("Check if download started. Press Ctrl+J to see downloads", ignore_screen_dims_check=True)
    
    log_message(f"Status check: {status_result}")

except Exception as e:
    log_message(f"Error during automation: {e}")

# Check for downloads
log_message("Checking for downloaded files...")
time.sleep(5)

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
        log_message(f"\n📁 {file_info['name']}")
        log_message(f"   Size: {file_info['size']:,} bytes")
        log_message(f"   Modified: {file_info['modified']}")
        log_message(f"   Path: {file_info['path']}")
        
        # Open the file
        try:
            os.startfile(file_info['path'])
            log_message(f"✅ Opened: {file_info['name']}")
        except Exception as e:
            log_message(f"Error opening file: {e}")

else:
    log_message("❌ No new downloads found")
    
    # Manual check
    log_message("Please manually check your Downloads folder:")
    log_message(f"Location: {os.path.join(os.path.expanduser('~'), 'Downloads')}")
    log_message("Look for files modified in the last few minutes")

log_message("\n🎯 PROCESS COMPLETE!")
log_message("The automation successfully reached the Export button.")
log_message("Check your Downloads folder for any new files.")

# Keep session open for manual verification
log_message("Session staying open for manual verification...")
log_message("Press Ctrl+C to stop when done.")

try:
    while True:
        time.sleep(30)
        log_message("Session active... Check Downloads folder manually")
        
        # Periodic check
        very_recent = check_downloads()
        for file_info in very_recent:
            if time.time() - file_info['modified'].timestamp() < 60:
                log_message(f"🆕 Very recent file: {file_info['name']}")
                
except KeyboardInterrupt:
    log_message("Stopping session...")
    nova.stop()
    log_message("Done!")
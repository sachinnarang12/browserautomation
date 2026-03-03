from nova_act import NovaAct
import os
import time
from datetime import datetime
import glob

def log_message(message):
    """Print timestamped log messages"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_downloads_folder(folder_path):
    """Check and list files in the downloads folder"""
    if os.path.exists(folder_path):
        files = os.listdir(folder_path)
        log_message(f"Files in {folder_path}: {files}")
        return files
    else:
        log_message(f"Folder {folder_path} does not exist")
        return []

# Create a specific download folder
download_folder = os.path.join(os.getcwd(), "nova_downloads")
os.makedirs(download_folder, exist_ok=True)
log_message(f"Created download folder: {download_folder}")

# Check initial state
initial_files = check_downloads_folder(download_folder)

log_message("Starting Nova Act automation with detailed monitoring...")

# Set browser download preferences to our specific folder
os.environ["NOVA_ACT_BROWSER_ARGS"] = f"--remote-debugging-port=9222 --download-directory={download_folder}"

# Initialize Nova Act
log_message("Initializing Nova Act...")
nova = NovaAct(
    starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
    headless=False,  # Set to False so we can see what's happening
    tty=False,
    nova_act_api_key=os.environ.get("NOVA_ACT_API_KEY", "")
)

log_message("Starting Nova Act session...")
nova.start()

# Step 1: Login
log_message("Step 1: Attempting login...")
login_result = nova.act("""Navigate to the login page and attempt to login using:
- Username: {{credential:utility_portal:username}}  
- Password: {{credential:utility_portal:password}}

If login fails, take a screenshot and describe what you see on the page. 
If login succeeds, confirm you are logged in and describe the page you see after login.""")

log_message(f"Login result: {login_result}")
check_downloads_folder(download_folder)

# Step 2: Navigate and select Active Home
log_message("Step 2: Looking for Active Home selector...")
home_result = nova.act("""Look for an "Active Home" dropdown or selector on the current page.
If found, click on it and select the option with value "103892 0".
Take a screenshot after selection to confirm it was applied.
If not found, describe what elements you can see on the page.""")

log_message(f"Active Home result: {home_result}")
check_downloads_folder(download_folder)

# Step 3: Find and click Export
log_message("Step 3: Click on More details, looking for Export button...")
export_result = nova.act("""Look for an "Export" button or link on the current page.
If found, click on it to start the download process.
Monitor for any download dialogs or file download indicators.
Take a screenshot after clicking export.""")

log_message(f"Export result: {export_result}")
check_downloads_folder(download_folder)

# Step 4: Wait and check for download
log_message("Step 4: Waiting for download to complete...")
time.sleep(10)  # Wait 10 seconds for download

download_result = nova.act("""Check if a file download has started or completed.
Look for download indicators in the browser.
If a download dialog appeared, make sure to save the file.
Take a final screenshot of the current state.""")

log_message(f"Download result: {download_result}")

# Final check
log_message("Final check of download folder...")
final_files = check_downloads_folder(download_folder)

# Compare initial and final files
new_files = set(final_files) - set(initial_files)
if new_files:
    log_message(f"New files downloaded: {list(new_files)}")
    for file in new_files:
        file_path = os.path.join(download_folder, file)
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            log_message(f"File: {file}, Size: {file_size} bytes")
else:
    log_message("No new files found in download folder")

# Also check default Downloads folder
log_message("Checking default Downloads folder...")
default_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
recent_files = []
try:
    for file in os.listdir(default_downloads):
        file_path = os.path.join(default_downloads, file)
        if os.path.isfile(file_path):
            mod_time = os.path.getmtime(file_path)
            if time.time() - mod_time < 3600:  # Files modified in last hour
                recent_files.append((file, datetime.fromtimestamp(mod_time)))
    
    if recent_files:
        log_message("Recent files in default Downloads:")
        for file, mod_time in recent_files:
            log_message(f"  - {file} (modified: {mod_time})")
    else:
        log_message("No recent files in default Downloads folder")
except Exception as e:
    log_message(f"Error checking default Downloads: {e}")

log_message("Automation completed. Keeping session open for manual inspection...")
log_message("Press Ctrl+C to stop the session when done.")

# Keep the session open for manual inspection
try:
    while True:
        time.sleep(30)
        log_message("Session still active... (Press Ctrl+C to stop)")
except KeyboardInterrupt:
    log_message("Stopping Nova Act session...")
    nova.stop()
    log_message("Session stopped.")
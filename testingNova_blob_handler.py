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

log_message("Starting Nova Act automation with blob download handling...")

# Initialize Nova Act
log_message("Initializing Nova Act...")
nova = NovaAct(
    starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
    headless=False,  # Keep visible to see what's happening
    tty=False,
    nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
)

log_message("Starting Nova Act session...")
nova.start()

# Step 1: Complete the full workflow to get to export
log_message("Step 1: Complete login and navigation...")
setup_result = nova.act("""Complete the following steps:
1. Login with username: narang.sachin@gmail.com and password: Testing1234!1
2. Find and select Active Home dropdown, choose "103892 0"
3. Navigate to the Usage section
4. Click the Export button and select Excel format

After clicking export, wait for any blob URL or download to appear.""")

log_message(f"Setup result: {setup_result}")

# Step 2: Handle the blob download
log_message("Step 2: Handling blob download...")
blob_result = nova.act("""Look for any blob URLs or download links that appeared after clicking export.
If you see a blob URL (starts with 'blob:'), do the following:
1. Right-click on the download link or blob URL
2. Select "Save link as..." or "Save as..."
3. Save the file with a descriptive name like "usage_export_103892.xlsx"
4. Choose the Downloads folder as the save location
5. Confirm the download

If no blob URL is visible, check the browser's download manager (Ctrl+J) for any pending downloads.""")

log_message(f"Blob handling result: {blob_result}")

# Step 3: Alternative approach - use JavaScript to download blob
log_message("Step 3: Using JavaScript to handle blob download...")
js_result = nova.act("""If the blob download didn't work with right-click, try this approach:
1. Open browser developer tools (F12)
2. Go to the Console tab
3. Look for any blob URLs in the Network tab or Console
4. If you find a blob URL, use JavaScript to download it:
   - Type this in console: 
     ```
     fetch('BLOB_URL_HERE')
       .then(response => response.blob())
       .then(blob => {
         const url = window.URL.createObjectURL(blob);
         const a = document.createElement('a');
         a.href = url;
         a.download = 'usage_export_103892.xlsx';
         document.body.appendChild(a);
         a.click();
         document.body.removeChild(a);
         window.URL.revokeObjectURL(url);
       });
     ```
   - Replace 'BLOB_URL_HERE' with the actual blob URL

Take a screenshot after attempting the download.""")

log_message(f"JavaScript result: {js_result}")

# Check for downloaded files
log_message("Checking for downloaded files...")
time.sleep(5)

# Check custom download folder
final_files = check_downloads_folder(download_folder)
new_files = set(final_files) - set(initial_files)

# Check default Downloads folder
default_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
log_message("Checking default Downloads folder for recent files...")

recent_files = []
try:
    for file in os.listdir(default_downloads):
        file_path = os.path.join(default_downloads, file)
        if os.path.isfile(file_path):
            mod_time = os.path.getmtime(file_path)
            if time.time() - mod_time < 1800:  # Files modified in last 30 minutes
                recent_files.append((file, datetime.fromtimestamp(mod_time)))
    
    if recent_files:
        log_message("Recent files in default Downloads (last 30 minutes):")
        for file, mod_time in recent_files:
            log_message(f"  - {file} (modified: {mod_time})")
    else:
        log_message("No recent files in default Downloads folder")
except Exception as e:
    log_message(f"Error checking default Downloads: {e}")

# Final instructions
log_message("=== MANUAL STEPS IF AUTOMATION DIDN'T WORK ===")
log_message("1. In the browser window, press Ctrl+J to open Downloads")
log_message("2. Look for any pending or failed downloads")
log_message("3. If you see the blob URL, copy it and paste here")
log_message("4. Try right-clicking on the Export button and 'Save link as'")
log_message("5. Check browser's Network tab (F12 -> Network) for the download request")

log_message("Session will remain open for manual inspection...")
log_message("Press Ctrl+C when done.")

# Keep session open
try:
    while True:
        time.sleep(60)
        log_message("Session still active... Check browser for downloads")
except KeyboardInterrupt:
    log_message("Stopping Nova Act session...")
    nova.stop()
    log_message("Session stopped.")
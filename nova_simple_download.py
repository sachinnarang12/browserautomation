from nova_act import NovaAct
import os
import time
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

log_message("Nova Act Simple Download - Focusing on Nova Act's download handling")

# The key insight: Nova Act might not handle downloads the same way a regular browser does
# Let's work WITH Nova Act's limitations, not against them

nova = NovaAct(
    starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
    headless=False,
    tty=False,
    nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
)

nova.start()

# Step 1: Get to the export page
log_message("Step 1: Navigate to export page...")
nav_result = nova.act("""Navigate to the export page:
1. Login with username: narang.sachin@gmail.com and password:Testing1234!12
2. Select Active Home dropdown and choose "103892 0". If LastPass Update password pops up,close that.
3. Navigate to the Usage section
4. Locate the Export button but DON'T click it yet
5. Take a screenshot showing the Export button is visible""")

log_message(f"Navigation: {nav_result}")

# Step 2: The key insight - let Nova Act tell us what happens when it clicks Export
log_message("Step 2: Let Nova Act describe what happens when clicking Export...")
click_result = nova.act("""Now I want you to click the Export button and describe EXACTLY what happens:

1. Click the Export button
2. Describe in detail what you observe:
   - Does a new tab open?
   - Does a download dialog appear?
   - Does the page change?
   - Do you see any URLs in the address bar?
   - Are there any error messages?
   - Do you see any loading indicators?

3. If a dropdown appears asking for format, select Excel/XLSX

4. Wait 10 seconds and describe what you see

5. Take a screenshot of the current state

Be very specific about what you observe - this will help us understand how Nova Act handles downloads.""")

log_message(f"Click result: {click_result}")

# Step 3: Based on what Nova Act observed, try to capture the download URL
log_message("Step 3: Trying to capture download information...")
capture_result = nova.act("""Based on what happened when you clicked Export, let's try to capture the download:

1. If you see a blob URL in the address bar, copy it and tell me what it is
2. If a new tab opened, switch to that tab and describe what you see
3. If nothing obvious happened, try right-clicking on the Export button and tell me what options you see
4. Check if there are any download notifications or indicators in the browser
5. Look at the browser's download area (usually bottom of browser or Ctrl+J)

Take a screenshot and describe everything you observe.""")

log_message(f"Capture result: {capture_result}")

# Step 4: Try Nova Act's approach to handling the download
log_message("Step 4: Working with Nova Act's download handling...")
download_result = nova.act("""Let's work with how Nova Act handles downloads:

1. If there's a blob URL visible, try to navigate to it directly
2. If there's a download in progress, wait for it to complete
3. If you can right-click and "Save as", do that
4. If none of the above work, try clicking Export again and immediately:
   - Press Ctrl+S to save the page
   - Or press Ctrl+J to open downloads
   - Or look for any browser notifications

5. Check the browser's Downloads folder by pressing Ctrl+J

Describe what happens with each attempt.""")

log_message(f"Download attempt: {download_result}")

# Step 5: Final verification
log_message("Step 5: Final verification...")
verify_result = nova.act("""Final verification steps:

1. Press Ctrl+J to open the browser's download manager
2. Look for any completed, in-progress, or failed downloads
3. If you see any downloads, describe their status and file names
4. Navigate to the Downloads folder in File Explorer (Windows key + E, then Downloads)
5. Look for any files that were created in the last few minutes
6. Take a screenshot of both the download manager and the Downloads folder

This will help us understand exactly how Nova Act is handling (or not handling) the download.""")

log_message(f"Verification: {verify_result}")

# Check local file system
log_message("Checking local file system for downloads...")
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
if os.path.exists(downloads_folder):
    recent_files = []
    for file in os.listdir(downloads_folder):
        file_path = os.path.join(downloads_folder, file)
        if os.path.isfile(file_path):
            mod_time = os.path.getmtime(file_path)
            if time.time() - mod_time < 600:  # Last 10 minutes
                size = os.path.getsize(file_path)
                recent_files.append((file, datetime.fromtimestamp(mod_time), size))
    
    if recent_files:
        log_message("Recent files found in Downloads:")
        for file, mod_time, size in recent_files:
            log_message(f"  📄 {file} - {mod_time} - {size:,} bytes")
    else:
        log_message("No recent files in Downloads folder")
else:
    log_message("Downloads folder not found")

log_message("Analysis complete. Key findings:")
log_message("1. How does Nova Act handle the Export button click?")
log_message("2. What type of download mechanism does the website use?")
log_message("3. Does Nova Act see download dialogs or blob URLs?")
log_message("4. Are there any browser-specific download behaviors?")

log_message("Session staying open for manual inspection. Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(30)
        log_message("Session active - analyze the findings above")
except KeyboardInterrupt:
    nova.stop()
    log_message("Session ended.")
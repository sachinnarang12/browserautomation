from nova_act import NovaAct
import os
import time
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_recent_downloads():
    """Check for recent downloads"""
    default_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    recent_files = []
    try:
        for file in os.listdir(default_downloads):
            file_path = os.path.join(default_downloads, file)
            if os.path.isfile(file_path):
                mod_time = os.path.getmtime(file_path)
                if time.time() - mod_time < 300:  # Last 5 minutes
                    recent_files.append((file, datetime.fromtimestamp(mod_time), os.path.getsize(file_path)))
        return recent_files
    except:
        return []

log_message("Starting MOST RELIABLE download method using Developer Tools Network tab")

# Initialize Nova Act
nova = NovaAct(
    starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
    headless=False,
    tty=False,
    nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
)

nova.start()

# Step 1: Complete login and navigation
log_message("Step 1: Login and navigate to export page...")
setup_result = nova.act("""Complete the full setup:
1. Login with username: narang.sachin@gmail.com and password: Testing1234!12
2. Select Active Home dropdown and choose "103892 0"
3. Navigate to the Usage section
4. Locate the Export button but DON'T click it yet

Take a screenshot when you're ready to export.""")

log_message(f"Setup completed: {setup_result}")

# Step 2: Open Developer Tools BEFORE clicking export
log_message("Step 2: Opening Developer Tools Network tab...")
devtools_result = nova.act("""Open Developer Tools and prepare for download capture:

1. Right-click anywhere on the page and select "Inspect" or "Inspect Element"
2. In the Developer Tools panel, click on the "Network" tab
3. Make sure the Network tab is recording (there should be a red record button or it should show network requests)
4. Clear any existing network requests by clicking the clear button (circle with line through it)
5. Keep the Developer Tools open and visible

Take a screenshot showing the Network tab is open and ready.""")

log_message(f"Developer Tools opened: {devtools_result}")

# Step 3: Click Export and monitor Network tab
log_message("Step 3: Clicking Export and monitoring Network requests...")
export_result = nova.act("""Now click Export and monitor the Network tab:

1. Click the "Export" button
2. If a dropdown appears, select "Excel" or "XLSX" format
3. Watch the Network tab for new requests that appear
4. Look for requests that might be the file download (often with .xlsx extension or containing "export" in the name)
5. You should see new network requests appear in the Network tab

Take a screenshot showing the Network requests that appeared after clicking Export.""")

log_message(f"Export clicked: {export_result}")

# Step 4: Download from Network tab
log_message("Step 4: Downloading file from Network tab...")
download_result = nova.act("""Download the file from the Network tab:

1. In the Network tab, look for the request that represents your export file
   - It might be named something like "export.xlsx", "usage.xlsx", or have a blob URL
   - Look for requests with response type "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or similar
   - The size should be reasonable for a data export (not 0 bytes)

2. Right-click on the correct network request
3. Select "Save as..." or "Save response as..." from the context menu
4. Choose your Downloads folder as the save location
5. Name the file "usage_export_103892.xlsx"
6. Click Save

Take a screenshot showing the successful download dialog or confirmation.""")

log_message(f"Download attempted: {download_result}")

# Step 5: Verify the download
log_message("Step 5: Verifying download success...")
time.sleep(5)

verify_result = nova.act("""Verify the download was successful:

1. Open File Explorer or press Windows key + E
2. Navigate to your Downloads folder
3. Look for the file you just saved (usage_export_103892.xlsx or similar)
4. Check the file size - it should be more than 0 bytes
5. Try to open the file to confirm it contains the usage data

Take a screenshot showing the downloaded file in your Downloads folder.""")

log_message(f"Verification: {verify_result}")

# Final check
log_message("Final check for downloaded files...")
final_downloads = check_recent_downloads()

if final_downloads:
    log_message("SUCCESS! Recent downloads found:")
    for file, mod_time, size in final_downloads:
        log_message(f"  ✅ {file}")
        log_message(f"     Modified: {mod_time}")
        log_message(f"     Size: {size:,} bytes")
        
        if any(keyword in file.lower() for keyword in ['export', 'usage', '103892', '.xlsx']):
            log_message(f"     🎯 This appears to be your usage export file!")
            log_message(f"     📁 Location: {os.path.join(os.path.expanduser('~'), 'Downloads', file)}")
else:
    log_message("❌ No recent downloads detected.")
    log_message("Please check the Network tab method manually or try the alternative approach below.")
    
    # Alternative if Network tab method didn't work
    alt_result = nova.act("""Alternative approach if Network tab didn't work:

    1. Go back to the export page
    2. Right-click directly on the "Export" button (not just anywhere on the page)
    3. If you see "Save link as..." in the context menu, click it
    4. Save the file to your Downloads folder
    
    If that doesn't work either:
    1. Click Export normally
    2. When the blob URL appears in the address bar, copy it
    3. Open a new tab
    4. Paste the blob URL and press Enter immediately
    
    Take a screenshot of any results.""")
    
    log_message(f"Alternative method: {alt_result}")

log_message("Process completed. Session will remain open for manual verification.")
log_message("Press Ctrl+C to stop when you've confirmed the download.")

try:
    while True:
        time.sleep(30)
        log_message("Session active... Check your Downloads folder")
        
        # Check for very recent downloads
        current_downloads = check_recent_downloads()
        for file, mod_time, size in current_downloads:
            if time.time() - mod_time.timestamp() < 60:
                log_message(f"🆕 Very recent download: {file} ({size:,} bytes)")
                
except KeyboardInterrupt:
    log_message("Stopping session...")
    nova.stop()
    log_message("Done!")
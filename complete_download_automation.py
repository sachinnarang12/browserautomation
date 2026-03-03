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

def check_recent_downloads():
    """Check for recent downloads in default Downloads folder"""
    default_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    recent_files = []
    try:
        for file in os.listdir(default_downloads):
            file_path = os.path.join(default_downloads, file)
            if os.path.isfile(file_path):
                mod_time = os.path.getmtime(file_path)
                if time.time() - mod_time < 600:  # Files modified in last 10 minutes
                    recent_files.append((file, datetime.fromtimestamp(mod_time), os.path.getsize(file_path)))
        return recent_files
    except Exception as e:
        log_message(f"Error checking downloads: {e}")
        return []

# Create a specific download folder
download_folder = os.path.join(os.getcwd(), "nova_downloads")
os.makedirs(download_folder, exist_ok=True)
log_message(f"Created download folder: {download_folder}")

# Check initial state
initial_files = check_downloads_folder(download_folder)
initial_downloads = check_recent_downloads()

log_message("Starting complete automation: Login → Navigate → Export → Download")

try:
    # Initialize Nova Act with better download handling
    log_message("Initializing Nova Act...")
    nova = NovaAct(
        starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
        headless=False,  # Keep visible for monitoring
        tty=False,
        nova_act_api_key=os.environ.get("NOVA_ACT_API_KEY", "")
    )

    log_message("Starting Nova Act session...")
    nova.start()

    # Step 1: Complete Login Process
    log_message("Step 1: Logging in...")
    login_result = nova.act("""Complete the login process:
    1. Enter username: {{credential:utility_portal:username}}
    2. Enter password: {{credential:utility_portal:password}}
    3. Click login/submit button
    4. Wait for the dashboard to load
    5. Confirm successful login by checking if you see account information
    
    Take a screenshot after successful login.""")
    
    log_message(f"Login completed: {login_result}")
    time.sleep(3)

    # Step 2: Select Active Home
    log_message("Step 2: Selecting Active Home...")
    home_result = nova.act("""Find and select the Active Home:
    1. Look for "Active Home" dropdown (usually shows account number)
    2. Click on the dropdown arrow
    3. Select the option "103892 0" or "103892 - Active"
    4. Confirm the selection is applied
    
    Take a screenshot after selection.""")
    
    log_message(f"Active Home selected: {home_result}")
    time.sleep(3)

    # Step 3: Navigate to Usage/Export Section
    log_message("Step 3: Navigating to Usage section...")
    usage_result = nova.act("""Navigate to the Usage section:
    1. Look for "Usage" tab, menu item, or link
    2. Click on it to go to the usage page
    3. Wait for the usage data to load
    4. Look for an "Export" button or option
    
    Take a screenshot when you reach the usage page.""")
    
    log_message(f"Usage navigation: {usage_result}")
    time.sleep(3)

    # Step 4: Export with Enhanced Download Handling
    log_message("Step 4: Exporting data with download handling...")
    export_result = nova.act("""Export the data and handle the download:
    1. Click the "Export" button
    2. If a dropdown appears, select "Excel" or "XLSX" format
    3. Wait for the export to process
    4. If a blob URL appears or download starts, handle it by:
       - Right-clicking on any download link and selecting "Save as"
       - Or if a blob URL appears in the address bar, press Enter to download
       - Or if a download dialog appears, click "Save" or "Download"
    5. Monitor for any download notifications in the browser
    
    Take a screenshot showing the export process.""")
    
    log_message(f"Export initiated: {export_result}")
    time.sleep(5)

    # Step 5: Handle Blob URL Download
    log_message("Step 5: Handling blob URL download...")
    blob_result = nova.act("""Handle the blob URL download:
    1. Look for any blob URLs that start with "blob:https://livingstonnj.my360-app.com/"
    2. If you see a blob URL, try these methods in order:
       a) Right-click on the download link → "Save link as" → Save to Downloads
       b) Copy the blob URL and paste it in the address bar, then press Enter
       c) Open browser console (right-click → Inspect → Console) and run:
          fetch('BLOB_URL_HERE').then(r=>r.blob()).then(b=>{let u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download='usage_export.xlsx';a.click();URL.revokeObjectURL(u);});
    3. Check browser downloads (Ctrl+J) for any pending downloads
    4. Confirm the file is saved to Downloads folder
    
    Take a screenshot showing the download completion.""")
    
    log_message(f"Blob download handled: {blob_result}")
    time.sleep(10)

    # Step 6: Verify Download Success
    log_message("Step 6: Verifying download...")
    verify_result = nova.act("""Verify the download was successful:
    1. Press Ctrl+J to open browser downloads
    2. Check if the export file appears in the downloads list
    3. If the file is there, click on it to open or show in folder
    4. Take a screenshot of the downloads page showing the successful download
    
    If no download is visible, try the export process again.""")
    
    log_message(f"Download verification: {verify_result}")

    # Final check for downloaded files
    log_message("Final check for downloaded files...")
    time.sleep(5)
    
    final_downloads = check_recent_downloads()
    new_downloads = []
    
    for file, mod_time, size in final_downloads:
        is_new = True
        for old_file, old_time, old_size in initial_downloads:
            if file == old_file and mod_time == old_time:
                is_new = False
                break
        if is_new:
            new_downloads.append((file, mod_time, size))
    
    if new_downloads:
        log_message("SUCCESS! New files downloaded:")
        for file, mod_time, size in new_downloads:
            log_message(f"  ✅ {file}")
            log_message(f"     Modified: {mod_time}")
            log_message(f"     Size: {size:,} bytes")
            
            # Check if it's likely our export file
            if any(keyword in file.lower() for keyword in ['export', 'usage', '103892', '.xlsx', '.xls']):
                log_message(f"     🎯 This appears to be the usage export file!")
    else:
        log_message("❌ No new downloads detected.")
        log_message("The blob URL may have expired or the download failed.")
        
        # Try one more time with a different approach
        log_message("Attempting alternative download method...")
        alt_result = nova.act("""Try alternative download approach:
        1. Go back to the export page
        2. Click Export again
        3. When the blob URL appears, immediately:
           - Copy the entire blob URL
           - Open a new tab
           - Paste the blob URL in the address bar
           - Press Enter immediately
        4. If that doesn't work, try right-clicking the export button and "Save link as"
        
        Take a screenshot of any results.""")
        
        log_message(f"Alternative method: {alt_result}")
        time.sleep(10)
        
        # Check one more time
        final_final_downloads = check_recent_downloads()
        newest_downloads = []
        for file, mod_time, size in final_final_downloads:
            is_newest = True
            for old_file, old_time, old_size in final_downloads:
                if file == old_file and mod_time == old_time:
                    is_newest = False
                    break
            if is_newest:
                newest_downloads.append((file, mod_time, size))
        
        if newest_downloads:
            log_message("SUCCESS on second attempt!")
            for file, mod_time, size in newest_downloads:
                log_message(f"  ✅ {file} ({size:,} bytes)")

    log_message("Automation completed. Session will remain open for manual inspection.")
    log_message("Press Ctrl+C to stop when you're done reviewing.")

    # Keep session open for manual inspection
    try:
        while True:
            time.sleep(60)
            log_message("Session active... Press Ctrl+C to stop")
            
            # Periodic check for new downloads
            current_downloads = check_recent_downloads()
            for file, mod_time, size in current_downloads:
                if time.time() - mod_time.timestamp() < 60:  # Very recent
                    log_message(f"🆕 New download detected: {file}")
                    
    except KeyboardInterrupt:
        log_message("Stopping Nova Act session...")
        nova.stop()
        log_message("Session stopped.")

except Exception as e:
    log_message(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()
    if 'nova' in locals():
        try:
            nova.stop()
        except:
            pass

log_message("Script completed.")
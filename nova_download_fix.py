from nova_act import NovaAct
import os
import time
from datetime import datetime
import json

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def setup_download_folder():
    """Create and configure download folder"""
    download_folder = os.path.join(os.getcwd(), "nova_downloads")
    os.makedirs(download_folder, exist_ok=True)
    log_message(f"Download folder: {download_folder}")
    return download_folder

log_message("Nova Act Download Fix - Addressing download handling issues")

download_folder = setup_download_folder()

# Configure Nova Act with proper download settings
log_message("Configuring Nova Act with download preferences...")

# Create browser preferences for downloads
browser_prefs = {
    "download.default_directory": download_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": False,
    "profile.default_content_settings.popups": 0,
    "profile.default_content_setting_values.automatic_downloads": 1
}

# Set Chrome arguments for downloads
chrome_args = [
    f"--download-directory={download_folder}",
    "--disable-popup-blocking",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--allow-running-insecure-content",
    "--disable-web-security",
    "--disable-features=VizDisplayCompositor"
]

log_message("Starting Nova Act with download-optimized configuration...")

nova = NovaAct(
    starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
    headless=False,
    tty=False,
    nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
)

nova.start()

# Step 1: Complete login and navigation
log_message("Step 1: Login and navigate to export...")
setup_result = nova.act("""Complete the login and navigation:
1. Login with username: narang.sachin@gmail.com and password: Testing1234!1
2. Select Active Home dropdown and choose "103892 0"
3. Navigate to the Usage section
4. Take a screenshot when you can see the Export button""")

log_message(f"Setup: {setup_result}")

# Step 2: Configure browser for downloads BEFORE clicking export
log_message("Step 2: Configuring browser download behavior...")
config_result = nova.act(f"""Before clicking export, configure the browser for automatic downloads:

1. Press F12 to open Developer Tools
2. Go to Console tab
3. Execute this JavaScript code to configure downloads:

navigator.serviceWorker.register('data:application/javascript,self.addEventListener("message", function(e) {{ if (e.data.type === "DOWNLOAD") {{ fetch(e.data.url).then(r => r.blob()).then(blob => {{ const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = e.data.filename || "export.xlsx"; a.click(); }}); }} }});');

4. Also execute this to handle blob URLs:
window.downloadBlob = function(url, filename) {{
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || 'export.xlsx';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}};

5. Take a screenshot showing the console is ready""")

log_message(f"Browser config: {config_result}")

# Step 3: Click export with download monitoring
log_message("Step 3: Clicking export with download monitoring...")
export_result = nova.act("""Now click the Export button and monitor for downloads:

1. Click the Export button
2. If a dropdown appears, select Excel/XLSX format
3. Immediately after clicking, execute this in the console to catch any blob URLs:

// Monitor for blob URLs and auto-download them
const originalCreateObjectURL = URL.createObjectURL;
URL.createObjectURL = function(blob) {
    const url = originalCreateObjectURL.call(this, blob);
    console.log('Blob URL created:', url);
    
    // Auto-download the blob
    const a = document.createElement('a');
    a.href = url;
    a.download = 'usage_export_103892.xlsx';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    return url;
};

4. Watch for any download indicators or file save dialogs
5. Take a screenshot of the result""")

log_message(f"Export clicked: {export_result}")

# Step 4: Alternative approach if blob monitoring didn't work
log_message("Step 4: Alternative download approach...")
alt_result = nova.act("""If the automatic download didn't work, try this alternative:

1. Look at the browser's address bar - if there's a blob URL, copy it
2. Open a new tab
3. Paste the blob URL and press Enter immediately
4. If that doesn't work, go back to the export page
5. Right-click on the Export button and look for "Save link as" or similar
6. Try clicking Export again and immediately press Ctrl+S to save the page

Take a screenshot of any download dialogs or results""")

log_message(f"Alternative approach: {alt_result}")

# Step 5: Check for downloads
log_message("Step 5: Checking for downloaded files...")
time.sleep(5)

# Check our download folder
download_files = []
if os.path.exists(download_folder):
    download_files = [f for f in os.listdir(download_folder) if os.path.isfile(os.path.join(download_folder, f))]

# Check default Downloads
default_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
recent_files = []
try:
    for file in os.listdir(default_downloads):
        file_path = os.path.join(default_downloads, file)
        if os.path.isfile(file_path):
            mod_time = os.path.getmtime(file_path)
            if time.time() - mod_time < 300:  # Last 5 minutes
                file_size = os.path.getsize(file_path)
                recent_files.append((file, datetime.fromtimestamp(mod_time), file_size))
except:
    pass

if download_files:
    log_message("✅ Files found in nova_downloads folder:")
    for file in download_files:
        file_path = os.path.join(download_folder, file)
        size = os.path.getsize(file_path)
        log_message(f"  📄 {file} ({size:,} bytes)")

if recent_files:
    log_message("✅ Recent files in Downloads folder:")
    for file, mod_time, size in recent_files:
        log_message(f"  📄 {file}")
        log_message(f"     ⏰ {mod_time}")
        log_message(f"     📊 {size:,} bytes")

if not download_files and not recent_files:
    log_message("❌ No downloads detected. Let's try one more approach...")
    
    final_result = nova.act("""Final attempt - manual download trigger:
    
    1. Go back to the export page if needed
    2. Open browser downloads (Ctrl+J)
    3. Click Export button
    4. If you see any pending downloads in the downloads panel, click on them
    5. Look for any notification bars at the bottom of the browser
    6. Try pressing Ctrl+Shift+Delete to clear cache, then try export again
    
    Take a screenshot of the downloads panel and any results""")
    
    log_message(f"Final attempt: {final_result}")

log_message("Process completed. Session staying open for manual verification.")
log_message("Check both folders:")
log_message(f"  1. Nova downloads: {download_folder}")
log_message(f"  2. Default Downloads: {default_downloads}")
log_message("Press Ctrl+C when done.")

try:
    while True:
        time.sleep(60)
        log_message("Session active - verify downloads manually")
except KeyboardInterrupt:
    nova.stop()
    log_message("Session ended.")
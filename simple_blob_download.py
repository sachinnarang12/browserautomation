from nova_act import NovaAct
import os
import time
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

log_message("Creating Nova Act session to handle blob download...")

nova = NovaAct(
    starting_page="https://livingstonnj.my360-app.com",
    headless=False,
    tty=False,
    nova_act_api_key=os.environ.get("NOVA_ACT_API_KEY", "")
)

nova.start()

blob_url = "blob:https://livingstonnj.my360-app.com/d8c2e906-58da-45d3-9181-4cc6d853d659"

log_message("Attempting to download blob URL...")

result = nova.act(f"""Navigate to this blob URL directly by typing it in the address bar: {blob_url}

If that doesn't work, try these steps:
1. Right-click anywhere on the page and select "Inspect" or "Inspect Element"
2. Click on the "Console" tab in the developer tools
3. Type or paste this JavaScript code:

fetch('{blob_url}').then(response => response.blob()).then(blob => {{
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'usage_export_103892.xlsx';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
}});

4. Press Enter to execute the code

Take a screenshot showing the result.""")

log_message(f"Result: {result}")

log_message("Checking Downloads folder...")
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

try:
    files = os.listdir(downloads_folder)
    recent_files = []
    for file in files:
        file_path = os.path.join(downloads_folder, file)
        if os.path.isfile(file_path):
            mod_time = os.path.getmtime(file_path)
            if time.time() - mod_time < 300:  # Last 5 minutes
                recent_files.append((file, datetime.fromtimestamp(mod_time)))
    
    if recent_files:
        log_message("Recent files found in Downloads:")
        for file, mod_time in recent_files:
            log_message(f"  - {file} (modified: {mod_time})")
    else:
        log_message("No recent files found")
        
except Exception as e:
    log_message(f"Error checking downloads: {e}")

log_message("Session complete. Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(30)
        log_message("Monitoring... Press Ctrl+C to stop")
except KeyboardInterrupt:
    nova.stop()
    log_message("Done!")
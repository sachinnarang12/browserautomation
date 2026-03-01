from nova_act import NovaAct
import os
import time
from datetime import datetime

def log_message(message):
    """Print timestamped log messages"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

# Create download folder
download_folder = os.path.join(os.getcwd(), "nova_downloads")
os.makedirs(download_folder, exist_ok=True)

log_message("Connecting to existing Nova Act session to handle blob download...")

# Since you already have a session running, let's create a new one to handle the blob
nova = NovaAct(
    starting_page="https://livingstonnj.my360-app.com",
    headless=False,
    tty=False,
    nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
)

nova.start()

log_message("Handling blob URL download...")

# Use JavaScript to download the blob URL
blob_url = "blob:https://livingstonnj.my360-app.com/d8c2e906-58da-45d3-9181-4cc6d853d659"

result = nova.act(f"""Navigate to the page where the blob URL was generated, then execute this JavaScript code in the browser console:

1. Press F12 to open Developer Tools
2. Go to the Console tab
3. Paste and execute this code:

```javascript
// Download blob URL
fetch('{blob_url}')
  .then(response => response.blob())
  .then(blob => {{
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'usage_export_103892_' + new Date().getTime() + '.xlsx';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    console.log('Download initiated');
  }})
  .catch(error => console.error('Download failed:', error));
```

After running this code, check your Downloads folder for the file.
Take a screenshot showing the console output.""")

log_message(f"Blob download result: {result}")

# Alternative approach - direct navigation to blob URL
log_message("Trying direct navigation to blob URL...")

direct_result = nova.act(f"""Try navigating directly to the blob URL: {blob_url}

If that doesn't work, try this alternative JavaScript approach:

```javascript
// Alternative download method
const link = document.createElement('a');
link.href = '{blob_url}';
link.download = 'usage_export_103892.xlsx';
link.style.display = 'none';
document.body.appendChild(link);
link.click();
document.body.removeChild(link);
```

Or try opening the blob URL in a new tab:
```javascript
window.open('{blob_url}', '_blank');
```

Take a screenshot of any results.""")

log_message(f"Direct navigation result: {direct_result}")

log_message("Session will remain open. Check your Downloads folder and press Ctrl+C when done.")

try:
    while True:
        time.sleep(30)
        # Check for new files
        if os.path.exists(download_folder):
            files = os.listdir(download_folder)
            if files:
                log_message(f"Files found in download folder: {files}")
        
        # Check default downloads
        default_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
        recent_files = []
        try:
            for file in os.listdir(default_downloads):
                file_path = os.path.join(default_downloads, file)
                if os.path.isfile(file_path):
                    mod_time = os.path.getmtime(file_path)
                    if time.time() - mod_time < 300:  # Last 5 minutes
                        recent_files.append((file, datetime.fromtimestamp(mod_time)))
            
            if recent_files:
                log_message("Recent downloads found:")
                for file, mod_time in recent_files:
                    log_message(f"  - {file} (modified: {mod_time})")
        except:
            pass
            
        log_message("Still monitoring... Press Ctrl+C to stop")
        
except KeyboardInterrupt:
    log_message("Stopping session...")
    nova.stop()
    log_message("Done!")
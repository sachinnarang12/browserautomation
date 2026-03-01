from nova_act import NovaAct
import os
import time
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_downloads():
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    recent_files = []
    try:
        for file in os.listdir(downloads_folder):
            file_path = os.path.join(downloads_folder, file)
            if os.path.isfile(file_path):
                mod_time = os.path.getmtime(file_path)
                if time.time() - mod_time < 300:  # Last 5 minutes
                    recent_files.append((file, datetime.fromtimestamp(mod_time)))
        return recent_files
    except:
        return []

log_message("Starting automated blob download...")

# Create Nova Act session
nova = NovaAct(
    starting_page="https://livingstonnj.my360-app.com",
    headless=False,
    tty=False,
    nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
)

nova.start()

blob_url = "blob:https://livingstonnj.my360-app.com/d8c2e906-58da-45d3-9181-4cc6d853d659"

log_message("Step 1: Opening Developer Tools and executing JavaScript...")

result1 = nova.act(f"""I need to download a blob URL. Please do the following:

1. Right-click anywhere on the page
2. Select "Inspect" or "Inspect Element" from the menu
3. In the Developer Tools that open, click on the "Console" tab
4. In the console, type this exact JavaScript code:

fetch('{blob_url}').then(response => response.blob()).then(blob => {{
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'usage_export_' + Date.now() + '.xlsx';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
  console.log('Download initiated');
}});

5. Press Enter to execute the code
6. Take a screenshot showing the console output""")

log_message(f"JavaScript execution result: {result1}")

# Check for downloads
time.sleep(5)
recent_files = check_downloads()
if recent_files:
    log_message("SUCCESS! Files downloaded:")
    for file, mod_time in recent_files:
        log_message(f"  - {file} (modified: {mod_time})")
else:
    log_message("No new downloads detected. Trying alternative method...")
    
    # Alternative method - direct navigation
    result2 = nova.act(f"""The JavaScript method may not have worked. Try this alternative:

    1. Click in the browser address bar (where the URL is shown)
    2. Select all text (Ctrl+A) and delete it
    3. Type or paste this blob URL: {blob_url}
    4. Press Enter
    
    This should trigger a direct download. Take a screenshot of what happens.""")
    
    log_message(f"Direct navigation result: {result2}")
    
    # Check again
    time.sleep(5)
    recent_files = check_downloads()
    if recent_files:
        log_message("SUCCESS! Files downloaded:")
        for file, mod_time in recent_files:
            log_message(f"  - {file} (modified: {mod_time})")
    else:
        log_message("Still no downloads. Trying final method...")
        
        # Final method - keyboard shortcuts
        result3 = nova.act(f"""Let's try using keyboard shortcuts to open Developer Tools:

        1. Press Ctrl+Shift+I (this should open Developer Tools)
        2. If that doesn't work, try Ctrl+Shift+J (opens Console directly)
        3. Once the Console is open, paste this code:
        
        fetch('{blob_url}').then(r=>r.blob()).then(b=>{{let u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download='export.xlsx';a.click();URL.revokeObjectURL(u);}});
        
        4. Press Enter
        5. Take a screenshot of the result""")
        
        log_message(f"Keyboard shortcut result: {result3}")

# Final check
time.sleep(10)
final_files = check_downloads()
if final_files:
    log_message("FINAL CHECK - Files found:")
    for file, mod_time in final_files:
        log_message(f"  - {file} (modified: {mod_time})")
        file_path = os.path.join(os.path.expanduser("~"), "Downloads", file)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            log_message(f"    Size: {size} bytes")
else:
    log_message("No downloads found. The blob URL may have expired.")
    log_message("You may need to go back to the website and generate a new export.")

log_message("Process complete. Keeping session open for 2 minutes for manual inspection...")

# Keep session open briefly
for i in range(4):
    time.sleep(30)
    log_message(f"Session active... {4-i} checks remaining")
    recent = check_downloads()
    if recent:
        log_message("New downloads detected!")
        for file, mod_time in recent:
            log_message(f"  - {file}")

nova.stop()
log_message("Session ended.")
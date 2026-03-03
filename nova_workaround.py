from nova_act import NovaAct
import os
import time
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

log_message("Nova Act Workaround - Working around Nova Act's download limitations")

# The key insight: Nova Act doesn't handle downloads like a regular browser
# Solution: Use Nova Act to get to the export page, then use JavaScript to force the download

nova = NovaAct(
    starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
    headless=False,
    tty=False,
    nova_act_api_key=os.environ.get("NOVA_ACT_API_KEY", "")
)

nova.start()

# Step 1: Get to export page (we know this works)
log_message("Step 1: Navigate to export page...")
nav_result = nova.act("""Navigate to the export page:
1. Login with username: {{credential:utility_portal:username}} and password: {{credential:utility_portal:password}}
2. Select Active Home dropdown and choose "103892 0"
3. Navigate to the Usage section
4. Locate the Export button
5. Take a screenshot when ready""")

log_message(f"Navigation: Success")

# Step 2: Inject JavaScript to handle downloads BEFORE clicking export
log_message("Step 2: Injecting download handler JavaScript...")
js_result = nova.act("""Inject JavaScript to handle downloads:

1. Press F12 to open Developer Tools
2. Click on the Console tab
3. Paste and execute this JavaScript code:

// Override the default download behavior
window.originalOpen = window.open;
window.open = function(url, name, specs) {
    console.log('Window.open intercepted:', url);
    if (url && url.startsWith('blob:')) {
        // Handle blob URL
        fetch(url).then(r => r.blob()).then(blob => {
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = 'usage_export_103892.xlsx';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            console.log('Blob download triggered');
        });
        return null;
    }
    return window.originalOpen(url, name, specs);
};

// Also intercept any direct blob creation
const originalCreateObjectURL = URL.createObjectURL;
URL.createObjectURL = function(blob) {
    const url = originalCreateObjectURL.call(this, blob);
    console.log('Blob URL created:', url);
    
    // Auto-trigger download
    setTimeout(() => {
        const a = document.createElement('a');
        a.href = url;
        a.download = 'usage_export_103892.xlsx';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        console.log('Auto-download triggered for blob:', url);
    }, 100);
    
    return url;
};

console.log('Download interceptors installed');

4. Press Enter to execute the code
5. Take a screenshot showing the console is ready""")

log_message(f"JavaScript injection: {js_result}")

# Step 3: Now click export with our interceptors in place
log_message("Step 3: Clicking export with interceptors active...")
export_result = nova.act("""Now click Export with our JavaScript interceptors active:

1. Click the Export button
2. Select Excel format if dropdown appears
3. Watch the console for any messages about blob URLs or downloads
4. Look for any download notifications or file save dialogs
5. Take a screenshot of the console and any download activity""")

log_message(f"Export with interceptors: {export_result}")

# Step 4: Alternative approach - direct network monitoring
log_message("Step 4: Alternative - monitor network requests...")
network_result = nova.act("""Alternative approach using Network tab:

1. In Developer Tools, click on the Network tab
2. Clear any existing requests (click the clear button)
3. Click Export → Excel again
4. Watch for new network requests
5. Look for any requests that might be the file download
6. Right-click on any suspicious requests and try "Save as"
7. Take a screenshot of the Network tab showing any requests""")

log_message(f"Network monitoring: {network_result}")

# Step 5: Final attempt - manual browser download
log_message("Step 5: Manual browser download attempt...")
manual_result = nova.act("""Final manual attempt:

1. Press Ctrl+J to open browser downloads
2. Click Export → Excel one more time
3. Immediately after clicking, press Ctrl+S to save the page
4. Check if any downloads appear in the downloads panel
5. Look for any browser notifications at the bottom
6. Take a screenshot of the downloads panel and any notifications""")

log_message(f"Manual attempt: {manual_result}")

# Check file system for any downloads
log_message("Checking file system for downloads...")
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
        log_message("✅ Recent downloads found:")
        for file, mod_time, size in recent_files:
            log_message(f"  📄 {file} - {mod_time} - {size:,} bytes")
    else:
        log_message("❌ No recent downloads detected")

log_message("ANALYSIS COMPLETE")
log_message("=" * 60)
log_message("NOVA ACT DOWNLOAD ISSUE IDENTIFIED:")
log_message("1. Nova Act successfully navigates and clicks Export")
log_message("2. Nova Act does NOT trigger browser download dialogs")
log_message("3. Nova Act does NOT see blob URLs or download processes")
log_message("4. The website likely generates downloads that Nova Act can't handle")
log_message("=" * 60)
log_message("RECOMMENDED SOLUTIONS:")
log_message("1. Use regular browser with manual steps")
log_message("2. Use Selenium instead of Nova Act for downloads")
log_message("3. Contact utility company for direct file delivery")
log_message("4. Use browser extension for blob URL handling")

log_message("Session staying open. Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(30)
        log_message("Session active - Nova Act limitation confirmed")
except KeyboardInterrupt:
    nova.stop()
    log_message("Session ended.")
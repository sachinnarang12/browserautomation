import requests
import os
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

# The blob URL you provided
blob_url = "blob:https://livingstonnj.my360-app.com/d8c2e906-58da-45d3-9181-4cc6d853d659"

log_message("Attempting to download blob URL directly...")

# Create downloads folder
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
local_folder = os.path.join(os.getcwd(), "nova_downloads")
os.makedirs(local_folder, exist_ok=True)

log_message(f"Downloads will be saved to: {downloads_folder}")
log_message(f"Local folder: {local_folder}")

# Unfortunately, blob URLs can't be accessed directly via requests
# They only exist in the browser context where they were created
log_message("ERROR: Blob URLs cannot be downloaded directly via Python requests")
log_message("They only exist in the browser session where they were created")

log_message("SOLUTION: We need to use the browser where the blob was created")

# Let's create a simple HTML file that can handle the download
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Blob Downloader</title>
</head>
<body>
    <h1>Blob URL Downloader</h1>
    <p>Blob URL: <code>{blob_url}</code></p>
    <button onclick="downloadBlob()">Download File</button>
    <div id="status"></div>
    
    <script>
    function downloadBlob() {{
        const status = document.getElementById('status');
        status.innerHTML = 'Attempting download...';
        
        fetch('{blob_url}')
            .then(response => {{
                if (!response.ok) {{
                    throw new Error('Network response was not ok');
                }}
                return response.blob();
            }})
            .then(blob => {{
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'usage_export_103892_' + Date.now() + '.xlsx';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                status.innerHTML = 'Download initiated! Check your Downloads folder.';
            }})
            .catch(error => {{
                console.error('Error:', error);
                status.innerHTML = 'Error: ' + error.message + '. The blob URL may have expired.';
            }});
    }}
    
    // Auto-trigger download when page loads
    window.onload = function() {{
        setTimeout(downloadBlob, 1000);
    }};
    </script>
</body>
</html>
"""

# Save HTML file
html_file = os.path.join(local_folder, "blob_downloader.html")
with open(html_file, 'w') as f:
    f.write(html_content)

log_message(f"Created HTML downloader: {html_file}")
log_message("INSTRUCTIONS:")
log_message("1. Open this HTML file in the SAME browser where you have the Nova Act session")
log_message("2. The download should start automatically")
log_message("3. If not, click the 'Download File' button")

# Also create a simple JavaScript file
js_content = f"""
// Paste this in the browser console where the blob URL was created
fetch('{blob_url}')
    .then(response => response.blob())
    .then(blob => {{
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'usage_export_103892.xlsx';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        console.log('Download completed!');
    }})
    .catch(error => console.error('Download failed:', error));
"""

js_file = os.path.join(local_folder, "download_script.js")
with open(js_file, 'w') as f:
    f.write(js_content)

log_message(f"Created JavaScript file: {js_file}")
log_message("You can also copy the contents of this file and paste it in the browser console")

print("\n" + "="*60)
print("NEXT STEPS:")
print("="*60)
print(f"1. Open this file in your browser: {html_file}")
print("2. Make sure you open it in the SAME browser where Nova Act is running")
print("3. The download should start automatically")
print("4. Check your Downloads folder for the file")
print("="*60)
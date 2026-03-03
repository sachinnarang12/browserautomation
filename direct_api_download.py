import requests
import os
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

# Create session to maintain cookies
session = requests.Session()

# Set headers to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

session.headers.update(headers)

log_message("Attempting to access the login page...")

try:
    # Step 1: Get login page
    login_url = "https://identity.my360-app.com/Account/Login"
    response = session.get(login_url)
    log_message(f"Login page status: {response.status_code}")
    
    # Step 2: Extract form data (you'd need to parse the HTML for hidden fields)
    # This is a simplified version - you'd need to extract CSRF tokens, etc.
    login_data = {
        'Email': '{{credential:utility_portal:username}}',
        'Password': '{{credential:utility_portal:password}}',
        'RememberMe': 'false'
    }
    
    # Step 3: Submit login
    log_message("Attempting login...")
    login_response = session.post(login_url, data=login_data)
    log_message(f"Login response status: {login_response.status_code}")
    
    if login_response.status_code == 200:
        log_message("Login appears successful")
        
        # Step 4: Try to access the export endpoint directly
        # You'd need to find the actual export URL from the website
        export_url = "https://livingstonnj.my360-app.com/api/export"  # This is a guess
        
        export_response = session.get(export_url)
        log_message(f"Export response status: {export_response.status_code}")
        
        if export_response.status_code == 200:
            # Save the file
            filename = f"usage_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = os.path.join(os.path.expanduser("~"), "Downloads", filename)
            
            with open(filepath, 'wb') as f:
                f.write(export_response.content)
            
            log_message(f"File saved: {filepath}")
            log_message(f"File size: {len(export_response.content)} bytes")
        else:
            log_message("Export request failed - need to find correct export URL")
    else:
        log_message("Login failed - may need CSRF tokens or different approach")

except Exception as e:
    log_message(f"Error: {e}")

log_message("Direct API approach completed")
log_message("Note: This approach requires finding the exact API endpoints used by the website")
from nova_act import NovaAct
import os
import time
import glob
from datetime import datetime
import PyPDF2
import subprocess
import sys

def log_message(message):
    """Print timestamped log messages"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_downloads_folder():
    """Check for recent downloads in multiple locations"""
    download_locations = [
        os.path.join(os.path.expanduser("~"), "Downloads"),
        os.path.join(os.getcwd(), "downloads"),
        os.path.join(os.getcwd(), "nova_downloads")
    ]
    
    recent_files = []
    for location in download_locations:
        if os.path.exists(location):
            try:
                for file in os.listdir(location):
                    file_path = os.path.join(location, file)
                    if os.path.isfile(file_path):
                        mod_time = os.path.getmtime(file_path)
                        if time.time() - mod_time < 300:  # Last 5 minutes
                            file_size = os.path.getsize(file_path)
                            recent_files.append({
                                'name': file,
                                'path': file_path,
                                'modified': datetime.fromtimestamp(mod_time),
                                'size': file_size,
                                'location': location
                            })
            except Exception as e:
                log_message(f"Error checking {location}: {e}")
    
    return recent_files

def read_pdf_content(pdf_path):
    """Extract text content from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_content = ""
            
            log_message(f"PDF has {len(pdf_reader.pages)} pages")
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    text_content += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                except Exception as e:
                    log_message(f"Error reading page {page_num + 1}: {e}")
            
            return text_content
    except Exception as e:
        log_message(f"Error reading PDF: {e}")
        return None

def summarize_usage_data(content):
    """Analyze and summarize the usage data from PDF content"""
    if not content:
        return "Could not extract content from PDF"
    
    lines = content.split('\n')
    summary = {
        'total_pages': content.count('--- Page'),
        'key_sections': [],
        'usage_data': [],
        'dates_found': [],
        'numbers_found': []
    }
    
    # Look for common utility usage patterns
    usage_keywords = ['usage', 'consumption', 'kwh', 'gallons', 'therms', 'billing', 'meter', 'reading']
    date_patterns = []
    
    for line in lines:
        line_lower = line.lower().strip()
        if any(keyword in line_lower for keyword in usage_keywords):
            summary['usage_data'].append(line.strip())
        
        # Look for dates
        if any(month in line_lower for month in ['january', 'february', 'march', 'april', 'may', 'june', 
                                                'july', 'august', 'september', 'october', 'november', 'december']):
            summary['dates_found'].append(line.strip())
        
        # Look for numerical data
        if any(char.isdigit() for char in line) and len(line.strip()) > 0:
            summary['numbers_found'].append(line.strip())
    
    return summary

def open_pdf_file(pdf_path):
    """Open PDF file with default system application"""
    try:
        if os.name == 'nt':  # Windows
            os.startfile(pdf_path)
        elif os.name == 'posix':  # macOS and Linux
            subprocess.call(['open', pdf_path])
        log_message(f"Opened PDF file: {pdf_path}")
        return True
    except Exception as e:
        log_message(f"Error opening PDF: {e}")
        return False

# Create download directory
download_folder = os.path.join(os.getcwd(), "nova_downloads")
os.makedirs(download_folder, exist_ok=True)

log_message("Starting comprehensive Nova Act automation with PDF analysis...")

# Check initial downloads
initial_downloads = check_downloads_folder()
log_message(f"Initial downloads found: {len(initial_downloads)}")

# Set browser args for download directory
os.environ["NOVA_ACT_BROWSER_ARGS"] = f"--remote-debugging-port=9222 --download-directory={download_folder}"

# Initialize Nova Act
nova = NovaAct(
    starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
    headless=False,
    tty=False,
    nova_act_api_key=os.environ.get("NOVA_ACT_API_KEY", "")
)

log_message("Starting Nova Act session...")
nova.start()

log_message("Executing comprehensive automation task...")

# Enhanced automation task with detailed download monitoring
result = nova.act("""Complete the full automation process with detailed monitoring:

1. Login using username: {{credential:utility_portal:username}} and password: {{credential:utility_portal:password}}
   - Enter username in Email address field
   - Enter password in Password field
   - Click Login button
   - If save password popup appears, dismiss it

2. After successful login, locate and interact with "Active Home" selector:
   - Find the Active Home dropdown
   - Click to open it
   - Select the option with value "103892 0"
   - Wait for page to update/refresh

3. Navigate to usage/export section:
   - Look for "More details" link and click it
   - Find the "Export" button or link
   - Take a screenshot before clicking export

4. Download process with detailed monitoring:
   - Click the Export button
   - If a format selection appears, choose Excel/XLSX
   - Monitor the browser's download indicator
   - Wait for download to complete (look for download completion notification)
   - Take a screenshot showing download completion

5. Verify download success:
   - Check browser's download history (Ctrl+J)
   - Confirm file appears in downloads
   - Take a screenshot of the downloads page

6. Open the downloaded file:
   - Navigate to the downloaded file location
   - Double-click to open the file
   - Take a screenshot showing the opened file

Provide detailed status updates for each step and confirm completion.""")

log_message(f"Automation result: {result}")

# Wait for download to complete
log_message("Waiting for download to complete...")
time.sleep(10)

# Check for new downloads
log_message("Checking for downloaded files...")
current_downloads = check_downloads_folder()

new_downloads = []
for current in current_downloads:
    is_new = True
    for initial in initial_downloads:
        if current['path'] == initial['path']:
            is_new = False
            break
    if is_new:
        new_downloads.append(current)

if new_downloads:
    log_message(f"SUCCESS! Found {len(new_downloads)} new download(s):")
    
    for download in new_downloads:
        log_message(f"📁 File: {download['name']}")
        log_message(f"   Path: {download['path']}")
        log_message(f"   Size: {download['size']:,} bytes")
        log_message(f"   Modified: {download['modified']}")
        log_message(f"   Location: {download['location']}")
        
        # Check if it's a PDF file
        if download['name'].lower().endswith('.pdf'):
            log_message(f"🔍 Analyzing PDF file: {download['name']}")
            
            # Open the PDF file
            log_message("Opening PDF file...")
            open_pdf_file(download['path'])
            
            # Read PDF content
            log_message("Extracting PDF content...")
            pdf_content = read_pdf_content(download['path'])
            
            if pdf_content:
                log_message("📄 PDF Content Summary:")
                log_message("=" * 50)
                
                # Analyze content
                summary = summarize_usage_data(pdf_content)
                
                log_message(f"Total Pages: {summary['total_pages']}")
                log_message(f"Usage Data Lines Found: {len(summary['usage_data'])}")
                log_message(f"Dates Found: {len(summary['dates_found'])}")
                
                if summary['usage_data']:
                    log_message("\n🔋 Usage Data Found:")
                    for i, usage_line in enumerate(summary['usage_data'][:10]):  # Show first 10
                        log_message(f"  {i+1}. {usage_line}")
                
                if summary['dates_found']:
                    log_message("\n📅 Dates Found:")
                    for i, date_line in enumerate(summary['dates_found'][:5]):  # Show first 5
                        log_message(f"  {i+1}. {date_line}")
                
                # Save full content to text file
                text_file_path = download['path'].replace('.pdf', '_content.txt')
                try:
                    with open(text_file_path, 'w', encoding='utf-8') as f:
                        f.write(pdf_content)
                    log_message(f"💾 Full PDF content saved to: {text_file_path}")
                except Exception as e:
                    log_message(f"Error saving content: {e}")
                
                log_message("=" * 50)
            else:
                log_message("❌ Could not extract PDF content")
        
        elif download['name'].lower().endswith(('.xlsx', '.xls')):
            log_message(f"📊 Excel file detected: {download['name']}")
            log_message("Opening Excel file...")
            open_pdf_file(download['path'])
            
        else:
            log_message(f"📄 Other file type: {download['name']}")
            log_message("Opening file...")
            open_pdf_file(download['path'])

else:
    log_message("❌ No new downloads detected")
    log_message("Checking browser downloads manually...")
    
    # Try to get Nova to check downloads
    download_check = nova.act("""Check the browser's download status:
    
    1. Press Ctrl+J to open downloads page
    2. Take a screenshot of the downloads page
    3. Look for any recent downloads
    4. If you see a downloaded file, click on it to open
    5. Describe what you see in the downloads""")
    
    log_message(f"Download check result: {download_check}")

log_message("Process completed!")
log_message("Session will remain open for manual verification.")
log_message("Press Ctrl+C to stop when you're done reviewing the files.")

try:
    while True:
        time.sleep(30)
        log_message("Session active... Check your downloaded files")
        
        # Periodic check for very recent downloads
        very_recent = check_downloads_folder()
        for download in very_recent:
            if time.time() - download['modified'].timestamp() < 60:
                log_message(f"🆕 Very recent download: {download['name']}")
                
except KeyboardInterrupt:
    log_message("Stopping Nova Act session...")
    nova.stop()
    log_message("Session stopped. All done!")
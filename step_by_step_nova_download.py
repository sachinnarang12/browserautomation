from nova_act import NovaAct
import os
import time
import glob
from datetime import datetime
import PyPDF2
import subprocess

def log_message(message):
    """Print timestamped log messages"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_downloads_folder():
    """Check for recent downloads"""
    download_locations = [
        os.path.join(os.path.expanduser("~"), "Downloads"),
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
                        if time.time() - mod_time < 600:  # Last 10 minutes
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

def analyze_content(content):
    """Analyze and summarize content"""
    if not content:
        return "Could not extract content"
    
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    # Look for key information
    usage_data = []
    dates = []
    numbers = []
    
    for line in lines:
        line_lower = line.lower()
        
        # Usage-related keywords
        if any(keyword in line_lower for keyword in ['usage', 'consumption', 'kwh', 'gallons', 'therms', 'billing']):
            usage_data.append(line)
        
        # Date patterns
        if any(month in line_lower for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                                                'jul', 'aug', 'sep', 'oct', 'nov', 'dec']):
            dates.append(line)
        
        # Lines with numbers
        if any(char.isdigit() for char in line) and len(line) < 100:
            numbers.append(line)
    
    summary = f"""
📊 CONTENT ANALYSIS SUMMARY
{'='*50}
Total Lines: {len(lines)}
Usage Data Lines: {len(usage_data)}
Date References: {len(dates)}
Numerical Data: {len(numbers)}

🔋 USAGE DATA FOUND:
{chr(10).join(f"  • {line}" for line in usage_data[:10])}

📅 DATES FOUND:
{chr(10).join(f"  • {line}" for line in dates[:5])}

🔢 KEY NUMBERS:
{chr(10).join(f"  • {line}" for line in numbers[:10])}
"""
    
    return summary

def open_file(file_path):
    """Open file with default application"""
    try:
        if os.name == 'nt':  # Windows
            os.startfile(file_path)
        else:
            subprocess.call(['open', file_path])
        return True
    except Exception as e:
        log_message(f"Error opening file: {e}")
        return False

# Create download directory
download_folder = os.path.join(os.getcwd(), "nova_downloads")
os.makedirs(download_folder, exist_ok=True)

log_message("Starting step-by-step Nova Act automation...")

# Check initial state
initial_downloads = check_downloads_folder()
log_message(f"Initial downloads: {len(initial_downloads)}")

# Initialize Nova Act
nova = NovaAct(
    starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
    headless=False,
    tty=False,
    nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
)

nova.start()

try:
    # Step 1: Login
    log_message("Step 1: Logging in...")
    login_result = nova.act("Login with the provided credentials. Enter the username in the email field and password in the password field, then click login.")
    log_message(f"Login result: {login_result}")
    time.sleep(3)

    # Step 2: Select Active Home
    log_message("Step 2: Selecting Active Home...")
    home_result = nova.act("Find the Active Home dropdown and select the option with value 103892 0.If save password pops up close that.")
    log_message(f"Active Home result: {home_result}")
    time.sleep(3)

    # Step 3: Navigate to export
    log_message("Step 3: Finding export option...")
    export_nav = nova.act("Look for 'More details' link and click it, then find the Export button.")
    log_message(f"Export navigation: {export_nav}")
    time.sleep(3)

    # Step 4: Download file
    log_message("Step 4: Downloading file...")
    download_result = nova.act("Click the Export button to download the file. Monitor for download completion.")
    log_message(f"Download result: {download_result}")
    time.sleep(10)  # Wait for download

    # Step 5: Check downloads
    log_message("Step 5: Checking for downloaded files...")
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
        log_message(f"🎉 SUCCESS! Found {len(new_downloads)} new download(s):")
        
        for download in new_downloads:
            log_message(f"\n📁 File: {download['name']}")
            log_message(f"   Path: {download['path']}")
            log_message(f"   Size: {download['size']:,} bytes")
            log_message(f"   Modified: {download['modified']}")
            
            # Open the file
            log_message("🔍 Opening file...")
            open_file(download['path'])
            
            # If it's a PDF, analyze it
            if download['name'].lower().endswith('.pdf'):
                log_message("📄 Analyzing PDF content...")
                pdf_content = read_pdf_content(download['path'])
                
                if pdf_content:
                    analysis = analyze_content(pdf_content)
                    log_message(analysis)
                    
                    # Save analysis to file
                    analysis_file = download['path'].replace('.pdf', '_analysis.txt')
                    try:
                        with open(analysis_file, 'w', encoding='utf-8') as f:
                            f.write(f"PDF Analysis for: {download['name']}\n")
                            f.write(f"Generated: {datetime.now()}\n\n")
                            f.write(analysis)
                            f.write(f"\n\nFULL CONTENT:\n{pdf_content}")
                        log_message(f"💾 Analysis saved to: {analysis_file}")
                    except Exception as e:
                        log_message(f"Error saving analysis: {e}")
                else:
                    log_message("❌ Could not extract PDF content")
            
            elif download['name'].lower().endswith(('.xlsx', '.xls')):
                log_message("📊 Excel file detected - opened with default application")
            
            else:
                log_message(f"📄 File type: {download['name'].split('.')[-1] if '.' in download['name'] else 'unknown'}")

    else:
        log_message("❌ No new downloads found")
        
        # Try to check browser downloads
        log_message("Checking browser downloads...")
        browser_check = nova.act("Press Ctrl+J to open downloads and check for recent downloads.")
        log_message(f"Browser check: {browser_check}")

    log_message("\n🎯 AUTOMATION COMPLETE!")
    log_message("Files have been downloaded and analyzed.")
    log_message("Check the opened files and analysis results above.")

except Exception as e:
    log_message(f"Error during automation: {e}")

finally:
    log_message("Keeping session open for manual review...")
    log_message("Press Ctrl+C to stop when done.")
    
    try:
        while True:
            time.sleep(30)
            log_message("Session active... Press Ctrl+C to stop")
    except KeyboardInterrupt:
        log_message("Stopping session...")
        nova.stop()
        log_message("Done!")
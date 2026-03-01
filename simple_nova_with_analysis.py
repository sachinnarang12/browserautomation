from nova_act import NovaAct
import os
import time
from datetime import datetime
import PyPDF2
import subprocess

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_downloads():
    """Check Downloads folder for recent files"""
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    recent_files = []
    
    if os.path.exists(downloads_path):
        try:
            for file in os.listdir(downloads_path):
                file_path = os.path.join(downloads_path, file)
                if os.path.isfile(file_path):
                    mod_time = os.path.getmtime(file_path)
                    if time.time() - mod_time < 600:  # Last 10 minutes
                        recent_files.append({
                            'name': file,
                            'path': file_path,
                            'size': os.path.getsize(file_path),
                            'modified': datetime.fromtimestamp(mod_time)
                        })
        except Exception as e:
            log_message(f"Error checking downloads: {e}")
    
    return recent_files

def analyze_pdf(pdf_path):
    """Read and analyze PDF content"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            content = ""
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    content += f"\n=== PAGE {page_num + 1} ===\n{page_text}\n"
                except Exception as e:
                    log_message(f"Error reading page {page_num + 1}: {e}")
            
            # Simple analysis
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            usage_lines = [line for line in lines if any(word in line.lower() 
                          for word in ['usage', 'kwh', 'consumption', 'billing', 'meter'])]
            
            date_lines = [line for line in lines if any(month in line.lower() 
                         for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                      'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])]
            
            log_message(f"📄 PDF Analysis:")
            log_message(f"   Pages: {len(pdf_reader.pages)}")
            log_message(f"   Total lines: {len(lines)}")
            log_message(f"   Usage-related lines: {len(usage_lines)}")
            log_message(f"   Date references: {len(date_lines)}")
            
            if usage_lines:
                log_message("🔋 Usage data found:")
                for i, line in enumerate(usage_lines[:5]):
                    log_message(f"   {i+1}. {line}")
            
            if date_lines:
                log_message("📅 Dates found:")
                for i, line in enumerate(date_lines[:3]):
                    log_message(f"   {i+1}. {line}")
            
            # Save full content
            text_file = pdf_path.replace('.pdf', '_content.txt')
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(content)
            log_message(f"💾 Full content saved to: {text_file}")
            
            return content
            
    except Exception as e:
        log_message(f"Error analyzing PDF: {e}")
        return None

def open_file(file_path):
    """Open file with default application"""
    try:
        os.startfile(file_path)
        return True
    except Exception as e:
        log_message(f"Error opening file: {e}")
        return False

log_message("Starting Nova Act with download monitoring and PDF analysis...")

# Check initial downloads
initial_downloads = check_downloads()
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
    # Complete the full process in one go
    log_message("Executing complete automation...")
    
    result = nova.act("""Complete these steps:
1. Login using narang.sachin@gmail.com and Testing1234!1
2. Select Active Home with value 103892 0
3. Click More details
4. Click Export to download the file
5. Take screenshots of each major step""")
    
    log_message(f"Automation result: {result}")
    
    # Wait for download
    log_message("Waiting for download to complete...")
    time.sleep(15)
    
    # Check for new downloads
    current_downloads = check_downloads()
    new_files = []
    
    for current in current_downloads:
        is_new = True
        for initial in initial_downloads:
            if current['path'] == initial['path']:
                is_new = False
                break
        if is_new:
            new_files.append(current)
    
    if new_files:
        log_message(f"🎉 SUCCESS! Found {len(new_files)} new file(s):")
        
        for file_info in new_files:
            log_message(f"\n📁 {file_info['name']}")
            log_message(f"   Size: {file_info['size']:,} bytes")
            log_message(f"   Modified: {file_info['modified']}")
            log_message(f"   Path: {file_info['path']}")
            
            # Open the file
            log_message("🔍 Opening file...")
            open_file(file_info['path'])
            
            # If PDF, analyze it
            if file_info['name'].lower().endswith('.pdf'):
                log_message("📄 Analyzing PDF...")
                analyze_pdf(file_info['path'])
            
            elif file_info['name'].lower().endswith(('.xlsx', '.xls')):
                log_message("📊 Excel file opened with default application")
            
            else:
                log_message(f"📄 File type: {file_info['name'].split('.')[-1]}")
    
    else:
        log_message("❌ No new downloads found")
        
        # Check browser downloads manually
        log_message("Checking browser downloads...")
        browser_result = nova.act("Press Ctrl+J to show downloads and take a screenshot")
        log_message(f"Browser downloads: {browser_result}")

except Exception as e:
    log_message(f"Error: {e}")

finally:
    log_message("\n🎯 PROCESS COMPLETE!")
    log_message("Check the files that were opened and analysis results above.")
    log_message("Session will remain open. Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(30)
            log_message("Monitoring... Press Ctrl+C to stop")
    except KeyboardInterrupt:
        nova.stop()
        log_message("Session stopped!")
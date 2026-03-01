from nova_act import NovaAct
import time
from datetime import datetime
import json
import csv

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def save_data_to_files(data, base_filename="usage_data_103892"):
    """Save extracted data to multiple formats"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save as JSON
    json_file = f"{base_filename}_{timestamp}.json"
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        log_message(f"💾 Saved JSON: {json_file}")
    except Exception as e:
        log_message(f"Error saving JSON: {e}")
    
    # Save as text
    txt_file = f"{base_filename}_{timestamp}.txt"
    try:
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"Usage Data Export for Account 103892\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write("="*60 + "\n\n")
            
            if isinstance(data, dict):
                for key, value in data.items():
                    f.write(f"{key}:\n{value}\n\n")
            else:
                f.write(str(data))
        log_message(f"💾 Saved TXT: {txt_file}")
    except Exception as e:
        log_message(f"Error saving TXT: {e}")
    
    return json_file, txt_file

log_message("🎯 NOVA ACT DATA EXTRACTION - Get data directly from the page")

nova = NovaAct(
    starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
    headless=False,
    tty=False,
    nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
)

nova.start()

try:
    # Step 1: Navigate to usage page
    log_message("🔐 Step 1: Navigating to usage data...")
    nav_result = nova.act("""Navigate to the usage data:
    1. Login with username: narang.sachin@gmail.com and password: Testing1234!123
    2. Select Active Home dropdown and choose "103892 0"
    3. Navigate to Usage History section
    4. Click More Details to see the full usage data
    5. Take a screenshot of the usage data page""")
    
    log_message("✅ Navigation completed")
    time.sleep(3)
    
    # Step 2: Extract all visible usage data
    log_message("📊 Step 2: Extracting usage data from the page...")
    extract_result = nova.act("""Extract ALL usage data visible on the page:
    
    1. Read and transcribe ALL usage information you can see including:
       - Account number and service address
       - All usage amounts (kWh, gallons, therms, etc.)
       - All dates and billing periods
       - All meter readings
       - Rate information
       - Any charts or graph data
       - Historical usage comparisons
    
    2. Provide the data in a structured format with clear labels
    
    3. If there are multiple months/periods, list each one separately
    
    4. Include any additional details like peak usage times, rate schedules, etc.
    
    Be very thorough - extract everything you can see on the page.""")
    
    log_message("✅ Data extraction completed")
    
    # Step 3: Get additional details if available
    log_message("🔍 Step 3: Looking for additional data sections...")
    additional_result = nova.act("""Look for and extract additional usage information:
    
    1. Check if there are tabs, links, or sections for:
       - Detailed billing history
       - Usage graphs/charts
       - Rate schedules
       - Meter reading history
       - Energy efficiency information
    
    2. If you find additional sections, navigate to them and extract that data too
    
    3. Provide a comprehensive summary of ALL usage-related information available""")
    
    log_message("✅ Additional data extraction completed")
    
    # Compile all extracted data
    extracted_data = {
        "account": "103892",
        "extraction_date": datetime.now().isoformat(),
        "navigation_result": str(nav_result),
        "main_usage_data": str(extract_result),
        "additional_data": str(additional_result)
    }
    
    # Save the data locally
    log_message("💾 Saving extracted data to local files...")
    json_file, txt_file = save_data_to_files(extracted_data)
    
    # Display summary
    print("\n" + "="*60)
    print("🎯 DATA EXTRACTION COMPLETE!")
    print("="*60)
    print(f"📄 Main Usage Data:")
    print(str(extract_result)[:500] + "..." if len(str(extract_result)) > 500 else str(extract_result))
    print("\n" + "="*60)
    print(f"💾 Files created:")
    print(f"  📄 {txt_file}")
    print(f"  📊 {json_file}")
    print("="*60)
    
    # Try to open the files
    try:
        import os
        os.startfile(txt_file)
        log_message(f"✅ Opened {txt_file}")
    except:
        pass

except Exception as e:
    log_message(f"❌ Error during extraction: {e}")

# Keep session open for manual verification
log_message("\n🔄 Session staying open for manual verification")
log_message("You can manually review the usage page in the browser")
log_message("Press Ctrl+C to stop when done")

try:
    while True:
        time.sleep(60)
        log_message("Session active - check the extracted data files")
except KeyboardInterrupt:
    nova.stop()
    log_message("✅ Session ended - data extraction complete!")
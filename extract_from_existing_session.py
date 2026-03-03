import os
from nova_act import NovaAct
import time
from datetime import datetime
import json

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def save_extracted_data(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"usage_data_103892_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Usage Data Extract for Account 103892\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write("="*60 + "\n\n")
            f.write(str(data))
        
        log_message(f"💾 Data saved to: {filename}")
        
        # Try to open the file
        os.startfile(filename)
        log_message(f"✅ Opened file: {filename}")
        
        return filename
    except Exception as e:
        log_message(f"Error saving data: {e}")
        return None

log_message("🎯 EXTRACTING DATA FROM EXISTING NOVA SESSION")

# Create a new Nova session to work with the existing browser
nova = NovaAct(
    starting_page="https://livingstonnj.my360-app.com/dashboard",
    headless=False,
    tty=False,
    nova_act_api_key=os.environ.get("NOVA_ACT_API_KEY", "")
)

try:
    nova.start()
    
    log_message("📊 Extracting all visible usage data...")
    
    # Extract data from whatever page is currently visible
    extract_result = nova.act("""Read and extract ALL text and data visible on the current page:

1. If you're on a login page, login with {{credential:utility_portal:username}} and {{credential:utility_portal:password}} first
2. Navigate to Usage section if not already there
3. Extract ALL usage information including:
   - Account details
   - Usage amounts and units
   - Billing periods and dates
   - Meter readings
   - Rate information
   - Any numerical data
   - Historical comparisons

Provide a complete transcription of all usage-related data you can see.""")
    
    log_message("✅ Data extraction completed")
    
    # Save the extracted data
    filename = save_extracted_data(extract_result)
    
    print("\n" + "="*60)
    print("🎯 DATA EXTRACTION COMPLETE!")
    print("="*60)
    print("Extracted Data Preview:")
    print(str(extract_result)[:800] + "..." if len(str(extract_result)) > 800 else str(extract_result))
    print("="*60)
    
    if filename:
        print(f"📄 Full data saved to: {filename}")
    
except Exception as e:
    log_message(f"❌ Error: {e}")

finally:
    try:
        nova.stop()
    except:
        pass
    log_message("✅ Extraction complete!")
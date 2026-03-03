from nova_act import NovaAct
import time
from datetime import datetime
import json
import os

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def save_extracted_content(content, base_filename="usage_data_103892"):
    """Save the actual extracted content to files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save as text file
    txt_file = f"{base_filename}_{timestamp}_CONTENT.txt"
    try:
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"Usage Data Content for Account 103892\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write("="*60 + "\n\n")
            f.write(content)
        log_message(f"💾 Saved content to: {txt_file}")
        
        # Try to open the file
        try:
            os.startfile(txt_file)
            log_message(f"✅ Opened {txt_file}")
        except:
            pass
            
        return txt_file
    except Exception as e:
        log_message(f"Error saving content: {e}")
        return None

log_message("🎯 NOVA ACT PDF CONTENT READER - Extract actual usage data content")

nova = NovaAct(
    starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
    headless=False,
    tty=False,
    nova_act_api_key=os.environ.get("NOVA_ACT_API_KEY", "")
)

nova.start()

try:
    # Step 1: Navigate to usage page
    log_message("🔐 Step 1: Navigating to usage data page...")
    nav_result = nova.act("""Navigate to the usage data:
    1. Login with username: {{credential:utility_portal:username}} and password: {{credential:utility_portal:password}}
    2. Select Active Home dropdown and choose "103892 0"
    3. Navigate to Usage History section
    4. Click More Details to see the full usage data""")
    
    log_message("✅ Navigation completed")
    time.sleep(5)
    
    # Step 2: Extract the actual content - be very specific about returning text
    log_message("📊 Step 2: Reading and transcribing ALL visible usage data...")
    extract_result = nova.act("""Please read and transcribe EVERYTHING you can see on this usage page. 
    
    I need you to return the actual text content, not metadata. Please provide:
    
    1. Account information and service address
    2. All usage amounts with units (kWh, gallons, therms, etc.)
    3. All dates and billing periods
    4. All meter readings and numbers
    5. Any rate information or charges
    6. Historical usage data if visible
    7. Any charts or graph values
    
    Return this as plain text that I can read - transcribe everything exactly as you see it on the page.
    Do not return metadata or technical information about the extraction process.
    Just give me the actual usage data content as readable text.""")
    
    log_message("✅ Content extraction completed")
    
    # Access the actual content from the ActResult
    if hasattr(extract_result, 'content'):
        actual_content = extract_result.content
        log_message("✅ Found content attribute")
    elif hasattr(extract_result, 'text'):
        actual_content = extract_result.text
        log_message("✅ Found text attribute")
    elif hasattr(extract_result, 'result'):
        actual_content = extract_result.result
        log_message("✅ Found result attribute")
    else:
        # Try to get string representation but look for actual content
        actual_content = str(extract_result)
        log_message("⚠️ Using string representation - checking for content...")
    
    # Display what we got
    print("\n" + "="*60)
    print("🎯 EXTRACTED CONTENT:")
    print("="*60)
    print(actual_content)
    print("="*60)
    
    # Save the content
    if actual_content and len(actual_content) > 100:  # Make sure we have substantial content
        content_file = save_extracted_content(actual_content)
        log_message(f"💾 Content saved to: {content_file}")
    else:
        log_message("⚠️ Content seems too short - might be metadata only")
        log_message("Let me try a different approach...")
        
        # Try a more direct approach
        direct_result = nova.act("""Look at the current page and tell me exactly what usage information you see.
        
        For example:
        - What is the account number?
        - What usage amounts do you see?
        - What time periods are shown?
        - What are the actual numbers and values displayed?
        
        Please give me the specific data values, not technical descriptions.""")
        
        direct_content = str(direct_result)
        print("\n" + "="*60)
        print("🎯 DIRECT EXTRACTION ATTEMPT:")
        print("="*60)
        print(direct_content)
        print("="*60)
        
        if direct_content:
            save_extracted_content(direct_content)

except Exception as e:
    log_message(f"❌ Error during extraction: {e}")

# Keep session open for manual verification
log_message("\n🔄 Session staying open for manual verification")
log_message("You can manually review the usage page in the browser")
log_message("Press Ctrl+C to stop when done")

try:
    while True:
        time.sleep(60)
        log_message("Session active - check the browser for usage data")
except KeyboardInterrupt:
    nova.stop()
    log_message("✅ Session ended - content extraction complete!")
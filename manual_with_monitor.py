import os
import time
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_downloads():
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
        except:
            pass
    
    return recent_files

print("="*60)
print("📋 MANUAL DOWNLOAD WITH MONITORING")
print("="*60)

log_message("🎯 MANUAL STEPS TO FOLLOW:")
print("""
1. 🌐 Open your web browser and go to:
   https://livingstonnj.my360-app.com

2. 🔐 Login with:
   Username: narang.sachin@gmail.com
   Password: Testing1234!1

3. 🏠 Select Active Home:
   - Look for "Active Home" dropdown
   - Select "103892 0"

4. 📊 Go to Usage:
   - Click on "Usage" in the left menu

5. 📥 Export Data:
   - Look for "Export" button
   - Click it to download

6. 💾 Save the file to your Downloads folder
""")

log_message("🔍 I'll monitor your Downloads folder for new files...")
log_message("📂 Downloads location: " + os.path.join(os.path.expanduser("~"), "Downloads"))

initial_downloads = check_downloads()
log_message(f"📁 Starting with {len(initial_downloads)} recent files")

if initial_downloads:
    log_message("Recent files already in Downloads:")
    for file_info in initial_downloads:
        log_message(f"  📄 {file_info['name']} ({file_info['size']:,} bytes)")

log_message("\n🔄 MONITORING STARTED - Follow the manual steps above")
log_message("Press Ctrl+C to stop monitoring when done")

try:
    while True:
        time.sleep(5)  # Check every 5 seconds
        
        current_downloads = check_downloads()
        new_files = [f for f in current_downloads if f not in initial_downloads]
        
        if new_files:
            log_message(f"🎉 NEW DOWNLOAD DETECTED!")
            for file_info in new_files:
                log_message(f"📄 File: {file_info['name']}")
                log_message(f"   📏 Size: {file_info['size']:,} bytes")
                log_message(f"   🕒 Modified: {file_info['modified']}")
                log_message(f"   📂 Path: {file_info['path']}")
                
                # Auto-open the file
                try:
                    os.startfile(file_info['path'])
                    log_message(f"✅ Automatically opened: {file_info['name']}")
                except Exception as e:
                    log_message(f"❌ Could not open file: {e}")
                
                # Update initial list to avoid re-detecting
                initial_downloads.append(file_info)
        
        # Show periodic status
        if int(time.time()) % 30 == 0:  # Every 30 seconds
            log_message("🔄 Still monitoring... Complete the manual steps above")
        
except KeyboardInterrupt:
    log_message("\n🛑 Monitoring stopped")
    
    # Final check
    final_downloads = check_downloads()
    all_new_files = [f for f in final_downloads if f not in initial_downloads]
    
    if all_new_files:
        log_message(f"📊 FINAL SUMMARY: Found {len(all_new_files)} new file(s)")
        for file_info in all_new_files:
            log_message(f"✅ {file_info['name']} - {file_info['size']:,} bytes")
    else:
        log_message("❌ No new downloads were detected")
        log_message("Please check your Downloads folder manually")
    
    log_message("🎯 Monitoring complete!")
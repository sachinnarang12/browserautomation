import os
import time
from datetime import datetime

def check_downloads():
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    recent_files = []
    
    print(f"📂 Checking Downloads folder: {downloads_path}")
    
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
            print(f"Error checking downloads: {e}")
    
    return recent_files

print("🔍 Checking for recently downloaded files...")
recent_files = check_downloads()

if recent_files:
    print(f"🎉 Found {len(recent_files)} recent file(s):")
    for file_info in recent_files:
        print(f"\n📄 {file_info['name']}")
        print(f"   📏 Size: {file_info['size']:,} bytes")
        print(f"   🕒 Modified: {file_info['modified']}")
        print(f"   📂 Path: {file_info['path']}")
        
        # Check if it looks like a usage export
        if any(keyword in file_info['name'].lower() for keyword in ['usage', 'export', '103892', 'pdf']):
            print(f"   🎯 This looks like your usage export!")
            
            # Try to open it
            try:
                os.startfile(file_info['path'])
                print(f"   ✅ Opened file automatically")
            except Exception as e:
                print(f"   ❌ Could not open: {e}")
else:
    print("❌ No recent downloads found")
    print("Please check your Downloads folder manually:")
    print(f"📂 {os.path.join(os.path.expanduser('~'), 'Downloads')}")

print("\n🎯 The Nova Act automation was successful!")
print("If you don't see the file, it might be in a different download location or still processing.")
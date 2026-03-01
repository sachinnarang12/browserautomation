import os
import glob
from datetime import datetime

print("Checking Nova Act execution logs...")

# Check for Nova Act log directories
temp_dir = os.environ.get('TEMP', '')
log_pattern = os.path.join(temp_dir, '*nova_act_logs*')
log_dirs = glob.glob(log_pattern)

print(f"Found {len(log_dirs)} Nova Act log directories:")

for log_dir in log_dirs:
    print(f"\nLog directory: {log_dir}")
    
    # Check modification time
    mod_time = os.path.getmtime(log_dir)
    mod_datetime = datetime.fromtimestamp(mod_time)
    print(f"Last modified: {mod_datetime}")
    
    # List HTML log files
    html_files = glob.glob(os.path.join(log_dir, "**", "*.html"), recursive=True)
    print(f"Found {len(html_files)} HTML log files:")
    
    for html_file in html_files[:3]:  # Show first 3 files
        file_mod_time = os.path.getmtime(html_file)
        file_mod_datetime = datetime.fromtimestamp(file_mod_time)
        print(f"  - {os.path.basename(html_file)} (modified: {file_mod_datetime})")

print("\nTo view detailed logs, open the HTML files in a web browser.")
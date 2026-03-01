import os
import time
from datetime import datetime
import PyPDF2

def find_recent_files():
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    recent_files = []
    
    print(f"📂 Checking: {downloads_path}")
    
    if os.path.exists(downloads_path):
        try:
            for file in os.listdir(downloads_path):
                file_path = os.path.join(downloads_path, file)
                if os.path.isfile(file_path):
                    mod_time = os.path.getmtime(file_path)
                    if time.time() - mod_time < 1800:  # Last 30 minutes
                        recent_files.append({
                            'name': file,
                            'path': file_path,
                            'size': os.path.getsize(file_path),
                            'modified': datetime.fromtimestamp(mod_time)
                        })
        except:
            pass
    
    recent_files.sort(key=lambda x: x['modified'], reverse=True)
    return recent_files

def analyze_pdf_simple(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            text = ""
            for page in pdf_reader.pages:
                try:
                    text += page.extract_text() + "\n"
                except:
                    pass
            
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            print(f"\n📄 PDF ANALYSIS: {os.path.basename(file_path)}")
            print(f"Pages: {len(pdf_reader.pages)}")
            print(f"Text lines: {len(lines)}")
            
            # Look for key info
            usage_lines = [line for line in lines if any(word in line.lower() for word in ['usage', 'kwh', 'consumption', 'billing'])]
            date_lines = [line for line in lines if any(month in line.lower() for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun'])]
            
            print(f"\n🔋 Usage data lines found: {len(usage_lines)}")
            for line in usage_lines[:5]:
                print(f"  • {line}")
            
            print(f"\n📅 Date references found: {len(date_lines)}")
            for line in date_lines[:3]:
                print(f"  • {line}")
            
            print(f"\n📄 First 500 characters:")
            print(text[:500])
            
            return True
    except Exception as e:
        print(f"Error analyzing PDF: {e}")
        return False

print("🔍 Looking for recent downloads...")
files = find_recent_files()

if files:
    print(f"📁 Found {len(files)} recent file(s):")
    
    for file_info in files:
        print(f"\n📄 {file_info['name']}")
        print(f"   Size: {file_info['size']:,} bytes")
        print(f"   Modified: {file_info['modified']}")
        
        if file_info['name'].lower().endswith('.pdf'):
            analyze_pdf_simple(file_info['path'])
        
        # Try to open
        try:
            os.startfile(file_info['path'])
            print(f"   ✅ Opened for review")
        except:
            pass
else:
    print("❌ No recent files found")
    print(f"Check manually: {os.path.join(os.path.expanduser('~'), 'Downloads')}")

print("\n🎯 Analysis complete!")
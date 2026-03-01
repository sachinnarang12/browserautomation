import os
import time
from datetime import datetime
import PyPDF2
import pandas as pd

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def find_recent_downloads():
    """Find recently downloaded files"""
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    recent_files = []
    
    log_message(f"📂 Searching Downloads folder: {downloads_path}")
    
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
                            'modified': datetime.fromtimestamp(mod_time),
                            'extension': file.split('.')[-1].lower() if '.' in file else ''
                        })
        except Exception as e:
            log_message(f"Error checking downloads: {e}")
    
    # Sort by modification time (newest first)
    recent_files.sort(key=lambda x: x['modified'], reverse=True)
    return recent_files

def analyze_pdf(file_path):
    """Analyze PDF content"""
    try:
        log_message(f"📄 Analyzing PDF: {os.path.basename(file_path)}")
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            log_message(f"📊 PDF has {len(pdf_reader.pages)} pages")
            
            # Extract all text
            full_text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    full_text += f"\n--- PAGE {page_num + 1} ---\n{page_text}\n"
                except Exception as e:
                    log_message(f"Error reading page {page_num + 1}: {e}")
            
            # Analyze content
            lines = [line.strip() for line in full_text.split('\n') if line.strip()]
            
            # Look for key information
            usage_data = []
            dates = []
            numbers = []
            account_info = []
            
            for line in lines:
                line_lower = line.lower()
                
                # Usage-related keywords
                if any(keyword in line_lower for keyword in ['usage', 'consumption', 'kwh', 'gallons', 'therms', 'billing', 'meter']):
                    usage_data.append(line)
                
                # Date patterns
                if any(month in line_lower for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                                                        'jul', 'aug', 'sep', 'oct', 'nov', 'dec']):
                    dates.append(line)
                
                # Account/address info
                if any(keyword in line_lower for keyword in ['account', 'address', 'service', 'customer']):
                    account_info.append(line)
                
                # Lines with numbers (potential usage values)
                if any(char.isdigit() for char in line) and len(line) < 100:
                    numbers.append(line)
            
            # Generate summary
            summary = f"""
📊 PDF ANALYSIS SUMMARY
{'='*60}
File: {os.path.basename(file_path)}
Size: {os.path.getsize(file_path):,} bytes
Pages: {len(pdf_reader.pages)}
Total Lines: {len(lines)}

🏠 ACCOUNT INFORMATION:
{chr(10).join(f"  • {line}" for line in account_info[:5])}

🔋 USAGE DATA FOUND:
{chr(10).join(f"  • {line}" for line in usage_data[:10])}

📅 DATE REFERENCES:
{chr(10).join(f"  • {line}" for line in dates[:5])}

🔢 KEY NUMERICAL DATA:
{chr(10).join(f"  • {line}" for line in numbers[:15])}

📄 FULL CONTENT PREVIEW:
{full_text[:1000]}{'...' if len(full_text) > 1000 else ''}
"""
            
            return summary, full_text
            
    except Exception as e:
        return f"❌ Error analyzing PDF: {e}", ""

def analyze_excel(file_path):
    """Analyze Excel content"""
    try:
        log_message(f"📊 Analyzing Excel: {os.path.basename(file_path)}")
        
        # Try to read Excel file
        df = pd.read_excel(file_path)
        
        summary = f"""
📊 EXCEL ANALYSIS SUMMARY
{'='*60}
File: {os.path.basename(file_path)}
Size: {os.path.getsize(file_path):,} bytes
Rows: {len(df)}
Columns: {len(df.columns)}

📋 COLUMN NAMES:
{chr(10).join(f"  • {col}" for col in df.columns)}

📄 FIRST FEW ROWS:
{df.head().to_string()}

📊 DATA SUMMARY:
{df.describe().to_string()}
"""
        
        return summary, df.to_string()
        
    except Exception as e:
        return f"❌ Error analyzing Excel: {e}", ""

# Main analysis
log_message("🔍 Looking for recently downloaded files...")

recent_files = find_recent_downloads()

if recent_files:
    log_message(f"📁 Found {len(recent_files)} recent file(s):")
    
    for i, file_info in enumerate(recent_files):
        log_message(f"\n📄 File {i+1}: {file_info['name']}")
        log_message(f"   📏 Size: {file_info['size']:,} bytes")
        log_message(f"   🕒 Modified: {file_info['modified']}")
        log_message(f"   📂 Path: {file_info['path']}")
        
        # Check if it looks like a usage export
        if any(keyword in file_info['name'].lower() for keyword in ['usage', 'export', '103892', 'utility']):
            log_message(f"   🎯 This looks like your usage export!")
            
            # Analyze based on file type
            if file_info['extension'] == 'pdf':
                summary, full_content = analyze_pdf(file_info['path'])
                print(summary)
                
                # Save analysis to file
                analysis_file = file_info['path'].replace('.pdf', '_analysis.txt')
                try:
                    with open(analysis_file, 'w', encoding='utf-8') as f:
                        f.write(f"Analysis of: {file_info['name']}\n")
                        f.write(f"Generated: {datetime.now()}\n\n")
                        f.write(summary)
                        f.write(f"\n\nFULL CONTENT:\n{full_content}")
                    log_message(f"💾 Analysis saved to: {analysis_file}")
                except Exception as e:
                    log_message(f"Error saving analysis: {e}")
                    
            elif file_info['extension'] in ['xlsx', 'xls']:
                summary, full_content = analyze_excel(file_info['path'])
                print(summary)
                
            else:
                log_message(f"   📄 File type: {file_info['extension']}")
                log_message(f"   ℹ️  Cannot analyze this file type automatically")
        
        # Try to open the file
        try:
            os.startfile(file_info['path'])
            log_message(f"   ✅ Opened file for manual review")
        except Exception as e:
            log_message(f"   ❌ Could not open file: {e}")

else:
    log_message("❌ No recent downloads found")
    log_message("Please check your Downloads folder manually:")
    log_message(f"📂 {os.path.join(os.path.expanduser('~'), 'Downloads')}")

log_message("\n🎯 File analysis complete!")
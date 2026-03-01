from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import os
import glob
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def setup_chrome_for_download():
    """Setup Chrome with download preferences to handle blob downloads"""
    download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "safebrowsing.disable_download_protection": True,
        "profile.default_content_settings.popups": 0,
        "profile.default_content_setting_values.automatic_downloads": 1
    })
    
    # Add arguments to handle downloads better
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-extensions")
    
    return chrome_options, download_dir

def wait_for_download(download_dir, timeout=30):
    """Wait for download to complete"""
    log_message(f"Waiting for download in {download_dir}...")
    
    # Get initial file count
    initial_files = set(os.listdir(download_dir))
    
    for i in range(timeout):
        time.sleep(1)
        current_files = set(os.listdir(download_dir))
        new_files = current_files - initial_files
        
        if new_files:
            for new_file in new_files:
                if not new_file.endswith('.crdownload'):  # Chrome temp download file
                    file_path = os.path.join(download_dir, new_file)
                    file_size = os.path.getsize(file_path)
                    log_message(f"✅ Download completed: {new_file} ({file_size:,} bytes)")
                    return file_path
        
        # Check for .crdownload files (Chrome downloading)
        crdownload_files = [f for f in current_files if f.endswith('.crdownload')]
        if crdownload_files:
            log_message(f"⏳ Download in progress: {crdownload_files[0]}")
    
    log_message("❌ Download timeout reached")
    return None

def selenium_utility_download():
    """Complete Selenium automation for utility download"""
    
    log_message("🚀 Starting Selenium Utility Download")
    
    try:
        options, download_dir = setup_chrome_for_download()
        
        log_message("Starting Chrome browser...")
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        
        # Navigate to login page
        login_url = "https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj"
        
        log_message("Navigating to login page...")
        driver.get(login_url)
        
        # Wait for login form
        wait = WebDriverWait(driver, 20)
        
        # Find and fill username
        log_message("Entering credentials...")
        username_field = wait.until(EC.presence_of_element_located((By.ID, "Email")))
        username_field.clear()
        username_field.send_keys("narang.sachin@gmail.com")
        
        # Find and fill password
        password_field = driver.find_element(By.ID, "Password")
        password_field.clear()
        password_field.send_keys("Testing1234!1")
        
        # Click login button
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        log_message("Logged in, waiting for dashboard...")
        time.sleep(5)
        
        # Wait for Active Home dropdown and select account
        log_message("Looking for Active Home dropdown...")
        try:
            # Try different possible selectors for the dropdown
            dropdown_selectors = [
                "//select[contains(@class, 'form-control')]",
                "//select[contains(@id, 'active')]",
                "//select[contains(@name, 'home')]",
                "//div[contains(@class, 'dropdown')]//button",
                "//button[contains(text(), '103892')]"
            ]
            
            dropdown_element = None
            for selector in dropdown_selectors:
                try:
                    dropdown_element = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    log_message(f"Found dropdown with selector: {selector}")
                    break
                except:
                    continue
            
            if dropdown_element:
                dropdown_element.click()
                time.sleep(2)
                
                # Try to select the account
                account_selectors = [
                    "//option[contains(text(), '103892')]",
                    "//a[contains(text(), '103892')]",
                    "//li[contains(text(), '103892')]"
                ]
                
                for selector in account_selectors:
                    try:
                        account_option = driver.find_element(By.XPATH, selector)
                        account_option.click()
                        log_message("Selected account 103892")
                        break
                    except:
                        continue
                        
        except Exception as e:
            log_message(f"Could not find/select Active Home dropdown: {e}")
            log_message("Continuing anyway...")
        
        time.sleep(3)
        
        # Navigate to Usage section
        log_message("Looking for Usage section...")
        usage_selectors = [
            "//a[contains(text(), 'Usage')]",
            "//button[contains(text(), 'Usage')]",
            "//li[contains(text(), 'Usage')]",
            "//div[contains(text(), 'Usage')]"
        ]
        
        usage_element = None
        for selector in usage_selectors:
            try:
                usage_element = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                usage_element.click()
                log_message("Clicked Usage section")
                break
            except:
                continue
        
        if not usage_element:
            log_message("❌ Could not find Usage section")
            return False
            
        time.sleep(3)
        
        # Find and click Export button
        log_message("Looking for Export button...")
        export_selectors = [
            "//button[contains(text(), 'Export')]",
            "//a[contains(text(), 'Export')]",
            "//input[@value='Export']",
            "//div[contains(text(), 'Export')]"
        ]
        
        export_element = None
        for selector in export_selectors:
            try:
                export_element = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                log_message(f"Found Export button with selector: {selector}")
                break
            except:
                continue
        
        if not export_element:
            log_message("❌ Could not find Export button")
            return False
        
        # Click Export
        log_message("Clicking Export button...")
        export_element.click()
        
        # Look for Excel option if dropdown appears
        time.sleep(2)
        try:
            excel_selectors = [
                "//option[contains(text(), 'Excel')]",
                "//a[contains(text(), 'Excel')]",
                "//button[contains(text(), 'Excel')]"
            ]
            
            for selector in excel_selectors:
                try:
                    excel_option = driver.find_element(By.XPATH, selector)
                    excel_option.click()
                    log_message("Selected Excel format")
                    break
                except:
                    continue
        except:
            log_message("No Excel format selection needed")
        
        # Wait for download
        log_message("Waiting for download to start...")
        downloaded_file = wait_for_download(download_dir, timeout=30)
        
        if downloaded_file:
            log_message(f"🎉 SUCCESS! File downloaded: {downloaded_file}")
            file_size = os.path.getsize(downloaded_file)
            log_message(f"📁 File size: {file_size:,} bytes")
            
            # Try to rename to something more descriptive
            try:
                new_name = f"usage_export_103892_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                new_path = os.path.join(download_dir, new_name)
                os.rename(downloaded_file, new_path)
                log_message(f"📝 Renamed to: {new_name}")
                return new_path
            except:
                return downloaded_file
        else:
            log_message("❌ Download failed or timed out")
            return False
            
    except Exception as e:
        log_message(f"❌ Error during automation: {e}")
        return False
    finally:
        try:
            log_message("Closing browser...")
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    try:
        result = selenium_utility_download()
        if result:
            log_message(f"✅ Download completed successfully: {result}")
        else:
            log_message("❌ Download failed")
    except ImportError:
        log_message("❌ Selenium not installed. Install with: pip install selenium")
        log_message("Also need ChromeDriver: https://chromedriver.chromium.org/")
    except Exception as e:
        log_message(f"❌ Unexpected error: {e}")
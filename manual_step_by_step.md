# Manual Step-by-Step Download Guide

## Most Reliable Method - Manual Browser Approach

### Step 1: Open Browser and Login
1. Open your web browser (Chrome, Edge, Firefox)
2. Go to: `https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj`
3. Login with:
   - Username: `YOUR_EMAIL`
   - Password: `YOUR_PASSWORD`

### Step 2: Select Active Home
1. Look for "Active Home" dropdown (shows account number)
2. Click the dropdown arrow
3. Select "103892 0" or "103892 - Active"

### Step 3: Navigate to Usage
1. Look for "Usage" tab or menu item
2. Click on it to go to usage page

### Step 4: Open Developer Tools BEFORE Export
**This is the key step for success:**
1. Right-click anywhere on the page
2. Select "Inspect" or "Inspect Element"
3. Click on the "Network" tab in Developer Tools
4. Click the clear button (🚫) to clear existing requests
5. Keep Developer Tools open

### Step 5: Click Export and Monitor
1. Click the "Export" button
2. Select "Excel" format if dropdown appears
3. **Watch the Network tab** - new requests will appear
4. Look for a request that looks like your export file

### Step 6: Download from Network Tab
1. In the Network tab, find the export request
2. Right-click on it
3. Select "Save as..." or "Save response as..."
4. Save to your Downloads folder
5. Name it something like "usage_export_103892.xlsx"

### Alternative Methods if Network Tab Doesn't Work:

#### Method A: Direct Blob URL
1. After clicking Export, look at the browser address bar
2. If you see a blob URL, copy it
3. Open new tab, paste the blob URL, press Enter

#### Method B: Right-click Export Button
1. Right-click directly on the Export button
2. If you see "Save link as...", click it
3. Save the file

#### Method C: Browser Downloads
1. Press Ctrl+J to open browser downloads
2. Look for any pending downloads
3. Click on them to complete

## Where to Find Your Downloaded File:
- **Windows**: `C:\Users\naran\Downloads\`
- Check file size - should be more than 0 bytes
- File should open in Excel

## Troubleshooting:
- If blob URL expires, go back and click Export again
- Try different browsers (Chrome, Edge, Firefox)
- Clear browser cache if having issues
- Make sure popup blockers are disabled
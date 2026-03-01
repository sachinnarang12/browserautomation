from nova_act import NovaAct
import time
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

log_message("Simple Navigation Helper - Gets you to the export page, then you download manually")

nova = NovaAct(
    starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
    headless=False,
    tty=False,
    nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
)

nova.start()

# Just get to the export page
result = nova.act("""Navigate to the export page:
1. Login with username: narang.sachin@gmail.com and password: Testing1234!1234. Then wait 1 minute for next screen to come up.
2. Locate and Select Active Home dropdown and choose "103892 0". Wait 15 seconds again. If Lastpass save password prompt comes up, click Never and close.
3. Navigate to the Usage History section. Locate More Details button and click that. Wait for 15 seconds.
4. Locate the Export button and Click here. On Pop up, Click PDF.""")

log_message(f"Navigation completed: {result}")

print("\n" + "="*60)
print("🎯 READY FOR MANUAL DOWNLOAD!")
print("="*60)
print("Now follow these steps manually in the browser:")
print("1. Right-click anywhere → Inspect → Network tab")
print("2. Clear network requests (click 🚫 button)")
print("3. Click Export → Excel")
print("4. In Network tab, right-click the export request → Save as")
print("5. Save to Downloads folder")
print("="*60)

log_message("Browser is ready. Follow the manual steps above.")
log_message("Session will stay open. Press Ctrl+C when done.")

try:
    while True:
        time.sleep(60)
        log_message("Session active - complete manual download steps")
except KeyboardInterrupt:
    nova.stop()
    log_message("Session ended.")
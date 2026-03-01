from nova_act import NovaAct
import os

print("Starting Nova Act automation...")

# Browser args enables browser debugging on port 9222.
os.environ["NOVA_ACT_BROWSER_ARGS"] = "--remote-debugging-port=9222"

# Initialize Nova Act with your starting page.
nova = NovaAct(
    starting_page="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
    headless=False,
    tty=False,
    nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
)

print("Starting Nova Act session...")
# Running nova.start will launch a new browser instance.
nova.start()

print("Executing automation task...")
# Execute the automation task
result = nova.act("""Login using the provided username(narang.sachin@gmail.com) and password(Testing1234!12).
Do not display, store, or log credentials at any time.

Navigate to the application login page (https://livingstonnj.my360-app.com) and authenticate using the retrieved credentials. Use Username in Email address textbox and password in password field.

If you can't login - STOP DONT TRY AGAIN; print username used. Tell first and last character of password used.

After successful login,close save password popup and  locate the "Active Home" selector.

Open the Active Home dropdown and select the option with value 103892 0.

Confirm that the selected Active Home has been applied (page refresh or context update).

Locate the "Export" action or button.

Click Export and download the generated PDF file.

Verify that the PDF download is complete and accessible via the browser. Open PDF so user can read and save on their laptop.""")

print("Task completed!")
print("Result:", result)

# Uncomment the line below to stop the session
# nova.stop()
print("Nova Act session is still running. You can manually stop it or let it timeout.")
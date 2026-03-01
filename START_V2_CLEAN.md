# Clean Start Instructions for V2 Dashboard

## ✅ Cleanup Complete
All Flask processes have been terminated. Port 5000 is now free.

---

## 🚀 Start V2 Dashboard (Clean)

### Step 1: Start the Dashboard
```bash
python agent_dashboard_v2.py
```

You should see:
```
✅ Default admin user created: username='admin', password='admin123'
🌐 Starting Portal Automation Agent V2.0 Dashboard
============================================================
📊 Access the dashboard at: http://localhost:5000
🔐 Default login: admin / admin123
⚠️  Please change the default password after first login!
============================================================
```

### Step 2: Open Browser
Navigate to: **http://localhost:5000**

### Step 3: Login
- Username: `admin`
- Password: `admin123`

### Step 4: Test the Credentials Screen
1. Click "Credentials" in the left sidebar
2. The page should load without errors
3. You should see "No Credentials Stored" (empty state)

### Step 5: Add a Test Credential
1. Click "Add Credential" button
2. Fill in:
   - Credential ID: `test_portal`
   - Description: `Test Portal`
   - URL: `https://example.com`
   - Username: `test@example.com`
   - Password: `TestPassword123`
3. Click "Save Credential"
4. You should see success message and the credential listed

---

## 🧪 Optional: Run Tests First

Before starting the dashboard, you can run tests:
```bash
python test_v2_dashboard.py
```

This will verify:
- Credential Manager works
- Authentication Manager works
- Database connection works
- Credential list format is correct

---

## 🐛 If You See Errors

### Multiple Instances Running
If you see "Address already in use" error:
```bash
# Check what's using port 5000
netstat -ano | Select-String ":5000"

# Kill the process (replace XXXX with PID)
taskkill /PID XXXX /F
```

### Template Errors
If credentials page shows errors, check the terminal output for the specific error message.

### Database Errors
If you see database errors:
```bash
# Delete and recreate database
del portal_agent.db
python agent_dashboard_v2.py
```

---

## ✅ What's Fixed

The credentials screen error has been fixed:
- **Issue**: `list_credentials()` returned a dict, template expected a list
- **Fix**: Convert dict to list format in the route handler
- **Result**: Credentials page now loads correctly

---

## 📝 Ready to Test

You now have:
1. ✅ All old processes killed
2. ✅ Port 5000 free
3. ✅ Credentials screen bug fixed
4. ✅ Clean environment

**Just run**: `python agent_dashboard_v2.py`

# Portal Automation Agent V2 - Deployment Guide

## Overview
This guide covers how to push this project to GitHub and deploy it on another machine using Kiro, Claude, or any other development environment.

---

## Part 1: Push to GitHub

### Step 1: Initialize Git Repository (if not already done)
```bash
git init
```

### Step 2: Create .gitignore
The project already has a `.gitignore` file. Make sure it excludes sensitive files:
- `portal_agent.db` (contains user passwords)
- `credentials_index.json` (contains credential metadata)
- `agent_config.json` (may contain task-specific data)
- `portal_agent.log`
- `*.pyc`, `__pycache__/`
- `.env` files

### Step 3: Add Remote Repository
```bash
git remote add origin https://github.com/YOUR_USERNAME/portal-automation-agent.git
```

### Step 4: Commit and Push
```bash
git add .
git commit -m "Portal Automation Agent V2 - Complete implementation with credential management"
git push -u origin main
```

---

## Part 2: Clone and Setup on New Machine

### Prerequisites
- Python 3.9 or higher
- Git installed
- Chrome/Chromium browser
- Windows OS (for Windows Credential Manager integration)

### Step 1: Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/portal-automation-agent.git
cd portal-automation-agent
```

### Step 2: Install Dependencies
```bash
# Install V2 requirements (includes all necessary packages)
pip install -r requirements_v2.txt

# Or install individual packages
pip install flask flask-login sqlalchemy bcrypt keyring nova-act PyPDF2
```

### Step 3: Initialize Database
```bash
python -c "from database import Database; db = Database(); print('Database initialized')"
```

This creates `portal_agent.db` with:
- Default admin user: `admin` / `admin123`
- Empty tasks and credentials tables

### Step 4: Add Your Credentials
```bash
# Interactive credential setup
python credential_manager.py add
```

Or use the web UI after starting the dashboard.

### Step 5: Start the Application

#### Option A: Start Both Services (Recommended)
```bash
# Terminal 1: Start the dashboard
python agent_dashboard_v2.py

# Terminal 2: Start the scheduler
python standalone_scheduler.py
```

#### Option B: Use the V1 CLI (Legacy)
```bash
python agent_cli.py list
python agent_cli.py add
```

### Step 6: Access the Dashboard
Open browser to: `http://localhost:5000`

Login with:
- Username: `admin`
- Password: `admin123`

**IMPORTANT:** Change the default password immediately after first login!

---

## Part 3: Configuration

### Credential Management
Credentials are stored securely in Windows Credential Manager. The system stores:
- **In Keyring (encrypted):** Username and password
- **In credentials_index.json:** Metadata only (description, URL, created date)

### Task Configuration
Tasks are stored in `agent_config.json` with format:
```json
{
  "tasks": [
    {
      "id": "task_123456_0",
      "name": "Daily Usage Export",
      "url": "https://livingstonnj.my360-app.com",
      "instructions": "Login with {{credential:utility_portal:username}} and {{credential:utility_portal:password}}...",
      "scheduled_time": "15:00",
      "enabled": true,
      "status": "pending"
    }
  ]
}
```

### Using Credential References in Tasks
In task instructions, reference stored credentials using:
```
{{credential:CREDENTIAL_ID:username}}
{{credential:CREDENTIAL_ID:password}}
```

Example:
```
Login with username {{credential:utility_portal:username}} and password {{credential:utility_portal:password}}
```

---

## Part 4: Testing

### Test Credential Retrieval
```bash
# Quick test (just checks if credential exists in keyring)
# Use the web UI: Click the checkmark icon next to credential

# Full login test (actually tries to login to portal)
python test_credential_login.py utility_portal
```

### Test Task Execution
```bash
# Run a task immediately (bypasses scheduler)
python run_task_now.py TASK_ID
```

### Check Logs
```bash
# View application logs
type portal_agent.log

# View Nova Act logs (if automation fails)
python check_nova_logs.py
```

---

## Part 5: Troubleshooting

### Issue: "Failed to fetch" when testing credentials
**Cause:** Nova Act conflicts with Flask debug mode  
**Solution:** Use the standalone test script instead:
```bash
python test_credential_login.py utility_portal
```

### Issue: Task shows "pending" but never runs
**Cause:** Scheduler started after the scheduled time  
**Solution:** Tasks only run at exact scheduled time. Either:
1. Reschedule task to future time
2. Run immediately: `python run_task_now.py TASK_ID`

### Issue: Credential not found
**Cause:** Credential not stored in Windows Credential Manager  
**Solution:** Re-add credential:
```bash
python credential_manager.py add
```

### Issue: Browser closes unexpectedly during automation
**Cause:** Nova Act/Playwright browser context issue  
**Solution:** 
1. Ensure Chrome/Chromium is installed
2. Run standalone scripts instead of through Flask
3. Check Nova Act logs for details

---

## Part 6: Project Structure

### Core V2 Files (Essential)
```
agent_dashboard_v2.py          # Main web dashboard
standalone_scheduler.py        # Background task scheduler
credential_manager.py          # Secure credential storage
auth_manager.py               # User authentication
database.py                   # SQLAlchemy models
requirements_v2.txt           # Python dependencies
```

### Templates (Essential)
```
templates/
├── base_v2.html              # Base template with Tailwind CSS
├── login_v2.html             # Login page
├── dashboard_v2.html         # Main dashboard
├── tasks_v2.html             # Task list
├── task_form_v2.html         # Task create/edit form
├── task_details_v2.html      # Task details
├── credentials.html          # Credential vault
├── credential_form.html      # Credential add form
├── users.html                # User management (admin)
├── profile.html              # User profile
└── error.html                # Error pages
```

### Automation Scripts (Working)
```
WORKING_simple_navigation_helper.py  # Production automation
nova_extract_and_recreate.py        # Data extraction
test_credential_login.py            # Credential testing
```

### Configuration Files
```
agent_config.json             # Task configuration (created on first run)
credentials_index.json        # Credential metadata (created on first add)
portal_agent.db              # SQLite database (created on first run)
```

### Legacy Files (Optional - Can be deleted)
```
app.py                       # Old Flask app
agent_dashboard.py           # V1 dashboard
templates/base.html          # V1 templates
templates/dashboard.html
templates/tasks.html
.ebextensions/               # AWS deployment configs
cloudformation/              # AWS infrastructure
```

---

## Part 7: Security Best Practices

### 1. Change Default Password
After first login, go to Profile → Change Password

### 2. Secure the Secret Key
In production, change the Flask secret key in `agent_dashboard_v2.py`:
```python
app.secret_key = 'your-secure-random-key-here'
```

### 3. Don't Commit Sensitive Files
Ensure `.gitignore` excludes:
- `portal_agent.db`
- `credentials_index.json`
- `agent_config.json`
- `*.log`

### 4. Backup Credentials
Windows Credential Manager stores credentials. To backup:
1. Export credentials manually from Credential Manager
2. Or re-add credentials on new machine

### 5. Use HTTPS in Production
For production deployment, use a proper WSGI server:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 agent_dashboard_v2:app
```

---

## Part 8: Quick Start Commands

### First Time Setup
```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/portal-automation-agent.git
cd portal-automation-agent
pip install -r requirements_v2.txt

# Initialize
python -c "from database import Database; Database()"

# Add credentials
python credential_manager.py add

# Start services
python agent_dashboard_v2.py  # Terminal 1
python standalone_scheduler.py  # Terminal 2
```

### Daily Usage
```bash
# Start dashboard (if not running)
python agent_dashboard_v2.py

# Access at http://localhost:5000
# Login: admin / admin123 (change on first login)
```

### Testing
```bash
# Test credential
python test_credential_login.py utility_portal

# Run task now
python run_task_now.py TASK_ID

# Check logs
type portal_agent.log
```

---

## Support

For issues or questions:
1. Check `portal_agent.log` for application logs
2. Check Nova Act logs: `python check_nova_logs.py`
3. Review this deployment guide
4. Check the README files: `README_V2.md`, `V2_QUICK_START.md`

---

## Version Information

- **Version:** 2.0
- **Python:** 3.9+
- **Framework:** Flask 2.3+
- **Automation:** Nova Act
- **Database:** SQLite with SQLAlchemy
- **Security:** bcrypt + Windows Credential Manager

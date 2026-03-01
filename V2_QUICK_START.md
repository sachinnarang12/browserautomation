# Portal Automation Agent V2.0 - Quick Start Guide

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements_v2.txt
```

### 2. Start the V2 Dashboard
```bash
python agent_dashboard_v2.py
```

The dashboard will start on **http://localhost:5000**

### 3. Login
- **Username**: `admin`
- **Password**: `admin123`
- ⚠️ **IMPORTANT**: Change this password immediately after first login!

---

## 📋 First Steps After Login

### Step 1: Change Default Password
1. Click on **Profile** in the sidebar
2. Enter current password: `admin123`
3. Enter your new secure password
4. Click **Update Password**

### Step 2: Add Your First Credential
1. Click on **Credentials** in the sidebar
2. Click **Add Credential** button
3. Fill in the form:
   - **Credential ID**: `utility_portal` (no spaces)
   - **Description**: `Livingston NJ Utility Portal`
   - **URL**: `https://livingstonnj.my360-app.com`
   - **Username**: `narang.sachin@gmail.com`
   - **Password**: `Testing1234!123`
4. Click **Save Credential**

✅ Your password is now encrypted and stored in Windows Credential Manager!

### Step 3: Migrate V1 Tasks (Optional)
If you have existing tasks from V1, run the migration tool:
```bash
python migrate_v1_to_v2.py
```

This will:
- Import all V1 tasks to the database
- Migrate credentials to secure keyring
- Backup your V1 configuration
- Update task instructions to use credential references

---

## 🔐 Security Features

### Credential Storage
- Passwords are **never** stored in plain text
- All credentials encrypted in **Windows Credential Manager**
- Only credential references stored in database
- Passwords retrieved securely at runtime

### User Authentication
- Password hashing with **bcrypt**
- Session management with **Flask-Login**
- "Remember me" functionality
- Secure logout

### Audit Trail
- All actions logged to database
- User activity tracking
- Task execution history

---

## 📖 Using Credentials in Tasks

### Old Way (V1 - Insecure)
```
Login with username: narang.sachin@gmail.com and password: Testing1234!123
```
❌ Password visible in plain text

### New Way (V2 - Secure)
```
Login with username {{credential:utility_portal:username}} and password {{credential:utility_portal:password}}
```
✅ Password stored securely in keyring

The system automatically replaces these placeholders at runtime!

---

## 🎯 Common Tasks

### View Dashboard
- Navigate to **Dashboard** to see:
  - Task statistics
  - Recent tasks
  - Upcoming scheduled tasks
  - System status

### Manage Tasks
1. Click **Tasks** in sidebar
2. View all tasks with status
3. Click on a task to see details
4. Run, edit, or delete tasks

### Manage Credentials
1. Click **Credentials** in sidebar
2. View all stored credentials
3. Add, test, or delete credentials
4. Copy usernames to clipboard

### User Management (Admin Only)
1. Click **Users** in sidebar
2. View all system users
3. Add or remove users
4. Manage user roles

---

## 🔧 Running the Scheduler

The scheduler runs tasks at their scheduled times. Start it separately:

```bash
python standalone_scheduler.py
```

⚠️ **Important**: Run the scheduler in a separate terminal from the dashboard!

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────┐
│     Web Dashboard (Port 5000)           │
│  - User Interface                       │
│  - Authentication                       │
│  - Credential Management                │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│     SQLite Database                     │
│  - Users                                │
│  - Tasks                                │
│  - Executions                           │
│  - Audit Logs                           │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│     Windows Credential Manager          │
│  - Encrypted Passwords                  │
│  - Secure Storage                       │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│     Standalone Scheduler                │
│  - Task Execution                       │
│  - Nova Act Integration                 │
│  - Error Handling                       │
└─────────────────────────────────────────┘
```

---

## 🆘 Troubleshooting

### Dashboard Won't Start
```bash
# Check if port 5000 is already in use
netstat -ano | findstr :5000

# Kill the process if needed
taskkill /PID <process_id> /F
```

### Can't Login
- Default credentials: `admin` / `admin123`
- If you changed password and forgot it, delete `portal_agent.db` to reset

### Credentials Not Working
```bash
# Test credential manager
python credential_manager.py list

# Add credential manually
python credential_manager.py add utility_portal narang.sachin@gmail.com Testing1234!123
```

### Tasks Not Executing
- Make sure `standalone_scheduler.py` is running
- Check `portal_agent.log` for errors
- Verify task is enabled in dashboard

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `agent_dashboard_v2.py` | Web dashboard application |
| `standalone_scheduler.py` | Task scheduler (run separately) |
| `portal_agent.db` | SQLite database |
| `portal_agent.log` | Application logs |
| `credential_manager.py` | CLI for credential management |
| `auth_manager.py` | CLI for user management |

---

## 🔄 Migrating from V1

### What Gets Migrated
- ✅ All tasks from `agent_config.json`
- ✅ Task schedules and settings
- ✅ Credentials extracted from instructions
- ✅ Task execution history

### What Stays the Same
- ✅ Nova Act integration
- ✅ Task execution logic
- ✅ Browser automation

### What Changes
- 🔐 Credentials now stored securely
- 📊 Database instead of JSON files
- 🎨 Modern UI with Tailwind CSS
- 👥 Multi-user support

---

## 📞 Next Steps

1. ✅ Login and change default password
2. ✅ Add your credentials
3. ✅ Migrate V1 tasks (if applicable)
4. ✅ Test credential management
5. ✅ Start the scheduler
6. ✅ Monitor task execution

---

## 🎉 You're Ready!

Your Portal Automation Agent V2.0 is now set up with:
- ✅ Secure credential storage
- ✅ User authentication
- ✅ Modern web interface
- ✅ Database backend
- ✅ Audit logging

Enjoy your secure, professional automation platform!

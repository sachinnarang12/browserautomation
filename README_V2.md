# Portal Automation Agent V2.0

> Professional automation platform with secure credential management, modern UI, and multi-user support

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 🎯 What's New in V2.0

### 🔐 Security First
- **Encrypted Credential Storage**: Passwords stored in Windows Credential Manager
- **User Authentication**: Secure login with bcrypt password hashing
- **Session Management**: Flask-Login integration with "remember me"
- **Audit Logging**: Complete activity tracking

### 🎨 Modern UI
- **Tailwind CSS**: Professional, responsive design
- **Intuitive Navigation**: Sidebar with clear sections
- **Real-time Updates**: Live task status monitoring
- **Mobile Friendly**: Works on all devices

### 📊 Database Backend
- **SQLAlchemy ORM**: Robust data management
- **SQLite Database**: No external dependencies
- **Relationships**: Proper foreign keys and constraints
- **Migration Tools**: Easy upgrade from V1

### 👥 Multi-User Support
- **User Management**: Admin can create/manage users
- **Role-Based Access**: Admin and user roles
- **Personal Profiles**: Each user manages their own settings

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_v2.txt
```

### 2. Start Dashboard
```bash
python agent_dashboard_v2.py
```

### 3. Login
- URL: **http://localhost:5000**
- Username: `admin`
- Password: `admin123`

### 4. Change Password
Navigate to Profile → Change Password

### 5. Add Credentials
Navigate to Credentials → Add Credential

---

## 📖 Documentation

- **[Quick Start Guide](V2_QUICK_START.md)** - Get up and running in 5 minutes
- **[Transformation Plan](V2_TRANSFORMATION_PLAN.md)** - Technical implementation details
- **[Progress Report](V2_PROGRESS.md)** - Current status and roadmap
- **[Product Roadmap](PRODUCT_ROADMAP_V2.md)** - Future features and enhancements

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Dashboard (Flask)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Authentication│  │   Tasks      │  │  Credentials │     │
│  │   & Users    │  │  Management  │  │    Vault     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   SQLite Database (SQLAlchemy)              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Users   │  │  Tasks   │  │Executions│  │AuditLogs │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│            Windows Credential Manager (Keyring)             │
│                  Encrypted Password Storage                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Standalone Scheduler (Background)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │Task Execution│  │  Nova Act    │  │Error Handling│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Security Features

### Credential Management
```python
# Old Way (V1) - INSECURE ❌
instructions = "Login with user@example.com and password MyPassword123"

# New Way (V2) - SECURE ✅
instructions = "Login with {{credential:portal:username}} and {{credential:portal:password}}"
```

### Password Storage
- ✅ Encrypted in Windows Credential Manager
- ✅ Never stored in plain text
- ✅ Never stored in database
- ✅ Only credential references in database
- ✅ Retrieved securely at runtime

### User Authentication
- ✅ Bcrypt password hashing
- ✅ Secure session management
- ✅ CSRF protection
- ✅ SQL injection prevention
- ✅ XSS protection

---

## 📁 Project Structure

```
portal-automation-agent/
├── agent_dashboard_v2.py          # Main dashboard application
├── standalone_scheduler.py        # Task scheduler (run separately)
├── credential_manager.py          # Credential management CLI
├── auth_manager.py               # User management CLI
├── database.py                   # Database models
├── migrate_v1_to_v2.py          # Migration tool
│
├── templates/                    # HTML templates
│   ├── base_v2.html             # Base template with sidebar
│   ├── login_v2.html            # Login page
│   ├── dashboard_v2.html        # Main dashboard
│   ├── tasks_v2.html            # Task list
│   ├── task_details_v2.html     # Task details
│   ├── credentials.html         # Credential vault
│   ├── credential_form.html     # Add credential
│   ├── users.html               # User management
│   ├── profile.html             # User profile
│   └── error.html               # Error pages
│
├── portal_agent.db              # SQLite database
├── portal_agent.log             # Application logs
│
├── requirements_v2.txt          # Python dependencies
├── README_V2.md                 # This file
├── V2_QUICK_START.md           # Quick start guide
└── V2_PROGRESS.md              # Progress tracking
```

---

## 🛠️ CLI Tools

### Credential Manager
```bash
# List all credentials
python credential_manager.py list

# Add a credential
python credential_manager.py add portal_id username password

# Get a credential
python credential_manager.py get portal_id

# Delete a credential
python credential_manager.py delete portal_id
```

### User Manager
```bash
# List all users
python auth_manager.py list

# Add a user
python auth_manager.py add username password

# Delete a user
python auth_manager.py delete username

# Change password
python auth_manager.py change-password username
```

---

## 🔄 Migrating from V1

### Automatic Migration
```bash
python migrate_v1_to_v2.py
```

This will:
1. ✅ Backup V1 configuration
2. ✅ Extract credentials from task instructions
3. ✅ Store credentials in Windows Credential Manager
4. ✅ Import tasks to database
5. ✅ Update task instructions with credential references
6. ✅ Verify migration success

### Manual Migration
If you prefer manual control:

1. **Add credentials manually**:
   ```bash
   python credential_manager.py add utility_portal user@example.com password123
   ```

2. **Update task instructions**:
   Replace plain-text credentials with:
   ```
   {{credential:utility_portal:username}}
   {{credential:utility_portal:password}}
   ```

3. **Import tasks via dashboard**:
   Use the web interface to create tasks

---

## 📊 Dashboard Features

### Dashboard Page
- Task statistics (total, pending, running, completed, failed)
- Recent tasks with status
- Upcoming scheduled tasks
- System status indicators

### Tasks Page
- List all tasks with filters
- Search functionality
- Task status badges
- Quick actions (view, edit, delete)

### Task Details Page
- Complete task information
- Execution history
- Schedule information
- Action buttons (run, edit, disable, delete)

### Credentials Page
- List all stored credentials
- Secure password display (masked)
- Add/delete credentials
- Copy username to clipboard
- Usage instructions

### Profile Page
- Account information
- Change password
- Last login tracking

### Users Page (Admin Only)
- List all users
- Add/remove users
- Manage user roles

---

## 🎯 Usage Examples

### Example 1: Utility Portal Automation
```python
# 1. Add credential
Credential ID: utility_portal
Username: narang.sachin@gmail.com
Password: Testing1234!123
URL: https://livingstonnj.my360-app.com

# 2. Create task
Name: Daily Usage Check
URL: https://livingstonnj.my360-app.com
Instructions: |
  1. Login with {{credential:utility_portal:username}} and {{credential:utility_portal:password}}
  2. Navigate to Usage section
  3. Export PDF report
Schedule: 08:00

# 3. Task runs automatically at 8 AM daily
```

### Example 2: Multiple Portal Automation
```python
# Add multiple credentials
python credential_manager.py add portal1 user1@example.com pass1
python credential_manager.py add portal2 user2@example.com pass2

# Create tasks using different credentials
Task 1: Uses {{credential:portal1:username}}
Task 2: Uses {{credential:portal2:username}}
```

---

## 🔧 Configuration

### Database Configuration
Edit `database.py` to change database settings:
```python
DATABASE_URL = 'sqlite:///portal_agent.db'
```

### Flask Configuration
Edit `agent_dashboard_v2.py`:
```python
app.secret_key = 'your-secret-key-here'  # Change in production!
```

### Scheduler Configuration
Edit `standalone_scheduler.py` for scheduling options

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process
taskkill /PID <process_id> /F
```

### Database Locked
```bash
# Stop all processes accessing the database
# Delete portal_agent.db-journal if it exists
```

### Credential Not Found
```bash
# List all credentials
python credential_manager.py list

# Re-add the credential
python credential_manager.py add <id> <username> <password>
```

### Task Not Executing
1. Check if scheduler is running
2. Verify task is enabled
3. Check `portal_agent.log` for errors
4. Verify credentials are correct

---

## 📈 Performance

- **Dashboard Load Time**: < 1 second
- **Task Execution**: Same as V1 (~57 seconds for utility portal)
- **Database Queries**: Optimized with SQLAlchemy
- **Credential Retrieval**: Instant from keyring

---

## 🔒 Security Best Practices

1. ✅ Change default admin password immediately
2. ✅ Use strong passwords (12+ characters)
3. ✅ Don't share credentials between users
4. ✅ Regularly review audit logs
5. ✅ Keep Python packages updated
6. ✅ Use HTTPS in production
7. ✅ Backup database regularly

---

## 🤝 Contributing

This is a personal automation project, but suggestions are welcome!

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🎉 Acknowledgments

- **Nova Act**: Browser automation framework
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Tailwind CSS**: UI framework
- **Keyring**: Secure credential storage

---

## 📞 Support

For issues or questions:
1. Check the documentation
2. Review `portal_agent.log`
3. Check the troubleshooting section

---

**Built with ❤️ for secure, reliable automation**

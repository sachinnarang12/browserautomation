# Portal Automation Agent V2

A secure, web-based automation agent for scheduling and executing browser automation tasks using Nova Act. Built with Flask, featuring credential management, task scheduling, and a modern web interface.

## Features

- 🔐 **Secure Credential Management**: Windows Credential Manager integration for encrypted password storage
- 📅 **Task Scheduling**: Schedule automation tasks to run at specific times
- 🌐 **Web Dashboard**: Modern, responsive UI built with Tailwind CSS
- 👤 **User Authentication**: Multi-user support with role-based access
- 🤖 **Nova Act Integration**: Browser automation for web scraping and interaction
- 📊 **Task Monitoring**: Real-time task status and execution history

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Windows OS (for Windows Credential Manager integration)
- Chrome/Chromium browser

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd portal-automation-agent
```

2. Install dependencies:
```bash
pip install -r requirements_v2.txt
```

3. Initialize the database:
```bash
python setup_v2.py
```

4. Start the dashboard:
```bash
python agent_dashboard_v2.py
```

5. Start the scheduler (in a separate terminal):
```bash
python standalone_scheduler.py
```

6. Access the dashboard at `http://localhost:5000`
   - Default login: `admin` / `admin123`
   - **Change the default password immediately!**

## Project Structure

```
portal-automation-agent/
├── agent_dashboard_v2.py      # Main web dashboard
├── standalone_scheduler.py     # Background task scheduler
├── credential_manager.py       # Secure credential storage
├── auth_manager.py            # User authentication
├── database.py                # Database models
├── portal_automation_agent.py # Task execution engine
├── templates/                 # HTML templates
│   ├── base_v2.html
│   ├── login_v2.html
│   ├── dashboard_v2.html
│   ├── tasks_v2.html
│   ├── credentials.html
│   └── ...
├── requirements_v2.txt        # Python dependencies
└── README_V2.md              # Detailed documentation
```

## Usage

### Adding Credentials

1. Navigate to **Credentials** in the dashboard
2. Click **Add Credential**
3. Fill in the credential details:
   - Credential ID (e.g., `utility_portal`)
   - Username
   - Password
   - Description
   - URL

Credentials are encrypted and stored in Windows Credential Manager.

### Creating Tasks

1. Navigate to **Tasks** in the dashboard
2. Click **Add Task**
3. Configure the task:
   - Name
   - URL
   - Instructions (use `{{credential:id:username}}` and `{{credential:id:password}}` placeholders)
   - Schedule time (HH:MM format)
   - Enable/disable

### Using Credentials in Tasks

Reference stored credentials in task instructions:

```
Login with username {{credential:utility_portal:username}} 
and password {{credential:utility_portal:password}}
```

The system automatically replaces these placeholders at runtime.

## Security

- Passwords are never stored in plain text
- All credentials encrypted in Windows Credential Manager
- User passwords hashed with bcrypt
- Session-based authentication with Flask-Login
- No sensitive data in configuration files

## Development

### Running Tests

```bash
# Test credential retrieval
python test_credential_login.py utility_portal

# Test Nova Act integration
python debug_nova.py
```

### Database Management

The SQLite database (`portal_agent.db`) stores:
- User accounts
- Task definitions (references only, no credentials)
- Execution history

To reset the database:
```bash
del portal_agent.db
python setup_v2.py
```

## Technology Stack

- **Backend**: Flask 2.3.3, Flask-Login
- **Database**: SQLAlchemy with SQLite
- **Automation**: Nova Act (browser automation)
- **Security**: bcrypt, Windows Credential Manager (keyring)
- **Frontend**: Tailwind CSS, Font Awesome
- **Scheduling**: Python schedule library

## Troubleshooting

### Task Not Running

- Check that `standalone_scheduler.py` is running
- Verify task is enabled in the dashboard
- Check task scheduled time hasn't passed

### Credential Test Fails

- Verify credential exists in Windows Credential Manager
- Run: `python credential_manager.py list`
- Test manually: `python test_credential_login.py <credential_id>`

### Browser Issues

- Ensure Chrome/Chromium is installed
- Check Nova Act API key is valid
- Review logs in `portal_agent.log`

## Contributing

This is a personal automation project. Feel free to fork and adapt for your needs.

## License

Private project - All rights reserved

## Acknowledgments

- Nova Act by Amazon for browser automation
- Flask community for the excellent web framework
- Tailwind CSS for the modern UI components

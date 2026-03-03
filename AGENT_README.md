# Portal Automation Agent

A flexible scheduling system for automating web portal tasks using Nova Act. This agent allows users to schedule multiple activities throughout the day with comprehensive status monitoring and reporting.

## 🚀 Features

- **Flexible Task Scheduling**: Schedule multiple portal automation tasks at different times
- **Nova Act Integration**: Powerful browser automation using Nova Act API
- **Web Dashboard**: User-friendly web interface for task management
- **CLI Interface**: Command-line tools for advanced users
- **Status Monitoring**: Real-time status reports and execution history
- **Error Handling**: Automatic retries and comprehensive error logging
- **Session Management**: Persistent browser sessions for manual verification

## 📋 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r agent_requirements.txt

# Verify Nova Act installation
python -c "from nova_act import NovaAct; print('Nova Act installed successfully')"
```

### 2. Basic Usage

#### Using the CLI Interface (Recommended)

```bash
# Add a new task interactively
python agent_cli.py add

# List all tasks
python agent_cli.py list

# Show status report
python agent_cli.py status

# Start the agent
python agent_cli.py start
```

#### Using the Web Dashboard

```bash
# Start the web dashboard
python agent_dashboard.py

# Open browser to http://localhost:5000
```

### 3. Example Task Creation

```bash
python agent_cli.py add
```

Follow the prompts:
- **Task name**: Daily Usage Report
- **Portal URL**: https://identity.my360-app.com/Account/Login?ReturnUrl=...
- **Scheduled time**: 09:00
- **Instructions**:
```
1. Login with username: YOUR_EMAIL and password: YOUR_PASSWORD
2. Wait for dashboard to load (10 seconds)
3. Select Active Home dropdown and choose "103892 0"
4. Navigate to Usage History section
5. Click More Details button
6. Click Export button and select PDF
7. Wait for download to complete
```

## 🛠️ Configuration

### Nova Act Configuration

The agent uses these default Nova Act settings:
- **API Key**: `YOUR_NOVA_ACT_API_KEY`
- **Browser**: Chrome/Chromium (headless=False for debugging)
- **Session Persistence**: Enabled for manual verification

### Task Configuration

Tasks are stored in `agent_config.json` with the following structure:

```json
{
  "tasks": [
    {
      "id": "task_1706789123_0",
      "name": "Daily Usage Report",
      "url": "https://portal.example.com",
      "instructions": "1. Login...\n2. Navigate...",
      "scheduled_time": "09:00",
      "status": "pending",
      "enabled": true,
      "max_retries": 3
    }
  ],
  "nova_config": {
    "headless": false,
    "tty": false,
    "nova_act_api_key": "YOUR_NOVA_ACT_API_KEY"
  }
}
```

## 📊 Monitoring and Status

### CLI Status Commands

```bash
# Show comprehensive status report
python agent_cli.py status

# List all tasks with current status
python agent_cli.py list

# Show detailed task information
python agent_cli.py details task_1706789123_0
```

### Web Dashboard

Access the web dashboard at `http://localhost:5000` for:
- Real-time status monitoring
- Visual task management
- Execution history
- Error reporting
- Agent control (start/stop)

### Status Report Example

```json
{
  "timestamp": "2026-02-01T18:30:00",
  "agent_status": "running",
  "total_tasks": 3,
  "active_sessions": 1,
  "task_statistics": {
    "pending": 2,
    "running": 1,
    "completed": 5,
    "failed": 0
  },
  "upcoming_tasks": [
    {
      "task_name": "Morning Report",
      "next_run": "2026-02-02T09:00:00",
      "time_until": "14:30:00"
    }
  ]
}
```

## 🔧 Advanced Usage

### Task Management

```bash
# Enable/disable tasks
python agent_cli.py enable task_1706789123_0
python agent_cli.py disable task_1706789123_0

# Delete tasks
python agent_cli.py delete task_1706789123_0

# View task details
python agent_cli.py details task_1706789123_0
```

### Programmatic Usage

```python
from portal_automation_agent import PortalAutomationAgent

# Create agent instance
agent = PortalAutomationAgent("my_config.json")

# Add a task
task_id = agent.add_task(
    name="Custom Task",
    url="https://example.com",
    instructions="1. Login\n2. Navigate\n3. Export",
    scheduled_time="14:30"
)

# Start the scheduler
agent.start_scheduler()

# Get status report
report = agent.get_status_report()
print(f"Agent status: {report['agent_status']}")
```

## 📝 Writing Effective Instructions

### Best Practices

1. **Be Specific**: Use exact element selectors and clear descriptions
2. **Include Wait Times**: Add appropriate delays for page loads
3. **Handle Errors**: Anticipate and handle common error scenarios
4. **Test Manually**: Verify instructions work manually before automation

### Example Instructions Template

```
1. Login with username: [USERNAME] and password: [PASSWORD]
2. Wait for dashboard to load (10 seconds)
3. Click on "[MENU_ITEM]" in the navigation menu
4. Select "[OPTION]" from the dropdown
5. Click the "[BUTTON_TEXT]" button
6. Wait for "[EXPECTED_ELEMENT]" to appear
7. Download/export the required data
8. Verify download completion
```

### Common Patterns

```bash
# Login sequence
1. Enter username in the email field
2. Enter password in the password field
3. Click "Login" button
4. Wait for redirect (5 seconds)

# Navigation sequence
1. Locate "[MENU]" menu item
2. Click to expand submenu
3. Select "[SUBMENU_ITEM]"
4. Wait for page load (3 seconds)

# Export sequence
1. Click "Export" or "Download" button
2. Select format (PDF/Excel/CSV)
3. Confirm export dialog
4. Wait for download to start
```

## 🚨 Error Handling

### Automatic Retries

- Tasks automatically retry up to 3 times on failure
- 5-minute delay between retry attempts
- Exponential backoff for persistent failures

### Common Issues

1. **Login Failures**: Check credentials and account status
2. **Element Not Found**: Verify selectors and page structure
3. **Timeout Errors**: Increase wait times for slow pages
4. **Download Issues**: Check browser download settings

### Debugging

```bash
# Check agent logs
tail -f portal_agent.log

# Test Nova Act integration
python debug_nova.py

# Verify task configuration
python agent_cli.py details task_id
```

## 🔒 Security Considerations

- **Credentials**: Store sensitive credentials securely
- **API Keys**: Protect Nova Act API key
- **Network**: Use HTTPS URLs when possible
- **Sessions**: Monitor active browser sessions
- **Logs**: Sanitize logs to remove sensitive data

## 📁 File Structure

```
portal_automation_agent.py    # Main agent class
agent_cli.py                 # Command-line interface
agent_dashboard.py           # Web dashboard
agent_config.json           # Task configuration (auto-generated)
portal_agent.log            # Execution logs
agent_requirements.txt      # Python dependencies
templates/                  # Web dashboard templates
├── base.html
├── dashboard.html
├── tasks.html
├── add_task.html
└── task_details.html
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of the Nova Act Utility Automation Project and follows the same licensing terms.

## 🆘 Support

For issues and questions:
1. Check the logs: `portal_agent.log`
2. Verify configuration: `agent_config.json`
3. Test Nova Act integration: `python debug_nova.py`
4. Review task instructions for accuracy

---

**Built with ❤️ using Nova Act and Python**
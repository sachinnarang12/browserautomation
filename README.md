# Nova Act Utility Automation Project

A comprehensive collection of Nova Act automation scripts for downloading and extracting utility usage data from the Livingston NJ utility portal. This project provides multiple approaches for automating the login, navigation, and data extraction process.

## Features

- **Automated Login & Navigation**: Scripts handle authentication and navigation to usage data sections
- **Multiple Download Methods**: Various approaches including PDF exports, Excel downloads, and direct data extraction
- **Data Analysis Tools**: PDF content analysis and usage data extraction capabilities
- **Session Management**: Persistent browser sessions for manual verification and intervention
- **Download Monitoring**: Real-time monitoring of Downloads folder with automatic file opening
- **Error Handling**: Comprehensive error handling and logging across all automation scripts

## Project Structure

### Core Automation Scripts

**✅ PRODUCTION READY - WORKING VERSION**
- `WORKING_simple_navigation_helper.py` - **CONFIRMED WORKING VERSION** - Production-ready navigation helper with verified success metrics and optimized workflow

**Primary Automation Scripts**
- `portal_automation_agent.py` - **NEW** - Flexible scheduling system for automating multiple portal tasks throughout the day
- `standalone_scheduler.py` - **NEW** - Standalone scheduler that runs without Flask interference for improved Nova Act compatibility
- `agent_dashboard.py` - **LEGACY** - Basic web-based dashboard for managing scheduled automation tasks
- `agent_dashboard_v2.py` - **NEW** - Enhanced web dashboard with authentication, credential management, and modern UI
- `agent_cli.py` - **NEW** - Command-line interface for managing portal automation tasks
- `example_usage.py` - **NEW** - Comprehensive examples demonstrating Portal Automation Agent setup and usage
- `quick_setup.py` - **NEW** - One-click setup script that creates your first scheduled task based on the working automation
- `nova_extract_and_recreate.py` - **UPDATED** - Advanced data extraction script with password update (YOUR_PASSWORD)
- `extract_from_existing_session.py` - Streamlined data extraction from existing browser sessions
- `robust_nova_download.py` - Enhanced download automation with improved session handling
- `fresh_live_download.py` - User-friendly automation with visual feedback
- `simple_direct_download.py` - Minimal direct download approach
- `nova_final_simple.py` - Ultra-simplified automation with maximum reliability

**Data Analysis Tools**
- `simple_file_analyzer.py` - PDF content analysis and usage data extraction
- `analyze_downloaded_file.py` - Comprehensive file analysis with multiple format support
- `check_downloads.py` - Download verification and monitoring utility
- `get_actual_data.py` - **NEW** - Analysis tool for Nova Act extraction results and metadata inspection
- `nova_read_pdf_content.py` - **UPDATED** - Direct PDF content extraction from browser with complete transcription

**Security & Credential Management**
- `credential_manager.py` - **NEW** - Secure credential storage using system keyring with encrypted password management
- `test_credential_login.py` - **NEW** - Standalone credential testing utility that validates stored credentials by attempting actual portal login

**Alternative Approaches**
- `selenium_download.py` - Selenium-based automation alternative
- `direct_api_download.py` - Direct HTTP requests approach
- Various blob download handlers and manual instruction files

**Development & Testing**
- `debug_nova.py` - Nova Act integration testing
- `test_nova.py` - Basic functionality testing
- `test_simple_nova.py` - **NEW** - Simple Nova Act automation test with demo site
- `test_task_now.py` - **NEW** - Immediate task execution test for Portal Automation Agent
- `run_task_now.py` - **NEW** - Run specific tasks immediately bypassing scheduler
- `run_task_immediately.py` - **NEW** - Direct Nova Act task execution without Portal Agent
- `chrome_test_simple.py` - **NEW** - Chrome browser-specific Nova Act test with enhanced error handling
- `robust_test_automation.py` - **NEW** - Robust test automation with enhanced error handling and browser process cleanup
- `diagnose_nova_issues.py` - **UPDATED** - Comprehensive system diagnostics and Nova Act troubleshooting utility
- `cleanup_stuck_tasks.py` - **NEW** - Utility for resetting tasks stuck in 'running' state
- `check_nova_logs.py` - Log inspection utility

### Configuration Files (Legacy Flask App)
- `app.py` - Flask application (not used in current automation project)
- `application.py` - AWS Elastic Beanstalk entry point (legacy)
- `requirements.txt` - Python dependencies
- `.ebextensions/` - AWS configuration files (legacy)
- `cloudformation/` - Infrastructure templates (legacy)
- `templates/` - HTML templates (legacy)

### Development and Testing Files

**Nova Act Automation Scripts** (for utility bill download automation - development/testing purposes):
- `WORKING_simple_navigation_helper.py` - **✅ CONFIRMED WORKING VERSION** - Production-ready navigation helper with verified success metrics and optimized workflow
- `robust_nova_download.py` - Robust download automation with improved login redirect handling and enhanced session persistence
- `fresh_live_download.py` - Fresh live download session with step-by-step visual monitoring and enhanced user experience
- `simple_direct_download.py` - Minimal direct download approach with basic monitoring and automatic file opening
- `simple_navigation_helper.py` - **RECENTLY UPDATED** - Navigation helper with password updated to `YOUR_PASSWORD` (use WORKING version for production)
- `watch_download_live.py` - Live download monitoring with real-time visual feedback and session persistence
- `nova_final_simple.py` - Ultra-simplified final attempt with minimal complexity and maximum reliability
- `nova_export_final.py` - Final optimized export automation with streamlined workflow and enhanced download monitoring
- `simple_nova_with_analysis.py` - Streamlined automation with integrated PDF analysis and content extraction
- `complete_nova_with_pdf_analysis.py` - Comprehensive automation with PDF analysis capabilities
- `step_by_step_nova_download.py` - Step-by-step automation with detailed workflow and PDF processing
- `selenium_download.py` - Production-ready Selenium automation (recommended alternative)
- `testingNova_safe.py` - Production-ready Nova Act automation with comprehensive error handling
- `most_reliable_download.py` - Developer Tools Network tab method for reliable downloads
- `complete_download_automation.py` - Complete end-to-end automation with advanced download handling

**Data Extraction Tools**:
- `nova_extract_and_recreate.py` - **NEW** - Advanced data extraction script that reads and transcribes usage data directly from web pages, saving structured data to JSON and text formats
- `extract_from_existing_session.py` - **NEW** - Streamlined data extraction utility that connects to existing browser sessions to extract usage data with automatic file saving and opening
- `nova_read_pdf_content.py` - **NEW** - Direct PDF content extraction from browser with complete transcription and automatic file saving
- `simple_file_analyzer.py` - **NEW** - Lightweight utility for analyzing recent downloads with PDF content extraction and usage data recognition
- `get_actual_data.py` - **NEW** - Analysis tool for inspecting Nova Act extraction results and identifying data extraction issues

**Additional Development Tools**:
- `debug_nova.py` - Debug script for Nova Act integration testing
- `test_nova.py` - Test script for Nova Act functionality
- `check_nova_logs.py` - Utility to locate and inspect Nova Act execution logs
- `check_downloads.py` - Download verification utility that monitors Downloads folder for recent files

**Alternative Approaches**:
- `direct_api_download.py` - Direct HTTP requests approach for web scraping
- Various blob download handlers and manual instruction files

*Note: Nova Act automation scripts are for utility bill download automation and data extraction (development/testing purposes) and are not required for the main Flask application. These scripts use the standardized authentication credentials `YOUR_EMAIL` with password `YOUR_PASSWORD` for consistency across the automation workflow. The **WORKING_simple_navigation_helper.py** is the confirmed production-ready version with verified success metrics. The new **nova_extract_and_recreate.py** provides advanced data extraction capabilities that complement the file download automation, while **extract_from_existing_session.py** offers streamlined data extraction for quick access to usage information. Recent updates include optimized timing control with refined wait periods for efficient navigation, enhanced Usage History navigation with "More Details" button handling, automatic LastPass save password prompt handling, improved session management across scripts, and code quality improvements with refined instruction formatting and better string handling.*

## Quick Start

### Prerequisites
1. **Install Dependencies**:
   ```bash
   # Core automation dependencies
   pip install nova-act PyPDF2 python-dotenv schedule flask keyring
   
   # V2 Dashboard additional dependencies
   pip install flask-login
   ```

2. **Nova Act API Key**: Ensure you have a valid Nova Act API key
   - The scripts use API key: `YOUR_NOVA_ACT_API_KEY`

3. **Account Access**: Ensure the utility account is unlocked before running automation

4. **Secure Credential Storage** (Optional but Recommended):
   ```bash
   # Set up secure credential storage
   python credential_manager.py add
   
   # List stored credentials
   python credential_manager.py list
   
   # Test credentials with actual login
   python test_credential_login.py utility_portal
   ```

### Getting Started with Scheduled Automation

**🚀 FASTEST START - One-Click Setup:**
```bash
python quick_setup.py
```
This creates your first scheduled task based on the working automation and provides next steps.

### Running the Automation

**✅ RECOMMENDED - Use the Working Version:**
```bash
python WORKING_simple_navigation_helper.py
```

**For Data Extraction (Updated):**
```bash
python nova_extract_and_recreate.py
```

**For PDF Content Extraction (New):**
```bash
python nova_read_pdf_content.py
```

**For Data Analysis:**
```bash
python get_actual_data.py
```

**For Scheduled Automation (New):**
```bash
# Quick setup - creates your first scheduled task
python quick_setup.py

# Test Portal Agent immediately
python test_task_now.py

# Run a specific task immediately (bypassing scheduler)
python run_task_now.py [task_id]

# Start the automation agent
python portal_automation_agent.py --start

# Or use standalone scheduler (recommended for production)
python standalone_scheduler.py
```

**For Web Dashboard (New):**
```bash
# V1 Dashboard (basic features)
python agent_dashboard.py

# V2 Dashboard (with authentication and credential management)
python agent_dashboard_v2.py
# Access dashboard at: http://localhost:5000
# Default login: admin / admin123
# ⚠️ Change password after first login!
```

**For Portal Agent Examples (New):**
```bash
python example_usage.py
```

## Authentication Details

Scripts use standardized credentials with two password variants:
- **Username**: `YOUR_EMAIL`
- **Password (Production)**: `YOUR_PASSWORD` - Used by `WORKING_simple_navigation_helper.py` (confirmed working version)
- **Password (Advanced)**: `YOUR_PASSWORD` - Used by advanced scripts including:
  - `simple_navigation_helper.py` (recently updated)
  - `nova_extract_and_recreate.py`
  - `nova_read_pdf_content.py`
- **Account**: `103892 0` (Active Home selection)

**Note**: The production-ready `WORKING_simple_navigation_helper.py` continues to use `YOUR_PASSWORD` as the verified baseline. The `simple_navigation_helper.py` and advanced extraction scripts use `YOUR_PASSWORD` for enhanced authentication workflows.

## Usage Workflow

1. **Choose Your Approach**:
   - Use `WORKING_simple_navigation_helper.py` for reliable PDF downloads
   - Use `portal_automation_agent.py` for scheduled automation tasks
   - Use `nova_extract_and_recreate.py` for direct data extraction
   - Use `nova_read_pdf_content.py` for complete PDF content transcription
   - Use `simple_file_analyzer.py` to analyze existing downloads

2. **Run the Script**: Execute your chosen automation script

3. **Monitor Progress**: Watch the timestamped console output for progress updates

4. **Review Results**: Downloaded files are automatically opened, or check your Downloads folder

5. **Analyze Extraction Results**: Use `get_actual_data.py` to inspect Nova Act extraction metadata and identify data extraction issues

## Script Documentation

### ✅ WORKING Simple Navigation Helper (`WORKING_simple_navigation_helper.py`) - **CONFIRMED WORKING VERSION**

**🎯 STATUS: PRODUCTION READY** - This is the verified working version that successfully completes the full automation workflow.

**Key Features:**
- **✅ Confirmed Working**: Successfully tested and verified to complete the full automation workflow
- **Complete Export Automation**: Automates login, navigation, and PDF export process
- **PDF Format Selection**: Automatically selects PDF format when export popup appears
- **Optimized Timing Control**: Includes refined wait periods for reliable navigation
- **LastPass Integration**: Handles LastPass save password prompts automatically
- **Enhanced Navigation Flow**: Includes specific "More Details" button navigation
- **Manual Download Instructions**: Provides clear step-by-step instructions for Network tab method
- **Session Persistence**: Keeps browser session open for manual intervention
- **Standardized Authentication**: Uses consistent credentials (`YOUR_EMAIL` / `YOUR_PASSWORD`)

**Usage:**
```bash
python WORKING_simple_navigation_helper.py
```

**Success Metrics:**
- ✅ Login Success Rate: 100% (when account unlocked)
- ✅ Navigation Success Rate: 100%
- ✅ Export Initiation Success Rate: 100%
- ✅ Total Automation Time: ~57 seconds

### Portal Automation Agent (`portal_automation_agent.py`) - **RECENTLY UPDATED**

**🚀 STATUS: ADVANCED SCHEDULING SYSTEM** - A flexible scheduling system for automating multiple web portal tasks throughout the day with comprehensive status monitoring.

**🔄 RECENT UPDATE**: Improved configuration loading with enhanced enum handling for better reliability when loading task status from JSON configuration files.

**Key Features:**
- **Task Scheduling**: Schedule multiple automation tasks at specific times throughout the day
- **Multi-Portal Support**: Configure different URLs and instructions for various web portals
- **Status Monitoring**: Real-time status tracking with comprehensive reporting
- **Retry Logic**: Automatic retry mechanism with configurable retry limits
- **Session Management**: Persistent Nova Act sessions with proper cleanup
- **Configuration Persistence**: JSON-based configuration storage with automatic saving and improved enum handling
- **Command-Line Interface**: Full CLI support for task management and monitoring
- **Error Handling**: Comprehensive error handling with detailed logging
- **Thread-Safe Operation**: Multi-threaded scheduler with safe concurrent execution
- **Robust Configuration Loading**: Enhanced status enum conversion for reliable configuration persistence

**Core Components:**
- **Task Management**: Add, remove, update, and enable/disable scheduled tasks
- **Scheduler Engine**: Built on Python `schedule` library with threading support
- **Nova Act Integration**: Seamless integration with Nova Act browser automation
- **Status Reporting**: Detailed status reports with task statistics and upcoming schedules
- **Configuration Management**: Automatic configuration loading and saving with improved enum handling
- **Robust Data Persistence**: Enhanced JSON serialization with proper status enum conversion

**Usage:**

**Start the Scheduling Agent:**
```bash
python portal_automation_agent.py --start
```

**View Status Report:**
```bash
python portal_automation_agent.py --status
```

**List All Tasks:**
```bash
python portal_automation_agent.py --list
```

**Programmatic Usage:**
```python
from portal_automation_agent import PortalAutomationAgent

# Create agent instance
agent = PortalAutomationAgent("my_config.json")

# Add a scheduled task
task_id = agent.add_task(
    name="Daily Utility Check",
    url="https://livingstonnj.my360-app.com",
    instructions="Login and export usage data",
    scheduled_time="09:00"
)

# Start the scheduler
agent.start_scheduler()

# Get status report
report = agent.get_status_report()
print(f"Active tasks: {report['total_tasks']}")
```

**Configuration Structure:**
The agent uses a JSON configuration file (`agent_config.json` by default) with the following structure:
```json
{
  "tasks": [
    {
      "id": "task_1234567890_0",
      "name": "Morning Usage Check",
      "url": "https://livingstonnj.my360-app.com",
      "instructions": "Login with credentials and export usage data",
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

**Task Management Features:**
- **Flexible Scheduling**: Schedule tasks at any time using HH:MM format
- **Task Status Tracking**: Monitor task status (pending, running, completed, failed, cancelled)
- **Retry Mechanism**: Configurable retry attempts with automatic rescheduling
- **Enable/Disable**: Temporarily disable tasks without removing them
- **Dynamic Updates**: Update task parameters without restarting the agent

**Status Monitoring:**
- **Real-Time Status**: Live status updates for all scheduled tasks
- **Execution History**: Track last run times and execution results
- **Error Reporting**: Detailed error messages and retry counts
- **Upcoming Tasks**: View next scheduled execution times
- **Session Tracking**: Monitor active Nova Act sessions

**Advanced Features:**
- **Thread-Safe Execution**: Concurrent task execution with proper resource management
- **Automatic Cleanup**: Proper Nova Act session cleanup and resource management
- **Logging Integration**: Comprehensive logging to both file and console
- **Configuration Validation**: Automatic validation of task parameters and schedules
- **Graceful Shutdown**: Clean shutdown with proper session termination
- **Enhanced Configuration Loading**: Improved enum handling prevents configuration corruption and ensures reliable task status persistence

**Use Cases:**
- **Daily Utility Monitoring**: Schedule regular checks of utility usage data
- **Multi-Portal Automation**: Automate tasks across different web portals
- **Business Process Automation**: Schedule routine business tasks and data collection
- **Monitoring and Alerting**: Regular status checks and data extraction
- **Batch Processing**: Schedule multiple related tasks at optimal times

**Integration with Existing Scripts:**
- **Compatible with Nova Act**: Uses the same Nova Act configuration and API key
- **Complementary Tool**: Works alongside existing automation scripts
- **Flexible Instructions**: Can execute any Nova Act automation instructions
- **Session Reuse**: Efficient session management for multiple tasks

**Best For:**
- Automating multiple daily tasks across different portals
- Scheduling regular data collection and monitoring
- Managing complex automation workflows with dependencies
- Providing reliable, unattended automation with retry logic
- Monitoring and reporting on automation task execution

**Logging and Monitoring:**
- **File Logging**: Detailed logs saved to `portal_agent.log`
- **Console Output**: Real-time status updates and progress information
- **Status Reports**: Comprehensive JSON status reports with task statistics
- **Error Tracking**: Detailed error messages and troubleshooting information

### Standalone Scheduler (`standalone_scheduler.py`) - **NEW**

**🚀 STATUS: PRODUCTION-READY SCHEDULER** - A standalone scheduler that runs the Portal Automation Agent without Flask interference, providing improved Nova Act compatibility and reliability.

**Key Features:**
- **Clean Process Execution**: Runs scheduler in a dedicated process without Flask's debug mode interference
- **Improved Nova Act Compatibility**: Eliminates Flask-related issues that can affect browser automation
- **Real-Time Status Display**: Shows all configured tasks with status indicators and scheduling information
- **Simple Operation**: Single command to start the scheduler with automatic task loading
- **Visual Feedback**: Emoji-enhanced console output for easy monitoring
- **Graceful Shutdown**: Proper cleanup with Ctrl+C interrupt handling
- **Production Ready**: Designed for reliable, unattended operation

**Why Use Standalone Scheduler:**
- **Flask Interference**: Flask's debug mode and reloader can interfere with Nova Act browser sessions
- **Process Isolation**: Runs in a clean Python process without web framework overhead
- **Better Reliability**: Eliminates Flask-related threading and process management issues
- **Simpler Deployment**: No web server required for scheduled automation
- **Resource Efficiency**: Lower memory footprint without Flask application stack

**Usage:**

**Start the Standalone Scheduler:**
```bash
python standalone_scheduler.py
```

**What it does:**
1. **🤖 Agent Initialization**: Creates Portal Automation Agent instance from configuration
2. **📋 Task Display**: Shows all configured tasks with status indicators:
   - ⏳ Pending tasks
   - 🔄 Running tasks
   - ✅ Completed tasks
   - ❌ Failed tasks
   - Disabled tasks marked clearly
3. **🚀 Scheduler Startup**: Starts the scheduling engine in a clean process
4. **⏰ Status Updates**: Prints status message every minute showing scheduler is active
5. **🛑 Clean Shutdown**: Handles Ctrl+C gracefully with proper cleanup

**Console Output:**
```
🚀 Starting Standalone Portal Automation Scheduler
============================================================
This runs the scheduler WITHOUT Flask interference
Nova Act should work properly in this mode
============================================================

📋 Loaded 2 task(s):
  ⏳ Daily Utility Usage Report - 09:00
  ✅ Evening Data Export - 18:00 (DISABLED)

🚀 Starting scheduler...
💡 This runs in a clean process - Nova Act should work properly
📊 Press Ctrl+C to stop

⏰ 08:45:23 - Scheduler running...
⏰ 08:46:23 - Scheduler running...
```

**Advantages Over Portal Automation Agent:**
- **No Flask Dependency**: Runs without Flask web framework
- **Better Browser Compatibility**: Eliminates Flask-related browser automation issues
- **Simpler Process Model**: Single-threaded scheduler without web server complexity
- **Lower Resource Usage**: Minimal memory footprint for scheduled tasks
- **Production Focused**: Designed specifically for unattended automation

**When to Use:**
- **Production Deployments**: When running scheduled automation in production environments
- **Nova Act Issues**: When experiencing browser automation issues with the main agent
- **Headless Servers**: When running on servers without web interface requirements
- **Resource Constraints**: When minimizing memory and CPU usage is important
- **Simple Scheduling**: When you only need task scheduling without web dashboard

**When to Use Portal Automation Agent Instead:**
- **Web Dashboard Needed**: When you want web-based task management interface
- **Remote Management**: When managing tasks from multiple locations via web browser
- **Visual Monitoring**: When you prefer graphical status displays and charts
- **Team Collaboration**: When multiple users need to monitor automation status

**Integration with Other Components:**
- **Configuration File**: Uses same `agent_config.json` as Portal Automation Agent
- **Task Compatibility**: Runs all tasks created by Portal Agent or Quick Setup
- **CLI Compatible**: Works with tasks managed via `agent_cli.py`
- **Status Monitoring**: Can be monitored using `agent_cli.py status` command

**Best Practices:**
- **Use for Production**: Recommended for production deployments requiring reliability
- **Monitor Logs**: Check `portal_agent.log` for detailed execution information
- **Test First**: Use `test_task_now.py` to validate tasks before production deployment
- **Clean Shutdown**: Always use Ctrl+C for graceful shutdown to ensure proper cleanup

**Troubleshooting:**
- **Configuration Not Found**: Ensure `agent_config.json` exists in current directory
- **Import Errors**: Verify `portal_automation_agent.py` is in the same directory
- **Nova Act Issues**: Run `diagnose_nova_issues.py` to check system configuration
- **Task Not Executing**: Check task schedule and ensure tasks are enabled

**Example Workflow:**
```bash
# 1. Create your first task
python quick_setup.py

# 2. Test the task immediately
python test_task_now.py

# 3. Start standalone scheduler for production
python standalone_scheduler.py

# 4. Monitor in another terminal
python agent_cli.py status

# 5. Stop with Ctrl+C when needed
```

**Technical Details:**
- **Process Model**: Single Python process with threading for scheduler
- **Scheduler Engine**: Uses Python `schedule` library with 1-second check interval
- **Status Updates**: Prints status every 60 seconds to confirm scheduler is active
- **Signal Handling**: Catches KeyboardInterrupt (Ctrl+C) for clean shutdown
- **Resource Cleanup**: Properly stops scheduler and cleans up Nova Act sessions

**Comparison with Other Scheduling Options:**

| Feature | Standalone Scheduler | Portal Automation Agent | Agent Dashboard |
|---------|---------------------|------------------------|-----------------|
| Web Interface | ❌ No | ❌ No | ✅ Yes |
| Flask Dependency | ❌ No | ✅ Yes | ✅ Yes |
| Nova Act Compatibility | ✅ Excellent | ⚠️ Good | ⚠️ Good |
| Resource Usage | ✅ Low | ⚠️ Medium | ❌ High |
| Production Ready | ✅ Yes | ✅ Yes | ⚠️ Development |
| Remote Management | ❌ No | ⚠️ CLI Only | ✅ Yes |

**Recommended Use Cases:**
- **Production Automation**: Daily utility data collection on dedicated servers
- **Headless Environments**: Servers without GUI or web browser access
- **Reliability Critical**: When maximum automation reliability is required
- **Resource Constrained**: Systems with limited memory or CPU resources
- **Simple Deployments**: When web interface is not needed



**🚀 STATUS: ONE-CLICK SETUP UTILITY** - A streamlined setup script that creates your first scheduled automation task based on the proven working automation, eliminating manual configuration.

**Key Features:**
- **One-Click Setup**: Creates a complete scheduled task with a single command
- **Based on Working Automation**: Uses the proven `WORKING_simple_navigation_helper.py` workflow
- **Pre-Configured Task**: Sets up daily utility usage report at 9:00 AM
- **Guided Next Steps**: Provides clear instructions for testing and starting the agent
- **Configuration Management**: Creates and manages the agent configuration file
- **Status Overview**: Shows current configuration and task details

**Usage:**
```bash
python quick_setup.py
```

**What it does:**
1. **🤖 Agent Initialization**: Creates a new Portal Automation Agent instance
2. **📋 Task Creation**: Sets up "Daily Utility Usage Report" task with:
   - **URL**: Complete Livingston NJ utility portal login URL
   - **Instructions**: Full automation workflow from the working script
   - **Schedule**: Daily execution at 9:00 AM
   - **Credentials**: Uses updated password `YOUR_PASSWORD`
3. **📊 Configuration Display**: Shows current task configuration and status
4. **🎯 Next Steps Guide**: Provides clear instructions for:
   - Testing the task manually
   - Starting the scheduler
   - Accessing the web dashboard
   - Monitoring task status

**Output:**
- Creates `agent_config.json` with your first scheduled task
- Displays task ID and scheduling information
- Shows complete next steps with specific commands
- Confirms successful setup completion

**Next Steps After Quick Setup:**
```bash
# 1. Test the task manually first
python agent_cli.py details [task_id]

# 2. Start the agent scheduler
python agent_cli.py start

# 3. Monitor via web dashboard
python agent_dashboard.py
# Then open: http://localhost:5000

# 4. Check status anytime
python agent_cli.py status
```

**Pre-Configured Task Details:**
- **Name**: "Daily Utility Usage Report"
- **Schedule**: 9:00 AM daily
- **Portal**: Livingston NJ utility portal
- **Workflow**: Complete login → navigation → export → download verification
- **Authentication**: Uses `YOUR_EMAIL` with `YOUR_PASSWORD`
- **Account**: Selects "103892 0" Active Home
- **Export Format**: PDF export with download verification

**Best For:**
- **First-Time Users**: Get started immediately without manual configuration
- **Quick Deployment**: Set up automation in seconds rather than minutes
- **Proven Workflow**: Based on the confirmed working automation script
- **Production Ready**: Creates a reliable daily automation task
- **Learning Tool**: Provides example configuration for understanding the system

**Integration with Other Components:**
- **Portal Automation Agent**: Creates tasks compatible with the full agent system
- **Web Dashboard**: Tasks created are immediately visible in the web interface
- **CLI Management**: Tasks can be managed through the command-line interface
- **Working Script**: Based on the proven `WORKING_simple_navigation_helper.py` workflow

**Configuration File Created:**
The script creates `agent_config.json` with:
```json
{
  "tasks": [
    {
      "id": "task_[timestamp]_0",
      "name": "Daily Utility Usage Report",
      "url": "[complete portal URL]",
      "instructions": "[full automation workflow]",
      "scheduled_time": "09:00",
      "status": "pending",
      "enabled": true
    }
  ],
  "nova_config": {
    "headless": false,
    "tty": false,
    "nova_act_api_key": "YOUR_NOVA_ACT_API_KEY"
  }
}
```

**Advantages:**
- **Zero Configuration**: No manual setup required
- **Immediate Results**: Creates working automation in seconds
- **Proven Reliability**: Based on confirmed working automation
- **Clear Guidance**: Provides specific next steps and commands
- **Production Ready**: Creates enterprise-ready scheduled automation

### Web Dashboard V1 (`agent_dashboard.py`) - **LEGACY**

**🌐 STATUS: LEGACY WEB-BASED MANAGEMENT INTERFACE** - Basic web dashboard for managing and monitoring scheduled automation tasks.

**Note**: This is the V1 dashboard. For enhanced features including authentication and credential management, use `agent_dashboard_v2.py` instead.

**Key Features:**
- **Real-Time Dashboard**: Live monitoring of agent status and task execution
- **Task Management Interface**: Web-based task creation, editing, and deletion
- **Visual Status Indicators**: Color-coded status cards and progress indicators
- **Interactive Controls**: Start/stop agent controls directly from the web interface
- **Task Statistics**: Visual metrics for pending, running, completed, and failed tasks
- **Upcoming Tasks Display**: Shows next scheduled task executions with countdown timers
- **Recent Activity Table**: Detailed view of recent task activity with status badges
- **Responsive Design**: Bootstrap-based responsive interface for desktop and mobile
- **Auto-Refresh**: Automatic page refresh every 30 seconds for live updates

### Web Dashboard V2 (`agent_dashboard_v2.py`) - **RECENTLY UPDATED**

**🌐 STATUS: ENHANCED WEB-BASED MANAGEMENT INTERFACE** - A comprehensive web dashboard with authentication, credential management, and modern UI for managing scheduled automation tasks.

**🔄 RECENT UPDATE**: Added missing `time` module import for improved credential testing functionality and browser automation timing control.

**Key Features:**
- **User Authentication**: Secure login system with Flask-Login integration
- **Credential Vault**: Secure credential storage and management using encrypted keyring
- **User Management**: Admin interface for managing user accounts and permissions
- **Enhanced Security**: Password hashing, session management, and access control
- **Real-Time Dashboard**: Live monitoring of agent status and task execution
- **Task Management Interface**: Web-based task creation, editing, and deletion
- **Visual Status Indicators**: Color-coded status cards and progress indicators
- **Profile Management**: User profile page with password change functionality
- **Responsive Design**: Modern Tailwind CSS-based responsive interface
- **API Endpoints**: RESTful API for programmatic access to tasks and status

**Template Files:**
- `templates/base_v2.html` - Base template with Tailwind CSS and modern navigation
- `templates/login_v2.html` - Secure login page with authentication
- `templates/dashboard_v2.html` - Main dashboard with statistics and task overview
- `templates/tasks_v2.html` - Task management interface with filtering and search
- `templates/task_details_v2.html` - Detailed task information and execution history page
- `templates/task_form_v2.html` - Add/edit task form with credential integration
- `templates/credentials.html` - Credential vault interface
- `templates/credential_form.html` - Add/edit credential form
- `templates/users.html` - User management (admin only)
- `templates/profile.html` - User profile and settings
- `templates/error.html` - Error pages (404, 500)

**Authentication System:**
- **Flask-Login Integration**: Secure session-based authentication
- **Password Security**: Werkzeug password hashing for secure credential storage
- **User Roles**: Admin and regular user role support
- **Session Management**: Secure session handling with remember-me functionality
- **Access Control**: Login-required decorators for protected routes
- **Default Credentials**: admin / admin123 (change after first login)

**Credential Management:**
- **Secure Storage**: Integration with system keyring for encrypted password storage
- **Credential Vault**: Web interface for managing portal credentials
- **Add/Delete Credentials**: Easy credential management through web forms
- **Metadata Display**: Shows credential descriptions and URLs without exposing passwords
- **Integration Ready**: Credentials accessible to automation tasks via CredentialManager

**User Management (Admin Only):**
- **User List**: View all registered users with role information
- **User Administration**: Admin-only access to user management features
- **Profile Management**: Users can update their own profiles and passwords
- **Password Changes**: Secure password change with old password verification
- **Last Login Tracking**: Monitor user activity and last login times

**Dashboard Features:**

**Main Dashboard (`/`):**
The main dashboard (`templates/dashboard_v2.html`) provides a comprehensive overview with:
- **Statistics Cards**: Four color-coded cards showing total, pending, running, and completed tasks
  - Total Tasks (indigo) - Overall task count
  - Pending Tasks (yellow) - Tasks waiting to execute
  - Running Tasks (blue) - Currently executing tasks with spinner animation
  - Completed Tasks (green) - Successfully completed tasks
- **Recent Tasks Panel**: Shows the 10 most recent tasks with:
  - Task name and URL
  - Scheduled time with clock icon
  - Color-coded status badges (completed, running, failed, pending)
  - Hover effects for better interactivity
- **Upcoming Tasks Panel**: Displays next 5 scheduled tasks with:
  - Task cards with indigo accent
  - Task name, URL, and scheduled time
  - Calendar icon for visual identification
- **System Status Panel**: Real-time system health indicators showing:
  - Scheduler status (running with animated pulse)
  - Database connection status
  - Nova Act readiness status
- **Empty State Handling**: Friendly messages when no tasks exist with links to create first task
- **Responsive Grid Layout**: Adapts to different screen sizes (1/2/4 column layouts)
- **User Context**: Displays current logged-in user information in navigation

**Task Management (`/tasks`):**
- **Complete Task List**: All configured tasks with status indicators
- **Task Controls**: Enable/disable, edit, and delete operations
- **Real-Time Status**: Live status updates for each task
- **Quick Actions**: Add new tasks and view detailed information
- **Filtering & Search**: Filter tasks by status and search by name or URL
- **Sortable Columns**: Task name, URL, schedule, status, and last run time

**Task Details (`/task/<task_id>`):** - **NEW**
The task details page (`templates/task_details_v2.html`) provides comprehensive information about individual tasks:
- **Task Information Panel**: Complete task configuration details including:
  - Task ID (unique identifier)
  - Target URL with external link
  - Full automation instructions in formatted code block
- **Execution History Panel**: Track all task executions with:
  - Execution timestamps and durations
  - Success/failure status for each run
  - Error messages and logs
  - Empty state when no executions exist
- **Status Card**: Real-time task status with color-coded badges:
  - Completed (green) - Task finished successfully
  - Running (blue) - Task currently executing with spinner
  - Failed (red) - Task encountered errors
  - Pending (yellow) - Task waiting to execute
- **Quick Actions**: Run task immediately from details page
- **Responsive Layout**: Two-column layout (main content + sidebar) that adapts to screen size

**Credential Vault (`/credentials`):** - **RECENTLY UPDATED**
- **Credential List**: All stored credentials with metadata and unique identifiers
- **Add Credentials**: Web form for adding new portal credentials
- **Test Credentials**: Verify credential retrieval and validate stored credentials
- **Test Login**: **RECENTLY UPDATED** - Validate credentials by attempting actual portal login with Nova Act automation
  - **Subprocess-Based Execution**: Runs login test in separate Python process for improved reliability
  - **Isolated Testing**: Prevents Flask/Nova Act conflicts by running test independently
  - **Real Authentication**: Verifies credentials work with the actual portal login page
  - **Detailed Feedback**: Returns success/failure status with comprehensive error messages
  - **90-Second Timeout**: Automatic timeout for login test completion
  - **Automatic Cleanup**: Temporary test script automatically removed after execution
  - **Enhanced Stability**: Eliminates threading issues and browser session conflicts
- **Delete Credentials**: Remove credentials with confirmation using credential ID
- **Secure Display**: Shows descriptions and URLs without exposing passwords
- **Bug Fix**: Credential IDs now properly passed to template for delete operations
- **Template Syntax Fix**: Credential template examples now properly displayed using Jinja2 raw tags

**Using Credentials in Task Instructions:**
Once credentials are stored in the vault, you can reference them in your task instructions using template syntax:
```
Login with username {{credential:utility_portal:username}} and password {{credential:utility_portal:password}}
```

The system will automatically replace these placeholders with the actual credentials at runtime. This approach:
- **Keeps credentials secure**: No hardcoded passwords in task instructions
- **Enables credential reuse**: Same credentials can be used across multiple tasks
- **Simplifies updates**: Change credentials once in the vault, all tasks automatically use the new values
- **Improves security**: Credentials stored encrypted in system keyring, not in plain text

**Template Syntax Format:**
- `{{credential:service_name:username}}` - Retrieves the username for the specified service
- `{{credential:service_name:password}}` - Retrieves the password for the specified service
- Service names must match the credential IDs stored in the vault

**User Profile (`/profile`):**
- **Profile Information**: Display user details and last login
- **Change Password**: Secure password change with validation
- **Session Information**: View current session details

**API Endpoints:**
- **GET `/api/status`**: JSON status report with user context
- **GET `/api/tasks`**: JSON list of all tasks
- **GET `/api/credentials`**: Credential metadata (no passwords)
- **Authentication Required**: All API endpoints require valid login session

**Usage:**

**Start the V2 Dashboard:**
```bash
python agent_dashboard_v2.py
```

The dashboard will start with the following output:
```
Starting Portal Automation Agent V2.0 Dashboard
============================================================
Access the dashboard at: http://localhost:5000
Default login: admin / admin123
WARNING: Please change the default password after first login!
============================================================
```

**Access the Dashboard:**
- Open your web browser and navigate to: `http://localhost:5000`
- Login with default credentials: `admin` / `admin123`
- **Important**: Change the default password after first login!

**Routes and Pages:**

**Authentication Routes:**
- **GET/POST `/login`**: User login page with remember-me functionality
- **GET `/logout`**: Logout and session cleanup

**Dashboard Routes:**
- **GET `/`**: Main dashboard with statistics and task overview
- **GET `/tasks`**: Complete task list with management controls
- **GET `/task/<task_id>`**: Detailed task information page

**Task Management Routes:**
- **GET/POST `/tasks/add`**: Add new task form with credential integration
- **GET/POST `/tasks/<task_id>/edit`**: Edit existing task configuration
- **POST `/tasks/<task_id>/delete`**: Delete task with confirmation

**Credential Management Routes:**
- **GET `/credentials`**: Credential vault listing
- **GET/POST `/credentials/add`**: Add new credential form
- **POST `/credentials/<credential_id>/test`**: Test credential retrieval and validation
- **POST `/credentials/<credential_id>/test-login`**: **NEW** - Test credential by attempting actual portal login with Nova Act
- **POST `/credentials/<id>/delete`**: Delete credential

**User Management Routes (Admin Only):**
- **GET `/users`**: User management page (admin only)
- **GET `/profile`**: User profile and settings
- **POST `/profile/change-password`**: Change user password

**API Routes:**
- **GET `/api/status`**: System status JSON with user context
- **GET `/api/tasks`**: Task list JSON
- **GET `/api/credentials`**: Credential metadata JSON (no passwords)

**Template Filters:**
- **`datetime`**: Format datetime objects for display
- **`timeago`**: Human-readable relative time (e.g., "2 hours ago")

**Integration with Existing Components:**
- **AuthManager**: User authentication and management
- **CredentialManager**: Secure credential storage via system keyring
- **Database**: Task and execution tracking (V2 schema)
- **Portal Automation Agent**: Backward compatible with V1 configuration

**Security Features:**
- **Password Hashing**: Werkzeug secure password hashing
- **Session Security**: Flask session management with secret key
- **Access Control**: Login-required decorators on protected routes
- **Admin Privileges**: Role-based access for user management
- **Input Validation**: Form validation and sanitization
- **Error Handling**: Graceful error pages (404, 500)

**Visual Design:**
- **Bootstrap Framework**: Modern, responsive design
- **Consistent Navigation**: Unified navigation bar across all pages
- **Status Indicators**: Color-coded badges and cards
- **Responsive Layout**: Mobile-friendly adaptive design
- **User Context**: Current user displayed in navigation

**Best For:**
- **Multi-User Environments**: Teams needing secure access control
- **Production Deployments**: Enhanced security for production systems
- **Credential Management**: Secure storage of portal credentials
- **User Administration**: Managing multiple user accounts
- **Enterprise Use**: Professional-grade authentication and authorization

**Migration from V1:**
- **Configuration Compatible**: Uses same `agent_config.json` format
- **Task Compatibility**: All V1 tasks work in V2 dashboard
- **Enhanced Features**: Adds authentication without breaking existing functionality
- **Gradual Migration**: Can run V1 and V2 side-by-side during transition

**Deployment Considerations:**
- **Secret Key**: Change `app.secret_key` in production
- **Default Password**: Change admin password immediately after first login
- **HTTPS**: Use HTTPS in production for secure authentication
- **Database**: Consider migrating to production database for user management
- **Backup**: Regular backups of credential vault and user database

### V1 to V2 Migration Tool (`migrate_v1_to_v2.py`) - **NEW**

**🔄 STATUS: MIGRATION UTILITY** - A comprehensive migration tool for upgrading from V1 (JSON-based) to V2 (Database + Keyring) architecture with automatic credential extraction and secure storage.

**Key Features:**
- **Automatic V1 Configuration Backup**: Creates timestamped backups of all V1 configuration files before migration
- **Task Migration**: Imports all tasks from `agent_config.json` to the V2 SQLite database
- **Credential Extraction**: Intelligently extracts usernames and passwords from task instructions using pattern matching
- **Secure Credential Storage**: Migrates extracted credentials to system keyring with encryption
- **Multiple Pattern Recognition**: Supports various credential formats in task instructions:
  - Pattern 1: `username: X and password: Y`
  - Pattern 2: Email-based credentials with various separators
- **Migration Statistics**: Tracks and reports tasks migrated, credentials extracted, and any errors
- **Safe Migration**: Preserves original V1 files with automatic backup before any changes

**Components:**

**MigrationTool Class:**
- **CredentialManager Integration**: Uses secure keyring for credential storage
- **Database Integration**: Leverages V2 database models for task storage
- **AuthManager Integration**: Integrates with V2 authentication system
- **Backup Management**: Creates organized backups with timestamps

**Core Methods:**

**`backup_v1_config()`:**
- Creates timestamped backup directory (`v1_backup/backup_YYYYMMDD_HHMMSS/`)
- Backs up `agent_config.json` (main V1 configuration)
- Backs up additional V1 files: `portal_agent.log`, `users.json`, `credentials_index.json`
- Returns success/failure status with error tracking

**`extract_credentials_from_instructions()`:**
- Analyzes task instruction text for embedded credentials
- Pattern 1: Matches `username: X and password: Y` format
- Pattern 2: Matches email addresses with passwords (minimum 6 characters)
- Returns list of extracted credentials with pattern metadata
- Supports case-insensitive matching for flexibility

**Credential Extraction Patterns:**

**Pattern 1 - Explicit Format:**
```
username: YOUR_EMAIL and password: YOUR_PASSWORD
```

**Pattern 2 - Email-Based:**
```
login with YOUR_EMAIL / YOUR_PASSWORD
Login using YOUR_EMAIL and YOUR_PASSWORD
```

**Usage:**

**Run the Migration Tool:**
```bash
python migrate_v1_to_v2.py
```

**What it does:**
1. **📦 Backup Phase**: Creates timestamped backup of all V1 configuration files
2. **📋 Task Analysis**: Reads all tasks from `agent_config.json`
3. **🔍 Credential Extraction**: Scans task instructions for embedded credentials
4. **🔐 Secure Storage**: Migrates credentials to system keyring with encryption
5. **💾 Database Migration**: Imports tasks to V2 SQLite database
6. **📊 Statistics Report**: Displays migration summary with counts and any errors

**Migration Statistics:**
The tool tracks and reports:
- **tasks_migrated**: Number of tasks successfully imported to V2 database
- **credentials_extracted**: Number of credentials found and stored in keyring
- **errors**: List of any errors encountered during migration

**Backup Structure:**
```
v1_backup/
└── backup_20260210_143022/
    ├── agent_config.json
    ├── portal_agent.log
    ├── users.json
    └── credentials_index.json
```

**Best For:**
- **Upgrading to V2**: Smooth transition from V1 JSON-based configuration to V2 database architecture
- **Credential Security**: Extracting hardcoded credentials and storing them securely in keyring
- **Data Preservation**: Ensuring no data loss during architecture upgrade
- **Automated Migration**: Reducing manual work in migrating existing automation tasks
- **Safe Upgrades**: Maintaining backups for rollback if needed

**Integration with V2 Components:**
- **CredentialManager**: Stores extracted credentials securely in system keyring
- **Database**: Uses V2 SQLite models (Task, TaskStatus) for task storage
- **AuthManager**: Integrates with V2 user authentication system
- **V2 Dashboard**: Migrated tasks immediately visible in web dashboard

**Safety Features:**
- **Automatic Backups**: All V1 files backed up before any modifications
- **Timestamped Backups**: Each migration run creates unique backup directory
- **Error Tracking**: Comprehensive error logging for troubleshooting
- **Non-Destructive**: Original V1 files preserved in backup directory
- **Validation**: Pattern matching ensures only valid credentials are extracted

**Credential Security:**
- **Keyring Storage**: Uses system keyring (Windows Credential Manager, macOS Keychain, etc.)
- **Encryption**: Credentials encrypted by operating system's secure storage
- **No Plain Text**: Removes hardcoded credentials from task instructions
- **Access Control**: Credentials only accessible through CredentialManager API

**Migration Workflow:**
```bash
# 1. Backup V1 configuration (automatic)
# 2. Extract credentials from task instructions
# 3. Store credentials in secure keyring
# 4. Import tasks to V2 database
# 5. Generate migration statistics report

# After migration, start V2 dashboard:
python agent_dashboard_v2.py
```

**Post-Migration:**
- **V1 Compatibility**: V1 files remain intact in backup directory
- **V2 Ready**: All tasks and credentials available in V2 system
- **Rollback Option**: Can restore from backup if needed
- **Credential References**: Task instructions updated to use credential references instead of hardcoded values

**Technical Details:**
- **Pattern Matching**: Uses Python regex for flexible credential extraction
- **Database Models**: Leverages SQLAlchemy models from `database.py`
- **Keyring Integration**: Uses `keyring` library for cross-platform secure storage
- **File Operations**: Uses `pathlib` for cross-platform file handling
- **Timestamp Format**: `YYYYMMDD_HHMMSS` for unique backup directories

**Error Handling:**
- **Backup Failures**: Tracked in statistics with specific error messages
- **Extraction Errors**: Logged but don't stop migration process
- **Database Errors**: Reported with details for troubleshooting
- **Graceful Degradation**: Continues migration even if some steps fail

**When to Use:**
- **First V2 Setup**: When setting up V2 dashboard for the first time with existing V1 tasks
- **Architecture Upgrade**: When upgrading from JSON-based to database-backed configuration
- **Security Improvement**: When moving from hardcoded credentials to secure keyring storage
- **Team Onboarding**: When migrating team's existing automation tasks to V2 system

**Prerequisites:**
- **V1 Configuration**: Existing `agent_config.json` file with tasks
- **V2 Components**: `credential_manager.py`, `database.py`, `auth_manager.py` installed
- **System Keyring**: Operating system keyring service available
- **Python Dependencies**: `keyring`, `sqlalchemy`, `flask-login` installed

**Limitations:**
- **Pattern Recognition**: Only extracts credentials matching defined patterns
- **Manual Review**: Complex credential formats may require manual migration
- **Single Run**: Designed for one-time migration (not incremental updates)
- **Credential Validation**: Does not validate extracted credentials are correct

### Nova Act Data Extraction (`nova_extract_and_recreate.py`) - **RECENTLY UPDATED**

**🔄 RECENT UPDATE**: Password updated to `YOUR_PASSWORD` for improved authentication reliability.

An advanced Nova Act automation script that extracts and structures usage data directly from web pages:

**Key Features:**
- **Direct Data Extraction**: Reads and transcribes usage data directly from web pages
- **Comprehensive Data Capture**: Extracts account numbers, usage amounts, dates, billing periods
- **Multi-Format Output**: Saves extracted data to both JSON and text formats
- **Visual Page Analysis**: Takes screenshots and provides detailed descriptions
- **Session Persistence**: Keeps browser open for manual verification
- **Updated Authentication**: Now uses password `YOUR_PASSWORD`

**Usage:**
```bash
python nova_extract_and_recreate.py
```

**What it does:**
1. **🔐 Navigation**: Automated login with updated credentials
2. **📊 Data Extraction**: Comprehensive extraction of all visible usage information
3. **🔍 Additional Data Mining**: Searches for supplementary information in tabs and sections
4. **💾 Data Storage**: Saves extracted data in multiple formats with timestamps
5. **✅ Verification**: Automatic file opening and session persistence

**Output Files:**
- `usage_data_103892_YYYYMMDD_HHMMSS.json` - Structured JSON data
- `usage_data_103892_YYYYMMDD_HHMMSS.txt` - Human-readable text format

### Extract from Existing Session (`extract_from_existing_session.py`)

A streamlined utility for quick data extraction from existing browser sessions:

**Key Features:**
- **Flexible Session Management**: Works with existing sessions or creates new ones
- **Simplified Data Extraction**: Focused on extracting visible usage data
- **Automatic File Handling**: Saves data to timestamped files and opens them
- **Smart Navigation**: Handles login automatically if needed
- **Clean Session Management**: Properly stops sessions after extraction

**Usage:**
```bash
python extract_from_existing_session.py
```

### Simple File Analyzer (`simple_file_analyzer.py`)

A lightweight utility for analyzing recently downloaded files:

**Key Features:**
- **Recent File Detection**: Scans Downloads folder for files from last 30 minutes
- **PDF Content Analysis**: Extracts and analyzes PDF content for utility data
- **Smart Content Recognition**: Identifies usage data and billing information
- **Automatic File Opening**: Opens detected files with default applications
- **Visual Feedback**: Organized output with emoji indicators

**Usage:**
```bash
pip install PyPDF2  # Required for PDF analysis
python simple_file_analyzer.py
```sage, consumption, and billing keywords
4. **📅 Date Recognition**: Finds date references and billing periods in the content
5. **✅ Auto-Opening**: Automatically opens all detected files for manual review
6. **📊 Content Summary**: Provides organized analysis with usage data counts and previews

**Output:**
- File count and detailed information for each recent download
- PDF-specific analysis including page count and text line count
- Usage data lines with keyword matching (usage, kwh, consumption, billing)
- Date references found in the document content
- First 500 characters of extracted text for content preview
- Automatic file opening for immediate review

**Best For:**
- Analyzing utility bill PDFs downloaded from automation scripts
- Quick content verification of downloaded documents
- Extracting usage data from PDF reports
- Reviewing billing information and date ranges
- Post-download analysis and content validation

### Download Verification Utility (`check_downloads.py`)

A standalone utility script for verifying and monitoring recent downloads from Nova Act automation scripts:

**Key Features:**
- **Recent File Detection**: Scans Downloads folder for files modified within the last 10 minutes
- **Smart File Recognition**: Automatically identifies utility export files by keywords (usage, export, 103892, pdf)
- **Automatic File Opening**: Opens detected export files using the system default application
- **Detailed File Information**: Shows file name, size, modification time, and full path
- **Error Handling**: Graceful handling of file system access errors
- **Visual Feedback**: Emoji-enhanced output for easy identification of results

**Usage:**
```bash
python check_downloads.py
```

**What it does:**
1. **📂 Folder Scanning**: Checks the user's Downloads folder for recent files
2. **🔍 File Analysis**: Identifies files modified within the last 10 minutes
3. **🎯 Smart Detection**: Recognizes utility export files by filename keywords
4. **✅ Auto-Opening**: Automatically opens identified export files
5. **📊 Detailed Reporting**: Provides comprehensive file information

**Output:**
- File count and detailed information for each recent download
- File size in human-readable format with comma separators
- Modification timestamps for tracking download times
- Full file paths for manual verification
- Success/failure indicators for file opening attempts
- Clear messaging when no recent downloads are found

**Best For:**
- Verifying Nova Act automation script results
- Checking if utility bill downloads completed successfully
- Troubleshooting download issues after automation runs
- Manual verification of export file availability
- Quick access to recently downloaded utility reports

**Integration with Nova Act Scripts:**
- Can be run after any Nova Act automation script to verify results
- Complements the built-in download monitoring in automation scripts
- Useful for troubleshooting when automation scripts don't detect downloads
- Provides manual verification option for automated workflows

### Nova Act Extraction Results Analyzer (`get_actual_data.py`) - **NEW**

A specialized analysis tool for inspecting Nova Act extraction results and identifying data extraction issues:

**Key Features:**
- **Extraction Metadata Analysis**: Reads and analyzes Nova Act extraction result files
- **Issue Identification**: Identifies when scripts save metadata instead of actual content
- **File Discovery**: Scans for usage-related files in the current directory
- **Extraction Summary**: Provides detailed summary of automation execution times
- **Troubleshooting Guidance**: Offers recommendations for improving data extraction

**Usage:**
```bash
python get_actual_data.py
```

**What it does:**
1. **📄 File Analysis**: Reads Nova Act extraction result JSON files (e.g., `usage_data_103892_YYYYMMDD_HHMMSS.json`)
2. **📊 Metadata Inspection**: Analyzes extraction metadata including dates, accounts, and execution times
3. **🔍 Issue Detection**: Identifies when automation successfully navigated but failed to extract actual content
4. **📁 File Discovery**: Searches for additional usage-related files in the project directory
5. **💡 Recommendations**: Provides guidance for improving data extraction workflows

**Output:**
- Extraction date and account information from result files
- Execution time summary for navigation and data extraction phases
- Clear identification of metadata vs. actual content issues
- List of all usage-related files found in the directory
- Specific recommendations for accessing actual extracted data
- Alternative approaches when automated extraction needs improvement

**Best For:**
- Troubleshooting Nova Act data extraction scripts
- Understanding why extraction results contain metadata instead of actual data
- Identifying successful navigation vs. failed content extraction
- Planning improvements to data extraction workflows
- Debugging Nova Act ActResult object handling

**Integration with Nova Act Scripts:**
- Designed to work with output from `nova_extract_and_recreate.py`
- Complements other data extraction and analysis tools
- Helps identify when Nova Act sessions need manual intervention
- Provides insights for improving automated data extraction methods

### Nova Act PDF Content Reader (`nova_read_pdf_content.py`) - **UPDATED**

A specialized Nova Act automation script that focuses on extracting complete PDF content directly from the browser with comprehensive transcription capabilities:

**🔄 RECENT UPDATE**: Password updated to `YOUR_PASSWORD` for improved authentication reliability and consistency with other scripts.

**Key Features:**
- **Direct PDF Content Extraction**: Reads PDF content directly from browser after generation
- **Complete Transcription**: Extracts ALL text content including usage data, dates, billing periods, and rates
- **Multi-Page Support**: Handles PDFs with multiple pages and sections
- **Structured Content Capture**: Maintains formatting and structure of original PDF
- **Automatic File Saving**: Saves extracted content to timestamped text files
- **Session Persistence**: Keeps browser open for manual verification
- **Comprehensive Data Extraction**: Captures account numbers, meter readings, service charges, and historical data

**Usage:**
```bash
python nova_read_pdf_content.py
```

**What it does:**
1. **🔐 Navigation & PDF Generation**: Automates login, navigation, and PDF export process
2. **📄 Direct PDF Reading**: Reads PDF content directly from browser or downloaded file
3. **📊 Complete Transcription**: Extracts every piece of information including:
   - Account number and service address
   - All usage data (kWh, gallons, therms, etc.)
   - All dates and billing periods
   - Meter readings and measurements
   - Rate schedules and pricing information
   - Charts, graphs, and tabular data
   - Historical usage comparisons
   - Service charges and fees
4. **📋 Multi-Page Processing**: Checks for and processes additional PDF pages/sections
5. **💾 Content Storage**: Saves complete extracted content to timestamped files
6. **✅ Automatic File Opening**: Opens saved content files for immediate review

**Output Files:**
- `usage_content_103892_YYYYMMDD_HHMMSS.txt` - Complete PDF content transcription

**Content Extraction Includes:**
- **Account Information**: Service address, account numbers, customer details
- **Usage Data**: Detailed consumption data across all utility types
- **Billing Information**: Rate schedules, service charges, fees, and pricing
- **Historical Data**: Usage comparisons and trend information
- **Meter Readings**: All meter readings and measurement data
- **Dates & Periods**: Complete billing periods and service dates
- **Additional Sections**: Terms, conditions, contact information

**Best For:**
- Complete PDF content extraction when file downloads are not working
- Comprehensive data transcription for detailed analysis
- Extracting structured usage data directly from browser-generated PDFs
- Capturing all billing and rate information in text format
- Creating searchable text versions of utility PDF reports

**Integration with Other Scripts:**
- Complements file download automation scripts
- Works with existing Nova Act session management
- Can be used when blob download methods fail
- Provides alternative to file-based PDF analysis tools

**Advantages over File Download Methods:**
- **No Download Required**: Reads content directly from browser
- **Complete Content Capture**: Extracts ALL text content, not just summaries
- **Structured Transcription**: Maintains original formatting and organization
- **Multi-Page Support**: Handles complex PDFs with multiple sections
- **Real-Time Processing**: Processes content immediately after PDF generation

### Simple Nova Act Test (`test_simple_nova.py`) - **NEW**

**🧪 STATUS: BASIC AUTOMATION TEST** - A simple test script for validating Nova Act integration and basic browser automation functionality using a demo site.

**Key Features:**
- **Demo Site Testing**: Uses DemoQA login page for safe testing without affecting production systems
- **Basic Automation Validation**: Tests fundamental Nova Act functionality including browser startup and screenshot capture
- **Non-Headless Mode**: Runs with visible browser for easy monitoring and debugging
- **Error Handling**: Comprehensive error handling with proper session cleanup
- **Quick Validation**: Fast test execution (approximately 20 seconds total)
- **Safe Testing Environment**: No risk to production utility portal or authentication systems

**Usage:**
```bash
python test_simple_nova.py
```

**What it does:**
1. **🚀 Nova Act Initialization**: Creates Nova Act instance with demo site URL
2. **🌐 Browser Launch**: Starts visible Chrome browser session
3. **⏱️ Page Loading**: Waits for page to fully load (5 seconds)
4. **📸 Screenshot Test**: Executes basic automation action (screenshot)
5. **⏳ Session Monitoring**: Keeps browser open for 10 seconds for visual verification
6. **🛑 Clean Shutdown**: Properly stops Nova Act session

**Test Configuration:**
- **Target URL**: `https://demoqa.com/login` (safe demo site)
- **Browser Mode**: Non-headless (visible browser window)
- **API Key**: Uses standard Nova Act API key (`YOUR_NOVA_ACT_API_KEY`)
- **Session Duration**: Approximately 20 seconds total execution time
- **TTY Mode**: Disabled for consistent behavior

**Output:**
- Step-by-step progress indicators with emoji feedback
- Success confirmation for each automation phase
- Clear error messages if any step fails
- Proper session cleanup regardless of success or failure

**Best For:**
- **Nova Act Integration Testing**: Verify Nova Act is properly installed and configured
- **API Key Validation**: Confirm API key is working correctly
- **Browser Compatibility**: Test Chrome/Chromium browser integration
- **Development Environment Setup**: Validate development environment before running production scripts
- **Troubleshooting**: Isolate Nova Act issues from utility portal-specific problems
- **Learning Tool**: Understand basic Nova Act automation patterns

**Advantages:**
- **Safe Testing**: No risk to production systems or authentication
- **Quick Validation**: Fast execution for rapid testing cycles
- **Visual Feedback**: Non-headless mode allows visual monitoring
- **Error Isolation**: Separates Nova Act issues from portal-specific problems
- **Development Ready**: Perfect for validating development environment setup

**Integration with Project:**
- **Prerequisite Testing**: Run before attempting utility portal automation
- **Development Workflow**: Use for validating Nova Act setup in new environments
- **Troubleshooting Tool**: Isolate Nova Act issues from portal authentication problems
- **Learning Resource**: Study basic Nova Act patterns before working with complex scripts

**When to Use:**
- Before running production utility automation scripts
- When setting up Nova Act in a new development environment
- When troubleshooting Nova Act installation or configuration issues
- When learning Nova Act automation patterns
- When validating API key functionality

**Expected Results:**
- Browser window opens and navigates to DemoQA login page
- Screenshot action completes successfully
- Console shows step-by-step progress with checkmarks
- Session closes cleanly after 20 seconds
- No errors or exceptions during execution

### Immediate Task Execution Test (`test_task_now.py`) - **NEW**

**🧪 STATUS: PORTAL AUTOMATION AGENT TEST** - A specialized test script for validating the Portal Automation Agent's task scheduling and execution system with immediate task execution.

**Key Features:**
- **Immediate Task Testing**: Creates and executes a test task within 60 seconds for rapid validation
- **Portal Agent Integration**: Tests the complete Portal Automation Agent workflow including task creation, scheduling, and execution
- **Safe Demo Environment**: Uses DemoQA login page for testing without affecting production systems
- **Real-Time Monitoring**: Provides live status updates during task execution with progress indicators
- **Automatic Task Management**: Creates, schedules, executes, and monitors a complete task lifecycle
- **Scheduler Validation**: Tests the scheduling engine and task execution pipeline
- **Status Tracking**: Monitors task status changes from pending to completion

**Usage:**
```bash
python test_task_now.py
```

**What it does:**
1. **🤖 Agent Initialization**: Creates Portal Automation Agent instance with configuration file
2. **⏰ Task Scheduling**: Schedules a test task to run in the next minute for immediate execution
3. **📋 Task Creation**: Creates "Immediate Test Task" with simple automation instructions
4. **🚀 Scheduler Startup**: Starts the Portal Automation Agent scheduler
5. **🔍 Real-Time Monitoring**: Monitors task execution with live status updates every 10 seconds
6. **📊 Status Reporting**: Reports task completion status, results, and any error messages
7. **🛑 Clean Shutdown**: Properly stops the scheduler and cleans up resources

**Test Task Configuration:**
- **Name**: "Immediate Test Task"
- **Target URL**: `https://demoqa.com/login` (safe demo site)
- **Schedule**: Next minute from current time (immediate execution)
- **Instructions**: Simple 4-step automation workflow:
  1. Navigate to the login page
  2. Wait for page to load (3 seconds)
  3. Take a screenshot of the page
  4. Close the browser

**Monitoring Features:**
- **Progress Indicators**: Real-time status updates with emoji feedback
- **Task Status Tracking**: Monitors task status changes (pending → running → completed/failed)
- **Execution Results**: Displays task results and any error messages
- **Timeout Protection**: 2-minute maximum wait time with automatic cleanup
- **Visual Feedback**: Clear console output with timestamps and status indicators

**Output:**
- Current time and scheduled execution time display
- Task ID confirmation and scheduler startup notification
- Real-time progress updates every 10 seconds
- Task completion status with results or error messages
- Clean shutdown confirmation

**Best For:**
- **Portal Agent Testing**: Validate Portal Automation Agent installation and configuration
- **Scheduler Validation**: Test the task scheduling and execution pipeline
- **Integration Testing**: Verify Nova Act integration within the Portal Agent system
- **Development Workflow**: Quick validation of Portal Agent functionality during development
- **Troubleshooting**: Isolate Portal Agent issues from complex automation workflows
- **Learning Tool**: Understand Portal Agent task lifecycle and monitoring

**Integration with Portal Automation Agent:**
- **Configuration File**: Uses `agent_config.json` for Portal Agent configuration
- **Task Management**: Demonstrates complete task creation and management workflow
- **Scheduler Integration**: Tests the built-in scheduling engine and execution pipeline
- **Status Monitoring**: Validates real-time task status tracking and reporting
- **Resource Management**: Tests proper session cleanup and resource management

**Advantages:**
- **Immediate Feedback**: Task executes within 60 seconds for rapid testing
- **Complete Workflow**: Tests entire Portal Agent pipeline from task creation to completion
- **Safe Environment**: Uses demo site to avoid affecting production systems
- **Real-Time Monitoring**: Live status updates provide immediate feedback
- **Automatic Cleanup**: Proper resource management and session cleanup

**When to Use:**
- Before deploying Portal Automation Agent in production
- When setting up Portal Agent in a new environment
- When troubleshooting Portal Agent scheduling or execution issues
- When validating Portal Agent configuration changes
- When learning Portal Agent task management patterns
- When testing Nova Act integration within the Portal Agent system

**Expected Results:**
- Task scheduled for execution in the next minute
- Browser window opens automatically when task executes
- Screenshot action completes successfully within the demo site
- Task status progresses from pending → running → completed
- Console shows real-time progress with clear status indicators
- Clean shutdown with proper resource cleanup

**Troubleshooting:**
- **Task Not Executing**: Check Portal Agent configuration file and Nova Act API key
- **Browser Issues**: Ensure Chrome/Chromium is installed and accessible
- **Scheduling Problems**: Verify system time and task scheduling logic
- **Status Tracking**: Check task status enum handling and configuration persistence
- **Resource Cleanup**: Ensure proper Nova Act session management and cleanup

### Run Task Now (`run_task_now.py`) - **NEW**

**⚡ STATUS: IMMEDIATE TASK EXECUTION UTILITY** - A command-line utility for running specific scheduled tasks immediately, bypassing the scheduler to execute tasks on-demand without waiting for their scheduled time.

**Key Features:**
- **Immediate Execution**: Run any configured task instantly without waiting for scheduled time
- **Task Selection**: Execute specific tasks by ID or automatically run the most recent task
- **Scheduler Bypass**: Direct task execution without starting the full scheduling engine
- **Configuration Integration**: Works seamlessly with existing `agent_config.json` tasks
- **Simple Interface**: Single command execution with minimal setup
- **Error Handling**: Comprehensive error reporting for troubleshooting
- **Status Reporting**: Clear success/failure indicators with execution feedback

**Usage:**

**Run a specific task by ID:**
```bash
python run_task_now.py task_1234567890_0
```

**Run the most recent task (no arguments):**
```bash
python run_task_now.py
```

**What it does:**
1. **📋 Configuration Loading**: Reads tasks from `agent_config.json`
2. **🔍 Task Lookup**: Finds the specified task by ID or selects the most recent task
3. **📊 Task Display**: Shows task name, URL, and instruction preview
4. **🤖 Agent Creation**: Initializes Portal Automation Agent for task execution
5. **🚀 Task Execution**: Runs the task immediately using `execute_task()` method
6. **✅ Result Reporting**: Reports success or failure with appropriate exit codes

**Command-Line Arguments:**
- **`task_id`** (optional): Specific task ID to execute
  - If provided: Executes the specified task
  - If omitted: Automatically executes the most recent task from configuration

**Output:**
```
🚀 Running task: Daily Utility Usage Report
   URL: https://livingstonnj.my360-app.com
   Instructions: Navigate to the export page:...

✅ Task completed successfully!
```

**Exit Codes:**
- **0**: Task completed successfully
- **1**: Task failed or error occurred

**Best For:**
- **Manual Task Execution**: Run scheduled tasks on-demand without waiting
- **Testing Tasks**: Validate task configuration before scheduling
- **Troubleshooting**: Debug task execution issues in isolation
- **Ad-Hoc Automation**: Execute automation workflows outside regular schedule
- **Development Workflow**: Quick task testing during development
- **Emergency Runs**: Execute critical tasks immediately when needed

**Integration with Portal Automation Agent:**
- **Configuration Compatible**: Uses same `agent_config.json` as Portal Agent
- **Task Compatibility**: Executes any task created via Portal Agent, CLI, or Quick Setup
- **Direct Execution**: Bypasses scheduler for immediate task execution
- **Agent Integration**: Uses `PortalAutomationAgent.execute_task()` method
- **Status Updates**: Task status updated in configuration file after execution

**Advantages:**
- **No Scheduler Required**: Execute tasks without starting the full scheduling engine
- **Immediate Results**: Get instant feedback on task execution
- **Simple Interface**: Single command with minimal arguments
- **Flexible Selection**: Run specific tasks or automatically select most recent
- **Quick Testing**: Validate tasks before adding to production schedule
- **Error Isolation**: Test individual tasks without affecting scheduled runs

**When to Use:**
- **Before Scheduling**: Test new tasks before adding them to the schedule
- **Troubleshooting**: Debug task execution issues in isolation
- **Manual Runs**: Execute tasks outside their regular schedule
- **Development**: Quick task validation during development
- **Emergency Execution**: Run critical tasks immediately when needed
- **Configuration Validation**: Verify task configuration is correct

**Comparison with Other Execution Methods:**

| Feature | run_task_now.py | test_task_now.py | Portal Agent --start |
|---------|----------------|------------------|---------------------|
| Scheduler Required | ❌ No | ✅ Yes | ✅ Yes |
| Immediate Execution | ✅ Yes | ⏰ 60s delay | ⏰ Scheduled time |
| Task Selection | ✅ Any task | ❌ Test task only | ✅ All scheduled |
| Use Case | On-demand runs | Agent testing | Production scheduling |
| Setup Complexity | ✅ Minimal | ⚠️ Medium | ⚠️ Medium |

**Example Workflows:**

**Test a newly created task:**
```bash
# 1. Create task with quick setup
python quick_setup.py

# 2. Get task ID from output
# Task ID: task_1234567890_0

# 3. Test immediately
python run_task_now.py task_1234567890_0

# 4. If successful, start scheduler
python standalone_scheduler.py
```

**Run most recent task:**
```bash
# Automatically runs the last task in agent_config.json
python run_task_now.py
```

**Troubleshooting workflow:**
```bash
# 1. List all tasks to find problematic task
python agent_cli.py list

# 2. Run specific task to debug
python run_task_now.py task_1234567890_0

# 3. Check logs for detailed error information
cat portal_agent.log
```

**Technical Details:**
- **Configuration File**: Reads from `agent_config.json` in current directory
- **Task Selection Logic**: Uses task ID or selects last task from tasks array
- **Execution Method**: Calls `PortalAutomationAgent.execute_task(task)` directly
- **Error Handling**: Catches and reports exceptions with appropriate exit codes
- **Status Updates**: Task status updated in configuration after execution

**Error Messages:**
- **"❌ No config file found"**: `agent_config.json` not found in current directory
- **"❌ Task {task_id} not found"**: Specified task ID doesn't exist in configuration
- **"❌ No tasks found"**: Configuration file has no tasks defined
- **"❌ Task failed: {error}"**: Task execution encountered an error

**Prerequisites:**
- **Configuration File**: `agent_config.json` must exist with at least one task
- **Portal Agent**: `portal_automation_agent.py` must be in the same directory
- **Nova Act**: Nova Act must be installed and configured
- **Task Configuration**: Tasks must have valid URL and instructions

**Integration with Other Tools:**
- **Quick Setup**: Run tasks created by `quick_setup.py`
- **Agent CLI**: Execute tasks managed via `agent_cli.py`
- **Web Dashboard**: Run tasks created through web interface
- **Manual Configuration**: Execute manually configured tasks from JSON

**Best Practices:**
- **Test First**: Always test new tasks with `run_task_now.py` before scheduling
- **Check Logs**: Review `portal_agent.log` for detailed execution information
- **Validate Configuration**: Ensure task configuration is correct before execution
- **Monitor Execution**: Watch browser window during execution for visual feedback
- **Handle Errors**: Check exit codes in scripts for automated error handling

**Limitations:**
- **Single Task Execution**: Executes one task at a time (no batch execution)
- **No Scheduling**: Does not add task to scheduler (one-time execution only)
- **Configuration Required**: Requires existing `agent_config.json` file
- **No Task Creation**: Cannot create new tasks (use CLI or Quick Setup instead)

### System Diagnostics Utility (`diagnose_nova_issues.py`) - **UPDATED**

**🔧 STATUS: COMPREHENSIVE SYSTEM DIAGNOSTICS** - An enhanced diagnostic utility that performs comprehensive system checks and validates Nova Act automation environment setup.

**🔄 RECENT UPDATE**: Complete rewrite with enhanced diagnostic capabilities including internet connectivity testing, dependency validation, and live Nova Act functionality testing.

**Key Features:**
- **Internet Connectivity Testing**: Validates network access to test sites and utility portals
- **Nova Act Installation Validation**: Confirms Nova Act is properly installed and importable
- **Playwright Integration Check**: Validates Playwright installation and browser availability
- **Chrome Process Monitoring**: Detects running Chrome processes that might interfere with automation
- **Live Functionality Testing**: Performs actual Nova Act automation test with real browser session
- **Comprehensive Error Reporting**: Detailed error messages with specific troubleshooting recommendations
- **Safe Testing Environment**: Uses Google.com for live testing to avoid affecting production systems

**Core Diagnostic Checks:**

**🌐 Network Connectivity:**
- Tests access to Google.com for basic internet connectivity
- Validates access to DemoQA.com for automation testing
- Checks specific test endpoints used by automation scripts
- Reports HTTP status codes and connection errors

**🔍 Nova Act Environment:**
- Confirms Nova Act package installation and version detection
- Validates Nova Act import functionality
- Tests API key configuration and accessibility
- Checks Nova Act module availability and compatibility

**🎭 Playwright Integration:**
- Validates Playwright installation (Nova Act dependency)
- Checks Playwright CLI accessibility
- Tests browser installation and availability
- Reports Playwright configuration issues

**🌐 Browser Process Management:**
- Scans for running Chrome/Chromium processes
- Identifies potential browser conflicts
- Provides process cleanup recommendations
- Platform-specific process detection (Windows/Linux/macOS)

**🧪 Live Functionality Testing:**
- Creates actual Nova Act session with test configuration
- Performs real browser automation (screenshot test)
- Validates complete automation pipeline
- Tests session startup, execution, and cleanup

**Usage:**
```bash
python diagnose_nova_issues.py
```

**What it does:**
1. **🌐 Connectivity Check**: Tests internet access and target site availability
2. **📦 Dependency Validation**: Confirms Nova Act and Playwright installations
3. **🔍 Environment Analysis**: Checks browser processes and system configuration
4. **🧪 Live Testing**: Performs actual Nova Act automation test with real browser
5. **📊 Results Summary**: Provides comprehensive diagnostic report with recommendations

**Diagnostic Output:**
- **✅ Success Indicators**: Green checkmarks for passed tests
- **❌ Failure Indicators**: Red X marks with specific error details
- **⚠️ Warning Indicators**: Yellow warnings for potential issues
- **💡 Recommendations**: Specific troubleshooting steps for identified problems

**Test Configuration:**
- **Target URL**: Google.com (safe, reliable test site)
- **Browser Mode**: Headless for automated testing
- **API Key**: Uses standard Nova Act API key
- **Test Duration**: Approximately 30 seconds total execution time
- **Session Management**: Proper startup and cleanup testing

**Troubleshooting Recommendations:**
The utility provides specific recommendations based on diagnostic results:

**For Playwright Issues:**
```bash
pip install playwright && playwright install
```

**For Nova Act Issues:**
```bash
pip install nova-act
```

**For Chrome Process Conflicts:**
- Close all Chrome windows and try again
- Kill Chrome processes if necessary

**For Network Issues:**
- Check internet connection
- Verify firewall settings
- Test with different network connection

**Best For:**
- **Environment Setup Validation**: Confirm Nova Act environment is properly configured
- **Troubleshooting Automation Issues**: Identify root causes of automation failures
- **Development Environment Testing**: Validate setup before running production scripts
- **Dependency Verification**: Ensure all required packages are installed correctly
- **System Health Checks**: Regular validation of automation environment
- **New Installation Testing**: Verify Nova Act setup in fresh environments

**Integration with Project:**
- **Prerequisite Testing**: Run before attempting utility portal automation
- **Development Workflow**: Use for validating development environment setup
- **Troubleshooting Tool**: First step in diagnosing automation issues
- **Environment Validation**: Confirm system readiness for production automation

**When to Use:**
- Before running any Nova Act automation scripts
- When experiencing unexplained automation failures
- After installing or updating Nova Act or dependencies
- When setting up automation in a new environment
- When troubleshooting browser or network connectivity issues
- As part of regular system maintenance and validation

**Expected Results:**
- All connectivity tests pass with HTTP 200 status codes
- Nova Act and Playwright import successfully
- No conflicting Chrome processes detected
- Live Nova Act test completes successfully with screenshot
- Clean session startup and shutdown
- Comprehensive diagnostic report with all green checkmarks

**Advanced Features:**
- **Platform Detection**: Adapts process checking for Windows/Linux/macOS
- **Error Isolation**: Separates network, dependency, and functionality issues
- **Detailed Logging**: Timestamped diagnostic output with progress indicators
- **Safe Testing**: Uses reliable test sites to avoid production system impact
- **Comprehensive Coverage**: Tests entire automation stack from network to browser

**Diagnostic Categories:**
- **🌐 Network Layer**: Internet connectivity and site accessibility
- **📦 Package Layer**: Python package installation and imports
- **🎭 Browser Layer**: Playwright and Chrome browser availability
- **🤖 Automation Layer**: Nova Act functionality and session management
- **🔧 System Layer**: Process management and resource availability

### Cleanup Stuck Tasks Utility (`cleanup_stuck_tasks.py`) - **NEW**

**🔧 STATUS: TASK RECOVERY UTILITY** - A specialized utility for resetting Portal Automation Agent tasks that are stuck in 'running' state, typically caused by unexpected browser closures or system interruptions.

**Key Features:**
- **Stuck Task Detection**: Automatically identifies tasks stuck in 'running' state
- **Safe Task Reset**: Resets stuck tasks to 'failed' status with explanatory error messages
- **Configuration Preservation**: Maintains all task configuration while updating status
- **Batch Processing**: Handles multiple stuck tasks in a single execution
- **Detailed Reporting**: Shows task details before and after reset
- **Configuration Persistence**: Automatically saves updated configuration to disk
- **Next Steps Guidance**: Provides clear instructions for restarting the scheduler

**Common Causes of Stuck Tasks:**
- **Browser Closed Unexpectedly**: User manually closes browser during task execution
- **System Interruption**: Computer shutdown or restart during automation
- **Process Termination**: Nova Act process killed or crashed during execution
- **Network Interruption**: Connection loss during critical automation steps
- **Scheduler Stopped**: Automation agent stopped while task was running

**Usage:**
```bash
python cleanup_stuck_tasks.py
```

**What it does:**
1. **🔍 Task Scanning**: Loads Portal Automation Agent configuration and scans all tasks
2. **🎯 Stuck Task Identification**: Identifies tasks with status 'running'
3. **📋 Task Details Display**: Shows complete information for each stuck task including:
   - Task name and ID
   - Current status
   - Last run timestamp
   - Task configuration details
4. **🔄 Status Reset**: Changes task status from 'running' to 'failed'
5. **📝 Error Message**: Adds explanatory error message about stuck state
6. **💾 Configuration Save**: Persists updated configuration to `agent_config.json`
7. **🎯 Next Steps**: Provides clear instructions for resuming automation

**Output:**
- **No Stuck Tasks**: Confirmation message when all tasks are in valid states
- **Stuck Tasks Found**: Detailed list of stuck tasks with complete information
- **Reset Confirmation**: Success message for each task reset
- **Configuration Saved**: Confirmation of configuration file update
- **Next Steps**: Specific commands for restarting the scheduler

**Example Output:**
```
🔧 Cleaning Up Stuck Tasks
==================================================
Found 2 stuck task(s):

📋 Task: Daily Utility Usage Report
   ID: task_1234567890_0
   Status: running
   Last Run: 2026-02-08 09:15:23

✅ Reset Daily Utility Usage Report to 'failed' status

📋 Task: Evening Data Export
   ID: task_1234567891_0
   Status: running
   Last Run: 2026-02-08 18:30:45

✅ Reset Evening Data Export to 'failed' status

💾 Configuration saved

🎯 Next Steps:
1. Start the scheduler: python agent_cli.py start
2. Or view status: python agent_cli.py status
3. Tasks will retry automatically if enabled
```

**Integration with Portal Automation Agent:**
- **Configuration File**: Uses same `agent_config.json` as Portal Automation Agent
- **Status Management**: Works with Portal Agent's task status system
- **Retry Logic**: Reset tasks can be automatically retried by the scheduler
- **Task Preservation**: Maintains all task configuration and scheduling information

**Best For:**
- **Recovery After Interruptions**: Restore automation after unexpected shutdowns
- **Browser Closure Recovery**: Fix tasks stuck after manual browser closure
- **System Maintenance**: Clean up task states after system restarts
- **Troubleshooting**: Reset tasks that appear stuck or unresponsive
- **Scheduler Restart**: Prepare tasks for clean scheduler restart
- **Development Testing**: Reset test tasks during development cycles

**When to Use:**
- After unexpected system shutdown or restart
- When browser was manually closed during task execution
- Before restarting the Portal Automation Agent scheduler
- When tasks show 'running' status but no browser is active
- After killing Nova Act processes during troubleshooting
- When scheduler appears stuck or unresponsive

**Safety Features:**
- **Non-Destructive**: Only changes task status, preserves all configuration
- **Explanatory Messages**: Adds clear error messages explaining the reset
- **Configuration Backup**: Original configuration preserved in task history
- **Selective Reset**: Only affects tasks actually stuck in 'running' state
- **Automatic Save**: Ensures configuration changes are persisted

**Workflow Integration:**
```bash
# 1. Detect and reset stuck tasks
python cleanup_stuck_tasks.py

# 2. Verify task status
python agent_cli.py status

# 3. Restart the scheduler
python agent_cli.py start

# 4. Monitor task execution
python agent_dashboard.py
```

**Advantages:**
- **Quick Recovery**: Restore automation in seconds without manual configuration editing
- **Safe Operation**: Non-destructive reset preserves all task configuration
- **Clear Feedback**: Detailed reporting of what was changed and why
- **Automatic Retry**: Reset tasks can be automatically retried by scheduler
- **Simple Usage**: Single command with no parameters required

**Technical Details:**
- **Status Transition**: Changes status from `TaskStatus.RUNNING` to `TaskStatus.FAILED`
- **Error Message**: Adds message "Task was stuck in running state - likely browser closed unexpectedly"
- **Configuration Format**: Maintains JSON configuration file structure
- **Task Preservation**: All task properties except status remain unchanged
- **Retry Eligibility**: Reset tasks remain eligible for automatic retry if enabled

**Troubleshooting:**
- **No Configuration File**: Ensure `agent_config.json` exists in current directory
- **Permission Issues**: Verify write permissions for configuration file
- **Import Errors**: Ensure `portal_automation_agent.py` is in same directory
- **Status Enum Issues**: Verify Portal Automation Agent is properly installed

**Related Tools:**
- **Portal Automation Agent**: Main scheduling system that creates tasks
- **Agent CLI**: Command-line interface for task management
- **Agent Dashboard**: Web interface for monitoring task status
- **Test Task Now**: Utility for testing task execution

### Authentication Manager (`auth_manager.py`) - **NEW**

**👤 STATUS: USER AUTHENTICATION SYSTEM** - A comprehensive user authentication and session management system for web dashboard access with secure password hashing and user management capabilities.

**Key Features:**
- **User Authentication**: Complete user login system with username/password authentication
- **Secure Password Storage**: Uses Werkzeug's secure password hashing (never stores plain text passwords)
- **Flask-Login Integration**: Seamless integration with Flask-Login for session management
- **User Management**: Create, list, update, and delete user accounts
- **Admin Privileges**: Support for admin users with elevated permissions
- **Default Admin Account**: Automatic creation of default admin user on first run
- **JSON Storage**: User data persisted in JSON file with automatic saving
- **Interactive CLI**: Command-line interface for user management
- **Password Change**: Secure password change functionality with old password verification

**User Model:**
- **User ID**: Unique identifier generated with secure tokens
- **Username**: Unique username for login
- **Password Hash**: Securely hashed password (never plain text)
- **Email**: Optional email address for user contact
- **Created At**: Timestamp of user account creation
- **Admin Flag**: Boolean indicating admin privileges

**Usage:**

**Interactive User Management:**
```bash
# Add new user interactively
python auth_manager.py add

# List all users (without passwords)
python auth_manager.py list
```

**Programmatic Usage in Web Applications:**
```python
from auth_manager import AuthManager, User
from flask_login import LoginManager, login_user, logout_user, login_required

# Initialize authentication manager
auth_manager = AuthManager('users.json')

# Create new user
user, error = auth_manager.create_user(
    username='john_doe',
    password='SecurePassword123',
    email='john@example.com',
    is_admin=False
)

if error:
    print(f"Error: {error}")
else:
    print(f"User created: {user.username}")

# Authenticate user
user = auth_manager.authenticate('john_doe', 'SecurePassword123')
if user:
    print(f"Login successful: {user.username}")
    # Use with Flask-Login
    login_user(user)
else:
    print("Invalid credentials")

# Get user by ID (for Flask-Login user_loader)
user = auth_manager.get_user(user_id)

# Get user by username
user = auth_manager.get_user_by_username('john_doe')

# Change password
success, message = auth_manager.change_password(
    user_id=user.id,
    old_password='SecurePassword123',
    new_password='NewSecurePassword456'
)

# List all users (metadata only)
users = auth_manager.list_users()
for user_info in users:
    print(f"{user_info['username']} - Admin: {user_info['is_admin']}")

# Delete user
success, message = auth_manager.delete_user(user_id)
```

**Interactive User Setup Flow:**
```bash
$ python auth_manager.py add

👤 User Setup
==================================================
Username: john_doe
Password: ****************
Confirm password: ****************
Email (optional): john@example.com
Admin user? (y/N): n

✅ User 'john_doe' created successfully
```

**List Users:**
```bash
$ python auth_manager.py list

👥 Users:
==================================================
• admin [ADMIN]
  Email: admin@localhost
  Created: 2026-02-10T14:30:45.123456

• john_doe
  Email: john@example.com
  Created: 2026-02-10T15:45:23.789012
```

**Core API Methods:**

**`create_user(username, password, email, is_admin)`**
- Creates new user with secure password hashing
- Validates username uniqueness
- Returns: (User object, error message) tuple
- Automatically saves to JSON file

**`authenticate(username, password)`**
- Validates username and password
- Returns: User object if successful, None if failed
- Uses secure password hash comparison

**`get_user(user_id)`**
- Retrieves user by unique ID
- Returns: User object or None
- Used by Flask-Login user_loader callback

**`get_user_by_username(username)`**
- Retrieves user by username
- Returns: User object or None
- Used for login form processing

**`change_password(user_id, old_password, new_password)`**
- Changes user password with verification
- Validates old password before updating
- Returns: (success boolean, message string) tuple

**`delete_user(user_id)`**
- Removes user from system
- Prevents deletion of last admin user
- Returns: (success boolean, message string) tuple

**`list_users()`**
- Lists all users without password hashes
- Returns: List of user metadata dictionaries
- Safe for display and logging

**Default Admin Account:**
On first run, the system automatically creates a default admin account:
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@localhost`
- **Admin**: Yes

⚠️ **IMPORTANT**: Change the default admin password immediately after first login!

**User Data Storage:**
- **File**: `users.json` (configurable)
- **Format**: JSON with user objects and metadata
- **Security**: Password hashes only, never plain text passwords
- **Automatic Saving**: Changes persisted immediately to disk

**Example `users.json` Structure:**
```json
{
  "users": [
    {
      "id": "a1b2c3d4e5f6g7h8",
      "username": "admin",
      "password_hash": "pbkdf2:sha256:...",
      "email": "admin@localhost",
      "created_at": "2026-02-10T14:30:45.123456",
      "is_admin": true
    },
    {
      "id": "i9j8k7l6m5n4o3p2",
      "username": "john_doe",
      "password_hash": "pbkdf2:sha256:...",
      "email": "john@example.com",
      "created_at": "2026-02-10T15:45:23.789012",
      "is_admin": false
    }
  ],
  "last_updated": "2026-02-10T15:45:23.789012"
}
```

**Flask-Login Integration Example:**
```python
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from auth_manager import AuthManager

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize Auth Manager
auth_manager = AuthManager('users.json')

@login_manager.user_loader
def load_user(user_id):
    return auth_manager.get_user(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = auth_manager.authenticate(username, password)
        if user:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('Admin access required', 'error')
        return redirect(url_for('dashboard'))
    
    users = auth_manager.list_users()
    return render_template('admin.html', users=users)
```

**Security Features:**
- **Password Hashing**: Uses Werkzeug's `generate_password_hash` with PBKDF2-SHA256
- **Secure Tokens**: User IDs generated with `secrets.token_hex` for unpredictability
- **Password Verification**: Secure comparison using `check_password_hash`
- **Admin Protection**: Prevents deletion of last admin user
- **No Plain Text**: Passwords never stored or logged in plain text

**Best Practices:**
- **Change Default Password**: Immediately change the default admin password
- **Strong Passwords**: Enforce strong password policies in your application
- **HTTPS Only**: Use HTTPS in production to protect credentials in transit
- **Session Security**: Configure Flask session security settings
- **Regular Backups**: Backup `users.json` file regularly
- **Access Control**: Implement proper authorization checks in your application

**System Requirements:**
- **Python Packages**: 
  - `flask-login` (for Flask integration)
  - `werkzeug` (for password hashing, included with Flask)
- **No External Database**: Uses JSON file storage for simplicity

**Installation:**
```bash
# Install required packages
pip install flask-login werkzeug

# Verify installation
python -c "from auth_manager import AuthManager; print('Auth Manager ready')"
```

**Best For:**
- **Web Dashboard Authentication**: Secure login for agent dashboard and web interfaces
- **Multi-User Systems**: Support multiple users with different permission levels
- **Development Environments**: Quick authentication setup without database complexity
- **Small Teams**: User management for small team deployments
- **Prototype Applications**: Rapid authentication implementation for prototypes

**Advantages:**
- **Simple Setup**: No database required, uses JSON file storage
- **Secure by Default**: Industry-standard password hashing
- **Flask Integration**: Seamless integration with Flask-Login
- **User Management**: Complete CRUD operations for user accounts
- **Admin Support**: Built-in admin user functionality
- **CLI Tools**: Command-line interface for user management

**Limitations:**
- **File-Based Storage**: Not suitable for high-concurrency applications
- **No Password Recovery**: Implement email-based recovery separately if needed
- **Basic Authorization**: Implement role-based access control separately if needed
- **Single File**: All users in one JSON file (consider database for large deployments)

**Integration with Project:**
- **Agent Dashboard**: Can be integrated with `agent_dashboard.py` for secure access
- **Web Interfaces**: Provides authentication for any Flask-based web interface
- **User Management**: CLI tools for managing dashboard users
- **Session Management**: Works with Flask session management

**Future Enhancements:**
- Integration with agent dashboard for secure access control
- Role-based access control (RBAC) beyond simple admin flag
- Password reset functionality with email verification
- Two-factor authentication (2FA) support
- User activity logging and audit trail
- Password expiration and rotation policies
- Account lockout after failed login attempts

**Troubleshooting:**

**Default Admin Not Created:**
- Delete `users.json` and restart to recreate default admin
- Check file permissions for write access

**Password Hash Errors:**
- Ensure Werkzeug is installed: `pip install werkzeug`
- Verify password is a string, not bytes

**User Not Found:**
- Check username spelling (case-sensitive)
- Use `list` command to see all users
- Verify `users.json` file exists and is readable

**Cannot Delete User:**
- Cannot delete last admin user (by design)
- Create another admin before deleting current admin

**Related Tools:**
- **Credential Manager**: For storing portal credentials (different from user authentication)
- **Agent Dashboard**: Web interface that can use this authentication system
- **Flask-Login**: Session management framework used by this system

### Secure Credential Manager (`credential_manager.py`) - **NEW**

**🔐 STATUS: PRODUCTION-READY SECURITY TOOL** - A secure credential management system that uses the operating system's keyring to store and retrieve sensitive authentication credentials with encryption.

**Key Features:**
- **System Keyring Integration**: Uses OS-level secure storage (Windows Credential Manager, macOS Keychain, Linux Secret Service)
- **Encrypted Password Storage**: Passwords are encrypted by the system keyring, never stored in plain text
- **Credential Indexing**: Maintains non-sensitive metadata in JSON index file
- **Interactive Setup**: User-friendly command-line interface for credential management
- **Multiple Credential Support**: Store and manage credentials for multiple portals and services
- **Programmatic Access**: Python API for integration with automation scripts
- **Secure Retrieval**: Retrieve credentials securely without exposing them in code or configuration files

**Security Architecture:**
- **Passwords**: Stored encrypted in system keyring (never in plain text files)
- **Usernames**: Stored encrypted in system keyring for consistency, also included in metadata index for display purposes
- **Metadata**: Non-sensitive information (username, description, URL, creation date) stored in JSON index
- **Separation of Concerns**: Sensitive data separated from configuration files
- **OS-Level Security**: Leverages operating system's native credential storage

**Usage:**

**Interactive Credential Setup:**
```bash
# Add new credentials interactively
python credential_manager.py add

# List all stored credentials (metadata only, no passwords)
python credential_manager.py list
```

**Programmatic Usage in Scripts:**
```python
from credential_manager import CredentialManager

# Initialize credential manager
manager = CredentialManager()

# Store credentials securely
manager.store_credential(
    credential_id="utility_portal",
    username="YOUR_EMAIL",
    password="YOUR_PASSWORD",
    description="Livingston NJ Utility Portal",
    url="https://livingstonnj.my360-app.com"
)

# Retrieve credentials
creds = manager.get_credential("utility_portal")
if creds:
    username = creds["username"]
    password = creds["password"]
    metadata = creds["metadata"]
    
    # Use credentials in automation
    print(f"Logging in as {username}")

# List all stored credentials (metadata only)
all_creds = manager.list_credentials()
for cred_id, metadata in all_creds.items():
    print(f"{cred_id}: {metadata['description']}")

# Update existing credentials
manager.update_credential(
    credential_id="utility_portal",
    password="NewPassword123",
    description="Updated description"
)

# Delete credentials
manager.delete_credential("utility_portal")
```

**Interactive Setup Flow:**
```bash
$ python credential_manager.py add

🔐 Secure Credential Setup
==================================================
Credential ID (e.g., 'utility_portal'): utility_portal
Description: Livingston NJ Utility Portal
URL: https://livingstonnj.my360-app.com
Username: YOUR_EMAIL
Password (hidden): ****************

✅ Credentials stored securely for 'utility_portal'
🔒 Password encrypted in system keyring
```

**List Stored Credentials:**
```bash
$ python credential_manager.py list

🔐 Stored Credentials
==================================================

📌 utility_portal
   Username: YOUR_EMAIL
   Description: Livingston NJ Utility Portal
   URL: https://livingstonnj.my360-app.com
   Created: 2026-02-10 14:30:45
```

**Core API Methods:**

**`store_credential(credential_id, username, password, description, url)`**
- Stores credentials securely in system keyring
- Saves metadata to JSON index file
- Encrypts password using OS keyring
- Returns: None

**`get_credential(credential_id)`**
- Retrieves credentials from keyring
- Returns: Dict with 'username', 'password', and 'metadata' keys
- Returns None if credential not found

**`list_credentials()`**
- Lists all stored credentials (metadata only)
- Returns: Dict of credential metadata (no passwords)
- Safe for display and logging

**`delete_credential(credential_id)`**
- Removes credentials from keyring and index
- Returns: True if successful, False if not found

**`update_credential(credential_id, username, password, description, url)`**
- Updates existing credentials
- All parameters optional (only updates provided values)
- Returns: True if successful, False if credential not found

**Configuration Files:**
- **`credentials_index.json`**: Non-sensitive metadata index
  - Credential IDs, usernames, and descriptions
  - URLs and creation timestamps
  - No passwords or sensitive data
  - Usernames included for display and identification purposes
- **System Keyring**: Encrypted credential storage
  - Windows: Windows Credential Manager
  - macOS: Keychain
  - Linux: Secret Service API (GNOME Keyring, KWallet)

**Integration with Automation Scripts:**

**Example: Secure Login in Nova Act Script:**
```python
from nova_act import NovaAct
from credential_manager import CredentialManager

# Retrieve credentials securely
manager = CredentialManager()
creds = manager.get_credential("utility_portal")

if not creds:
    print("❌ Credentials not found. Run: python credential_manager.py add")
    exit(1)

# Use credentials in automation
nova = NovaAct(
    starting_page=creds["metadata"]["url"],
    headless=False,
    tty=False,
    nova_act_api_key="YOUR_NOVA_ACT_API_KEY"
)

nova.start()

# Login with secure credentials
result = nova.act(f"""
Login with username: {creds['username']} and password: {creds['password']}
Navigate to usage section and export data.
""")

print(f"Automation result: {result}")
nova.stop()
```

**Security Best Practices:**
- **Never Hardcode Credentials**: Use credential manager instead of hardcoding passwords
- **Separate Metadata**: Keep sensitive data separate from configuration files
- **OS-Level Encryption**: Leverage operating system's secure credential storage
- **Access Control**: System keyring respects OS user permissions
- **Audit Trail**: Metadata includes creation timestamps for tracking

**System Requirements:**
- **Python Package**: `keyring` (install with `pip install keyring`)
- **Operating System Support**:
  - Windows: Windows Credential Manager (built-in)
  - macOS: Keychain (built-in)
  - Linux: Secret Service API (requires GNOME Keyring or KWallet)

**Installation:**
```bash
# Install keyring package
pip install keyring

# Verify installation
python -c "import keyring; print('Keyring installed successfully')"
```

**Best For:**
- **Production Deployments**: Secure credential storage for production automation
- **Multi-User Environments**: Each user's credentials stored separately
- **Security Compliance**: Meet security requirements for credential management
- **Development Workflows**: Avoid hardcoding credentials in scripts
- **Team Collaboration**: Share scripts without exposing credentials
- **Credential Rotation**: Easy password updates without modifying scripts

**Advantages Over Hardcoded Credentials:**
- **Security**: Passwords encrypted by OS, never in plain text
- **Separation**: Credentials separate from code and configuration
- **Flexibility**: Easy credential updates without code changes
- **Compliance**: Meets security best practices and compliance requirements
- **User-Specific**: Each user maintains their own credentials
- **Audit Trail**: Track when credentials were created and updated

**Migration from Hardcoded Credentials:**
```python
# Before (hardcoded - not secure):
username = "YOUR_EMAIL"
password = "YOUR_PASSWORD"

# After (secure credential manager):
from credential_manager import CredentialManager
manager = CredentialManager()
creds = manager.get_credential("utility_portal")
username = creds["username"]
password = creds["password"]
```

**Troubleshooting:**

**Keyring Not Available:**
```bash
# Linux: Install keyring backend
sudo apt-get install gnome-keyring  # Ubuntu/Debian
sudo yum install gnome-keyring      # RHEL/CentOS

# Verify keyring backend
python -c "import keyring; print(keyring.get_keyring())"
```

**Permission Issues:**
- Ensure user has access to system keyring
- On Linux, ensure keyring daemon is running
- On macOS, may need to grant Keychain access

**Credential Not Found:**
- Verify credential ID matches exactly (case-sensitive)
- Use `list` command to see all stored credentials
- Re-add credential if necessary

**Related Tools:**
- **Portal Automation Agent**: Can be integrated with credential manager for secure authentication
- **Nova Act Scripts**: All automation scripts can use credential manager
- **Environment Variables**: Alternative to credential manager for simpler deployments

**Future Enhancements:**
- Integration with Portal Automation Agent configuration
- Automatic credential rotation support
- Multi-factor authentication token storage
- Credential sharing across team members (with encryption)
- Backup and restore functionality

### Credential Login Tester (`test_credential_login.py`) - **NEW**

**🧪 STATUS: CREDENTIAL VALIDATION TOOL** - A standalone testing utility that validates stored credentials by attempting actual portal login using Nova Act automation.

**Key Features:**
- **Real Login Testing**: Validates credentials by attempting actual portal authentication
- **Nova Act Integration**: Uses browser automation to test credentials in real-world scenarios
- **Credential Manager Integration**: Retrieves credentials securely from system keyring
- **Visual Verification**: Keeps browser open for 10 seconds to visually confirm login success
- **Success Detection**: Automatically detects successful login by checking for dashboard elements
- **Error Reporting**: Provides detailed error messages and stack traces for troubleshooting
- **Interactive Mode**: Lists available credentials if none specified
- **Command-Line Interface**: Simple CLI for testing specific credentials

**Usage:**

**Test Specific Credential:**
```bash
# Test a specific credential by ID
python test_credential_login.py utility_portal
```

**Interactive Mode:**
```bash
# Run without arguments to see available credentials
python test_credential_login.py

# Output:
Available credentials:
  - utility_portal
  - backup_portal
  - test_account

Enter credential ID to test: utility_portal
```

**What it does:**
1. **🔐 Credential Retrieval**: Retrieves username and password from secure keyring storage
2. **🌐 Browser Launch**: Initializes Nova Act with Livingston NJ utility portal login URL
3. **📝 Login Attempt**: Enters credentials and submits login form
4. **⏳ Wait Period**: Waits 10 seconds for page to load and process authentication
5. **✅ Verification**: Checks for "Active Home" dropdown or dashboard elements to confirm success
6. **👁️ Visual Inspection**: Keeps browser open for 10 seconds for manual verification
7. **📊 Result Report**: Reports success or failure with detailed status information

**Output Example:**

**Successful Login:**
```bash
$ python test_credential_login.py utility_portal

Testing credential: utility_portal
Username: YOUR_EMAIL
URL: https://livingstonnj.my360-app.com

Initializing browser...
Browser started

Attempting login...
Login result: [Nova Act execution details]
Verification result: SUCCESS - Dashboard elements found

✅ LOGIN TEST SUCCESSFUL!

Browser will stay open for 10 seconds for inspection...
Browser closed
```

**Failed Login:**
```bash
$ python test_credential_login.py invalid_cred

Testing credential: invalid_cred
Username: test@example.com
URL: https://livingstonnj.my360-app.com

Initializing browser...
Browser started

Attempting login...
Login result: [Nova Act execution details]
Verification result: FAILED - Still on login page

❌ LOGIN TEST FAILED

Browser will stay open for 10 seconds for inspection...
Browser closed
```

**Credential Not Found:**
```bash
$ python test_credential_login.py nonexistent

Credential 'nonexistent' not found
```

**Core Functionality:**

**`test_login(credential_id)` Function:**
- **Parameters**: `credential_id` (string) - ID of credential to test
- **Returns**: Boolean - True if login successful, False otherwise
- **Process**:
  1. Retrieves credential from CredentialManager
  2. Initializes Nova Act browser session
  3. Navigates to portal login page
  4. Enters username and password
  5. Submits login form
  6. Waits for page load
  7. Verifies successful login by checking for dashboard elements
  8. Keeps browser open for visual inspection
  9. Closes browser and returns result

**Login Verification Logic:**
The script checks for successful login by looking for:
- "Active Home" dropdown element (primary indicator)
- Dashboard page elements (secondary indicator)
- Absence of login page elements (negative check)

Returns "SUCCESS" if logged in, "FAILED" if still on login page or error page.

**Integration with Credential Manager:**
```python
from credential_manager import CredentialManager

manager = CredentialManager()
cred = manager.get_credential(credential_id)

if not cred:
    print(f"Credential '{credential_id}' not found")
    return False

username = cred['username']
password = cred['password']
url = cred['metadata'].get('url', 'N/A')
```

**Nova Act Configuration:**
- **Starting Page**: Full Livingston NJ utility portal login URL with OAuth parameters
- **Headless Mode**: False (visible browser for verification)
- **TTY Mode**: False (non-interactive terminal mode)
- **API Key**: Uses standard Nova Act API key `YOUR_NOVA_ACT_API_KEY`

**Login Instructions:**
The script provides detailed instructions to Nova Act:
```
Login to the portal:
1. Enter username: {username}
2. Enter password: {password}
3. Click login button
4. Wait 10 seconds for the page to load
5. Check if login was successful by looking for dashboard or home page elements
```

**Best For:**
- **Credential Validation**: Verify stored credentials are correct before using in automation
- **Troubleshooting**: Diagnose authentication issues in automation scripts
- **Credential Testing**: Test newly added credentials before production use
- **Security Audits**: Verify credential storage and retrieval works correctly
- **Development**: Quick way to test portal access without running full automation

**Use Cases:**

**Before Running Automation:**
```bash
# Test credentials first
python test_credential_login.py utility_portal

# If successful, run automation
python portal_automation_agent.py --start
```

**After Adding New Credentials:**
```bash
# Add new credential
python credential_manager.py add

# Test the new credential
python test_credential_login.py new_portal_id
```

**Troubleshooting Failed Automation:**
```bash
# If automation fails, test credentials
python test_credential_login.py utility_portal

# Check if credentials are the issue
```

**Advantages:**
- **Real-World Testing**: Tests actual portal login, not just credential retrieval
- **Visual Verification**: Browser stays open for manual confirmation
- **Quick Validation**: Fast way to verify credentials work
- **Error Detection**: Identifies authentication issues before automation runs
- **No Side Effects**: Read-only operation, doesn't modify any data

**Technical Details:**
- **Browser Session**: 10-second wait for page load + 10-second inspection window
- **Success Detection**: Looks for "Active Home" dropdown or dashboard elements
- **Error Handling**: Comprehensive try-catch with stack trace output
- **Cleanup**: Properly stops Nova Act session after test
- **Timeout**: Total test time approximately 30-40 seconds

**Error Handling:**
```python
try:
    # Test login process
    success = test_login(credential_id)
except Exception as e:
    print(f"\n❌ Error during login test: {e}")
    import traceback
    traceback.print_exc()
    return False
```

**Integration with Other Tools:**
- **Credential Manager**: Retrieves credentials from secure keyring
- **Nova Act**: Uses same browser automation framework as main scripts
- **Portal Automation Agent**: Can validate credentials before scheduled tasks
- **V2 Dashboard**: Complements web-based credential testing feature

**Comparison with Dashboard Test Login:**

| Feature | test_credential_login.py | Dashboard Test Login |
|---------|-------------------------|---------------------|
| Interface | Command-line | Web browser |
| Credential Selection | CLI argument | Dropdown menu |
| Visual Feedback | Terminal output | Web page |
| Browser Visibility | Always visible | Configurable |
| Inspection Time | 10 seconds | Configurable |
| Use Case | Development/CLI | Production/Web UI |

**Prerequisites:**
- **Credential Manager**: Credentials must be stored using `credential_manager.py`
- **Nova Act**: Nova Act package installed and configured
- **Browser**: Chrome/Chromium browser available
- **API Key**: Valid Nova Act API key configured

**Limitations:**
- **Single Credential**: Tests one credential at a time
- **Manual Verification**: Requires visual inspection for confirmation
- **Browser Required**: Cannot run in headless-only environments
- **Timeout**: Fixed 10-second wait periods (not configurable)

**Future Enhancements:**
- Configurable wait times and inspection periods
- Batch testing of multiple credentials
- Automated success detection without visual inspection
- Integration with CI/CD pipelines for credential validation
- Detailed logging of login attempts and results

### Other Development Scripts

For additional automation and testing capabilities, see the various Nova Act and Selenium scripts included in the project. These are primarily for development and testing purposes and include comprehensive automation workflows, download handling, and PDF analysis features.

## Troubleshooting

### Common Issues

**Account Access**
- **Account Locked**: Ensure the utility account is unlocked before running automation
- **Authentication Errors**: Scripts use standardized credentials (`YOUR_EMAIL` / `YOUR_PASSWORD`)
- **Login Redirect Issues**: Use `robust_nova_download.py` for improved redirect handling

**Nova Act Issues**
- **Browser Compatibility**: Nova Act scripts require Chrome/Chromium browser
- **API Key**: Ensure Nova Act API key `YOUR_NOVA_ACT_API_KEY` is valid
- **Session Persistence**: Most scripts keep browser sessions open for manual verification

**Download Issues**
- **File Detection**: Scripts monitor Downloads folder for files modified within last 5-10 minutes
- **Automatic Opening**: Scripts use `os.startfile()` on Windows to open downloaded files
- **Manual Verification**: Check Downloads folder manually if automatic detection fails

**Timing Issues**
- **Screen Transitions**: Working version includes optimized wait periods for reliable navigation
- **LastPass Interference**: Working version automatically handles password manager prompts
- **Page Loading**: Scripts include balanced wait times for reliable page loading

### Script Selection Guide

**For Production Use:**
- ✅ **RECOMMENDED**: `WORKING_simple_navigation_helper.py` - Confirmed working version with 100% success rates

**For Scheduled Automation:**
- `standalone_scheduler.py` - **NEW** - Standalone scheduler without Flask interference (recommended for production)
- `portal_automation_agent.py` - **NEW** - Advanced scheduling system for multiple daily automation tasks
- `agent_dashboard.py` - **NEW** - Web-based dashboard for managing and monitoring scheduled tasks

**For Data Extraction:**
- `nova_extract_and_recreate.py` - Direct web data extraction (recently updated with new password)
- `extract_from_existing_session.py` - Quick data extraction from existing sessions
- `nova_read_pdf_content.py` - **NEW** - Direct PDF content extraction and transcription

**For File Analysis:**
- `simple_file_analyzer.py` - Analyze recently downloaded files
- `analyze_downloaded_file.py` - Comprehensive file analysis
- `get_actual_data.py` - Analyze Nova Act extraction results and metadata

**For Development/Testing:**
- `diagnose_nova_issues.py` - **UPDATED** - Comprehensive system diagnostics and troubleshooting (run this first)
- `debug_nova.py` - Nova Act integration testing
- `test_nova.py` - Basic functionality testing
- `test_simple_nova.py` - **NEW** - Simple Nova Act automation test with demo site
- `test_task_now.py` - **NEW** - Immediate task execution test for Portal Automation Agent
- `run_task_now.py` - **NEW** - Run specific tasks immediately bypassing scheduler
- `run_task_immediately.py` - **NEW** - Direct Nova Act task execution without Portal Agent
- `chrome_test_simple.py` - **NEW** - Chrome browser-specific Nova Act test with enhanced error handling
- `cleanup_stuck_tasks.py` - **NEW** - Reset tasks stuck in 'running' state
- `check_nova_logs.py` - Log inspection utility

### Recent Updates

**Simple Navigation Helper Password Update (Latest)**
- **Password Updated**: `simple_navigation_helper.py` password changed to `YOUR_PASSWORD` for consistency with advanced extraction scripts
- **Alignment with Data Extraction**: Now uses same password as `nova_extract_and_recreate.py` and `nova_read_pdf_content.py`
- **Improved Authentication**: Enhanced authentication reliability across all automation workflows
- **Note**: The confirmed working version `WORKING_simple_navigation_helper.py` continues to use `YOUR_PASSWORD` as the production-ready baseline

**Portal Automation Agent Enhancement (Previous)**
- **Improved Configuration Loading**: Enhanced enum handling in `portal_automation_agent.py` for more reliable task status persistence
- **Better Error Prevention**: Status enum conversion now handles edge cases to prevent configuration corruption
- **Enhanced Reliability**: Improved JSON configuration loading prevents issues when restarting the automation agent

**Earlier Updates**
- `nova_extract_and_recreate.py` updated with password: `YOUR_PASSWORD` (advanced extraction script)
- Standardized authentication credentials across all scripts
- Enhanced timing control and session management
- Improved error handling and logging
- Added comprehensive data extraction capabilities

## Legacy Flask Application

This project contains legacy Flask application files that are not part of the current Nova Act automation functionality:

- `app.py` - Flask web application (not used)
- `application.py` - AWS Elastic Beanstalk entry point (not used)
- `templates/` - HTML templates (not used)
- `.ebextensions/` - AWS configuration (not used)
- `cloudformation/` - Infrastructure templates (not used)

These files remain for historical reference but are not required for the Nova Act automation workflows.
#!/usr/bin/env python3
"""
Portal Automation Agent - Example Usage
Demonstrates how to set up and use the Portal Automation Agent
"""

from portal_automation_agent import PortalAutomationAgent
import time
import json

def main():
    print("🤖 Portal Automation Agent - Example Usage")
    print("=" * 50)
    
    # Create agent instance
    agent = PortalAutomationAgent("example_config.json")
    
    # Example 1: Add a utility portal task (based on existing working script)
    print("\n📋 Adding utility portal task...")
    utility_task_id = agent.add_task(
        name="Daily Utility Usage Report",
        url="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
        instructions="""Navigate to the export page:
1. Login with username: {{credential:utility_portal:username}} and password: {{credential:utility_portal:password}}. Then wait 1 minute for next screen to come up.
2. Locate and Select Active Home dropdown and choose "103892 0". Wait 15 seconds again. If Lastpass save password prompt comes up, click Never and close.
3. Navigate to the Usage History section. Locate More Details button and click that. Wait for 15 seconds.
4. Locate the Export button and Click here. On Pop up, Click PDF.
5. Wait for download to complete and verify file is saved.""",
        scheduled_time="09:00"
    )
    print(f"✅ Created utility task: {utility_task_id}")
    
    # Example 2: Add a generic web portal task
    print("\n📋 Adding generic portal task...")
    generic_task_id = agent.add_task(
        name="Weekly Report Download",
        url="https://example-portal.com/login",
        instructions="""Weekly report automation:
1. Login with credentials from environment variables
2. Navigate to Reports section
3. Select "Weekly Summary" report
4. Set date range to last 7 days
5. Click Export button
6. Choose Excel format
7. Wait for download to complete""",
        scheduled_time="17:30"
    )
    print(f"✅ Created generic task: {generic_task_id}")
    
    # Example 3: Add a monitoring task
    print("\n📋 Adding monitoring task...")
    monitor_task_id = agent.add_task(
        name="System Health Check",
        url="https://monitoring.example.com/dashboard",
        instructions="""System monitoring check:
1. Login to monitoring dashboard
2. Check all system status indicators
3. Verify all services are green
4. If any issues found, take screenshot
5. Export system metrics for last 24 hours
6. Save report to designated folder""",
        scheduled_time="06:00"
    )
    print(f"✅ Created monitoring task: {monitor_task_id}")
    
    # Show current tasks
    print("\n📊 Current Tasks:")
    tasks = agent.list_tasks()
    for task in tasks:
        print(f"  • {task['name']} - {task['scheduled_time']} ({task['status']})")
    
    # Show status report
    print("\n📈 Status Report:")
    report = agent.get_status_report()
    print(f"  Agent Status: {report['agent_status']}")
    print(f"  Total Tasks: {report['total_tasks']}")
    print(f"  Task Statistics: {report['task_statistics']}")
    
    # Example of updating a task
    print(f"\n🔧 Updating task {utility_task_id}...")
    agent.update_task(utility_task_id, scheduled_time="08:30")
    print("✅ Task updated successfully")
    
    # Example of disabling a task
    print(f"\n⏸️ Disabling task {monitor_task_id}...")
    agent.update_task(monitor_task_id, enabled=False)
    print("✅ Task disabled")
    
    # Start the scheduler (commented out for example)
    print("\n🚀 To start the scheduler, uncomment the following lines:")
    print("# agent.start_scheduler()")
    print("# print('Agent is running... Press Ctrl+C to stop')")
    print("# try:")
    print("#     while True:")
    print("#         time.sleep(60)")
    print("# except KeyboardInterrupt:")
    print("#     agent.stop_scheduler()")
    print("#     print('Agent stopped')")
    
    # Show how to use CLI instead
    print("\n💡 Alternative: Use the CLI interface")
    print("python agent_cli.py start")
    print("python agent_cli.py status")
    print("python agent_cli.py list")
    
    # Show how to use web dashboard
    print("\n🌐 Alternative: Use the web dashboard")
    print("python agent_dashboard.py")
    print("Then open: http://localhost:5000")
    
    print("\n✨ Example completed! Check 'example_config.json' for the generated configuration.")

if __name__ == "__main__":
    main()
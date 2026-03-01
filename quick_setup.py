#!/usr/bin/env python3
"""
Quick Setup Script for Portal Automation Agent
Sets up your first scheduled task based on your working automation
"""

from portal_automation_agent import PortalAutomationAgent
import json

def main():
    print("🚀 Portal Automation Agent - Quick Setup")
    print("=" * 50)
    
    # Create agent instance
    agent = PortalAutomationAgent("agent_config.json")
    
    print("\n📋 Setting up your utility portal automation task...")
    
    # Your existing working automation converted to a scheduled task
    task_id = agent.add_task(
        name="Daily Utility Usage Report",
        url="https://identity.my360-app.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dmy360-app%26state%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0semicolon%25252Fdashboard%26redirect_uri%3Dhttps%253A%252F%252Flivingstonnj.my360-app.com%252F%26scope%3Dopenid%2520profile%2520offline_access%26code_challenge%3DclK8rXphATi0e_O9iK0eNojFKkUtEPAqfj2CKrNnC5Q%26code_challenge_method%3DS256%26nonce%3DVHZnalRySDdsbEFUaWpHUWktZEZrNUliR2lrYy1XUzJYWDdOVjZmRnFvMEQ0%26dns%3Dlivingstonnj",
        instructions="""Navigate to the export page:
1. Login with username: narang.sachin@gmail.com and password: Testing1234!123. Then wait 1 minute for next screen to come up.
2. Locate and Select Active Home dropdown and choose "103892 0". Wait 15 seconds again. If Lastpass save password prompt comes up, click Never and close.
3. Navigate to the Usage History section. Locate More Details button and click that. Wait for 15 seconds.
4. Locate the Export button and Click here. On Pop up, Click PDF.
5. Wait for download to complete and verify file is saved to Downloads folder.""",
        scheduled_time="09:00"  # 9 AM daily
    )
    
    print(f"✅ Created task: {task_id}")
    print(f"📅 Scheduled for: 9:00 AM daily")
    
    # Show status
    print("\n📊 Current Configuration:")
    tasks = agent.list_tasks()
    for task in tasks:
        print(f"  • {task['name']}")
        print(f"    - URL: {task['url'][:60]}...")
        print(f"    - Time: {task['scheduled_time']}")
        print(f"    - Status: {task['status']}")
        print(f"    - Enabled: {task['enabled']}")
    
    print("\n🎯 Next Steps:")
    print("1. Test the task manually first:")
    print("   python agent_cli.py details", task_id)
    print()
    print("2. Start the agent scheduler:")
    print("   python agent_cli.py start")
    print()
    print("3. Monitor via web dashboard:")
    print("   python agent_dashboard.py")
    print("   Then open: http://localhost:5000")
    print()
    print("4. Check status anytime:")
    print("   python agent_cli.py status")
    
    print(f"\n💾 Configuration saved to: agent_config.json")
    print("🎉 Setup complete! Your automation is ready to run daily at 9:00 AM")

if __name__ == "__main__":
    main()
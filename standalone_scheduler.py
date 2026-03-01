#!/usr/bin/env python3
"""
Standalone Scheduler - Run without Flask interference
Runs the scheduler in a clean process without Flask's debug mode
"""

from portal_automation_agent import PortalAutomationAgent
import time
import sys

def main():
    print("🚀 Starting Standalone Portal Automation Scheduler")
    print("=" * 60)
    print("This runs the scheduler WITHOUT Flask interference")
    print("Nova Act should work properly in this mode")
    print("=" * 60)
    
    # Create agent
    agent = PortalAutomationAgent("agent_config.json")
    
    # Show current tasks
    tasks = agent.list_tasks()
    print(f"\n📋 Loaded {len(tasks)} task(s):")
    for task in tasks:
        status_emoji = {
            'pending': '⏳',
            'running': '🔄',
            'completed': '✅',
            'failed': '❌'
        }.get(task['status'], '❓')
        
        enabled_str = "" if task['enabled'] else " (DISABLED)"
        print(f"  {status_emoji} {task['name']} - {task['scheduled_time']}{enabled_str}")
    
    print("\n🚀 Starting scheduler...")
    print("💡 This runs in a clean process - Nova Act should work properly")
    print("📊 Press Ctrl+C to stop\n")
    
    # Start scheduler
    agent.start_scheduler()
    
    try:
        while True:
            time.sleep(60)
            # Print status every minute
            print(f"⏰ {time.strftime('%H:%M:%S')} - Scheduler running...")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping scheduler...")
        agent.stop_scheduler()
        print("✅ Scheduler stopped successfully")
        sys.exit(0)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Cleanup Stuck Tasks
Reset tasks that are stuck in 'running' state
"""

from portal_automation_agent import PortalAutomationAgent, TaskStatus
from datetime import datetime

def main():
    print("🔧 Cleaning Up Stuck Tasks")
    print("=" * 50)
    
    agent = PortalAutomationAgent("agent_config.json")
    
    stuck_tasks = []
    for task_id, task in agent.tasks.items():
        if task.status == TaskStatus.RUNNING:
            stuck_tasks.append((task_id, task))
    
    if not stuck_tasks:
        print("✅ No stuck tasks found")
        return
    
    print(f"Found {len(stuck_tasks)} stuck task(s):\n")
    
    for task_id, task in stuck_tasks:
        print(f"📋 Task: {task.name}")
        print(f"   ID: {task_id}")
        print(f"   Status: {task.status.value}")
        print(f"   Last Run: {task.last_run}")
        print()
        
        # Reset to failed status with explanation
        task.status = TaskStatus.FAILED
        task.error_message = "Task was stuck in running state - likely browser closed unexpectedly"
        
        print(f"✅ Reset {task.name} to 'failed' status")
        print()
    
    agent.save_config()
    print("💾 Configuration saved")
    print()
    print("🎯 Next Steps:")
    print("1. Start the scheduler: python agent_cli.py start")
    print("2. Or view status: python agent_cli.py status")
    print("3. Tasks will retry automatically if enabled")

if __name__ == "__main__":
    main()
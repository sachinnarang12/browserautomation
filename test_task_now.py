#!/usr/bin/env python3
"""
Test Task Execution - Run a task immediately for testing
"""

from portal_automation_agent import PortalAutomationAgent
import time

def main():
    print("🧪 Testing Task Execution Now")
    print("=" * 40)
    
    # Create agent instance
    agent = PortalAutomationAgent("agent_config.json")
    
    # Create a simple test task that runs immediately
    current_time = time.strftime("%H:%M")
    next_minute = time.strftime("%H:%M", time.localtime(time.time() + 60))
    
    print(f"⏰ Current time: {current_time}")
    print(f"📅 Scheduling test task for: {next_minute}")
    
    # Add a simple test task
    task_id = agent.add_task(
        name="Immediate Test Task",
        url="https://demoqa.com/login",
        instructions="""Simple test automation:
1. Navigate to the login page
2. Wait for page to load (3 seconds)
3. Take a screenshot of the page
4. Close the browser""",
        scheduled_time=next_minute
    )
    
    print(f"✅ Created test task: {task_id}")
    print(f"🚀 Starting scheduler...")
    
    # Start the scheduler
    agent.start_scheduler()
    
    print("⏳ Waiting for task execution...")
    print("🔍 Watch for browser window to appear")
    print("📊 Press Ctrl+C to stop after task completes")
    
    try:
        # Wait and monitor
        for i in range(120):  # Wait up to 2 minutes
            time.sleep(1)
            
            # Check task status
            if task_id in agent.tasks:
                task = agent.tasks[task_id]
                if task.status.value != 'pending' and task.status.value != 'running':
                    print(f"\n✅ Task completed with status: {task.status.value}")
                    if task.result:
                        print(f"📋 Result: {task.result}")
                    if task.error_message:
                        print(f"❌ Error: {task.error_message}")
                    break
            
            if i % 10 == 0:  # Print status every 10 seconds
                print(f"⏳ Waiting... ({i}s)")
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
    finally:
        agent.stop_scheduler()
        print("✅ Test completed")

if __name__ == "__main__":
    main()
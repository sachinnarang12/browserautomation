#!/usr/bin/env python3
"""
Run a specific task immediately (bypassing scheduler)
"""

import json
import sys
from pathlib import Path
from portal_automation_agent import PortalAutomationAgent

def run_task_now(task_id):
    """Run a task immediately"""
    config_file = Path('agent_config.json')
    
    if not config_file.exists():
        print("❌ No config file found")
        return False
    
    with open(config_file, 'r') as f:
        data = json.load(f)
    
    # Find the task
    task = next((t for t in data['tasks'] if t['id'] == task_id), None)
    
    if not task:
        print(f"❌ Task {task_id} not found")
        return False
    
    print(f"🚀 Running task: {task['name']}")
    print(f"   URL: {task['url']}")
    print(f"   Instructions: {task['instructions'][:100]}...")
    print()
    
    # Create agent and run task
    agent = PortalAutomationAgent()
    
    try:
        result = agent.execute_task(task)
        print(f"\n✅ Task completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Task failed: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        task_id = sys.argv[1]
    else:
        # Run the most recent task
        config_file = Path('agent_config.json')
        with open(config_file, 'r') as f:
            data = json.load(f)
        
        if not data['tasks']:
            print("❌ No tasks found")
            sys.exit(1)
        
        # Get the last task
        task_id = data['tasks'][-1]['id']
        print(f"📋 Running most recent task: {task_id}")
    
    success = run_task_now(task_id)
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Portal Automation Agent CLI
User-friendly command-line interface for managing scheduled portal automation tasks.
"""

import json
import sys
from datetime import datetime
from typing import Optional
from portal_automation_agent import PortalAutomationAgent, TaskStatus
import argparse

class AgentCLI:
    """Command-line interface for the Portal Automation Agent"""
    
    def __init__(self, config_file: str = "agent_config.json"):
        self.agent = PortalAutomationAgent(config_file)
    
    def add_task_interactive(self):
        """Interactive task creation"""
        print("\n🤖 Add New Automation Task")
        print("=" * 40)
        
        name = input("Task name: ").strip()
        if not name:
            print("❌ Task name is required")
            return
        
        url = input("Portal URL: ").strip()
        if not url:
            print("❌ URL is required")
            return
        
        print("\nEnter automation instructions (multi-line, press Enter twice to finish):")
        instructions_lines = []
        while True:
            line = input()
            if line == "" and instructions_lines and instructions_lines[-1] == "":
                break
            instructions_lines.append(line)
        
        instructions = "\n".join(instructions_lines[:-1])  # Remove last empty line
        
        if not instructions.strip():
            print("❌ Instructions are required")
            return
        
        while True:
            scheduled_time = input("Scheduled time (HH:MM, 24-hour format): ").strip()
            try:
                datetime.strptime(scheduled_time, "%H:%M")
                break
            except ValueError:
                print("❌ Invalid time format. Use HH:MM (e.g., 14:30)")
        
        task_id = self.agent.add_task(name, url, instructions, scheduled_time)
        print(f"✅ Task created successfully with ID: {task_id}")
    
    def list_tasks(self):
        """Display all tasks in a formatted table"""
        tasks = self.agent.list_tasks()
        
        if not tasks:
            print("📋 No tasks configured")
            return
        
        print(f"\n📋 Scheduled Tasks ({len(tasks)} total)")
        print("=" * 80)
        
        # Header
        print(f"{'ID':<12} {'Name':<20} {'Time':<8} {'Status':<12} {'Last Run':<20}")
        print("-" * 80)
        
        # Tasks
        for task in tasks:
            last_run = "Never"
            if task['last_run']:
                try:
                    dt = datetime.fromisoformat(task['last_run'].replace('Z', '+00:00'))
                    last_run = dt.strftime("%m/%d %H:%M")
                except:
                    last_run = "Invalid"
            
            status_emoji = {
                'pending': '⏳',
                'running': '🔄',
                'completed': '✅',
                'failed': '❌',
                'cancelled': '🚫'
            }.get(task['status'], '❓')
            
            enabled_indicator = "" if task['enabled'] else " (DISABLED)"
            
            print(f"{task['id']:<12} {task['name'][:19]:<20} {task['scheduled_time']:<8} "
                  f"{status_emoji} {task['status']:<10} {last_run:<20}{enabled_indicator}")
    
    def show_status(self):
        """Display comprehensive status report"""
        report = self.agent.get_status_report()
        
        print(f"\n🤖 Portal Automation Agent Status")
        print("=" * 50)
        print(f"Agent Status: {'🟢 Running' if report['agent_status'] == 'running' else '🔴 Stopped'}")
        print(f"Total Tasks: {report['total_tasks']}")
        print(f"Active Sessions: {report['active_sessions']}")
        print(f"Last Updated: {datetime.fromisoformat(report['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Task statistics
        stats = report['task_statistics']
        print(f"\n📊 Task Statistics:")
        print(f"  ⏳ Pending: {stats.get('pending', 0)}")
        print(f"  🔄 Running: {stats.get('running', 0)}")
        print(f"  ✅ Completed: {stats.get('completed', 0)}")
        print(f"  ❌ Failed: {stats.get('failed', 0)}")
        
        # Upcoming tasks
        if report['upcoming_tasks']:
            print(f"\n⏰ Next Scheduled Tasks:")
            for task in report['upcoming_tasks']:
                next_run = datetime.fromisoformat(task['next_run'])
                print(f"  • {task['task_name']} - {next_run.strftime('%H:%M')} ({task['time_until']})")
        
        # Failed tasks
        failed_tasks = [t for t in report['tasks'].values() if t['status'] == 'failed']
        if failed_tasks:
            print(f"\n❌ Failed Tasks:")
            for task in failed_tasks:
                print(f"  • {task['name']} - {task.get('error', 'Unknown error')}")
    
    def task_details(self, task_id: str):
        """Show detailed information about a specific task"""
        if task_id not in self.agent.tasks:
            print(f"❌ Task {task_id} not found")
            return
        
        task = self.agent.tasks[task_id]
        
        print(f"\n📋 Task Details: {task.name}")
        print("=" * 50)
        print(f"ID: {task.id}")
        print(f"Name: {task.name}")
        print(f"URL: {task.url}")
        print(f"Scheduled Time: {task.scheduled_time}")
        print(f"Status: {task.status.value}")
        print(f"Enabled: {'Yes' if task.enabled else 'No'}")
        print(f"Created: {task.created_at}")
        print(f"Last Run: {task.last_run or 'Never'}")
        print(f"Retry Count: {task.retry_count}/{task.max_retries}")
        
        if task.error_message:
            print(f"Last Error: {task.error_message}")
        
        if task.result:
            print(f"\nLast Result:")
            print("-" * 30)
            print(task.result[:500] + ("..." if len(task.result) > 500 else ""))
        
        print(f"\nInstructions:")
        print("-" * 30)
        print(task.instructions)
    
    def enable_disable_task(self, task_id: str, enable: bool):
        """Enable or disable a task"""
        if self.agent.update_task(task_id, enabled=enable):
            status = "enabled" if enable else "disabled"
            print(f"✅ Task {task_id} {status} successfully")
        else:
            print(f"❌ Task {task_id} not found")
    
    def delete_task(self, task_id: str):
        """Delete a task with confirmation"""
        if task_id not in self.agent.tasks:
            print(f"❌ Task {task_id} not found")
            return
        
        task = self.agent.tasks[task_id]
        print(f"⚠️  Are you sure you want to delete task '{task.name}'? (y/N): ", end="")
        
        if input().lower().strip() == 'y':
            if self.agent.remove_task(task_id):
                print(f"✅ Task {task_id} deleted successfully")
            else:
                print(f"❌ Failed to delete task {task_id}")
        else:
            print("❌ Deletion cancelled")
    
    def start_agent(self):
        """Start the agent scheduler"""
        print("🚀 Starting Portal Automation Agent...")
        self.agent.start_scheduler()
        
        try:
            print("✅ Agent is running. Press Ctrl+C to stop.")
            print("📊 Use 'python agent_cli.py status' in another terminal to monitor")
            
            while True:
                import time
                time.sleep(60)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping agent...")
            self.agent.stop_scheduler()
            print("✅ Agent stopped successfully")

def main():
    parser = argparse.ArgumentParser(
        description="Portal Automation Agent CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python agent_cli.py add                    # Add new task interactively
  python agent_cli.py list                   # List all tasks
  python agent_cli.py status                 # Show status report
  python agent_cli.py details task_123       # Show task details
  python agent_cli.py enable task_123        # Enable a task
  python agent_cli.py disable task_123       # Disable a task
  python agent_cli.py delete task_123        # Delete a task
  python agent_cli.py start                  # Start the agent
        """
    )
    
    parser.add_argument("--config", default="agent_config.json", help="Configuration file path")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add task command
    subparsers.add_parser("add", help="Add a new task interactively")
    
    # List tasks command
    subparsers.add_parser("list", help="List all tasks")
    
    # Status command
    subparsers.add_parser("status", help="Show agent status report")
    
    # Task details command
    details_parser = subparsers.add_parser("details", help="Show detailed task information")
    details_parser.add_argument("task_id", help="Task ID to show details for")
    
    # Enable task command
    enable_parser = subparsers.add_parser("enable", help="Enable a task")
    enable_parser.add_argument("task_id", help="Task ID to enable")
    
    # Disable task command
    disable_parser = subparsers.add_parser("disable", help="Disable a task")
    disable_parser.add_argument("task_id", help="Task ID to disable")
    
    # Delete task command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", help="Task ID to delete")
    
    # Start agent command
    subparsers.add_parser("start", help="Start the agent scheduler")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = AgentCLI(args.config)
    
    try:
        if args.command == "add":
            cli.add_task_interactive()
        elif args.command == "list":
            cli.list_tasks()
        elif args.command == "status":
            cli.show_status()
        elif args.command == "details":
            cli.task_details(args.task_id)
        elif args.command == "enable":
            cli.enable_disable_task(args.task_id, True)
        elif args.command == "disable":
            cli.enable_disable_task(args.task_id, False)
        elif args.command == "delete":
            cli.delete_task(args.task_id)
        elif args.command == "start":
            cli.start_agent()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
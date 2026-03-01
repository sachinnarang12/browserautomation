#!/usr/bin/env python3
"""
Portal Automation Agent
A flexible scheduling system for automating web portal tasks using Nova Act.
Allows users to schedule multiple activities throughout the day with status monitoring.
"""

import json
import time
import schedule
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
from nova_act import NovaAct
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('portal_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class PortalTask:
    """Represents a scheduled portal automation task"""
    id: str
    name: str
    url: str
    instructions: str
    scheduled_time: str  # HH:MM format
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = ""
    last_run: Optional[str] = None
    result: Optional[str] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    enabled: bool = True
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

class PortalAutomationAgent:
    """Main agent class for managing scheduled portal automation tasks"""
    
    def __init__(self, config_file: str = "agent_config.json"):
        self.config_file = Path(config_file)
        self.tasks: Dict[str, PortalTask] = {}
        self.nova_sessions: Dict[str, NovaAct] = {}
        self.is_running = False
        self.scheduler_thread = None
        
        # Nova Act configuration
        self.nova_config = {
            "headless": False,
            "tty": False,
            "nova_act_api_key": "3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
        }
        
        self.load_config()
        
    def load_config(self):
        """Load tasks and configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    
                # Load tasks
                for task_data in data.get('tasks', []):
                    # Convert status string back to enum
                    if 'status' in task_data and isinstance(task_data['status'], str):
                        task_data['status'] = TaskStatus(task_data['status'])
                    task = PortalTask(**task_data)
                    self.tasks[task.id] = task
                    
                # Load Nova Act config if present
                if 'nova_config' in data:
                    self.nova_config.update(data['nova_config'])
                    
                logger.info(f"Loaded {len(self.tasks)} tasks from config")
            except Exception as e:
                logger.error(f"Error loading config: {e}")
        else:
            logger.info("No existing config found, starting fresh")
    
    def save_config(self):
        """Save current tasks and configuration to file"""
        try:
            # Convert tasks to dict format with proper enum handling
            tasks_data = []
            for task in self.tasks.values():
                task_dict = asdict(task)
                # Convert enum to string for JSON serialization
                task_dict['status'] = task.status.value
                tasks_data.append(task_dict)
            
            data = {
                'tasks': tasks_data,
                'nova_config': self.nova_config,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
                
            logger.info("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def add_task(self, name: str, url: str, instructions: str, scheduled_time: str) -> str:
        """Add a new scheduled task"""
        task_id = f"task_{int(time.time())}_{len(self.tasks)}"
        
        task = PortalTask(
            id=task_id,
            name=name,
            url=url,
            instructions=instructions,
            scheduled_time=scheduled_time
        )
        
        self.tasks[task_id] = task
        self.save_config()
        
        # Schedule the task
        self._schedule_task(task)
        
        logger.info(f"Added new task: {name} scheduled for {scheduled_time}")
        return task_id
    
    def remove_task(self, task_id: str) -> bool:
        """Remove a scheduled task"""
        if task_id in self.tasks:
            # Cancel any running Nova session for this task
            if task_id in self.nova_sessions:
                try:
                    self.nova_sessions[task_id].stop()
                    del self.nova_sessions[task_id]
                except:
                    pass
            
            del self.tasks[task_id]
            self.save_config()
            logger.info(f"Removed task: {task_id}")
            return True
        return False
    
    def update_task(self, task_id: str, **kwargs) -> bool:
        """Update an existing task"""
        if task_id not in self.tasks:
            return False
            
        task = self.tasks[task_id]
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        self.save_config()
        
        # Reschedule if time changed
        if 'scheduled_time' in kwargs:
            self._schedule_task(task)
            
        logger.info(f"Updated task: {task_id}")
        return True
    
    def _schedule_task(self, task: PortalTask):
        """Schedule a task with the scheduler"""
        if not task.enabled:
            return
            
        try:
            schedule.every().day.at(task.scheduled_time).do(
                self._execute_task, task.id
            ).tag(task.id)
            logger.info(f"Scheduled task {task.name} for {task.scheduled_time}")
        except Exception as e:
            logger.error(f"Error scheduling task {task.id}: {e}")
    
    def _execute_task(self, task_id: str):
        """Execute a scheduled task"""
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found")
            return
            
        task = self.tasks[task_id]
        
        if not task.enabled:
            logger.info(f"Task {task.name} is disabled, skipping")
            return
            
        logger.info(f"Starting execution of task: {task.name}")
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.last_run = datetime.now().isoformat()
        self.save_config()
        
        try:
            # Create Nova Act session
            nova = NovaAct(
                starting_page=task.url,
                **self.nova_config
            )
            
            self.nova_sessions[task_id] = nova
            nova.start()
            
            # Execute the instructions
            result = nova.act(task.instructions)
            
            # Update task with success
            task.status = TaskStatus.COMPLETED
            task.result = str(result)
            task.retry_count = 0
            
            logger.info(f"Task {task.name} completed successfully")
            
        except Exception as e:
            logger.error(f"Task {task.name} failed: {e}")
            
            # Update task with failure
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            task.retry_count += 1
            
            # Schedule retry if under max retries
            if task.retry_count < task.max_retries:
                retry_time = datetime.now() + timedelta(minutes=5)
                schedule.every().day.at(retry_time.strftime("%H:%M")).do(
                    self._execute_task, task_id
                ).tag(f"{task_id}_retry")
                logger.info(f"Scheduled retry for task {task.name} at {retry_time}")
        
        finally:
            # Clean up Nova session
            if task_id in self.nova_sessions:
                try:
                    # Keep session open for manual verification if needed
                    # self.nova_sessions[task_id].stop()
                    pass
                except:
                    pass
            
            self.save_config()
    
    def start_scheduler(self):
        """Start the task scheduler"""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return
            
        self.is_running = True
        
        # Schedule all enabled tasks
        for task in self.tasks.values():
            if task.enabled:
                self._schedule_task(task)
        
        # Start scheduler thread
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logger.info("Portal Automation Agent started")
    
    def stop_scheduler(self):
        """Stop the task scheduler"""
        self.is_running = False
        
        # Stop all Nova sessions
        for session in self.nova_sessions.values():
            try:
                session.stop()
            except:
                pass
        self.nova_sessions.clear()
        
        # Clear all scheduled jobs
        schedule.clear()
        
        logger.info("Portal Automation Agent stopped")
    
    def _run_scheduler(self):
        """Main scheduler loop"""
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                time.sleep(5)
    
    def get_status_report(self) -> Dict[str, Any]:
        """Generate a comprehensive status report"""
        now = datetime.now()
        
        report = {
            "timestamp": now.isoformat(),
            "agent_status": "running" if self.is_running else "stopped",
            "total_tasks": len(self.tasks),
            "active_sessions": len(self.nova_sessions),
            "tasks": {}
        }
        
        # Task statistics
        status_counts = {}
        for status in TaskStatus:
            status_counts[status.value] = sum(1 for task in self.tasks.values() if task.status == status)
        
        report["task_statistics"] = status_counts
        
        # Individual task details
        for task_id, task in self.tasks.items():
            task_info = {
                "name": task.name,
                "status": task.status.value,
                "scheduled_time": task.scheduled_time,
                "last_run": task.last_run,
                "retry_count": task.retry_count,
                "enabled": task.enabled
            }
            
            if task.status == TaskStatus.FAILED:
                task_info["error"] = task.error_message
            elif task.status == TaskStatus.COMPLETED:
                task_info["result"] = task.result[:200] + "..." if len(task.result or "") > 200 else task.result
                
            report["tasks"][task_id] = task_info
        
        # Next scheduled runs
        upcoming = []
        for task in self.tasks.values():
            if task.enabled and task.status != TaskStatus.RUNNING:
                try:
                    next_run = datetime.strptime(task.scheduled_time, "%H:%M").replace(
                        year=now.year, month=now.month, day=now.day
                    )
                    if next_run <= now:
                        next_run += timedelta(days=1)
                    
                    upcoming.append({
                        "task_name": task.name,
                        "next_run": next_run.isoformat(),
                        "time_until": str(next_run - now)
                    })
                except:
                    pass
        
        report["upcoming_tasks"] = sorted(upcoming, key=lambda x: x["next_run"])[:5]
        
        return report
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """List all tasks with their current status"""
        return [
            {
                "id": task.id,
                "name": task.name,
                "url": task.url,
                "scheduled_time": task.scheduled_time,
                "status": task.status.value,
                "enabled": task.enabled,
                "last_run": task.last_run,
                "retry_count": task.retry_count
            }
            for task in self.tasks.values()
        ]

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Portal Automation Agent")
    parser.add_argument("--config", default="agent_config.json", help="Configuration file path")
    parser.add_argument("--start", action="store_true", help="Start the scheduler")
    parser.add_argument("--status", action="store_true", help="Show status report")
    parser.add_argument("--list", action="store_true", help="List all tasks")
    
    args = parser.parse_args()
    
    agent = PortalAutomationAgent(args.config)
    
    if args.status:
        report = agent.get_status_report()
        print(json.dumps(report, indent=2))
    elif args.list:
        tasks = agent.list_tasks()
        print(json.dumps(tasks, indent=2))
    elif args.start:
        agent.start_scheduler()
        try:
            while True:
                time.sleep(60)
                logger.info("Agent running... Press Ctrl+C to stop")
        except KeyboardInterrupt:
            agent.stop_scheduler()
            logger.info("Agent stopped")
    else:
        print("Use --start to run the agent, --status for status, --list for tasks")

if __name__ == "__main__":
    main()
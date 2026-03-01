#!/usr/bin/env python3
"""
Portal Automation Agent Web Dashboard
Web-based interface for managing scheduled portal automation tasks.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
import json
from portal_automation_agent import PortalAutomationAgent, TaskStatus

app = Flask(__name__)
app.secret_key = 'portal_agent_dashboard_secret_key'

# Global agent instance
agent = PortalAutomationAgent()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    status_report = agent.get_status_report()
    return render_template('dashboard.html', report=status_report)

@app.route('/tasks')
def tasks():
    """Tasks management page"""
    tasks = agent.list_tasks()
    return render_template('tasks.html', tasks=tasks)

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    """Add new task page"""
    if request.method == 'POST':
        try:
            name = request.form['name'].strip()
            url = request.form['url'].strip()
            instructions = request.form['instructions'].strip()
            scheduled_time = request.form['scheduled_time'].strip()
            
            if not all([name, url, instructions, scheduled_time]):
                flash('All fields are required', 'error')
                return render_template('add_task.html')
            
            # Validate time format
            datetime.strptime(scheduled_time, "%H:%M")
            
            task_id = agent.add_task(name, url, instructions, scheduled_time)
            flash(f'Task "{name}" created successfully!', 'success')
            return redirect(url_for('tasks'))
            
        except ValueError:
            flash('Invalid time format. Use HH:MM (24-hour format)', 'error')
        except Exception as e:
            flash(f'Error creating task: {str(e)}', 'error')
    
    return render_template('add_task.html')

@app.route('/task/<task_id>')
def task_details(task_id):
    """Task details page"""
    if task_id not in agent.tasks:
        flash('Task not found', 'error')
        return redirect(url_for('tasks'))
    
    task = agent.tasks[task_id]
    return render_template('task_details.html', task=task)

@app.route('/api/tasks', methods=['GET'])
def api_tasks():
    """API endpoint for tasks list"""
    return jsonify(agent.list_tasks())

@app.route('/api/status', methods=['GET'])
def api_status():
    """API endpoint for status report"""
    return jsonify(agent.get_status_report())

@app.route('/api/task/<task_id>/toggle', methods=['POST'])
def api_toggle_task(task_id):
    """API endpoint to enable/disable task"""
    if task_id not in agent.tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    current_status = agent.tasks[task_id].enabled
    new_status = not current_status
    
    if agent.update_task(task_id, enabled=new_status):
        return jsonify({
            'success': True,
            'enabled': new_status,
            'message': f'Task {"enabled" if new_status else "disabled"}'
        })
    else:
        return jsonify({'error': 'Failed to update task'}), 500

@app.route('/api/task/<task_id>/delete', methods=['DELETE'])
def api_delete_task(task_id):
    """API endpoint to delete task"""
    if agent.remove_task(task_id):
        return jsonify({'success': True, 'message': 'Task deleted'})
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/api/agent/start', methods=['POST'])
def api_start_agent():
    """API endpoint to start the agent"""
    try:
        agent.start_scheduler()
        return jsonify({'success': True, 'message': 'Agent started'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/agent/stop', methods=['POST'])
def api_stop_agent():
    """API endpoint to stop the agent"""
    try:
        agent.stop_scheduler()
        return jsonify({'success': True, 'message': 'Agent stopped'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🌐 Starting Portal Automation Agent Dashboard")
    print("📊 Access the dashboard at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
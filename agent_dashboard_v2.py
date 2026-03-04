#!/usr/bin/env python3
"""
Portal Automation Agent V2.0 - Enhanced Dashboard
Web dashboard with authentication, credential management, and modern UI
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from datetime import datetime
import json
import os
import time
from pathlib import Path

from auth_manager import AuthManager, User
from credential_manager import CredentialManager
from database import Database, Task as DBTask, Credential as DBCredential, Execution, TaskStatus

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(32).hex())
# Ensure error handlers work even in debug mode (otherwise Flask
# propagates exceptions to Werkzeug's HTML debugger, breaking JSON APIs)
app.config['PROPAGATE_EXCEPTIONS'] = False
app.config['TRAP_HTTP_EXCEPTIONS'] = False

# Initialize managers
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

auth_manager = AuthManager()
credential_manager = CredentialManager()
db = Database()

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    return auth_manager.get_user(user_id)

# ============================================================================
# Authentication Routes
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        user = auth_manager.authenticate(username, password)
        
        if user:
            login_user(user, remember=remember)
            
            # Update last login
            session['last_login'] = datetime.now().isoformat()
            
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login_v2.html')

@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('login'))

# ============================================================================
# Dashboard Routes
# ============================================================================

@app.route('/')
@login_required
def dashboard():
    """Main dashboard"""
    # Get tasks from V1 config (temporary until migration complete)
    config_file = Path('agent_config.json')
    tasks = []
    
    if config_file.exists():
        with open(config_file, 'r') as f:
            data = json.load(f)
            tasks = data.get('tasks', [])
    
    # Calculate statistics
    stats = {
        'total': len(tasks),
        'pending': sum(1 for t in tasks if t.get('status') == 'pending'),
        'running': sum(1 for t in tasks if t.get('status') == 'running'),
        'completed': sum(1 for t in tasks if t.get('status') == 'completed'),
        'failed': sum(1 for t in tasks if t.get('status') == 'failed'),
    }
    
    # Get upcoming tasks
    upcoming = [t for t in tasks if t.get('enabled', True) and t.get('status') != 'running']
    upcoming = sorted(upcoming, key=lambda x: x.get('scheduled_time', ''))[:5]
    
    return render_template('dashboard_v2.html', 
                         stats=stats, 
                         tasks=tasks[:10],  # Recent 10
                         upcoming=upcoming,
                         user=current_user)

@app.route('/tasks')
@login_required
def tasks():
    """Tasks list page"""
    config_file = Path('agent_config.json')
    tasks = []
    
    if config_file.exists():
        with open(config_file, 'r') as f:
            data = json.load(f)
            tasks = data.get('tasks', [])
    
    return render_template('tasks_v2.html', tasks=tasks, user=current_user)

@app.route('/task/<task_id>')
@login_required
def task_details(task_id):
    """Task details page"""
    config_file = Path('agent_config.json')
    
    if config_file.exists():
        with open(config_file, 'r') as f:
            data = json.load(f)
            tasks = data.get('tasks', [])
            
            task = next((t for t in tasks if t['id'] == task_id), None)
            
            if task:
                return render_template('task_details_v2.html', task=task, user=current_user)
    
    flash('Task not found', 'error')
    return redirect(url_for('tasks'))

# ============================================================================
# Task Management Routes
# ============================================================================

@app.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    """Add new task"""
    if request.method == 'POST':
        import time
        
        name = request.form.get('name')
        url = request.form.get('url')
        instructions = request.form.get('instructions')
        scheduled_time = request.form.get('scheduled_time')
        enabled = request.form.get('enabled') == 'on'
        
        # Load existing config
        config_file = Path('agent_config.json')
        if config_file.exists():
            with open(config_file, 'r') as f:
                data = json.load(f)
        else:
            data = {'tasks': []}
        
        # Create new task
        task_id = f"task_{int(time.time())}_{len(data['tasks'])}"
        new_task = {
            'id': task_id,
            'name': name,
            'url': url,
            'instructions': instructions,
            'scheduled_time': scheduled_time,
            'enabled': enabled,
            'status': 'pending',
            'last_run': None,
            'retry_count': 0,
            'max_retries': 3
        }
        
        data['tasks'].append(new_task)
        
        # Save config
        with open(config_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        flash(f'Task "{name}" created successfully', 'success')
        return redirect(url_for('tasks'))
    
    # Get credentials for dropdown
    creds_dict = credential_manager.list_credentials()
    creds = [{'id': cid, 'username': cdata.get('username', '')} 
             for cid, cdata in creds_dict.items()]
    
    return render_template('task_form_v2.html', task=None, credentials=creds, user=current_user)

@app.route('/tasks/<task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """Edit existing task"""
    config_file = Path('agent_config.json')
    
    if not config_file.exists():
        flash('No tasks found', 'error')
        return redirect(url_for('tasks'))
    
    with open(config_file, 'r') as f:
        data = json.load(f)
    
    task = next((t for t in data['tasks'] if t['id'] == task_id), None)
    
    if not task:
        flash('Task not found', 'error')
        return redirect(url_for('tasks'))
    
    if request.method == 'POST':
        task['name'] = request.form.get('name')
        task['url'] = request.form.get('url')
        task['instructions'] = request.form.get('instructions')
        task['scheduled_time'] = request.form.get('scheduled_time')
        task['enabled'] = request.form.get('enabled') == 'on'
        
        # Save config
        with open(config_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        flash(f'Task "{task["name"]}" updated successfully', 'success')
        return redirect(url_for('task_details', task_id=task_id))
    
    # Get credentials for dropdown
    creds_dict = credential_manager.list_credentials()
    creds = [{'id': cid, 'username': cdata.get('username', '')} 
             for cid, cdata in creds_dict.items()]
    
    return render_template('task_form_v2.html', task=task, credentials=creds, user=current_user)

@app.route('/tasks/<task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    """Delete task"""
    config_file = Path('agent_config.json')
    
    if not config_file.exists():
        flash('No tasks found', 'error')
        return redirect(url_for('tasks'))
    
    with open(config_file, 'r') as f:
        data = json.load(f)
    
    data['tasks'] = [t for t in data['tasks'] if t['id'] != task_id]
    
    with open(config_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    flash('Task deleted successfully', 'success')
    return redirect(url_for('tasks'))

# ============================================================================
# Credential Management Routes
# ============================================================================

@app.route('/credentials')
@login_required
def credentials():
    """Credentials vault page"""
    creds_dict = credential_manager.list_credentials()
    # Convert dict to list of credentials with id included
    creds = []
    for cred_id, cred_data in creds_dict.items():
        cred_item = {
            'credential_id': cred_id,
            'username': cred_data.get('username', ''),
            'description': cred_data.get('description', ''),
            'url': cred_data.get('url', ''),
            'created_at': cred_data.get('created_at', '')
        }
        creds.append(cred_item)
    return render_template('credentials.html', credentials=creds, user=current_user)

@app.route('/credentials/add', methods=['GET', 'POST'])
@login_required
def add_credential():
    """Add new credential"""
    if request.method == 'POST':
        credential_id = request.form.get('credential_id')
        description = request.form.get('description')
        url = request.form.get('url')
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            credential_manager.store_credential(
                credential_id, username, password, description, url
            )
            flash(f'Credential "{credential_id}" added successfully', 'success')
            return redirect(url_for('credentials'))
        except Exception as e:
            flash(f'Error adding credential: {str(e)}', 'error')
    
    return render_template('credential_form.html', user=current_user)

@app.route('/credentials/<credential_id>/test', methods=['POST'])
@login_required
def test_credential(credential_id):
    """Test if credential can be retrieved"""
    try:
        cred = credential_manager.get_credential(credential_id)
        
        if cred:
            # Successfully retrieved
            return jsonify({
                'success': True,
                'message': f'Credential "{credential_id}" retrieved successfully',
                'username': cred['username'],
                'has_password': bool(cred['password'])
            })
        else:
            return jsonify({
                'success': False,
                'message': f'Credential "{credential_id}" not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error testing credential: {str(e)}'
        }), 500

@app.route('/credentials/<credential_id>/test-login', methods=['POST'])
@login_required
def test_credential_login(credential_id):
    """Provide instructions for testing credential login"""
    try:
        # Get credential to verify it exists
        cred = credential_manager.get_credential(credential_id)
        if not cred:
            return jsonify({
                'success': False,
                'message': f'Credential "{credential_id}" not found'
            }), 404
        
        # Return instructions for manual test
        return jsonify({
            'success': True,
            'message': 'To test this credential with actual login, run this command in your terminal:',
            'command': f'python test_credential_login.py {credential_id}',
            'details': f'This will open a browser and attempt to login as {cred["username"]}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/credentials/<credential_id>/delete', methods=['POST'])
@login_required
def delete_credential(credential_id):
    """Delete credential"""
    if credential_manager.delete_credential(credential_id):
        flash(f'Credential "{credential_id}" deleted successfully', 'success')
    else:
        flash('Credential not found', 'error')
    
    return redirect(url_for('credentials'))

# ============================================================================
# User Management Routes (Admin Only)
# ============================================================================

@app.route('/users')
@login_required
def users():
    """User management page (admin only)"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    users_list = auth_manager.list_users()
    return render_template('users.html', users=users_list, user=current_user)

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('profile.html', user=current_user)

@app.route('/profile/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if new_password != confirm_password:
        flash('New passwords do not match', 'error')
        return redirect(url_for('profile'))
    
    success, message = auth_manager.change_password(
        current_user.id, old_password, new_password
    )
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('profile'))

# ============================================================================
# API Routes
# ============================================================================

@app.route('/api/task/<task_id>/run', methods=['POST'])
@login_required
def run_task(task_id):
    """Execute a task immediately in a background thread"""
    try:
        return _run_task_inner(task_id)
    except Exception as e:
        # Absolute safety net - always return JSON, never crash
        return jsonify({
            'success': False,
            'message': f'Unexpected server error: {type(e).__name__}: {e}'
        }), 500


def _run_task_inner(task_id):
    """Inner logic for run_task, separated so the outer handler can catch everything"""
    # Test import before doing anything else
    try:
        from portal_automation_agent import PortalAutomationAgent
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Cannot import automation agent: {type(e).__name__}: {e}. '
                       f'Run: pip install nova-act schedule'
        }), 500

    config_file = Path('agent_config.json')
    if not config_file.exists():
        return jsonify({'success': False, 'message': 'No config file found'}), 404

    with open(config_file, 'r') as f:
        data = json.load(f)

    task = next((t for t in data['tasks'] if t['id'] == task_id), None)
    if not task:
        return jsonify({'success': False, 'message': f'Task {task_id} not found'}), 404

    # Detect stale "running" tasks (stuck for more than 10 minutes)
    if task.get('status') == 'running':
        last_run = task.get('last_run')
        stale = False
        if last_run:
            try:
                started_at = datetime.fromisoformat(last_run.replace('Z', '+00:00'))
                if (datetime.now() - started_at).total_seconds() > 600:
                    stale = True
            except Exception:
                stale = True
        else:
            stale = True

        if stale:
            # Reset the stuck task so it can be re-run
            task['status'] = 'pending'
            task['error_message'] = 'Previous run was stuck and has been reset'
            with open(config_file, 'w') as f:
                json.dump(data, f, indent=2)
        else:
            return jsonify({'success': False, 'message': 'Task is already running'}), 409

    # Check API key is set before starting
    if not os.environ.get('NOVA_ACT_API_KEY'):
        return jsonify({
            'success': False,
            'message': 'NOVA_ACT_API_KEY environment variable is not set. '
                       'Set it before running tasks: $env:NOVA_ACT_API_KEY="your-key"'
        }), 400

    import threading

    def run_in_background(tid):
        """Run task in background thread with crash-safe status updates"""
        try:
            agent = PortalAutomationAgent()
            agent._execute_task(tid)
        except Exception as e:
            # If the agent constructor or _execute_task crashes before
            # it can update the config, we must reset the status here
            import logging
            logging.getLogger(__name__).error(f"Background task {tid} failed: {e}")
            try:
                with open('agent_config.json', 'r') as f:
                    cfg = json.load(f)
                for t in cfg.get('tasks', []):
                    if t['id'] == tid and t.get('status') == 'running':
                        t['status'] = 'failed'
                        t['error_message'] = f'Task crashed: {e}'
                        break
                with open('agent_config.json', 'w') as f:
                    json.dump(cfg, f, indent=2)
            except Exception:
                pass

    thread = threading.Thread(target=run_in_background, args=(task_id,), daemon=True)
    thread.start()

    return jsonify({
        'success': True,
        'message': f'Task "{task.get("name", task_id)}" started. Check status for progress.'
    })

@app.route('/api/task/<task_id>/status')
@login_required
def task_status(task_id):
    """Get current task status (for polling)"""
    config_file = Path('agent_config.json')
    if not config_file.exists():
        return jsonify({'success': False, 'message': 'No config found'}), 404

    with open(config_file, 'r') as f:
        data = json.load(f)

    task = next((t for t in data['tasks'] if t['id'] == task_id), None)
    if not task:
        return jsonify({'success': False, 'message': 'Task not found'}), 404

    return jsonify({
        'success': True,
        'status': task.get('status', 'unknown'),
        'last_run': task.get('last_run'),
        'result': task.get('result'),
        'error_message': task.get('error_message'),
        'retry_count': task.get('retry_count', 0)
    })

@app.route('/api/task/<task_id>/reset', methods=['POST'])
@login_required
def reset_task(task_id):
    """Reset a stuck task back to pending"""
    config_file = Path('agent_config.json')
    if not config_file.exists():
        return jsonify({'success': False, 'message': 'No config found'}), 404

    with open(config_file, 'r') as f:
        data = json.load(f)

    task = next((t for t in data['tasks'] if t['id'] == task_id), None)
    if not task:
        return jsonify({'success': False, 'message': 'Task not found'}), 404

    task['status'] = 'pending'
    task['error_message'] = None

    with open(config_file, 'w') as f:
        json.dump(data, f, indent=2)

    return jsonify({'success': True, 'message': 'Task has been reset to pending'})

@app.route('/api/task/<task_id>/logs')
@login_required
def task_logs(task_id):
    """Return the last 50 lines of portal_agent.log related to this task"""
    log_file = Path('portal_agent.log')
    lines = []
    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                all_lines = f.readlines()
            # Return the last 100 lines (they include task context)
            lines = [l.rstrip() for l in all_lines[-100:]]
        except Exception:
            pass
    return jsonify({'success': True, 'lines': lines})

@app.route('/api/status')
@login_required
def api_status():
    """System status API"""
    config_file = Path('agent_config.json')
    tasks = []
    
    if config_file.exists():
        with open(config_file, 'r') as f:
            data = json.load(f)
            tasks = data.get('tasks', [])
    
    return jsonify({
        'status': 'running',
        'total_tasks': len(tasks),
        'user': current_user.username,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/tasks')
@login_required
def api_tasks():
    """Tasks API"""
    config_file = Path('agent_config.json')
    
    if config_file.exists():
        with open(config_file, 'r') as f:
            data = json.load(f)
            return jsonify(data.get('tasks', []))
    
    return jsonify([])

@app.route('/api/credentials')
@login_required
def api_credentials():
    """Credentials API (metadata only, no passwords)"""
    creds = credential_manager.list_credentials()
    return jsonify(creds)

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """404 error handler - return JSON for API routes"""
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'message': 'Not found'}), 404
    return render_template('error.html',
                         error_code=404,
                         error_message='Page not found',
                         user=current_user if current_user.is_authenticated else None), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler - return JSON for API routes"""
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'message': f'Server error: {error}'}), 500
    return render_template('error.html',
                         error_code=500,
                         error_message='Internal server error',
                         user=current_user if current_user.is_authenticated else None), 500

@app.errorhandler(Exception)
def handle_exception(error):
    """Catch-all error handler - ensures API routes always return JSON"""
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'message': f'Server error: {error}'}), 500
    return render_template('error.html',
                         error_code=500,
                         error_message=str(error),
                         user=current_user if current_user.is_authenticated else None), 500

# ============================================================================
# Template Filters
# ============================================================================

@app.template_filter('datetime')
def format_datetime(value):
    """Format datetime for display"""
    if not value:
        return 'Never'
    
    try:
        if isinstance(value, str):
            dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        else:
            dt = value
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return value

@app.template_filter('timeago')
def timeago(value):
    """Human-readable time ago"""
    if not value:
        return 'Never'
    
    try:
        if isinstance(value, str):
            dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        else:
            dt = value
        
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 365:
            return f'{diff.days // 365} year(s) ago'
        elif diff.days > 30:
            return f'{diff.days // 30} month(s) ago'
        elif diff.days > 0:
            return f'{diff.days} day(s) ago'
        elif diff.seconds > 3600:
            return f'{diff.seconds // 3600} hour(s) ago'
        elif diff.seconds > 60:
            return f'{diff.seconds // 60} minute(s) ago'
        else:
            return 'Just now'
    except:
        return value

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    print("Starting Portal Automation Agent V2.0 Dashboard")
    print("=" * 60)
    print("Access the dashboard at: http://localhost:5000")
    print("Default login: admin / admin123")
    print("WARNING: Please change the default password after first login!")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True, use_reloader=False)
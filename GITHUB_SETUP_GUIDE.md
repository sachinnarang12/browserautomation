# GitHub Setup Guide

Complete step-by-step instructions for pushing this project to GitHub and cloning it in Claude Code (VS Code).

## Part 1: Push Code to GitHub

### Step 1: Create GitHub Repository

1. Go to https://github.com
2. Click the **+** icon in the top right → **New repository**
3. Fill in repository details:
   - **Repository name**: `portal-automation-agent` (or your preferred name)
   - **Description**: "Secure web-based automation agent with Nova Act integration"
   - **Visibility**: Choose **Private** (recommended for automation scripts)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **Create repository**
5. **Keep this page open** - you'll need the repository URL

### Step 2: Configure Git (First Time Only)

Open a terminal in your project folder and run:

```bash
# Set your name (replace with your name)
git config --global user.name "Your Name"

# Set your email (use your GitHub email)
git config --global user.email "your.email@example.com"
```

### Step 3: Initialize Git Repository

In your project folder (`C:\Users\naran\Kiro`), run:

```bash
# Initialize git repository
git init

# Add all files (respects .gitignore)
git add .

# Create first commit
git commit -m "Initial commit: Portal Automation Agent V2"
```

### Step 4: Connect to GitHub

Replace `<your-username>` and `<repo-name>` with your actual values:

```bash
# Add GitHub as remote origin
git remote add origin https://github.com/<your-username>/<repo-name>.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**If prompted for credentials:**
- Username: Your GitHub username
- Password: Use a **Personal Access Token** (not your GitHub password)

### Step 5: Create Personal Access Token (If Needed)

If you don't have a token:

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click **Generate new token** → **Generate new token (classic)**
3. Give it a name: "Portal Automation Agent"
4. Select scopes: Check **repo** (full control of private repositories)
5. Click **Generate token**
6. **COPY THE TOKEN** - you won't see it again!
7. Use this token as your password when pushing

### Step 6: Verify Upload

1. Refresh your GitHub repository page
2. You should see all your files uploaded
3. Check that sensitive files are NOT there:
   - ❌ `portal_agent.db`
   - ❌ `credentials_index.json`
   - ❌ `agent_config.json`
   - ❌ `.env`

---

## Part 2: Clone in Claude Code (VS Code)

### Step 1: Open Claude Code

1. Launch Claude Code (VS Code)
2. Close any open folders/workspaces

### Step 2: Clone Repository

**Method A: Using Command Palette**

1. Press `Ctrl+Shift+P` (Windows) or `Cmd+Shift+P` (Mac)
2. Type: `Git: Clone`
3. Press Enter
4. Paste your repository URL: `https://github.com/<your-username>/<repo-name>.git`
5. Choose a folder location (e.g., `C:\Projects\`)
6. Click **Select Repository Location**
7. When prompted, click **Open** to open the cloned repository

**Method B: Using Terminal**

1. In Claude Code, open Terminal: `Ctrl+` ` (backtick)
2. Navigate to where you want to clone:
   ```bash
   cd C:\Projects
   ```
3. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   ```
4. Open the folder: File → Open Folder → Select the cloned folder

### Step 3: Install Dependencies

In Claude Code terminal:

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements_v2.txt
```

### Step 4: Setup Application

```bash
# Initialize database
python setup_v2.py

# Add your credentials
python credential_manager.py add
```

### Step 5: Configure for Your Environment

1. Update credentials in Credential Manager
2. Create tasks in the dashboard
3. Update any hardcoded values if needed

### Step 6: Run Application

Open two terminals in Claude Code:

**Terminal 1 - Dashboard:**
```bash
python agent_dashboard_v2.py
```

**Terminal 2 - Scheduler:**
```bash
python standalone_scheduler.py
```

Access dashboard at: http://localhost:5000

---

## Part 3: Keeping Code in Sync

### Push Changes to GitHub

After making changes:

```bash
# Check what changed
git status

# Add all changes
git add .

# Commit with a message
git commit -m "Description of changes"

# Push to GitHub
git push
```

### Pull Changes from GitHub

To get latest changes on another machine:

```bash
# Pull latest changes
git pull origin main
```

---

## Part 4: Working Across Multiple Machines

### On Machine A (Original):

```bash
# Make changes
git add .
git commit -m "Updated task scheduler"
git push
```

### On Machine B (Clone):

```bash
# Get latest changes
git pull

# Install any new dependencies
pip install -r requirements_v2.txt

# Run application
python agent_dashboard_v2.py
```

---

## Important Notes

### Files NOT in Git (Intentionally)

These files are excluded by `.gitignore` and must be recreated on each machine:

- `portal_agent.db` - Run `python setup_v2.py`
- `credentials_index.json` - Add credentials via dashboard or CLI
- `agent_config.json` - Create tasks via dashboard
- `users.json` - Created automatically on first run

### Security Best Practices

1. ✅ **Never commit** sensitive files (database, credentials, logs)
2. ✅ Use **Private repository** for automation scripts
3. ✅ Change default admin password immediately
4. ✅ Use **Personal Access Tokens** instead of passwords
5. ✅ Keep `.gitignore` updated

### Troubleshooting

**"Permission denied" when pushing:**
- Use Personal Access Token instead of password
- Check token has `repo` scope

**"Repository not found":**
- Verify repository URL is correct
- Check you have access to the repository
- Ensure repository is not deleted

**Files showing as modified but unchanged:**
- Line ending differences (Windows vs Unix)
- Run: `git config core.autocrlf true`

---

## Quick Reference Commands

```bash
# Check status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push

# Pull from GitHub
git pull

# View commit history
git log --oneline

# Discard local changes
git checkout -- <file>

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main
```

---

## Need Help?

- Git documentation: https://git-scm.com/doc
- GitHub guides: https://guides.github.com
- VS Code Git integration: https://code.visualstudio.com/docs/editor/versioncontrol

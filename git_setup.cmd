@echo off
echo ========================================
echo Git Setup for Portal Automation Agent
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo Git is installed!
echo.

REM Configure git user
set /p USERNAME="Enter your name (for Git commits): "
set /p EMAIL="Enter your email (use your GitHub email): "

git config --global user.name "%USERNAME%"
git config --global user.email "%EMAIL%"

echo.
echo Git configured successfully!
echo Name: %USERNAME%
echo Email: %EMAIL%
echo.

REM Add all files
echo Adding files to git...
git add .

REM Show status
echo.
echo Files to be committed:
git status --short

echo.
echo ========================================
echo Next Steps:
echo ========================================
echo 1. Create a repository on GitHub.com
echo 2. Run these commands (replace with your repo URL):
echo.
echo    git commit -m "Initial commit: Portal Automation Agent V2"
echo    git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo See GITHUB_SETUP_GUIDE.md for detailed instructions
echo ========================================
pause

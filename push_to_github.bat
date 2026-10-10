@echo off
setlocal

echo ===================================================
echo   Pushing TaskFlow Project to GitHub
echo   Repository: https://github.com/penchalsangam/sample_train.git
echo ===================================================
echo.

cd /d "%~dp0"

:: 1. Initialize git repository if not already initialized
if not exist ".git" (
    echo [*] Initializing git repository...
    git init
) else (
    echo [*] Git repository already initialized.
)

:: 2. Set default branch to main
git branch -M main

:: 3. Configure or update remote origin
git remote get-url origin >nul 2>&1
if %errorlevel% equ 0 (
    echo [*] Updating remote origin URL...
    git remote set-url origin https://github.com/penchalsangam/sample_train.git
) else (
    echo [*] Adding remote origin...
    git remote add origin https://github.com/penchalsangam/sample_train.git
)

:: 4. Stage all files
echo [*] Staging files...
git add .

:: 5. Commit changes
echo [*] Committing files...
git commit -m "feat: complete FastAPI TaskFlow mini project with SQLite, REST CRUD, and UI dashboard"

:: 6. Push to GitHub
echo [*] Pushing to GitHub (main branch)...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ===================================================
    echo [SUCCESS] Code pushed successfully to GitHub!
    echo URL: https://github.com/penchalsangam/sample_train
    echo ===================================================
) else (
    echo.
    echo ===================================================
    echo [NOTE] If the remote repository already contains files
    echo        (e.g., a README or license), you can run:
    echo        git pull origin main --rebase
    echo        git push -u origin main
    echo ===================================================
)

echo.
pause

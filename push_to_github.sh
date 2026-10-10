#!/usr/bin/env bash
set -e

echo "==================================================="
echo "  Pushing TaskFlow Project to GitHub"
echo "  Repository: https://github.com/penchalsangam/sample_train.git"
echo "==================================================="

# Navigate to script directory
cd "$(dirname "$0")"

# 1. Initialize git repository if needed
if [ ! -d ".git" ]; then
    echo "[*] Initializing git repository..."
    git init
else
    echo "[*] Git repository already exists."
fi

# 2. Set default branch to main
git branch -M main

# 3. Configure or update remote
if git remote | grep -q "^origin$"; then
    echo "[*] Updating remote origin URL..."
    git remote set-url origin https://github.com/penchalsangam/sample_train.git
else
    echo "[*] Adding remote origin..."
    git remote add origin https://github.com/penchalsangam/sample_train.git
fi

# 4. Stage all files
echo "[*] Staging files..."
git add .

# 5. Commit changes
echo "[*] Committing files..."
git commit -m "feat: complete FastAPI TaskFlow mini project with SQLite, REST CRUD, and UI dashboard" || echo "No new changes to commit."

# 6. Push to GitHub
echo "[*] Pushing to GitHub (main branch)..."
git push -u origin main
echo "==================================================="
echo "[SUCCESS] Code pushed successfully!"
echo "==================================================="

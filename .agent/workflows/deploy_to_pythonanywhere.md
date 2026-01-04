---
description: Deploy Flask App to PythonAnywhere
---
# Deployment Guide: PythonAnywhere

Follow these steps to deploy "EntreHub" to the live web.

## 1. Upload to GitHub
First, we need to get your code into a repository.
1. Create a new repository on GitHub (e.g., `entrehub-project`).
2. Run these commands locally in your terminal:
   ```powershell
   git init
   git add .
   git commit -m "Initial Deployment"
   git branch -M main
   # Replace YOUR_REPO_URL below with your actual GitHub URL
   git remote add origin https://github.com/YOUR_USERNAME/entrehub-project.git
   git push -u origin main
   ```

## 2. Setup PythonAnywhere
1. Create a free account at [pythonanywhere.com](https://www.pythonanywhere.com/).
2. Go to the **Consoles** tab -> **Bash** console.
3. Clone your repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/entrehub-project.git
   ```

## 3. Create Virtual Environment
In the PythonAnywhere Bash console:
```bash
cd entrehub-project
mkvirtualenv --python=/usr/bin/python3.10 my-virtualenv
pip install -r requirements.txt
```

## 4. Configure Web App
1. Go to the **Web** tab.
2. Click **Add a new web app** -> **Next** -> **Manual Configuration** -> **Python 3.10**.
3. **Virtualenv section:** Enter the path `~/.virtualenvs/my-virtualenv`.
4. **Code section:**
   - Source code: `/home/YOUR_USERNAME/entrehub-project`
   - Working directory: `/home/YOUR_USERNAME/entrehub-project`
5. **WSGI Configuration File:**
   - Click the link to edit the WSGI file.
   - Delete everything and paste this:
     ```python
     import sys
     import os

     # Add your project directory to the sys.path
     path = '/home/YOUR_USERNAME/entrehub-project'
     if path not in sys.path:
         sys.path.append(path)

     from app import app as application
     ```
   - **Important:** Replace `YOUR_USERNAME` with your actual PythonAnywhere username.

## 5. Live!
Click the green **Reload** button at the top of the Web tab. Your site will be live at `your-username.pythonanywhere.com`.

# Git Repository Setup Commands

## Step 1: Initialize Git Repository
```bash
git init
```

## Step 2: Add all important files
```bash
git add main.py
git add requirements.txt
git add .env.template
git add .gitignore
git add README.md
git add data/
git add test_retell.py
git add test_sheets.py
git add test_complete_system.py
git add create_retell_agent.py
git add create_retell_agent_simple.py
git add auto_ngrok_setup.py
git add setup_ngrok.py
git add try_api_endpoints.py
git add RETELL_SETUP.md
git add SHEETS_SETUP.md
git add DEPLOYMENT.md
git add NGROK_INSTRUCTIONS.md
```

## Step 3: Create initial commit
```bash
git commit -m "Initial commit: Complete Formi Voice AI system with Retell AI integration

✅ FastAPI backend with hotel information APIs
✅ Retell AI integration with function calling
✅ Google Sheets logging for conversation data
✅ Token management under 800 tokens
✅ Comprehensive error handling
✅ Production-ready deployment configuration
✅ Complete test suite and documentation

Features:
- Room information and availability checking
- Dynamic pricing based on dates  
- Hotel policies and cancellation information
- Conversation logging with call analysis
- WebSocket support for real-time communication
- Automated setup scripts and deployment guides"
```

## Step 4: Add remote repository
```bash
git remote add origin https://github.com/YOUR_USERNAME/formi-voice-ai-assignment.git
```

## Step 5: Push to GitHub
```bash
git branch -M main
git push -u origin main
```

---

## Quick Check: Files that will be committed
Run this to see what files will be added:
```bash
git status
```

Make sure these files are NOT in the staging area:
- .env (your actual secrets)
- service_account.json (credentials)
- ngrok.exe (large binary)
- __pycache__/ (Python cache)

## Alternative: Add everything except secrets
```bash
git add .
git status
# Check the list and make sure no secrets are included
```

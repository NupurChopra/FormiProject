## Simple Ngrok Setup Instructions

### Step 1: Get ngrok auth token
1. Go to: https://dashboard.ngrok.com/get-started/your-authtoken
2. Sign up for FREE ngrok account  
3. Copy your authtoken (looks like: 2abcd...)

### Step 2: Configure ngrok (run these commands one by one)

# First, configure with your authtoken:
.\ngrok.exe config add-authtoken YOUR_ACTUAL_AUTHTOKEN_HERE

# Then start the tunnel:
.\ngrok.exe http 8000

### Step 3: Copy the HTTPS URL
After running the second command, you'll see:
```
Forwarding    https://abc123.ngrok.io -> http://localhost:8000
```

Copy the HTTPS URL (e.g., https://abc123.ngrok.io)

### Step 4: Update Retell AI Dashboard
1. Go to: https://app.retellai.com/dashboard
2. Find your agent: "Formi Hotel Receptionist"  
3. Update webhook URL to: https://your-ngrok-url.ngrok.io/retell/function-call

### Step 5: Test your system!
Your voice AI is now ready to receive calls!

---

Your current setup:
- ✅ FastAPI server running on http://localhost:8000
- ✅ Agent ID: agent_0d23ea1f821ad8714cb1560e48
- ✅ Ngrok downloaded and ready
- ⏳ Need: authtoken setup and webhook update

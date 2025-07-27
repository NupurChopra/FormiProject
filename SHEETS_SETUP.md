# Google Sheets Setup Guide

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Google Sheets API
   - Google Drive API

## Step 2: Create Service Account

1. Go to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Give it a name like "formi-sheets-service"
4. Click "Create and Continue"
5. Skip role assignment for now
6. Click "Done"

## Step 3: Create Service Account Key

1. Click on the created service account
2. Go to "Keys" tab
3. Click "Add Key" > "Create New Key"
4. Select "JSON" format
5. Download the key file
6. Rename it to `service_account.json` and place it in your project root

## Step 4: Create Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it exactly: `formi_call`
4. Add headers in the first row:
   ```
   Call Time | Phone Number | Call Outcome | Check In Date | Check Out Date | Customer Name | Room Name | Number of Guests | Call Summary
   ```

## Step 5: Share Sheet with Service Account

1. Open your `service_account.json` file
2. Copy the "client_email" value
3. In Google Sheets, click "Share"
4. Paste the client_email
5. Give it "Editor" permissions
6. Uncheck "Notify people"
7. Click "Share"

## Step 6: Test Configuration

Run the test script:

```bash
python test_sheets.py
```

## Common Issues and Solutions

### Issue: "Spreadsheet not found"

- Make sure the sheet is named exactly `formi_call`
- Ensure the service account has access to the sheet

### Issue: "Permission denied"

- Check if the service account email has editor access to the sheet
- Verify the APIs are enabled in Google Cloud Console

### Issue: "File not found: service_account.json"

- Make sure the file is in the project root directory
- Check the filename is exactly `service_account.json`

### Issue: "Authentication failed"

- Make sure the service account key is valid
- Check if the Google Sheets API is enabled

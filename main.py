from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
import tiktoken
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = FastAPI()
def limit_tokens(text: str, max_tokens=800):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    return encoding.decode(tokens[:max_tokens])

def log_conversation_to_sheet(log_data: dict):
    try:
        print("🔍 Starting Google Sheets logging...")
        print("📋 Input data:", log_data)
        
        if not os.path.exists("service_account.json"):
            raise FileNotFoundError("service_account.json file not found")
        
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
        client = gspread.authorize(creds)

        try:
            spreadsheet = client.open("formi_call")
            sheet = spreadsheet.sheet1
        except gspread.SpreadsheetNotFound:
          
            try:
                spreadsheets = client.openall()
                for ss in spreadsheets:
                    print(f"   - {ss.title}")
            except:
                print("   - Could not list spreadsheets")
            raise Exception("Spreadsheet 'formi_call' not found")

       
        try:
            headers = sheet.row_values(1)
        except Exception as e:
            print("Could not read headers:", e)

        row = [
            log_data.get("Call_Time", "NA"),
            log_data.get("Phone_Number", "NA"), 
            log_data.get("Call_Outcome", "NA"),
            log_data.get("Check_In_Date", "NA"),
            log_data.get("Check_Out_Date", "NA"),
            log_data.get("Customer_Name", "NA"),
            log_data.get("Room_Name", "NA"),
            log_data.get("Number_of_Guests", "NA"),
            log_data.get("Call_Summary", "NA")
        ]

        sheet.append_row(row)
        print("Row successfully appended to sheet")
        
        return True

    except FileNotFoundError as e:
        raise
        
    except Exception as e:
        import traceback
        raise

@app.get("/")
def root():
    return {"message": "Hello from Formi backend!"}


@app.get("/info/{category}")
def get_info(category: str):
    try:
        with open(os.path.join("data", f"{category}.json")) as f:
            data = json.load(f)
            limited_text = limit_tokens(json.dumps(data))
            return {"success": True, "data": limited_text}
    except FileNotFoundError:
        return {"success": False, "message": "Category not found"}
    except Exception as e:
        return {"success": False, "message": str(e)}


class QueryInput(BaseModel):
    query: str

@app.post("/classify-query")
def classify_query(input: QueryInput):
    query = input.query.lower()

    if "cancel" in query or "refund" in query:
        return {"category": "policies"}
    elif "room" in query or "executive" in query:
        return {"category": "room_info"}
    elif "price" in query or "cost" in query or "availability" in query:
        return {"category": "pricing"}
    else:
        return {"category": "misc"}


class LogEntry(BaseModel):
    Call_Time: str
    Phone_Number: str
    Call_Outcome: str
    Check_In_Date: str
    Check_Out_Date: str
    Customer_Name: str
    Room_Name: str
    Number_of_Guests: str
    Call_Summary: str

@app.post("/log-conversation")
def log_conversation(entry: LogEntry):
    try:
        print("Received data:", entry.dict())
        result = log_conversation_to_sheet(entry.dict())
        return {"success": True, "message": "Data logged successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print("ERROR in log-conversation:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

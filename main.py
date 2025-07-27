from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
import tiktoken
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
import asyncio
import websockets
from datetime import datetime
from typing import Dict, Any

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
        return {"category": "discount"}  # Using discount.json for policies
    elif "room" in query or "executive" in query:
        return {"category": "rooms"}  # Using rooms.json
    elif "price" in query or "cost" in query or "availability" in query:
        return {"category": "pricing"}  # Using pricing.json  
    elif "staff" in query or "contact" in query:
        return {"category": "staff"}  # Using staff.json
    elif "hotel" in query or "location" in query or "amenities" in query:
        return {"category": "hotel"}  # Using hotel.json
    else:
        return {"category": "hotel"}  # Default to hotel info


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

@app.post("/search-info")
def search_info(input: QueryInput):
    category = classify_query(input).get("category")
    try:
        with open(f"data/{category}.json") as f:
            data = json.load(f)
            # Handle both chunked and non-chunked data
            if isinstance(data, dict) and "chunks" in data:
                chunks = data["chunks"]
            elif isinstance(data, list):
                chunks = [json.dumps(item) for item in data]
            else:
                chunks = [json.dumps(data)]
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Information category not found.")
    
    # Simple text matching
    matches = [c for c in chunks if input.query.lower() in c.lower()]
    
    if not matches:
        # If no exact matches, return the first few chunks as fallback
        matches = chunks[:2] if chunks else []

    if not matches:
        return {"success": False, "message": "No relevant information found."}

    # Limit token size for each match
    limited_matches = [limit_tokens(match) for match in matches[:2]]

    return {
        "success": True,
        "category": category,
        "matches": limited_matches
    }

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

# --------------------------
# 7. Retell AI Integration Models
# --------------------------
class RetellCallEvent(BaseModel):
    event: str
    call_id: str
    timestamp: str
    data: Dict[str, Any] = {}

class RetellFunctionCall(BaseModel):
    function_name: str
    arguments: Dict[str, Any]
    call_id: str

class RetellResponse(BaseModel):
    response: str
    end_call: bool = False

# --------------------------
# 8. Retell AI Function Calling
# --------------------------
@app.post("/retell/function-call")
async def handle_retell_function_call(function_call: RetellFunctionCall):
    """Handle function calls from Retell AI agent"""
    try:
        function_name = function_call.function_name
        args = function_call.arguments
        
        print(f"🤖 Retell function call: {function_name}")
        print(f"📋 Arguments: {args}")
        
        if function_name == "get_room_info":
            return await get_room_info_for_retell(args)
        elif function_name == "get_pricing_info":
            return await get_pricing_info_for_retell(args)
        elif function_name == "check_availability":
            return await check_availability_for_retell(args)
        elif function_name == "get_hotel_policies":
            return await get_hotel_policies_for_retell(args)
        elif function_name == "log_conversation_data":
            return await log_conversation_for_retell(args)
        else:
            return {
                "response": "I'm sorry, I don't have information about that. Please ask about room availability, pricing, or hotel policies.",
                "end_call": False
            }
    except Exception as e:
        print(f"❌ Error in function call: {str(e)}")
        return {
            "response": "I'm sorry, I'm having trouble accessing that information right now. Is there anything else I can help you with?",
            "end_call": False
        }

# --------------------------
# 9. Retell AI Helper Functions
# --------------------------
async def get_room_info_for_retell(args: Dict):
    """Get room information for Retell AI"""
    try:
        room_type = args.get("room_type", "").lower()
        
        with open("data/rooms.json") as f:
            rooms = json.load(f)
        
        # Find matching rooms
        matching_rooms = []
        for room in rooms:
            if room_type in room.get("room_name", "").lower() or not room_type:
                matching_rooms.append(room)
        
        if not matching_rooms:
            return {
                "response": "I couldn't find information about that specific room type. We have Amani Rooms, Amani Premium Rooms, and other options available. Would you like me to tell you about our available rooms?",
                "end_call": False
            }
        
        # Create response with room details
        room_info = matching_rooms[0]  # Take first match
        response = f"Here's information about the {room_info['room_name']}: "
        response += f"It has {room_info['number_of_bedrooms']} bedrooms and {room_info['number_of_bathrooms']} bathrooms, "
        response += f"accommodating up to {room_info['max_guests']} guests. "
        
        if room_info.get('pool_available') == 'Yes':
            response += "It includes pool access. "
        
        response += f"We have {room_info['total_number_of_rooms_available']} of these rooms available. "
        response += "Would you like to know about pricing or check availability for specific dates?"
        
        return {
            "response": limit_tokens(response, 700),
            "end_call": False
        }
    except Exception as e:
        return {
            "response": "I'm sorry, I'm having trouble accessing room information right now. Please try again or ask about something else.",
            "end_call": False
        }

async def get_pricing_info_for_retell(args: Dict):
    """Get pricing information for Retell AI"""
    try:
        room_name = args.get("room_name", "")
        date = args.get("date", "")
        
        with open("data/pricing.json") as f:
            pricing_data = json.load(f)
        
        # Search for pricing
        relevant_prices = []
        for item in pricing_data[:50]:  # Limit search
            price_info = item.get("Property Name\tdate\tprice", "")
            if room_name.lower() in price_info.lower() or date in price_info:
                relevant_prices.append(price_info)
        
        if not relevant_prices:
            return {
                "response": f"I don't have specific pricing information for {room_name} on {date}. Our room rates vary by date and season. I can help you check availability and get current pricing. Would you like me to connect you with our reservations team for exact pricing?",
                "end_call": False
            }
        
        # Format pricing response
        response = "Here's the pricing information I found: "
        for price in relevant_prices[:3]:  # Show max 3 prices
            parts = price.split('\t')
            if len(parts) >= 3:
                response += f"{parts[0]} on {parts[1]} costs ₹{parts[2]}. "
        
        response += "Prices may vary based on season and availability. Would you like to proceed with a booking?"
        
        return {
            "response": limit_tokens(response, 700),
            "end_call": False
        }
    except Exception as e:
        return {
            "response": "I'm having trouble accessing pricing information. Let me connect you with our reservations team who can provide current rates and help with booking.",
            "end_call": False
        }

async def check_availability_for_retell(args: Dict):
    """Check room availability for Retell AI"""
    try:
        check_in = args.get("check_in_date", "")
        check_out = args.get("check_out_date", "")
        guests = args.get("guests", 2)
        room_type = args.get("room_type", "")
        
        with open("data/rooms.json") as f:
            rooms = json.load(f)
        
        available_rooms = []
        for room in rooms:
            if int(room.get("max_guests", 0)) >= int(guests):
                if not room_type or room_type.lower() in room.get("room_name", "").lower():
                    available_rooms.append(room)
        
        if not available_rooms:
            return {
                "response": f"I don't have rooms available for {guests} guests in the {room_type} category. Let me suggest some alternatives or you can speak with our reservations team for more options.",
                "end_call": False
            }
        
        response = f"Great! I found availability for {guests} guests"
        if check_in and check_out:
            response += f" from {check_in} to {check_out}"
        response += ". Here are your options: "
        
        for room in available_rooms[:2]:  # Show max 2 options
            response += f"{room['room_name']} (up to {room['max_guests']} guests, {room['total_number_of_rooms_available']} available), "
        
        response += "Would you like me to help you with booking one of these rooms?"
        
        return {
            "response": limit_tokens(response, 700),
            "end_call": False
        }
    except Exception as e:
        return {
            "response": "I'm having trouble checking availability right now. Let me connect you with our reservations team who can check real-time availability and help with your booking.",
            "end_call": False
        }

async def get_hotel_policies_for_retell(args: Dict):
    """Get hotel policies for Retell AI"""
    try:
        policy_type = args.get("policy_type", "").lower()
        
        with open("data/hotel.json") as f:
            policies = json.load(f)
        
        response = ""
        if "cancellation" in policy_type or not policy_type:
            response += f"Our cancellation policy: {policies.get('cancellation_policy', 'Please contact us for cancellation details.')} "
        
        if "visitor" in policy_type or not policy_type:
            response += f"Visitor policy: {policies.get('visitor_policy', 'Please check with reception.')} "
        
        if "kids" in policy_type or "children" in policy_type or not policy_type:
            response += f"Kids policy: {policies.get('kids_policy', 'Children are welcome.')} "
        
        if not response:
            response = "I can help you with information about our cancellation policy, visitor policy, or children's policy. What would you like to know?"
        
        return {
            "response": limit_tokens(response, 700),
            "end_call": False
        }
    except Exception as e:
        return {
            "response": "I'm having trouble accessing policy information. Let me connect you with our front desk who can provide detailed policy information.",
            "end_call": False
        }

async def log_conversation_for_retell(args: Dict):
    """Log conversation data from Retell AI"""
    try:
        # Extract conversation data
        log_data = {
            "Call_Time": args.get("call_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "Phone_Number": args.get("phone_number", "NA"),
            "Call_Outcome": args.get("call_outcome", "ENQUIRY"),
            "Check_In_Date": args.get("check_in_date", "NA"),
            "Check_Out_Date": args.get("check_out_date", "NA"),
            "Customer_Name": args.get("customer_name", "NA"),
            "Room_Name": args.get("room_name", "NA"),
            "Number_of_Guests": str(args.get("number_of_guests", "NA")),
            "Call_Summary": args.get("call_summary", "Customer interaction logged")
        }
        
        # Log to sheets
        log_conversation_to_sheet(log_data)
        
        return {
            "response": "Thank you for calling Formi Hotel. Your request has been recorded and our team will follow up with you shortly. Have a great day!",
            "end_call": True
        }
    except Exception as e:
        print(f"❌ Error logging conversation: {str(e)}")
        return {
            "response": "Thank you for calling. If you need any further assistance, please don't hesitate to call us back.",
            "end_call": True
        }

# --------------------------
# 10. Retell AI Webhooks
# --------------------------
@app.post("/retell/webhook")
async def retell_webhook(event: RetellCallEvent):
    """Handle Retell AI webhooks"""
    try:
        print(f"🔔 Retell webhook: {event.event}")
        print(f"📞 Call ID: {event.call_id}")
        print(f"📋 Data: {event.data}")
        
        if event.event == "call_started":
            print("📞 Call started")
        elif event.event == "call_ended":
            print("📞 Call ended")
            # You can add additional logging here
        elif event.event == "call_analyzed":
            print("📊 Call analyzed")
            # Extract and log call summary if available
            if event.data:
                summary_data = {
                    "Call_Time": event.timestamp,
                    "Phone_Number": event.data.get("from_number", "NA"),
                    "Call_Outcome": event.data.get("call_outcome", "MISC"),
                    "Check_In_Date": event.data.get("check_in_date", "NA"),
                    "Check_Out_Date": event.data.get("check_out_date", "NA"),
                    "Customer_Name": event.data.get("customer_name", "NA"),
                    "Room_Name": event.data.get("room_name", "NA"),
                    "Number_of_Guests": str(event.data.get("number_of_guests", "NA")),
                    "Call_Summary": event.data.get("call_summary", "Call completed")
                }
                try:
                    log_conversation_to_sheet(summary_data)
                except Exception as log_error:
                    print(f"❌ Error logging webhook data: {str(log_error)}")
        
        return {"status": "received"}
    except Exception as e:
        print(f"❌ Error in webhook: {str(e)}")
        return {"status": "error", "message": str(e)}

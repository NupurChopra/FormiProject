# Retell AI Configuration Guide

## 1. Create Retell AI Account
1. Go to https://retellai.com
2. Sign up for an account
3. Get your API key from the dashboard

## 2. Create Agent Configuration

### Agent Prompt:
```
You are a professional hotel receptionist for Formi Hotel. You help customers with:
- Room inquiries and availability
- Pricing information  
- Hotel policies
- Booking assistance

Be friendly, professional, and helpful. Always collect customer details when they want to book.

Available functions:
- get_room_info: Get information about room types
- get_pricing_info: Get pricing for specific rooms and dates
- check_availability: Check room availability for dates
- get_hotel_policies: Get hotel policies (cancellation, visitor, etc.)
- log_conversation_data: Log conversation at the end

Important: Always end calls by logging the conversation data with collected information.
```

### Function Definitions:
```json
[
  {
    "name": "get_room_info",
    "description": "Get information about hotel rooms",
    "parameters": {
      "type": "object",
      "properties": {
        "room_type": {
          "type": "string",
          "description": "Type of room (e.g., Executive, Premium, Standard)"
        }
      }
    }
  },
  {
    "name": "get_pricing_info", 
    "description": "Get pricing information for rooms",
    "parameters": {
      "type": "object",
      "properties": {
        "room_name": {
          "type": "string",
          "description": "Name of the room"
        },
        "date": {
          "type": "string", 
          "description": "Date in YYYY-MM-DD format"
        }
      }
    }
  },
  {
    "name": "check_availability",
    "description": "Check room availability",
    "parameters": {
      "type": "object",
      "properties": {
        "check_in_date": {
          "type": "string",
          "description": "Check-in date in YYYY-MM-DD format"
        },
        "check_out_date": {
          "type": "string", 
          "description": "Check-out date in YYYY-MM-DD format"
        },
        "guests": {
          "type": "integer",
          "description": "Number of guests"
        },
        "room_type": {
          "type": "string",
          "description": "Preferred room type"
        }
      }
    }
  },
  {
    "name": "get_hotel_policies",
    "description": "Get hotel policies information",
    "parameters": {
      "type": "object", 
      "properties": {
        "policy_type": {
          "type": "string",
          "description": "Type of policy (cancellation, visitor, kids, etc.)"
        }
      }
    }
  },
  {
    "name": "log_conversation_data",
    "description": "Log conversation data at the end of call",
    "parameters": {
      "type": "object",
      "properties": {
        "phone_number": {"type": "string"},
        "call_outcome": {"type": "string", "enum": ["ENQUIRY", "AVAILABILITY", "POST_BOOKING", "MISC"]},
        "check_in_date": {"type": "string"}, 
        "check_out_date": {"type": "string"},
        "customer_name": {"type": "string"},
        "room_name": {"type": "string"},
        "number_of_guests": {"type": "integer"},
        "call_summary": {"type": "string"}
      }
    }
  }
]
```

## 3. Configure Webhooks
- Webhook URL: `https://your-domain.com/retell/webhook`
- Function Call URL: `https://your-domain.com/retell/function-call`

## 4. Test Your Integration
1. Start your FastAPI server: `uvicorn main:app --reload`
2. Use ngrok to expose your local server: `ngrok http 8000`
3. Update Retell AI with your ngrok URL
4. Test the phone integration

## 5. Deploy to Production
For production, deploy to:
- Railway
- Heroku  
- AWS Lambda
- Google Cloud Functions
- Or any cloud provider

Make sure to:
- Set environment variables for API keys
- Use HTTPS endpoints
- Monitor logs for debugging

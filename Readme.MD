# Formi Hotel Voice AI Assistant

A comprehensive voice AI system built with FastAPI and Retell AI integration for hotel reservations and customer service.

## 🚀 Features

- **Voice AI Integration**: Full Retell AI integration with function calling
- **Hotel Information System**: Room details, pricing, and availability checking
- **Google Sheets Logging**: Automatic conversation logging to Google Sheets
- **Token Management**: Intelligent response chunking under 800 tokens
- **RESTful API**: Complete API endpoints for all hotel operations
- **Real-time Processing**: Under 800ms response time for voice interactions

## 📋 Project Structure

```
FormiProject/
├── main.py                 # Main FastAPI application
├── requirements.txt        # Python dependencies
├── test_retell.py         # Retell AI integration tests
├── test_sheets.py         # Google Sheets integration tests
├── RETELL_SETUP.md        # Retell AI configuration guide
├── SHEETS_SETUP.md        # Google Sheets setup guide
├── service_account.json   # Google service account (not in repo)
├── .env.template          # Environment variables template
├── .gitignore             # Git ignore rules
└── data/                  # Hotel information data
    ├── rooms.json         # Room information
    ├── pricing.json       # Pricing data
    ├── hotel.json         # Hotel policies
    ├── discount.json      # Discount information
    └── staff.json         # Staff information
```

## 🛠️ Technical Stack

- **Backend**: FastAPI (Python)
- **Voice AI**: Retell AI platform
- **Database**: Google Sheets API
- **Token Management**: tiktoken (OpenAI tokenizer)
- **Real-time**: WebSocket support
- **Phone Integration**: Twilio (for testing)

## 📚 API Endpoints

### Core Endpoints
- `GET /` - Health check
- `GET /info/{category}` - Get hotel information by category
- `POST /classify-query` - Classify user queries
- `POST /search-info` - Search for specific information
- `POST /log-conversation` - Log conversation data

### Retell AI Integration
- `POST /retell/function-call` - Handle Retell AI function calls
- `POST /retell/webhook` - Receive Retell AI webhooks

### Available Functions for Retell AI
1. **get_room_info** - Get room details and amenities
2. **get_pricing_info** - Get pricing for specific dates
3. **check_availability** - Check room availability  
4. **get_hotel_policies** - Get hotel policies (cancellation, etc.)
5. **log_conversation_data** - Log call data at the end

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Google Sheets
1. Follow instructions in `SHEETS_SETUP.md`
2. Place `service_account.json` in project root
3. Create and share a sheet named `formi_call`

### 3. Setup Retell AI
1. Follow instructions in `RETELL_SETUP.md`
2. Configure your agent with the provided functions
3. Set webhook URLs to your deployed endpoints

### 4. Run the Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Test the System
```bash
# Test Google Sheets integration
python test_sheets.py

# Test Retell AI integration
python test_retell.py
```

## 🔧 Configuration

### Environment Variables
Copy `.env.template` to `.env` and fill in your values:
```
RETELL_API_KEY=your_retell_api_key
RETELL_AGENT_ID=your_agent_id
GOOGLE_SHEETS_SPREADSHEET_NAME=formi_call
```

### Retell AI Agent Configuration
Use the function definitions and prompts provided in `RETELL_SETUP.md` to configure your Retell AI agent.

## 📊 Data Management

### Information Categories
- **rooms.json**: Room types, amenities, capacity
- **pricing.json**: Dynamic pricing by date
- **hotel.json**: Policies and restrictions
- **discount.json**: Available discounts
- **staff.json**: Staff information

### Token Limitation Handling
All responses are automatically limited to 800 tokens using tiktoken to ensure compatibility with Retell AI's requirements.

## 🎯 Call Flow Example

1. **Customer calls** the Twilio number
2. **Retell AI** answers and processes speech
3. **Function calls** are made to your FastAPI endpoints
4. **Information is retrieved** and chunked under 800 tokens
5. **Response is returned** to Retell AI for speech synthesis
6. **Conversation is logged** to Google Sheets automatically

## 📱 Testing the Voice System

### Local Testing (with ngrok)
```bash
# Start your server
uvicorn main:app --reload

# In another terminal, expose with ngrok
ngrok http 8000

# Use the ngrok URL in Retell AI configuration
```

### Production Deployment
Deploy to platforms like:
- Railway
- Heroku
- AWS Lambda
- Google Cloud Functions
- Vercel

## 📝 Logging Format

Conversations are logged to Google Sheets with these fields:
- Call Time
- Phone Number  
- Call Outcome (ENQUIRY/AVAILABILITY/POST_BOOKING/MISC)
- Check In/Out Dates
- Customer Name
- Room Name
- Number of Guests
- Call Summary

## 🔍 Monitoring & Debugging

### Logs
The application provides detailed logging for:
- Function calls from Retell AI
- Google Sheets operations
- Error handling and debugging
- Token counting and response limits

### Testing Scripts
- `test_retell.py` - Test all Retell AI functions
- `test_sheets.py` - Test Google Sheets logging

## 🚨 Error Handling

The system includes comprehensive error handling for:
- Missing or invalid data
- Google Sheets connection issues
- Retell AI function call failures
- Network timeouts and retries
- Token limit exceeding

## 📈 Performance Optimizations

- Response times under 800ms
- Efficient data chunking
- Connection pooling for external APIs
- Caching for frequently accessed data
- Async operations where possible

## 🔐 Security Considerations

- Service account JSON not in repository
- Environment variable configuration
- Input validation and sanitization
- Rate limiting for API endpoints
- HTTPS enforcement in production

## 🤝 Contributing

This project was built as part of the Formi SDE assignment. The development process includes:

1. **Regular commits** documenting development progress
2. **Test-driven development** with comprehensive test coverage
3. **Documentation-first** approach with detailed setup guides
4. **Error handling** and edge case management
5. **Performance optimization** for real-time voice interactions

## 📞 Assignment Completion

This system fulfills all requirements:
- ✅ APIs for information delivery under 800 tokens
- ✅ Google Sheets integration for conversation logging
- ✅ Retell AI integration with function calling
- ✅ Phone system testing capability
- ✅ Comprehensive documentation and testing
- ✅ Real-time performance under 800ms
- ✅ Error handling and edge cases
- ✅ GitHub repository with regular commits

---

**Built with ❤️ for Formi Hotel Assignment**

# HTTP Request Scripts

This folder contains HTTP request files for manual testing of the Inflation API endpoints. These files use the HTTP Client format supported by many IDEs and tools.

## 📁 Files Overview

| File | Description |
|------|-------------|
| `health.http` | Health check and documentation endpoints |
| `inflation-rates.http` | Get inflation rates for specific years |
| `value-change.http` | Calculate value changes between years |
| `current-value.http` | Calculate current value of historical amounts |
| `examples.http` | Real-world use cases and examples |
| `error-cases.http` | Error scenarios and edge cases |

## 🚀 How to Use

### Option 1: VS Code with REST Client Extension
1. Install the "REST Client" extension in VS Code
2. Open any `.http` file
3. Click "Send Request" above any request
4. View the response in the split pane

### Option 2: IntelliJ IDEA / WebStorm
1. Open any `.http` file in IntelliJ IDEA or WebStorm
2. Click the green arrow (▶️) next to any request
3. View responses in the HTTP Client tab

### Option 3: Command Line with curl
Convert the HTTP requests to curl commands:

```bash
# Health check
curl http://localhost:8000/health

# Get inflation rate
curl http://localhost:8000/api/v1/inflation/rate/2020

# POST request with JSON
curl -X POST http://localhost:8000/api/v1/inflation/current-value \
  -H "Content-Type: application/json" \
  -d '{"original_year": 2020, "amount": 100.0}'
```

### Option 4: HTTPie (if installed)
```bash
# Health check
http GET localhost:8000/health

# Get inflation rate  
http GET localhost:8000/api/v1/inflation/rate/2020

# POST request
http POST localhost:8000/api/v1/inflation/current-value original_year:=2020 amount:=100.0
```

## 🎯 Getting Started

1. **Start the server first:**
   ```bash
   uv run uvicorn inflation_api.main:app --reload
   ```

2. **Try the basic requests:**
   - Start with `health.http` to verify the server is running
   - Then try `inflation-rates.http` to get familiar with the API
   - Use `examples.http` for common real-world scenarios

3. **Explore advanced features:**
   - `value-change.http` for inflation calculations
   - `current-value.http` for purchasing power analysis
   - `error-cases.http` to understand error handling

## 📊 API Base Information

- **Base URL:** `http://localhost:8000`
- **API Version:** `/api/v1`
- **Health Check:** `/health`
- **Documentation:** `/docs` (Swagger UI) or `/redoc`

## 💡 Tips

- **Server must be running** on localhost:8000 for requests to work
- Check `/docs` endpoint for interactive API documentation
- Most endpoints support both GET (query params) and POST (JSON body) methods
- The API validates input and provides detailed error messages
- All financial calculations use high-precision decimals
- Years must be in range 1800-2100, with available data from 2015-2025

## 🧪 Test Scenarios

### Basic Usage
- Get inflation rate for any year
- Calculate how much $100 from 2020 is worth today
- Compare dollar values between any two years

### Advanced Examples
- Salary adjustment calculations
- Investment return vs inflation analysis
- Historical purchasing power comparisons
- Reverse calculations (future to past)

### Error Testing
- Invalid years, amounts, and date ranges
- Missing data scenarios
- Validation error responses
- HTTP status code verification
# Testing the /api/match-programs Endpoint

## Quick Test Commands

### 1. Test GET request (should now work!)
```bash
curl -X GET http://localhost:5000/api/match-programs
```

### 2. Test POST request with full data
```bash
curl -X POST http://localhost:5000/api/match-programs \
  -H "Content-Type: application/json" \
  -d '{
    "sscPercentage": 75,
    "hscPercentage": 80,
    "hscGroup": "Pre-Engineering",
    "interests": ["Computer Science", "Technology"],
    "budget": 200000,
    "preferredLocation": "Karachi"
  }'
```

### 3. Test POST request with minimal data
```bash
curl -X POST http://localhost:5000/api/match-programs \
  -H "Content-Type: application/json" \
  -d '{
    "sscPercentage": 60,
    "hscPercentage": 65,
    "budget": 100000
  }'
```

### 4. Test POST request for medical student
```bash
curl -X POST http://localhost:5000/api/match-programs \
  -H "Content-Type: application/json" \
  -d '{
    "sscPercentage": 85,
    "hscPercentage": 88,
    "hscGroup": "Pre-Medical",
    "interests": ["Medicine", "Dentistry"],
    "budget": 500000,
    "preferredLocation": "Lahore"
  }'
```

## Expected Results

### GET Request Response:
```json
{
  "success": false,
  "message": "Please send a POST request with JSON data containing: sscPercentage, hscPercentage, hscGroup, interests, budget, preferredLocation",
  "example": {
    "sscPercentage": 75,
    "hscPercentage": 80,
    "hscGroup": "Pre-Engineering",
    "interests": ["Computer Science", "Technology"],
    "budget": 200000,
    "preferredLocation": "Karachi"
  }
}
```

### POST Request Response:
```json
{
  "success": true,
  "total_matches": 15,
  "matches": [
    {
      "program_name": "BS Computer Science",
      "university_name": "Example University",
      "campus_name": "Main Campus",
      "total_fee": 180000,
      "duration_years": 4,
      "match_score": 95.5
    }
    // ... more matches
  ]
}
```

## Troubleshooting

1. **Make sure your Flask server is running:**
   ```bash
   cd backend
   python app.py
   # or
   flask run
   ```

2. **If you get connection refused:**
   - Check if the server is running on port 5000
   - Try `http://127.0.0.1:5000` instead of `localhost`

3. **If you get timeout:**
   - The matching algorithm might be taking time
   - Try with smaller budget or different parameters

4. **If you get JSON parsing errors:**
   - Make sure your JSON is properly formatted
   - Check that all quotes are straight quotes `"` not curly quotes `"` 
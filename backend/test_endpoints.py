#!/usr/bin/env python3
import requests
import json

def test_match_programs_endpoint():
    """Test both GET and POST methods for the match-programs endpoint"""
    
    base_url = 'http://localhost:5000/api/match-programs'
    
    print("🧪 Testing /api/match-programs endpoint")
    print("=" * 50)
    
    # Test 1: GET request (should now work and return helpful message)
    print("\n1️⃣ Testing GET request...")
    try:
        response = requests.get(base_url, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ GET request successful!")
            print(f"   Message: {data.get('message', 'No message')}")
            if 'example' in data:
                print(f"   Example data provided: ✅")
        else:
            print(f"   ❌ GET request failed: {response.text}")
    except Exception as e:
        print(f"   ❌ GET request error: {e}")
    
    # Test 2: POST request with valid data
    print("\n2️⃣ Testing POST request with valid data...")
    test_data = {
        "sscPercentage": 75,
        "hscPercentage": 80,
        "hscGroup": "Pre-Engineering",
        "interests": ["Computer Science", "Technology"],
        "budget": 200000,
        "preferredLocation": "Karachi"
    }
    
    try:
        response = requests.post(
            base_url,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ POST request successful!")
            print(f"   Total matches: {data.get('total_matches', 0)}")
            print(f"   Response size: {len(response.content)} bytes")
            
            # Show first few matches if available
            if 'matches' in data and data['matches']:
                print(f"   First match: {data['matches'][0].get('program_name', 'N/A')}")
        else:
            print(f"   ❌ POST request failed: {response.text}")
    except Exception as e:
        print(f"   ❌ POST request error: {e}")
    
    # Test 3: POST request with minimal data
    print("\n3️⃣ Testing POST request with minimal data...")
    minimal_data = {
        "sscPercentage": 60,
        "hscPercentage": 65,
        "budget": 100000
    }
    
    try:
        response = requests.post(
            base_url,
            json=minimal_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ POST request successful!")
            print(f"   Total matches: {data.get('total_matches', 0)}")
        else:
            print(f"   ❌ POST request failed: {response.text}")
    except Exception as e:
        print(f"   ❌ POST request error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Testing complete!")

if __name__ == "__main__":
    test_match_programs_endpoint() 
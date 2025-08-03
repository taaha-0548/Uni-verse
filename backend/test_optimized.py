#!/usr/bin/env python3
import requests
import time

def test_optimized_server():
    print("Testing optimized server...")
    
    test_data = {
        "sscPercentage": 75,
        "hscPercentage": 80,
        "hscGroup": "Pre-Engineering",
        "interests": ["Computer Science"],
        "budget": 500000,
        "preferredLocation": ""
    }
    
    try:
        start_time = time.time()
        
        response = requests.post(
            'http://localhost:5000/api/match-programs',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Request completed in {elapsed:.3f}s")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Matches found: {data.get('total_matches', 0)}")
            print(f"   Response size: {len(response.content)} bytes")
            return True
        else:
            print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out after 30s")
        return False
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    test_optimized_server() 
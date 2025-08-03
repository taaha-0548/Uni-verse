#!/usr/bin/env python3
"""
Comprehensive API Testing Script for Uni-verse Backend
Tests the /api/match-programs endpoint and diagnoses issues
"""

import requests
import json
import sys
from datetime import datetime

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_step(step_num, description):
    """Print a formatted step"""
    print(f"\n[STEP {step_num}] {description}")
    print("-" * 40)

def test_server_connection():
    """Test if the server is running and accessible"""
    print_step(1, "Testing Server Connection")
    
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        print(f"✅ Server is running!")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running or not accessible")
        print("   Make sure to run: cd backend && python app.py")
        return False
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return False

def test_get_request():
    """Test GET request to the endpoint (should fail)"""
    print_step(2, "Testing GET Request (Expected to Fail)")
    
    try:
        response = requests.get('http://localhost:5000/api/match-programs', timeout=5)
        print(f"❌ GET request should have failed but got status: {response.status_code}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"✅ GET request correctly failed: {e}")
        return True

def test_post_request_without_data():
    """Test POST request without proper data"""
    print_step(3, "Testing POST Request Without Data")
    
    try:
        response = requests.post('http://localhost:5000/api/match-programs', timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        return response.status_code != 405  # Should not be Method Not Allowed
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_post_request_with_valid_data():
    """Test POST request with valid data"""
    print_step(4, "Testing POST Request With Valid Data")
    
    # Sample student data
    test_data = {
        "sscPercentage": 80,
        "hscPercentage": 85,
        "hscGroup": "Pre-Engineering",
        "interests": ["Computer Science", "Engineering"],
        "budget": 500000,
        "preferredLocation": "Karachi"
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/api/match-programs',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ POST request successful!")
            data = response.json()
            print(f"   Success: {data.get('success', 'N/A')}")
            print(f"   Total Matches: {data.get('total_matches', 'N/A')}")
            if 'matched_offerings' in data:
                print(f"   Number of Offerings: {len(data['matched_offerings'])}")
                if data['matched_offerings']:
                    print(f"   First Match: {data['matched_offerings'][0]['program_name']}")
            return True
        else:
            print(f"❌ POST request failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_post_request_with_invalid_data():
    """Test POST request with invalid data"""
    print_step(5, "Testing POST Request With Invalid Data")
    
    # Test with missing required fields
    invalid_data = {
        "sscPercentage": "invalid",  # Should be number
        "hscPercentage": 85,
        # Missing hscGroup
        "budget": "not_a_number"
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/api/match-programs',
            json=invalid_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 500:
            print("✅ Server correctly handled invalid data with 500 error")
            return True
        elif response.status_code == 200:
            print("⚠️ Server accepted invalid data (might be an issue)")
            return True
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_cors_headers():
    """Test CORS headers"""
    print_step(6, "Testing CORS Headers")
    
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        
        if cors_header:
            print(f"✅ CORS header found: {cors_header}")
            return True
        else:
            print("⚠️ No CORS header found")
            return False
            
    except Exception as e:
        print(f"❌ Error testing CORS: {e}")
        return False

def test_database_connection():
    """Test if database is accessible"""
    print_step(7, "Testing Database Connection")
    
    try:
        # Test a simple endpoint that uses the database
        response = requests.get('http://localhost:5000/api/stats', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                stats = data.get('stats', {})
                print("✅ Database connection successful!")
                print(f"   Universities: {stats.get('universities', 'N/A')}")
                print(f"   Programs: {stats.get('programs', 'N/A')}")
                print(f"   Offerings: {stats.get('offerings', 'N/A')}")
                return True
            else:
                print("❌ Database query failed")
                return False
        else:
            print(f"❌ Stats endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing database: {e}")
        return False

def main():
    """Main testing function"""
    print_header("Uni-verse API Testing Script")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Run all tests
    tests = [
        ("Server Connection", test_server_connection),
        ("GET Request Test", test_get_request),
        ("POST Without Data", test_post_request_without_data),
        ("POST With Valid Data", test_post_request_with_valid_data),
        ("POST With Invalid Data", test_post_request_with_invalid_data),
        ("CORS Headers", test_cors_headers),
        ("Database Connection", test_database_connection)
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print_header("Test Results Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    print("\nDetailed Results:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    # Provide recommendations
    print_header("Recommendations")
    
    if not any(name == "Server Connection" and result for name, result in results):
        print("1. Start the backend server: cd backend && python app.py")
    
    if not any(name == "POST With Valid Data" and result for name, result in results):
        print("2. Check your .env file configuration")
        print("3. Verify database connection string")
        print("4. Check if all required packages are installed")
    
    if not any(name == "Database Connection" and result for name, result in results):
        print("5. Database connection issues detected")
        print("   - Check DATABASE_URL in .env file")
        print("   - Verify database is running")
        print("   - Check if tables exist")
    
    print("\n" + "="*60)
    print("Testing Complete!")
    print("="*60)

if __name__ == "__main__":
    main() 
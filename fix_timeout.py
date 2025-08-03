#!/usr/bin/env python3
"""
Fix for the timeout issue in /api/match-programs endpoint
"""

import requests
import json
import time

def test_with_timeout():
    """Test the endpoint with different timeout values"""
    print("="*60)
    print("Testing Timeout Issues")
    print("="*60)
    
    # Test data
    test_data = {
        "sscPercentage": 80,
        "hscPercentage": 85,
        "hscGroup": "Pre-Engineering",
        "interests": ["Computer Science"],
        "budget": 500000,
        "preferredLocation": "Karachi"
    }
    
    timeouts = [5, 10, 30, 60]
    
    for timeout in timeouts:
        print(f"\nTesting with {timeout} second timeout...")
        start_time = time.time()
        
        try:
            response = requests.post(
                'http://localhost:5000/api/match-programs',
                json=test_data,
                headers={'Content-Type': 'application/json'},
                timeout=timeout
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"✅ Request completed in {duration:.2f} seconds")
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Success: {data.get('success')}")
                print(f"   Total Matches: {data.get('total_matches')}")
                if 'matched_offerings' in data:
                    print(f"   Number of Offerings: {len(data['matched_offerings'])}")
                break
            else:
                print(f"   Response: {response.text[:200]}...")
                
        except requests.exceptions.Timeout:
            print(f"❌ Request timed out after {timeout} seconds")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_simple_query():
    """Test a simpler query to see if the issue is with the complex query"""
    print("\n" + "="*60)
    print("Testing Simple Database Query")
    print("="*60)
    
    try:
        # Test the stats endpoint which uses a simple query
        response = requests.get('http://localhost:5000/api/stats', timeout=5)
        print(f"Stats endpoint: {response.status_code}")
        
        # Test universities endpoint
        response = requests.get('http://localhost:5000/api/universities', timeout=5)
        print(f"Universities endpoint: {response.status_code}")
        
        # Test programs endpoint
        response = requests.get('http://localhost:5000/api/programs', timeout=5)
        print(f"Programs endpoint: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error testing simple queries: {e}")

def test_with_smaller_data():
    """Test with smaller dataset to see if it's a data volume issue"""
    print("\n" + "="*60)
    print("Testing with Smaller Dataset")
    print("="*60)
    
    # Test with very restrictive criteria
    small_test_data = {
        "sscPercentage": 95,  # Very high score
        "hscPercentage": 95,  # Very high score
        "hscGroup": "Pre-Engineering",
        "interests": ["Computer Science"],
        "budget": 1000000,  # Very high budget
        "preferredLocation": "Karachi"
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            'http://localhost:5000/api/match-programs',
            json=small_test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        end_time = time.time()
        
        print(f"Request completed in {end_time - start_time:.2f} seconds")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Total Matches: {data.get('total_matches')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_with_timeout()
    test_simple_query()
    test_with_smaller_data() 
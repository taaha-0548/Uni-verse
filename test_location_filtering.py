#!/usr/bin/env python3
"""
Test location filtering functionality
"""

import requests
import json

def test_location_filtering():
    """Test location filtering with different cities"""
    print("🧪 TESTING LOCATION FILTERING")
    print("=" * 60)
    
    # Test with Karachi
    test_data_karachi = {
        "sscPercentage": "90",
        "hscPercentage": "90",
        "hscGroup": "Pre-Medical",
        "interestPriorities": [
            {"interest": "Computer Science", "priority": 1}
        ],
        "interests": ["Computer Science"],
        "budget": "1000000000",
        "preferredLocation": "Karachi"
    }
    
    # Test with Lahore
    test_data_lahore = {
        "sscPercentage": "90",
        "hscPercentage": "90",
        "hscGroup": "Pre-Medical",
        "interestPriorities": [
            {"interest": "Computer Science", "priority": 1}
        ],
        "interests": ["Computer Science"],
        "budget": "1000000000",
        "preferredLocation": "Lahore"
    }
    
    # Test with Islamabad
    test_data_islamabad = {
        "sscPercentage": "90",
        "hscPercentage": "90",
        "hscGroup": "Pre-Medical",
        "interestPriorities": [
            {"interest": "Computer Science", "priority": 1}
        ],
        "interests": ["Computer Science"],
        "budget": "1000000000",
        "preferredLocation": "Islamabad"
    }
    
    try:
        print("Testing Karachi location filtering:")
        response1 = requests.post('http://localhost:5000/api/match-programs', json=test_data_karachi)
        if response1.status_code == 200:
            data1 = response1.json()
            offerings1 = data1.get('matched_offerings', [])
            
            print(f"✅ Found {len(offerings1)} matched offerings for Karachi")
            
            # Check cities in results
            cities_karachi = set()
            for offering in offerings1[:10]:
                city = offering['campus']['city']
                cities_karachi.add(city)
                print(f"   - {offering['program_name']} in {city}")
            
            print(f"   Cities found: {', '.join(cities_karachi)}")
            
            # Verify all cities contain "karachi"
            all_karachi = all('karachi' in city.lower() for city in cities_karachi)
            if all_karachi:
                print(f"   ✅ All programs are from Karachi")
            else:
                print(f"   ❌ Some programs are not from Karachi")
        
        print("\nTesting Lahore location filtering:")
        response2 = requests.post('http://localhost:5000/api/match-programs', json=test_data_lahore)
        if response2.status_code == 200:
            data2 = response2.json()
            offerings2 = data2.get('matched_offerings', [])
            
            print(f"✅ Found {len(offerings2)} matched offerings for Lahore")
            
            # Check cities in results
            cities_lahore = set()
            for offering in offerings2[:10]:
                city = offering['campus']['city']
                cities_lahore.add(city)
                print(f"   - {offering['program_name']} in {city}")
            
            print(f"   Cities found: {', '.join(cities_lahore)}")
            
            # Verify all cities contain "lahore"
            all_lahore = all('lahore' in city.lower() for city in cities_lahore)
            if all_lahore:
                print(f"   ✅ All programs are from Lahore")
            else:
                print(f"   ❌ Some programs are not from Lahore")
        
        print("\nTesting Islamabad location filtering:")
        response3 = requests.post('http://localhost:5000/api/match-programs', json=test_data_islamabad)
        if response3.status_code == 200:
            data3 = response3.json()
            offerings3 = data3.get('matched_offerings', [])
            
            print(f"✅ Found {len(offerings3)} matched offerings for Islamabad")
            
            # Check cities in results
            cities_islamabad = set()
            for offering in offerings3[:10]:
                city = offering['campus']['city']
                cities_islamabad.add(city)
                print(f"   - {offering['program_name']} in {city}")
            
            print(f"   Cities found: {', '.join(cities_islamabad)}")
            
            # Verify all cities contain "islamabad"
            all_islamabad = all('islamabad' in city.lower() for city in cities_islamabad)
            if all_islamabad:
                print(f"   ✅ All programs are from Islamabad")
            else:
                print(f"   ❌ Some programs are not from Islamabad")
                
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    test_location_filtering()
    print("\n🎉 Location Filtering Test Complete!")
    print("=" * 60) 
import requests
import json

# Test data matching your payload
test_data = {
    "sscPercentage": "90",
    "hscPercentage": "90", 
    "qualificationType": "HSC/A-Level",
    "hscGroup": "Pre-Medical",
    "budget": "10000000000",
    "preferredLocation": "Karachi",
    "interests": ["Medicine", "Pharmacy", "Computer Science", "Psychology"],
    "interestPriorities": [
        {"interest": "Medicine", "priority": 1},
        {"interest": "Pharmacy", "priority": 2},
        {"interest": "Computer Science", "priority": 3},
        {"interest": "Psychology", "priority": 4}
    ]
}

def test_ranking():
    """Test the new ranking logic"""
    try:
        # Test the new ranking endpoint
        response = requests.post('http://localhost:5000/api/test-ranking', json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Test ranking endpoint working!")
            print(f"Found {len(result['test_programs'])} programs")
            
            # Show top 5 programs with interest matches
            interest_matches = [p for p in result['test_programs'] if p['has_interest_match']]
            print(f"\n📊 Programs with interest matches: {len(interest_matches)}")
            
            for i, program in enumerate(interest_matches[:5]):
                print(f"{i+1}. {program['program_name']} - {program['university']}")
                print(f"   Priority Score: {program['priority_score']}")
                print(f"   Matched Interests: {', '.join(program['matched_interests'])}")
                print(f"   Tags: {', '.join(program['tags'])}")
                print()
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_main_endpoint():
    """Test the main match-programs endpoint"""
    try:
        response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Main endpoint working!")
            print(f"Found {len(result['matched_offerings'])} matched offerings")
            
            # Show top 5 results
            print("\n📊 Top 5 matched programs:")
            for i, offering in enumerate(result['matched_offerings'][:5]):
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']}")
                print(f"   Match Score: {offering['match_score']}")
                print(f"   Tags: {', '.join(offering['tags'])}")
                print()
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing ranking logic fixes...")
    print("=" * 50)
    
    # Test both endpoints
    test_ranking()
    print("-" * 30)
    test_main_endpoint() 
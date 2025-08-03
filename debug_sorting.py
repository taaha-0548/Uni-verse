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

def debug_sorting():
    """Debug the sorting logic"""
    try:
        response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("🔍 Debugging sorting logic...")
            print(f"Total offerings: {len(result['matched_offerings'])}")
            
            # Look at the first 10 results and their sorting criteria
            for i, offering in enumerate(result['matched_offerings'][:10]):
                print(f"\n{i+1}. {offering['program_name']} - {offering['university']['name']}")
                print(f"   Match Score: {offering['match_score']}")
                print(f"   Tags: {', '.join(offering['tags'])}")
                
                # Check if this should have interest match
                program_tags = [tag.lower() for tag in offering['tags']]
                has_medicine = any(tag in ['medicine', 'mbbs', 'doctor'] for tag in program_tags)
                has_nursing = any(tag in ['nursing'] for tag in program_tags)
                has_pharmacy = any(tag in ['pharmacy'] for tag in program_tags)
                
                print(f"   Has Medicine: {has_medicine}")
                print(f"   Has Nursing: {has_nursing}")
                print(f"   Has Pharmacy: {has_pharmacy}")
                
                # Calculate what the priority score should be
                priority_score = 0
                if has_medicine:
                    priority_score = 1000  # Priority 1
                elif has_pharmacy:
                    priority_score = 900   # Priority 2
                elif has_nursing:
                    priority_score = 0     # Not in priorities
                
                print(f"   Expected Priority Score: {priority_score}")
                print(f"   Debug Priority Score: {offering.get('debug_priority_score', 'N/A')}")
                print(f"   Debug Has Interest Match: {offering.get('debug_has_interest_match', 'N/A')}")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    debug_sorting() 
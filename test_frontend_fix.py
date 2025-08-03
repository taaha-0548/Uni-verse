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

def test_backend_ranking():
    """Test that backend ranking is working correctly"""
    try:
        response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Backend ranking test:")
            print(f"Found {len(result['matched_offerings'])} matched offerings")
            
            # Show top 10 results to see the ranking
            print("\n📊 Top 10 programs (backend ranking):")
            for i, offering in enumerate(result['matched_offerings'][:10]):
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']}")
                print(f"   Match Score: {offering['match_score']}")
                print(f"   Tags: {', '.join(offering['tags'])}")
                
                # Check if this should be a medicine program
                program_tags = [tag.lower() for tag in offering['tags']]
                has_medicine = any(tag in ['medicine', 'mbbs', 'doctor'] for tag in program_tags)
                has_nursing = any(tag in ['nursing'] for tag in program_tags)
                has_pharmacy = any(tag in ['pharmacy'] for tag in program_tags)
                
                if has_medicine and not has_nursing and not has_pharmacy:
                    print(f"   ✅ This is a core medicine program!")
                elif has_medicine and has_nursing:
                    print(f"   ⚠️  This is nursing (allied health)")
                elif has_medicine and has_pharmacy:
                    print(f"   ⚠️  This is pharmacy (allied health)")
                else:
                    print(f"   ℹ️  Other program type")
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
    print("🧪 Testing frontend fix...")
    print("=" * 50)
    
    test_backend_ranking() 
import requests
import json

# Test data matching your exact payload
test_data = {
    "sscPercentage": "90",
    "hscPercentage": "90", 
    "qualificationType": "HSC/A-Level",
    "hscGroup": "Pre-Medical",
    "budget": "10000000000",
    "preferredLocation": "Karachi",
    "interests": ["Medicine", "Computer Science", "Pharmacy"],
    "interestPriorities": [
        {"interest": "Medicine", "priority": 1},
        {"interest": "Computer Science", "priority": 2},
        {"interest": "Pharmacy", "priority": 3}
    ]
}

def test_medicine_priority():
    """Test that medicine programs rank first"""
    try:
        response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Medicine priority test:")
            print(f"Found {len(result['matched_offerings'])} matched offerings")
            
            # Show top 15 results to see the ranking
            print("\n📊 Top 15 programs (should show Medicine first):")
            for i, offering in enumerate(result['matched_offerings'][:15]):
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']}")
                print(f"   Match Score: {offering['match_score']}")
                print(f"   Tags: {', '.join(offering['tags'])}")
                
                # Check if this should be a medicine program
                program_tags = [tag.lower() for tag in offering['tags']]
                has_medicine = any(tag in ['medicine', 'mbbs', 'doctor'] for tag in program_tags)
                has_nursing = any(tag in ['nursing'] for tag in program_tags)
                has_pharmacy = any(tag in ['pharmacy'] for tag in program_tags)
                has_cs = any(tag in ['computer science', 'software engineering'] for tag in program_tags)
                
                if has_medicine and not has_nursing and not has_pharmacy:
                    print(f"   ✅ CORE MEDICINE PROGRAM (Priority 1)")
                elif has_medicine and has_nursing:
                    print(f"   ⚠️  NURSING (allied health)")
                elif has_medicine and has_pharmacy:
                    print(f"   ⚠️  PHARMACY (allied health)")
                elif has_cs:
                    print(f"   💻 COMPUTER SCIENCE (Priority 2)")
                else:
                    print(f"   ℹ️  Other program type")
                print()
            
            # Count programs by type
            medicine_count = 0
            nursing_count = 0
            pharmacy_count = 0
            cs_count = 0
            
            for offering in result['matched_offerings'][:20]:
                program_tags = [tag.lower() for tag in offering['tags']]
                has_medicine = any(tag in ['medicine', 'mbbs', 'doctor'] for tag in program_tags)
                has_nursing = any(tag in ['nursing'] for tag in program_tags)
                has_pharmacy = any(tag in ['pharmacy'] for tag in program_tags)
                has_cs = any(tag in ['computer science', 'software engineering'] for tag in program_tags)
                
                if has_medicine and not has_nursing and not has_pharmacy:
                    medicine_count += 1
                elif has_medicine and has_nursing:
                    nursing_count += 1
                elif has_medicine and has_pharmacy:
                    pharmacy_count += 1
                elif has_cs:
                    cs_count += 1
            
            print(f"\n📈 Summary of top 20 programs:")
            print(f"   Core Medicine: {medicine_count}")
            print(f"   Nursing: {nursing_count}")
            print(f"   Pharmacy: {pharmacy_count}")
            print(f"   Computer Science: {cs_count}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Medicine Priority Fix...")
    print("=" * 50)
    
    test_medicine_priority() 
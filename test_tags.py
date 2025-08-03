import requests
import json

# Test the new tag-based priority system
def test_tag_based_priority():
    print("=== Testing Tag-Based Priority System ===")
    
    # Test data with Medicine as highest priority
    test_data = {
        "ssc_percentage": 85,
        "hsc_percentage": 80,
        "hsc_group": "Pre-Medical",
        "interests": ["medicine", "pharmacy", "dentistry"],
        "interestPriorities": [
            {"interest": "medicine", "priority": 1},
            {"interest": "pharmacy", "priority": 2},
            {"interest": "dentistry", "priority": 3}
        ],
        "budget": 500000,
        "preferred_location": "Karachi"
    }
    
    try:
        # Call the match-programs endpoint
        response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API call successful")
            print(f"Total matches: {data.get('total_matches', 0)}")
            
            if 'matched_offerings' in data:
                print("\n=== Top 10 Results ===")
                for i, offering in enumerate(data['matched_offerings'][:10]):
                    print(f"{i+1}. {offering['program_name']}")
                    print(f"   University: {offering['university']['name']}")
                    print(f"   Tags: {offering['tags']}")
                    print(f"   Match Score: {offering['match_score']}")
                    print(f"   Annual Fee: PKR {offering['annual_fee']:,}")
                    print()
        else:
            print(f"❌ API call failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def check_available_tags():
    print("=== Checking Available Tags ===")
    
    try:
        # Get all program offerings to see what tags are available
        response = requests.get('http://localhost:5000/api/program-offerings')
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API call successful")
            
            if 'offerings' in data:
                # Collect all unique tags
                all_tags = set()
                medical_programs = []
                engineering_programs = []
                cs_programs = []
                
                for offering in data['offerings']:
                    if offering.get('tags'):
                        for tag in offering['tags']:
                            all_tags.add(tag.lower())
                    
                    # Categorize programs for analysis
                    program_name = offering['program_name'].lower()
                    if any(med in program_name for med in ['mbbs', 'medicine', 'medical']):
                        medical_programs.append(offering)
                    elif any(eng in program_name for eng in ['engineering', 'civil', 'electrical', 'mechanical']):
                        engineering_programs.append(offering)
                    elif any(cs in program_name for cs in ['computer', 'software', 'information technology']):
                        cs_programs.append(offering)
                
                print(f"\nTotal unique tags: {len(all_tags)}")
                print("Available tags:")
                for tag in sorted(all_tags):
                    print(f"  - {tag}")
                
                print(f"\nMedical programs found: {len(medical_programs)}")
                for prog in medical_programs[:5]:
                    print(f"  - {prog['program_name']} (Tags: {prog.get('tags', [])})")
                
                print(f"\nEngineering programs found: {len(engineering_programs)}")
                for prog in engineering_programs[:5]:
                    print(f"  - {prog['program_name']} (Tags: {prog.get('tags', [])})")
                
                print(f"\nCS programs found: {len(cs_programs)}")
                for prog in cs_programs[:5]:
                    print(f"  - {prog['program_name']} (Tags: {prog.get('tags', [])})")
                
        else:
            print(f"❌ API call failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Starting tag-based priority system test...")
    check_available_tags()
    print("\n" + "="*50 + "\n")
    test_tag_based_priority() 
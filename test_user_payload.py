#!/usr/bin/env python3
"""
Test with user's exact payload
"""

import requests
import json

def test_user_payload():
    """Test with user's exact payload"""
    print("🧪 TESTING USER'S EXACT PAYLOAD")
    print("=" * 60)
    
    # User's exact payload
    test_data = {
        "sscPercentage": "90",
        "hscPercentage": "90",
        "qualificationType": "HSC/A-Level",
        "hscGroup": "Pre-Medical",
        "budget": "1000000000",
        "interestPriorities": [
            {"interest": "Computer Science", "priority": 1},
            {"interest": "Software Engineering", "priority": 2}
        ],
        "interests": ["Computer Science", "Software Engineering", "Medicine"],
        "preferredLocation": "Karachi",
        "scoreType": "ssc_hsc"
    }
    
    try:
        response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
        if response.status_code == 200:
            data = response.json()
            offerings = data.get('matched_offerings', [])
            
            print(f"✅ Found {len(offerings)} matched offerings")
            print(f"\n📊 Top 20 programs (should show CS first, then Medicine):")
            
            # Track what we see
            medicine_count = 0
            cs_count = 0
            other_count = 0
            
            for i, offering in enumerate(offerings[:20], 1):
                program_name = offering['program_name']
                match_score = offering['match_score']
                tags = offering.get('tags', [])
                
                # Categorize the program
                if any(tag in ['mbbs', 'doctor'] for tag in tags):
                    category = "✅ CORE MEDICINE (MBBS)"
                    medicine_count += 1
                elif any(tag in ['medicine', 'medical'] for tag in tags) and not any(tag in ['nursing', 'pharmacy', 'allied-health'] for tag in tags):
                    category = "✅ CORE MEDICINE"
                    medicine_count += 1
                elif any(tag in ['computer science', 'computer-science', 'software engineering', 'software-engineering', 'software', 'programming'] for tag in tags):
                    category = "💻 COMPUTER SCIENCE"
                    cs_count += 1
                else:
                    category = "📚 OTHER"
                    other_count += 1
                
                print(f"{i:2d}. {program_name}")
                print(f"     Match Score: {match_score}")
                print(f"     Tags: {', '.join(tags)}")
                print(f"     {category}")
                print()
            
            print(f"\n📈 Summary of top 20 programs:")
            print(f"   Medicine: {medicine_count}")
            print(f"   Computer Science: {cs_count}")
            print(f"   Other: {other_count}")
            
            # Analyze priority logic
            print(f"\n🔍 Priority Analysis:")
            print(f"   Expected: Computer Science (Priority 1) should be at top")
            print(f"   Expected: Software Engineering (Priority 2) should be second")
            print(f"   Actual: CS programs found: {cs_count}")
            print(f"   Actual: Medicine programs found: {medicine_count}")
            
            if cs_count > medicine_count:
                print(f"   ✅ Priority 1 (CS) is ranking higher than Medicine")
            else:
                print(f"   ❌ Priority logic may not be working correctly")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    test_user_payload()
    print("\n🎉 Test Complete!")
    print("=" * 60) 
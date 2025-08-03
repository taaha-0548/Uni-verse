#!/usr/bin/env python3
"""
Debug script to analyze why Medicine programs are still ranking higher than CS programs
"""

import requests
import json

def debug_priority_issue():
    """Debug the priority issue"""
    print("🔍 DEBUGGING PRIORITY ISSUE")
    print("=" * 60)
    
    test_data = {
        "sscPercentage": "90",
        "hscPercentage": "90",
        "hscGroup": "Pre-Medical",
        "interestPriorities": [
            {"interest": "Computer Science", "priority": 1},
            {"interest": "Software Engineering", "priority": 2}
        ],
        "interests": ["Computer Science", "Software Engineering", "Medicine"],
        "budget": "1000000000",
        "preferredLocation": "Karachi"
    }
    
    try:
        response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
        if response.status_code == 200:
            data = response.json()
            offerings = data.get('matched_offerings', [])
            
            print(f"✅ Found {len(offerings)} matched offerings")
            print(f"\n🔍 Analyzing first 20 programs:")
            
            for i, offering in enumerate(offerings[:20], 1):
                program_name = offering['program_name']
                match_score = offering['match_score']
                tags = offering.get('tags', [])
                
                # Check what this program should match
                medicine_match = any(tag in ['mbbs', 'doctor', 'medicine', 'medical'] for tag in tags) and not any(tag in ['nursing', 'pharmacy'] for tag in tags)
                cs_match = any(tag in ['computer science', 'software engineering'] for tag in tags)
                software_match = any(tag in ['software'] for tag in tags)
                programming_match = any(tag in ['programming'] for tag in tags)
                
                print(f"\n{i:2d}. {program_name}")
                print(f"     Match Score: {match_score}")
                print(f"     Tags: {', '.join(tags)}")
                print(f"     Medicine Match: {medicine_match}")
                print(f"     CS Match: {cs_match}")
                print(f"     Software Match: {software_match}")
                print(f"     Programming Match: {programming_match}")
                
                # Calculate expected priority score
                expected_priority = 0
                if cs_match or software_match or programming_match:
                    expected_priority = (11 - 1) * 100  # Priority 1 = 1000
                    expected_priority += 400  # CS boost
                elif medicine_match:
                    expected_priority = (11 - 3) * 100  # Priority 3 = 800 (if Medicine is priority 3)
                    if any(tag in ['mbbs', 'doctor'] for tag in tags):
                        expected_priority += 500  # MBBS boost
                    else:
                        expected_priority += 400  # Medicine boost
                
                print(f"     Expected Priority Score: {expected_priority}")
                
                if cs_match or software_match or programming_match:
                    print(f"     → Should be Priority 1 (Computer Science)")
                elif medicine_match:
                    print(f"     → Should be Priority 3 (Medicine)")
                else:
                    print(f"     → No priority match")
                    
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

def debug_cs_programs():
    """Find CS programs in the results"""
    print("\n🔍 FINDING CS PROGRAMS")
    print("=" * 60)
    
    test_data = {
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
    
    try:
        response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
        if response.status_code == 200:
            data = response.json()
            offerings = data.get('matched_offerings', [])
            
            print(f"✅ Found {len(offerings)} matched offerings")
            
            # Find CS programs
            cs_programs = []
            for i, offering in enumerate(offerings):
                program_name = offering['program_name']
                tags = offering.get('tags', [])
                
                if any(tag in ['computer science', 'software engineering', 'software', 'programming'] for tag in tags):
                    cs_programs.append({
                        'index': i,
                        'name': program_name,
                        'tags': tags,
                        'match_score': offering['match_score']
                    })
            
            print(f"\n💻 Found {len(cs_programs)} CS programs:")
            for program in cs_programs[:10]:
                print(f"   {program['index']:3d}. {program['name']}")
                print(f"       Tags: {', '.join(program['tags'])}")
                print(f"       Match Score: {program['match_score']}")
                print()
                
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    debug_priority_issue()
    debug_cs_programs()
    print("\n🎉 Debug Complete!")
    print("=" * 60) 
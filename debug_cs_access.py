#!/usr/bin/env python3
"""
Debug script to check why CS programs aren't appearing for Pre-Medical students
"""

import requests
import json

def debug_cs_access():
    """Debug CS access for Pre-Medical students"""
    print("🧪 Debugging CS Access for Pre-Medical Students")
    print("=" * 60)
    
    # Test with Pre-Medical student
    test_data = {
        "sscPercentage": 90,
        "hscPercentage": 90,
        "hscGroup": "Pre-Medical",
        "interestPriorities": [
            {"interest": "Computer Science", "priority": 1},
            {"interest": "Medicine", "priority": 2}
        ],
        "interests": ["Computer Science", "Medicine"],
        "budget": 1000000,
        "preferredLocation": "Karachi"
    }
    
    try:
        response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
        if response.status_code == 200:
            data = response.json()
            offerings = data.get('matched_offerings', [])
            subject_restrictions = data.get('subject_restrictions', {})
            
            print(f"✅ Found {len(offerings)} matched offerings")
            print(f"📊 Subject restrictions: {subject_restrictions}")
            
            # Check what interests are being filtered
            filtered_interests = subject_restrictions.get('filtered_interests', [])
            allowed_interests = subject_restrictions.get('allowed_interests', [])
            
            print(f"\n🔍 Interest Analysis:")
            print(f"   Original interests: {test_data['interests']}")
            print(f"   Allowed interests: {allowed_interests}")
            print(f"   Filtered interests: {filtered_interests}")
            
            # Check if CS is in allowed interests
            cs_allowed = "Computer Science" in allowed_interests
            cs_filtered = "Computer Science" in filtered_interests
            
            print(f"\n💻 Computer Science Access:")
            print(f"   CS in allowed interests: {cs_allowed}")
            print(f"   CS in filtered interests: {cs_filtered}")
            
            # Look for CS programs in results
            cs_programs = []
            medicine_programs = []
            other_programs = []
            
            for offering in offerings[:50]:  # Check first 50
                program_name = offering['program_name']
                tags = offering.get('tags', [])
                
                if any(tag in ['computer science', 'software engineering'] for tag in tags):
                    cs_programs.append(program_name)
                elif any(tag in ['medicine', 'medical', 'mbbs', 'doctor'] for tag in tags):
                    medicine_programs.append(program_name)
                else:
                    other_programs.append(program_name)
            
            print(f"\n📊 Program Analysis (first 50):")
            print(f"   CS programs found: {len(cs_programs)}")
            print(f"   Medicine programs found: {len(medicine_programs)}")
            print(f"   Other programs found: {len(other_programs)}")
            
            if cs_programs:
                print(f"\n💻 CS Programs found:")
                for i, program in enumerate(cs_programs[:10], 1):
                    print(f"   {i}. {program}")
            else:
                print(f"\n❌ No CS programs found!")
                
            # Check if there are any CS programs in the database at all
            print(f"\n🔍 Checking all programs for CS tags...")
            cs_tagged_programs = []
            
            for offering in offerings:
                program_name = offering['program_name']
                tags = offering.get('tags', [])
                
                if any(tag in ['computer science', 'software engineering', 'computer'] for tag in tags):
                    cs_tagged_programs.append({
                        'name': program_name,
                        'tags': tags
                    })
            
            print(f"   Total CS-tagged programs in database: {len(cs_tagged_programs)}")
            
            if cs_tagged_programs:
                print(f"   Sample CS programs:")
                for i, program in enumerate(cs_tagged_programs[:5], 1):
                    print(f"   {i}. {program['name']} - Tags: {', '.join(program['tags'])}")
            else:
                print(f"   ❌ No CS-tagged programs found in database!")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

def test_ics_student_cs():
    """Test ICS student to see if CS programs exist"""
    print("\n🧪 Testing ICS Student (should have CS access)")
    print("=" * 60)
    
    test_data = {
        "sscPercentage": 90,
        "hscPercentage": 90,
        "hscGroup": "ICS (Computer Science)",
        "interestPriorities": [
            {"interest": "Computer Science", "priority": 1}
        ],
        "interests": ["Computer Science"],
        "budget": 1000000,
        "preferredLocation": "Karachi"
    }
    
    try:
        response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
        if response.status_code == 200:
            data = response.json()
            offerings = data.get('matched_offerings', [])
            
            print(f"✅ Found {len(offerings)} matched offerings")
            
            cs_programs = []
            for offering in offerings[:20]:
                program_name = offering['program_name']
                tags = offering.get('tags', [])
                
                if any(tag in ['computer science', 'software engineering'] for tag in tags):
                    cs_programs.append(program_name)
            
            print(f"📊 CS programs found: {len(cs_programs)}")
            
            if cs_programs:
                print(f"💻 CS Programs:")
                for i, program in enumerate(cs_programs[:10], 1):
                    print(f"   {i}. {program}")
            else:
                print(f"❌ No CS programs found even for ICS student!")
                
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    print("🧪 CS ACCESS DEBUGGING")
    print("=" * 60)
    
    debug_cs_access()
    test_ics_student_cs()
    
    print("\n🎉 Debug Complete!")
    print("=" * 60) 
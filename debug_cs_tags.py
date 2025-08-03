#!/usr/bin/env python3
"""
Debug script to analyze what tags Computer Science programs actually have
"""

import requests
import json

def debug_cs_tags():
    """Debug what tags CS programs actually have"""
    print("🔍 DEBUGGING COMPUTER SCIENCE TAGS")
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
            print(f"\n🔍 Analyzing first 50 programs for CS tags:")
            
            cs_programs = []
            medicine_programs = []
            engineering_programs = []
            other_programs = []
            
            for i, offering in enumerate(offerings[:50], 1):
                program_name = offering['program_name']
                tags = offering.get('tags', [])
                
                # Check what type of program this is
                if any(tag in ['mbbs', 'doctor', 'medicine', 'medical'] for tag in tags) and not any(tag in ['nursing', 'pharmacy'] for tag in tags):
                    medicine_programs.append({
                        'name': program_name,
                        'tags': tags,
                        'index': i
                    })
                elif any(tag in ['computer science', 'software engineering'] for tag in tags):
                    cs_programs.append({
                        'name': program_name,
                        'tags': tags,
                        'index': i
                    })
                elif any(tag in ['computer', 'electronics'] for tag in tags) and any(tag in ['engineering'] for tag in tags):
                    engineering_programs.append({
                        'name': program_name,
                        'tags': tags,
                        'index': i
                    })
                else:
                    other_programs.append({
                        'name': program_name,
                        'tags': tags,
                        'index': i
                    })
            
            print(f"\n📊 Program Analysis:")
            print(f"   Medicine programs: {len(medicine_programs)}")
            print(f"   CS programs: {len(cs_programs)}")
            print(f"   Engineering programs: {len(engineering_programs)}")
            print(f"   Other programs: {len(other_programs)}")
            
            if cs_programs:
                print(f"\n💻 Computer Science Programs found:")
                for program in cs_programs[:10]:
                    print(f"   {program['index']:2d}. {program['name']}")
                    print(f"       Tags: {', '.join(program['tags'])}")
                    print()
            else:
                print(f"\n❌ No Computer Science programs found!")
                
            if medicine_programs:
                print(f"\n🏥 Medicine Programs found:")
                for program in medicine_programs[:5]:
                    print(f"   {program['index']:2d}. {program['name']}")
                    print(f"       Tags: {', '.join(program['tags'])}")
                    print()
                    
            # Check if there are any programs with 'software' or 'programming' tags
            software_programs = []
            programming_programs = []
            
            for offering in offerings:
                program_name = offering['program_name']
                tags = offering.get('tags', [])
                
                if any(tag in ['software'] for tag in tags):
                    software_programs.append(program_name)
                if any(tag in ['programming'] for tag in tags):
                    programming_programs.append(program_name)
            
            print(f"\n🔍 Tag Analysis:")
            print(f"   Programs with 'software' tag: {len(software_programs)}")
            print(f"   Programs with 'programming' tag: {len(programming_programs)}")
            
            if software_programs:
                print(f"   Software programs: {software_programs[:5]}")
            if programming_programs:
                print(f"   Programming programs: {programming_programs[:5]}")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    debug_cs_tags()
    print("\n🎉 Debug Complete!")
    print("=" * 60) 
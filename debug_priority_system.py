#!/usr/bin/env python3
"""
Comprehensive debug script to analyze the priority system
Finds the root cause of why CS programs are appearing mixed with Medicine programs
"""

import requests
import json

def debug_priority_scores():
    """Debug the priority scoring system"""
    print("🔍 DEBUGGING PRIORITY SCORING SYSTEM")
    print("=" * 60)
    
    test_data = {
        "sscPercentage": 90,
        "hscPercentage": 90,
        "hscGroup": "Pre-Medical",
        "interestPriorities": [
            {"interest": "Medicine", "priority": 1},
            {"interest": "Computer Science", "priority": 2}
        ],
        "interests": ["Medicine", "Computer Science"],
        "budget": 1000000,
        "preferredLocation": "Karachi"
    }
    
    try:
        response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
        if response.status_code == 200:
            data = response.json()
            offerings = data.get('matched_offerings', [])
            
            print(f"✅ Found {len(offerings)} matched offerings")
            print(f"\n🔍 Analyzing Priority Scores for First 20 Programs:")
            
            for i, offering in enumerate(offerings[:20], 1):
                program_name = offering['program_name']
                match_score = offering['match_score']
                tags = offering.get('tags', [])
                
                # Analyze what this program should match
                medicine_match = any(tag in ['mbbs', 'doctor', 'medicine', 'medical'] for tag in tags) and not any(tag in ['nursing', 'pharmacy'] for tag in tags)
                cs_match = any(tag in ['computer science', 'software engineering', 'computer'] for tag in tags)
                
                # Calculate expected priority score
                expected_priority = 0
                if medicine_match:
                    expected_priority = (11 - 1) * 100  # Priority 1 = 1000
                    if any(tag in ['mbbs', 'doctor'] for tag in tags):
                        expected_priority += 500  # MBBS boost
                    else:
                        expected_priority += 400  # Medicine boost
                elif cs_match:
                    expected_priority = (11 - 2) * 100  # Priority 2 = 900
                    expected_priority += 400  # CS boost
                
                print(f"\n{i:2d}. {program_name}")
                print(f"     Tags: {', '.join(tags)}")
                print(f"     Match Score: {match_score}")
                print(f"     Medicine Match: {medicine_match}")
                print(f"     CS Match: {cs_match}")
                print(f"     Expected Priority Score: {expected_priority}")
                
                if medicine_match:
                    print(f"     → Should be Priority 1 (Medicine)")
                elif cs_match:
                    print(f"     → Should be Priority 2 (Computer Science)")
                else:
                    print(f"     → No priority match")
                    
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

def debug_priority_order():
    """Test priority order with different configurations"""
    print("\n🧪 TESTING PRIORITY ORDER")
    print("=" * 60)
    
    # Test 1: Medicine Priority 1, CS Priority 2
    test_data_1 = {
        "sscPercentage": 90,
        "hscPercentage": 90,
        "hscGroup": "Pre-Medical",
        "interestPriorities": [
            {"interest": "Medicine", "priority": 1},
            {"interest": "Computer Science", "priority": 2}
        ],
        "interests": ["Medicine", "Computer Science"],
        "budget": 1000000,
        "preferredLocation": "Karachi"
    }
    
    # Test 2: CS Priority 1, Medicine Priority 2
    test_data_2 = {
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
        print("Test 1: Medicine Priority 1, CS Priority 2")
        response1 = requests.post('http://localhost:5000/api/match-programs', json=test_data_1)
        if response1.status_code == 200:
            data1 = response1.json()
            offerings1 = data1.get('matched_offerings', [])
            
            print(f"   Found {len(offerings1)} offerings")
            
            # Count programs by type in first 10
            medicine_count_1 = 0
            cs_count_1 = 0
            
            for offering in offerings1[:10]:
                tags = offering.get('tags', [])
                if any(tag in ['mbbs', 'doctor', 'medicine', 'medical'] for tag in tags) and not any(tag in ['nursing', 'pharmacy'] for tag in tags):
                    medicine_count_1 += 1
                elif any(tag in ['computer science', 'software engineering', 'computer'] for tag in tags):
                    cs_count_1 += 1
            
            print(f"   First 10 - Medicine: {medicine_count_1}, CS: {cs_count_1}")
            
            # Check if Medicine programs come first
            first_medicine_index = -1
            first_cs_index = -1
            
            for i, offering in enumerate(offerings1):
                tags = offering.get('tags', [])
                if first_medicine_index == -1 and any(tag in ['mbbs', 'doctor', 'medicine', 'medical'] for tag in tags) and not any(tag in ['nursing', 'pharmacy'] for tag in tags):
                    first_medicine_index = i
                if first_cs_index == -1 and any(tag in ['computer science', 'software engineering', 'computer'] for tag in tags):
                    first_cs_index = i
                if first_medicine_index != -1 and first_cs_index != -1:
                    break
            
            print(f"   First Medicine at index: {first_medicine_index}")
            print(f"   First CS at index: {first_cs_index}")
            
            if first_medicine_index < first_cs_index:
                print(f"   ✅ Medicine programs come before CS programs")
            else:
                print(f"   ❌ CS programs come before Medicine programs")
        
        print("\nTest 2: CS Priority 1, Medicine Priority 2")
        response2 = requests.post('http://localhost:5000/api/match-programs', json=test_data_2)
        if response2.status_code == 200:
            data2 = response2.json()
            offerings2 = data2.get('matched_offerings', [])
            
            print(f"   Found {len(offerings2)} offerings")
            
            # Count programs by type in first 10
            medicine_count_2 = 0
            cs_count_2 = 0
            
            for offering in offerings2[:10]:
                tags = offering.get('tags', [])
                if any(tag in ['mbbs', 'doctor', 'medicine', 'medical'] for tag in tags) and not any(tag in ['nursing', 'pharmacy'] for tag in tags):
                    medicine_count_2 += 1
                elif any(tag in ['computer science', 'software engineering', 'computer'] for tag in tags):
                    cs_count_2 += 1
            
            print(f"   First 10 - Medicine: {medicine_count_2}, CS: {cs_count_2}")
            
            # Check if CS programs come first
            first_medicine_index = -1
            first_cs_index = -1
            
            for i, offering in enumerate(offerings2):
                tags = offering.get('tags', [])
                if first_medicine_index == -1 and any(tag in ['mbbs', 'doctor', 'medicine', 'medical'] for tag in tags) and not any(tag in ['nursing', 'pharmacy'] for tag in tags):
                    first_medicine_index = i
                if first_cs_index == -1 and any(tag in ['computer science', 'software engineering', 'computer'] for tag in tags):
                    first_cs_index = i
                if first_medicine_index != -1 and first_cs_index != -1:
                    break
            
            print(f"   First Medicine at index: {first_medicine_index}")
            print(f"   First CS at index: {first_cs_index}")
            
            if first_cs_index < first_medicine_index:
                print(f"   ✅ CS programs come before Medicine programs")
            else:
                print(f"   ❌ Medicine programs come before CS programs")
                
    except Exception as e:
        print(f"❌ Connection error: {e}")

def debug_sort_key_logic():
    """Debug the sort_key function logic"""
    print("\n🔧 DEBUGGING SORT_KEY LOGIC")
    print("=" * 60)
    
    test_data = {
        "sscPercentage": 90,
        "hscPercentage": 90,
        "hscGroup": "Pre-Medical",
        "interestPriorities": [
            {"interest": "Medicine", "priority": 1},
            {"interest": "Computer Science", "priority": 2}
        ],
        "interests": ["Medicine", "Computer Science"],
        "budget": 1000000,
        "preferredLocation": "Karachi"
    }
    
    try:
        response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
        if response.status_code == 200:
            data = response.json()
            offerings = data.get('matched_offerings', [])
            
            print(f"✅ Found {len(offerings)} matched offerings")
            print(f"\n🔍 Analyzing Sort Key Logic for First 10 Programs:")
            
            for i, offering in enumerate(offerings[:10], 1):
                program_name = offering['program_name']
                match_score = offering['match_score']
                tags = offering.get('tags', [])
                
                # Simulate the sort_key logic
                medicine_match = any(tag in ['mbbs', 'doctor', 'medicine', 'medical'] for tag in tags) and not any(tag in ['nursing', 'pharmacy'] for tag in tags)
                cs_match = any(tag in ['computer science', 'software engineering', 'computer'] for tag in tags)
                
                # Calculate expected priority score
                priority_score = 0
                if medicine_match:
                    priority_score = (11 - 1) * 100  # Priority 1 = 1000
                    if any(tag in ['mbbs', 'doctor'] for tag in tags):
                        priority_score += 500  # MBBS boost
                    else:
                        priority_score += 400  # Medicine boost
                elif cs_match:
                    priority_score = (11 - 2) * 100  # Priority 2 = 900
                    priority_score += 400  # CS boost
                
                # Expected sort key tuple
                if priority_score > 0:
                    expected_sort_key = (priority_score, 0, 0)
                else:
                    expected_sort_key = (0, match_score, 0)
                
                print(f"\n{i:2d}. {program_name}")
                print(f"     Tags: {', '.join(tags)}")
                print(f"     Match Score: {match_score}")
                print(f"     Medicine Match: {medicine_match}")
                print(f"     CS Match: {cs_match}")
                print(f"     Calculated Priority Score: {priority_score}")
                print(f"     Expected Sort Key: {expected_sort_key}")
                
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

def debug_category_matching():
    """Debug the interest category matching logic"""
    print("\n🏷️  DEBUGGING CATEGORY MATCHING")
    print("=" * 60)
    
    # Test different program types
    test_programs = [
        {"name": "MBBS", "tags": ["mbbs", "doctor", "medical", "medicine"]},
        {"name": "Medicine", "tags": ["medicine", "medical"]},
        {"name": "BE Computer Engineering", "tags": ["computer", "electronics", "engineering", "technology"]},
        {"name": "BS Computer Science", "tags": ["computer science", "software engineering"]},
        {"name": "BS Nursing", "tags": ["nursing", "medical"]},
        {"name": "BS Pharmacy", "tags": ["pharmacy", "medical"]}
    ]
    
    # Define the interest categories from backend
    interest_categories = {
        'medicine': {
            'core_tags': ['mbbs', 'doctor'],
            'general_tags': ['medicine', 'medical'],
            'exclusion_tags': ['nursing', 'pharmacy', 'allied-health'],
            'boost_tags': ['mbbs', 'doctor']
        },
        'computer science': {
            'core_tags': ['computer science', 'software engineering', 'programming', 'software', 'computer'],
            'general_tags': ['computer', 'electronics'],
            'exclusion_tags': ['information technology', 'it', 'information systems'],
            'boost_tags': ['computer science', 'software engineering', 'computer']
        }
    }
    
    print("Testing Medicine Category Matching:")
    for program in test_programs:
        program_tags = program['tags']
        interest = 'medicine'
        
        if interest in interest_categories:
            category = interest_categories[interest]
            has_core = any(tag in category['core_tags'] for tag in program_tags)
            has_exclusion = any(tag in category['exclusion_tags'] for tag in program_tags)
            has_general = any(tag in category['general_tags'] for tag in program_tags) if not has_exclusion else False
            
            matched = has_core or has_general
            
            print(f"   {program['name']}: {matched} (Core: {has_core}, General: {has_general}, Exclusion: {has_exclusion})")
    
    print("\nTesting Computer Science Category Matching:")
    for program in test_programs:
        program_tags = program['tags']
        interest = 'computer science'
        
        if interest in interest_categories:
            category = interest_categories[interest]
            has_core = any(tag in category['core_tags'] for tag in program_tags)
            has_exclusion = any(tag in category['exclusion_tags'] for tag in program_tags)
            has_general = any(tag in category['general_tags'] for tag in program_tags) if not has_exclusion else False
            
            matched = has_core or has_general
            
            print(f"   {program['name']}: {matched} (Core: {has_core}, General: {has_general}, Exclusion: {has_exclusion})")

if __name__ == "__main__":
    print("🔍 PRIORITY SYSTEM ROOT CAUSE ANALYSIS")
    print("=" * 60)
    
    debug_priority_scores()
    debug_priority_order()
    debug_sort_key_logic()
    debug_category_matching()
    
    print("\n🎉 Analysis Complete!")
    print("=" * 60) 
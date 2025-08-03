#!/usr/bin/env python3
"""
Test priority logic analysis with specific user payload
Analyzes how the priority system handles the user's interest priorities
"""

import requests
import json

def test_user_priority_payload():
    """Test with the user's specific payload"""
    print("🧪 Testing User Priority Payload")
    print("=" * 60)
    
    # User's exact payload
    test_data = {
        "sscPercentage": "90",
        "hscPercentage": "90", 
        "qualificationType": "HSC/A-Level",
        "hscGroup": "Pre-Medical",
        "budget": "1000000000000",
        "hscPercentage": "90",
        "interestPriorities": [
            {"interest": "Medicine", "priority": 1},
            {"interest": "Computer Science", "priority": 2}
        ],
        "interests": ["Medicine", "Computer Science", "Nursing", "Psychology"],
        "preferredLocation": "Karachi",
        "qualificationType": "HSC/A-Level",
        "scoreType": "ssc_hsc",
        "sscPercentage": "90"
    }
    
    try:
        response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
        if response.status_code == 200:
            data = response.json()
            offerings = data.get('matched_offerings', [])
            print(f"✅ Found {len(offerings)} matched offerings")
            
            print("\n📊 Top 20 programs (should show Medicine first, then Computer Science):")
            
            # Track what we see
            medicine_count = 0
            cs_count = 0
            nursing_count = 0
            psychology_count = 0
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
                elif any(tag in ['computer', 'electronics'] for tag in tags) and any(tag in ['engineering'] for tag in tags):
                    category = "⚙️  ENGINEERING (Computer)"
                    cs_count += 1
                elif any(tag in ['nursing'] for tag in tags):
                    category = "⚠️  NURSING"
                    nursing_count += 1
                elif any(tag in ['psychology'] for tag in tags):
                    category = "🧠 PSYCHOLOGY"
                    psychology_count += 1
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
            print(f"   Nursing: {nursing_count}")
            print(f"   Psychology: {psychology_count}")
            print(f"   Other: {other_count}")
            
            # Analyze priority logic
            print(f"\n🔍 Priority Analysis:")
            print(f"   Expected: Medicine (Priority 1) should be at top")
            print(f"   Expected: Computer Science (Priority 2) should be second")
            print(f"   Actual: Medicine programs found: {medicine_count}")
            print(f"   Actual: CS programs found: {cs_count}")
            
            if medicine_count > cs_count:
                print(f"   ✅ Priority 1 (Medicine) is ranking higher than Priority 2 (CS)")
            else:
                print(f"   ❌ Priority logic may not be working correctly")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

def test_priority_order():
    """Test different priority orders to verify logic"""
    print("\n🧪 Testing Priority Order Logic")
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
            
            medicine_count_1 = 0
            cs_count_1 = 0
            
            for offering in offerings1[:10]:
                tags = offering.get('tags', [])
                if any(tag in ['mbbs', 'doctor', 'medicine', 'medical'] for tag in tags) and not any(tag in ['nursing', 'pharmacy'] for tag in tags):
                    medicine_count_1 += 1
                elif any(tag in ['computer science', 'software engineering'] for tag in tags):
                    cs_count_1 += 1
            
            print(f"   Medicine programs: {medicine_count_1}")
            print(f"   CS programs: {cs_count_1}")
        
        print("\nTest 2: CS Priority 1, Medicine Priority 2")
        response2 = requests.post('http://localhost:5000/api/match-programs', json=test_data_2)
        if response2.status_code == 200:
            data2 = response2.json()
            offerings2 = data2.get('matched_offerings', [])
            
            medicine_count_2 = 0
            cs_count_2 = 0
            
            for offering in offerings2[:10]:
                tags = offering.get('tags', [])
                if any(tag in ['mbbs', 'doctor', 'medicine', 'medical'] for tag in tags) and not any(tag in ['nursing', 'pharmacy'] for tag in tags):
                    medicine_count_2 += 1
                elif any(tag in ['computer science', 'software engineering'] for tag in tags):
                    cs_count_2 += 1
            
            print(f"   Medicine programs: {medicine_count_2}")
            print(f"   CS programs: {cs_count_2}")
            
            print(f"\n🔍 Priority Order Analysis:")
            print(f"   Test 1 (Medicine Priority 1): Medicine={medicine_count_1}, CS={cs_count_1}")
            print(f"   Test 2 (CS Priority 1): Medicine={medicine_count_2}, CS={cs_count_2}")
            
            if medicine_count_1 > cs_count_1 and cs_count_2 > medicine_count_2:
                print(f"   ✅ Priority order is working correctly!")
            else:
                print(f"   ❌ Priority order may not be working correctly")
                
    except Exception as e:
        print(f"❌ Connection error: {e}")

def test_debug_priority_logic():
    """Debug the priority logic by examining a few programs"""
    print("\n🧪 Debug Priority Logic")
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
            
            print(f"Analyzing first 5 programs:")
            for i, offering in enumerate(offerings[:5], 1):
                program_name = offering['program_name']
                match_score = offering['match_score']
                tags = offering.get('tags', [])
                
                print(f"\n{i}. {program_name}")
                print(f"   Match Score: {match_score}")
                print(f"   Tags: {', '.join(tags)}")
                
                # Check what interests this program matches
                medicine_match = any(tag in ['mbbs', 'doctor', 'medicine', 'medical'] for tag in tags) and not any(tag in ['nursing', 'pharmacy'] for tag in tags)
                cs_match = any(tag in ['computer science', 'software engineering'] for tag in tags)
                
                print(f"   Matches Medicine: {medicine_match}")
                print(f"   Matches CS: {cs_match}")
                
                if medicine_match:
                    print(f"   → Should get Priority 1 score")
                elif cs_match:
                    print(f"   → Should get Priority 2 score")
                else:
                    print(f"   → No priority match")
                    
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    print("🧪 PRIORITY LOGIC ANALYSIS")
    print("=" * 60)
    
    # Test with user's exact payload
    test_user_priority_payload()
    
    # Test priority order logic
    test_priority_order()
    
    # Debug priority logic
    test_debug_priority_logic()
    
    print("\n🎉 Analysis Complete!")
    print("=" * 60) 
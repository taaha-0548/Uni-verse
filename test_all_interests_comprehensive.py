#!/usr/bin/env python3
"""
Comprehensive test for all interests and student backgrounds
Tests the priority ranking logic for different student groups and their interests
"""

import requests
import json

def test_pre_medical_student():
    """Test Pre-Medical student with Medicine priority"""
    print("🧪 Testing Pre-Medical Student (Medicine Priority)")
    print("=" * 60)
    
    test_data = {
        "sscPercentage": 90,
        "hscPercentage": 90,
        "hscGroup": "Pre-Medical",
        "interests": ["Medicine", "Pharmacy", "Computer Science"],
        "interestPriorities": [
            {"interest": "Medicine", "priority": 1},
            {"interest": "Pharmacy", "priority": 2},
            {"interest": "Computer Science", "priority": 3}
        ],
        "budget": 1000000,
        "preferredLocation": "Karachi"
    }
    
    try:
        response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
        if response.status_code == 200:
            data = response.json()
            offerings = data.get('matched_offerings', [])
            print(f"✅ Found {len(offerings)} matched offerings")
            
            print("\n📊 Top 10 programs (should show Medicine first):")
            for i, offering in enumerate(offerings[:10], 1):
                program_name = offering['program_name']
                match_score = offering['match_score']
                tags = offering.get('tags', [])
                
                # Categorize the program
                if any(tag in ['mbbs', 'doctor'] for tag in tags):
                    category = "✅ CORE MEDICINE (MBBS)"
                elif any(tag in ['medicine', 'medical'] for tag in tags) and not any(tag in ['nursing', 'pharmacy', 'allied-health'] for tag in tags):
                    category = "✅ CORE MEDICINE"
                elif any(tag in ['nursing'] for tag in tags):
                    category = "⚠️  NURSING (allied health)"
                elif any(tag in ['pharmacy'] for tag in tags):
                    category = "⚠️  PHARMACY (allied health)"
                elif any(tag in ['computer science', 'software engineering'] for tag in tags):
                    category = "💻 COMPUTER SCIENCE"
                else:
                    category = "📚 OTHER"
                
                print(f"{i}. {program_name}")
                print(f"   Match Score: {match_score}")
                print(f"   Tags: {', '.join(tags)}")
                print(f"   {category}")
                print()
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

def test_pre_engineering_student():
    """Test Pre-Engineering student with Engineering priority"""
    print("\n🧪 Testing Pre-Engineering Student (Engineering Priority)")
    print("=" * 60)
    
    test_data = {
        "sscPercentage": 85,
        "hscPercentage": 85,
        "hscGroup": "Pre-Engineering",
        "interests": ["Engineering", "Computer Science", "Business"],
        "interestPriorities": [
            {"interest": "Engineering", "priority": 1},
            {"interest": "Computer Science", "priority": 2},
            {"interest": "Business", "priority": 3}
        ],
        "budget": 1000000,
        "preferredLocation": "Lahore"
    }
    
    try:
        response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
        if response.status_code == 200:
            data = response.json()
            offerings = data.get('matched_offerings', [])
            print(f"✅ Found {len(offerings)} matched offerings")
            
            print("\n📊 Top 10 programs (should show Engineering first):")
            for i, offering in enumerate(offerings[:10], 1):
                program_name = offering['program_name']
                match_score = offering['match_score']
                tags = offering.get('tags', [])
                
                # Categorize the program
                if any(tag in ['civil', 'electrical', 'mechanical', 'chemical'] for tag in tags):
                    category = "✅ CORE ENGINEERING"
                elif any(tag in ['engineering'] for tag in tags) and not any(tag in ['technology', 'information technology'] for tag in tags):
                    category = "✅ ENGINEERING"
                elif any(tag in ['computer science', 'software engineering'] for tag in tags):
                    category = "💻 COMPUTER SCIENCE"
                elif any(tag in ['business administration', 'finance', 'accounting'] for tag in tags):
                    category = "💼 BUSINESS"
                elif any(tag in ['technology', 'information technology'] for tag in tags):
                    category = "⚠️  TECHNOLOGY (not core engineering)"
                else:
                    category = "📚 OTHER"
                
                print(f"{i}. {program_name}")
                print(f"   Match Score: {match_score}")
                print(f"   Tags: {', '.join(tags)}")
                print(f"   {category}")
                print()
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

def test_ics_student():
    """Test ICS student with Computer Science priority"""
    print("\n🧪 Testing ICS Student (Computer Science Priority)")
    print("=" * 60)
    
    test_data = {
        "sscPercentage": 80,
        "hscPercentage": 80,
        "hscGroup": "ICS (Computer Science)",
        "interests": ["Computer Science", "Engineering", "Business"],
        "interestPriorities": [
            {"interest": "Computer Science", "priority": 1},
            {"interest": "Engineering", "priority": 2},
            {"interest": "Business", "priority": 3}
        ],
        "budget": 800000,
        "preferredLocation": "Islamabad"
    }
    
    try:
        response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
        if response.status_code == 200:
            data = response.json()
            offerings = data.get('matched_offerings', [])
            print(f"✅ Found {len(offerings)} matched offerings")
            
            print("\n📊 Top 10 programs (should show Computer Science first):")
            for i, offering in enumerate(offerings[:10], 1):
                program_name = offering['program_name']
                match_score = offering['match_score']
                tags = offering.get('tags', [])
                
                # Categorize the program
                if any(tag in ['computer science', 'software engineering'] for tag in tags):
                    category = "✅ CORE COMPUTER SCIENCE"
                elif any(tag in ['computer'] for tag in tags) and not any(tag in ['information technology', 'it'] for tag in tags):
                    category = "✅ COMPUTER SCIENCE"
                elif any(tag in ['engineering'] for tag in tags):
                    category = "🔧 ENGINEERING"
                elif any(tag in ['business'] for tag in tags):
                    category = "💼 BUSINESS"
                elif any(tag in ['information technology', 'it'] for tag in tags):
                    category = "⚠️  IT (not core CS)"
                else:
                    category = "📚 OTHER"
                
                print(f"{i}. {program_name}")
                print(f"   Match Score: {match_score}")
                print(f"   Tags: {', '.join(tags)}")
                print(f"   {category}")
                print()
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

def test_icom_student():
    """Test ICom student with Business priority"""
    print("\n🧪 Testing ICom Student (Business Priority)")
    print("=" * 60)
    
    test_data = {
        "sscPercentage": 75,
        "hscPercentage": 75,
        "hscGroup": "ICom (Commerce)",
        "interests": ["Business", "Arts", "Law"],
        "interestPriorities": [
            {"interest": "Business", "priority": 1},
            {"interest": "Arts", "priority": 2},
            {"interest": "Law", "priority": 3}
        ],
        "budget": 600000,
        "preferredLocation": "Karachi"
    }
    
    try:
        response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
        if response.status_code == 200:
            data = response.json()
            offerings = data.get('matched_offerings', [])
            print(f"✅ Found {len(offerings)} matched offerings")
            
            print("\n📊 Top 10 programs (should show Business first):")
            for i, offering in enumerate(offerings[:10], 1):
                program_name = offering['program_name']
                match_score = offering['match_score']
                tags = offering.get('tags', [])
                
                # Categorize the program
                if any(tag in ['business administration', 'finance', 'accounting'] for tag in tags):
                    category = "✅ CORE BUSINESS"
                elif any(tag in ['business'] for tag in tags) and not any(tag in ['management', 'administration'] for tag in tags):
                    category = "✅ BUSINESS"
                elif any(tag in ['arts', 'fine arts'] for tag in tags):
                    category = "🎨 ARTS"
                elif any(tag in ['law', 'legal'] for tag in tags):
                    category = "⚖️  LAW"
                elif any(tag in ['management', 'administration'] for tag in tags):
                    category = "⚠️  MANAGEMENT (not core business)"
                else:
                    category = "📚 OTHER"
                
                print(f"{i}. {program_name}")
                print(f"   Match Score: {match_score}")
                print(f"   Tags: {', '.join(tags)}")
                print(f"   {category}")
                print()
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

def test_ia_student():
    """Test IA student with Arts priority"""
    print("\n🧪 Testing IA Student (Arts Priority)")
    print("=" * 60)
    
    test_data = {
        "sscPercentage": 70,
        "hscPercentage": 70,
        "hscGroup": "IA (Arts)",
        "interests": ["Arts", "Law", "Business"],
        "interestPriorities": [
            {"interest": "Arts", "priority": 1},
            {"interest": "Law", "priority": 2},
            {"interest": "Business", "priority": 3}
        ],
        "budget": 500000,
        "preferredLocation": "Lahore"
    }
    
    try:
        response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
        if response.status_code == 200:
            data = response.json()
            offerings = data.get('matched_offerings', [])
            print(f"✅ Found {len(offerings)} matched offerings")
            
            print("\n📊 Top 10 programs (should show Arts first):")
            for i, offering in enumerate(offerings[:10], 1):
                program_name = offering['program_name']
                match_score = offering['match_score']
                tags = offering.get('tags', [])
                
                # Categorize the program
                if any(tag in ['fine arts', 'visual arts', 'performing arts'] for tag in tags):
                    category = "✅ CORE ARTS"
                elif any(tag in ['arts'] for tag in tags) and not any(tag in ['humanities', 'liberal arts'] for tag in tags):
                    category = "✅ ARTS"
                elif any(tag in ['law', 'legal'] for tag in tags):
                    category = "⚖️  LAW"
                elif any(tag in ['business'] for tag in tags):
                    category = "💼 BUSINESS"
                elif any(tag in ['humanities', 'liberal arts'] for tag in tags):
                    category = "⚠️  HUMANITIES (not core arts)"
                else:
                    category = "📚 OTHER"
                
                print(f"{i}. {program_name}")
                print(f"   Match Score: {match_score}")
                print(f"   Tags: {', '.join(tags)}")
                print(f"   {category}")
                print()
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    print("🧪 COMPREHENSIVE INTEREST PRIORITY TESTING")
    print("=" * 60)
    
    # Test all student backgrounds
    test_pre_medical_student()
    test_pre_engineering_student()
    test_ics_student()
    test_icom_student()
    test_ia_student()
    
    print("\n🎉 Testing Complete!")
    print("=" * 60) 
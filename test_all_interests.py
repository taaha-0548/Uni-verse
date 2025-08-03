import requests
import json

def test_pre_medical_student():
    """Test Pre-Medical student with Medicine priority"""
    test_data = {
        "sscPercentage": "90",
        "hscPercentage": "90", 
        "qualificationType": "HSC/A-Level",
        "hscGroup": "Pre-Medical",
        "budget": "10000000000",
        "preferredLocation": "Karachi",
        "interests": ["Medicine", "Pharmacy", "Computer Science"],
        "interestPriorities": [
            {"interest": "Medicine", "priority": 1},
            {"interest": "Pharmacy", "priority": 2},
            {"interest": "Computer Science", "priority": 3}
        ]
    }
    
    response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
    if response.status_code == 200:
        result = response.json()
        print("✅ Pre-Medical Student Test:")
        print(f"Found {len(result['matched_offerings'])} matched offerings")
        
        # Show top 10 results
        print("\n📊 Top 10 programs (should show Medicine first):")
        for i, offering in enumerate(result['matched_offerings'][:10]):
            program_tags = [tag.lower() for tag in offering['tags']]
            has_mbbs = any(tag in ['mbbs', 'doctor'] for tag in program_tags)
            has_pharmacy = any(tag in ['pharmacy'] for tag in program_tags)
            has_cs = any(tag in ['computer science', 'software engineering'] for tag in program_tags)
            
            if has_mbbs:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} ✅ MBBS")
            elif has_pharmacy:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} 💊 Pharmacy")
            elif has_cs:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} 💻 CS")
            else:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} ℹ️ Other")
        print()

def test_pre_engineering_student():
    """Test Pre-Engineering student with Engineering priority"""
    test_data = {
        "sscPercentage": "85",
        "hscPercentage": "85", 
        "qualificationType": "HSC/A-Level",
        "hscGroup": "Pre-Engineering",
        "budget": "8000000",
        "preferredLocation": "Lahore",
        "interests": ["Engineering", "Computer Science", "Technology"],
        "interestPriorities": [
            {"interest": "Engineering", "priority": 1},
            {"interest": "Computer Science", "priority": 2},
            {"interest": "Technology", "priority": 3}
        ]
    }
    
    response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
    if response.status_code == 200:
        result = response.json()
        print("✅ Pre-Engineering Student Test:")
        print(f"Found {len(result['matched_offerings'])} matched offerings")
        
        # Show top 10 results
        print("\n📊 Top 10 programs (should show Engineering first):")
        for i, offering in enumerate(result['matched_offerings'][:10]):
            program_tags = [tag.lower() for tag in offering['tags']]
            has_core_eng = any(tag in ['civil', 'electrical', 'mechanical', 'chemical'] for tag in program_tags)
            has_cs = any(tag in ['computer science', 'software engineering'] for tag in program_tags)
            has_tech = any(tag in ['technology', 'information technology'] for tag in program_tags)
            
            if has_core_eng:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} 🔧 Core Engineering")
            elif has_cs:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} 💻 CS")
            elif has_tech:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} ⚡ Technology")
            else:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} ℹ️ Other")
        print()

def test_ics_student():
    """Test ICS student with Computer Science priority"""
    test_data = {
        "sscPercentage": "80",
        "hscPercentage": "80", 
        "qualificationType": "HSC/A-Level",
        "hscGroup": "ICS (Computer Science)",
        "budget": "6000000",
        "preferredLocation": "Islamabad",
        "interests": ["Computer Science", "Software Engineering", "Information Technology"],
        "interestPriorities": [
            {"interest": "Computer Science", "priority": 1},
            {"interest": "Software Engineering", "priority": 2},
            {"interest": "Information Technology", "priority": 3}
        ]
    }
    
    response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
    if response.status_code == 200:
        result = response.json()
        print("✅ ICS Student Test:")
        print(f"Found {len(result['matched_offerings'])} matched offerings")
        
        # Show top 10 results
        print("\n📊 Top 10 programs (should show CS first):")
        for i, offering in enumerate(result['matched_offerings'][:10]):
            program_tags = [tag.lower() for tag in offering['tags']]
            has_core_cs = any(tag in ['computer science', 'software engineering'] for tag in program_tags)
            has_it = any(tag in ['information technology', 'web development'] for tag in program_tags)
            
            if has_core_cs:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} 💻 Core CS")
            elif has_it:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} ⚡ IT")
            else:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} ℹ️ Other")
        print()

def test_icom_student():
    """Test ICom student with Business priority"""
    test_data = {
        "sscPercentage": "75",
        "hscPercentage": "75", 
        "qualificationType": "HSC/A-Level",
        "hscGroup": "ICom (Commerce)",
        "budget": "5000000",
        "preferredLocation": "Karachi",
        "interests": ["Business", "Commerce", "Economics"],
        "interestPriorities": [
            {"interest": "Business", "priority": 1},
            {"interest": "Commerce", "priority": 2},
            {"interest": "Economics", "priority": 3}
        ]
    }
    
    response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
    if response.status_code == 200:
        result = response.json()
        print("✅ ICom Student Test:")
        print(f"Found {len(result['matched_offerings'])} matched offerings")
        
        # Show top 10 results
        print("\n📊 Top 10 programs (should show Business first):")
        for i, offering in enumerate(result['matched_offerings'][:10]):
            program_tags = [tag.lower() for tag in offering['tags']]
            has_business = any(tag in ['business', 'management', 'finance'] for tag in program_tags)
            has_commerce = any(tag in ['commerce', 'accounting'] for tag in program_tags)
            has_economics = any(tag in ['economics'] for tag in program_tags)
            
            if has_business:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} 💼 Business")
            elif has_commerce:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} 📊 Commerce")
            elif has_economics:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} 📈 Economics")
            else:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} ℹ️ Other")
        print()

def test_ia_student():
    """Test IA student with Arts priority"""
    test_data = {
        "sscPercentage": "70",
        "hscPercentage": "70", 
        "qualificationType": "HSC/A-Level",
        "hscGroup": "IA (Arts)",
        "budget": "4000000",
        "preferredLocation": "Lahore",
        "interests": ["Arts", "Literature", "Psychology"],
        "interestPriorities": [
            {"interest": "Arts", "priority": 1},
            {"interest": "Literature", "priority": 2},
            {"interest": "Psychology", "priority": 3}
        ]
    }
    
    response = requests.post('http://localhost:5000/api/match-programs', json=test_data)
    if response.status_code == 200:
        result = response.json()
        print("✅ IA Student Test:")
        print(f"Found {len(result['matched_offerings'])} matched offerings")
        
        # Show top 10 results
        print("\n📊 Top 10 programs (should show Arts first):")
        for i, offering in enumerate(result['matched_offerings'][:10]):
            program_tags = [tag.lower() for tag in offering['tags']]
            has_arts = any(tag in ['arts', 'literature', 'philosophy'] for tag in program_tags)
            has_psychology = any(tag in ['psychology'] for tag in program_tags)
            has_humanities = any(tag in ['humanities', 'social sciences'] for tag in program_tags)
            
            if has_arts:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} 🎨 Arts")
            elif has_psychology:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} 🧠 Psychology")
            elif has_humanities:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} 📚 Humanities")
            else:
                print(f"{i+1}. {offering['program_name']} - {offering['university']['name']} ℹ️ Other")
        print()

if __name__ == "__main__":
    print("🧪 Testing All Student Backgrounds and Interests...")
    print("=" * 60)
    
    test_pre_medical_student()
    print("-" * 40)
    test_pre_engineering_student()
    print("-" * 40)
    test_ics_student()
    print("-" * 40)
    test_icom_student()
    print("-" * 40)
    test_ia_student() 
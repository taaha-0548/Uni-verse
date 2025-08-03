import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    print("Error: DATABASE_URL environment variable is required.")
    sys.exit(1)

engine = create_engine(DATABASE_URL)

def add_tags():
    """Add specific tags to programs to improve priority-based sorting"""
    
    # Define tag mappings for different program types
    tag_mappings = {
        # Medical programs - most specific tags first
        'MBBS': ['medicine', 'medical', 'doctor', 'mbbs'],
        'BDS': ['dentistry', 'dental', 'medicine'],
        'DVM': ['veterinary', 'animal', 'medicine'],
        
        # Allied health programs
        'BS Nursing': ['nursing', 'allied-health', 'medicine'],
        'BS Medical Technology': ['medical-technology', 'allied-health', 'medicine'],
        'BS Pharmacy': ['pharmacy', 'allied-health', 'medicine'],
        'BS Physiotherapy': ['physiotherapy', 'allied-health', 'medicine'],
        'BS Medical Laboratory': ['medical-laboratory', 'allied-health', 'medicine'],
        
        # Engineering programs
        'Civil Engineering': ['engineering', 'civil', 'construction'],
        'Electrical Engineering': ['engineering', 'electrical', 'electronics'],
        'Mechanical Engineering': ['engineering', 'mechanical', 'manufacturing'],
        'Chemical Engineering': ['engineering', 'chemical', 'process'],
        'Software Engineering': ['engineering', 'software', 'computer-science'],
        'Computer Engineering': ['engineering', 'computer', 'electronics'],
        
        # Computer Science programs
        'Computer Science': ['computer-science', 'programming', 'technology'],
        'Information Technology': ['information-technology', 'computer-science', 'technology'],
        'Data Science': ['data-science', 'computer-science', 'analytics'],
        'Artificial Intelligence': ['artificial-intelligence', 'computer-science', 'technology'],
        'Cybersecurity': ['cybersecurity', 'computer-science', 'security'],
        
        # Business programs
        'Business Administration': ['business', 'management', 'administration'],
        'Commerce': ['commerce', 'business', 'economics'],
        'Economics': ['economics', 'business', 'social-sciences'],
        'Finance': ['finance', 'business', 'banking'],
        'Accounting': ['accounting', 'business', 'finance'],
        'Marketing': ['marketing', 'business', 'advertising'],
        
        # Arts and Humanities
        'English Literature': ['literature', 'humanities', 'arts'],
        'History': ['history', 'humanities', 'arts'],
        'Philosophy': ['philosophy', 'humanities', 'arts'],
        'Psychology': ['psychology', 'social-sciences', 'humanities'],
        'Sociology': ['sociology', 'social-sciences', 'humanities'],
        'Political Science': ['political-science', 'social-sciences', 'humanities'],
    }
    
    with engine.connect() as conn:
        # First, let's see what programs exist
        result = conn.execute(text("""
            SELECT DISTINCT p.id, p.name, p.code
            FROM programs p
            ORDER BY p.name
        """))
        
        programs = result.fetchall()
        print(f"Found {len(programs)} programs in database")
        
        # Create tags if they don't exist
        all_tags = set()
        for tags in tag_mappings.values():
            all_tags.update(tags)
        
        for tag in all_tags:
            try:
                conn.execute(text("""
                    INSERT INTO tags (name) VALUES (:tag)
                    ON CONFLICT (name) DO NOTHING
                """), {'tag': tag})
            except Exception as e:
                print(f"Error adding tag '{tag}': {e}")
        
        conn.commit()
        print(f"Added {len(all_tags)} tags to database")
        
        # Now add tags to programs
        for program in programs:
            program_name = program.name
            program_id = program.id
            
            # Find matching tags for this program
            matched_tags = []
            for pattern, tags in tag_mappings.items():
                if pattern.lower() in program_name.lower():
                    matched_tags.extend(tags)
                    break
            
            # If no specific match, add general tags based on program name
            if not matched_tags:
                program_lower = program_name.lower()
                if any(med in program_lower for med in ['mbbs', 'medicine', 'medical']):
                    matched_tags = ['medicine', 'medical']
                elif any(eng in program_lower for eng in ['engineering', 'engineer']):
                    matched_tags = ['engineering']
                elif any(cs in program_lower for cs in ['computer', 'software', 'information']):
                    matched_tags = ['computer-science', 'technology']
                elif any(bus in program_lower for bus in ['business', 'commerce', 'economics']):
                    matched_tags = ['business', 'commerce']
                elif any(arts in program_lower for arts in ['arts', 'humanities', 'literature']):
                    matched_tags = ['humanities', 'arts']
            
            # Add tags to program offerings
            if matched_tags:
                # Get tag IDs
                tag_ids = []
                for tag in matched_tags:
                    result = conn.execute(text("SELECT id FROM tags WHERE name = :tag"), {'tag': tag})
                    tag_row = result.fetchone()
                    if tag_row:
                        tag_ids.append(tag_row.id)
                
                # Get all offerings for this program
                result = conn.execute(text("""
                    SELECT po.id FROM program_offerings po 
                    WHERE po.program_id = :program_id
                """), {'program_id': program_id})
                
                offerings = result.fetchall()
                
                # Add tags to each offering
                for offering in offerings:
                    offering_id = offering.id
                    for tag_id in tag_ids:
                        try:
                            conn.execute(text("""
                                INSERT INTO program_offering_tags (offering_id, tag_id) 
                                VALUES (:offering_id, :tag_id)
                                ON CONFLICT (offering_id, tag_id) DO NOTHING
                            """), {'offering_id': offering_id, 'tag_id': tag_id})
                        except Exception as e:
                            print(f"Error adding tag to offering {offering_id}: {e}")
                
                print(f"Added tags {matched_tags} to {program_name} ({len(offerings)} offerings)")
        
        conn.commit()
        print("Tag seeding completed!")

if __name__ == "__main__":
    add_tags() 
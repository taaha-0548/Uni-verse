from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from backend.models import db, University, Campus, Program, ProgramOffering, ProgramOfferingBoard, ProgramOfferingGroup, ProgramOfferingTest, ProgramOfferingTag, Tag, EntranceTestType
import datetime
import os
from dotenv import load_dotenv
from sqlalchemy import text

DIST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
app = Flask(__name__, static_folder=DIST_DIR, static_url_path="")
# Load environment variables

load_dotenv()

app = Flask(__name__)

# Database configuration from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required. Please check your .env file.")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# PostgreSQL optimizations
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_size': 10,
    'max_overflow': 20
}

CORS(app)
db.init_app(app)

@app.route('/')
def home():
    return jsonify({
        "message": "Uni-verse API is running!",
        "endpoints": {
            "match_programs": "/api/match-programs",
            "universities": "/api/universities", 
            "programs": "/api/programs",
            "campuses": "/api/campuses",
            "program_offerings": "/api/program-offerings",
            "program_detail": "/api/program/<id>",
            "university_detail": "/api/university/<id>",
            "search_programs": "/api/search-programs",
            "stats": "/api/stats"
        }
    })

@app.route('/api/match-programs', methods=['POST'])
def match_programs():
    """Match student profile with available program offerings"""
    try:
        data = request.get_json()
        
        # Extract student data
        ssc_percentage = float(data.get('sscPercentage', 0))
        hsc_percentage = float(data.get('hscPercentage', 0))
        hsc_group = data.get('hscGroup', '')
        interests = data.get('interests', [])
        budget = int(data.get('budget', 0))
        preferred_location = data.get('preferredLocation', '')
        
        # Define subject group restrictions based on official NED prospectus criteria
        subject_restrictions = {
            'Pre-Engineering': [
                # Pre-Engineering: Eligible for ALL programs (most versatile group)
                # According to prospectus: Eligible for all disciplines available within their academic group
                'architecture', 'artificial-intelligence', 'biomedical-engineering',
                'chemical-engineering', 'chemistry', 'civil-engineering', 
                'computational-finance', 'computer-science', 'computer-systems',
                'cyber-security', 'data-science', 'development-studies', 'economics',
                'electrical-engineering', 'electronic-engineering', 'engineering',
                'english-linguistics', 'finance', 'food-engineering', 'gaming-animation',
                'ics', 'industrial-manufacturing', 'management-sciences', 
                'materials-engineering', 'mechanical-engineering', 'metallurgical-engineering',
                'petrochemical-engineering', 'petroleum-engineering', 'physics',
                'polymer-engineering', 'software-engineering', 'telecommunications',
                'textile-sciences'
            ],
            'ICS (Computer Science)': [
                # ICS: Eligible for BS programs + Computer Science + Architecture (NO Engineering)
                # According to prospectus: NOT eligible for Engineering programs
                'architecture', 'artificial-intelligence', 'computer-science', 'computer-systems',
                'cyber-security', 'data-science', 'chemistry', 'computational-finance',
                'development-studies', 'economics', 'english-linguistics', 'finance',
                'gaming-animation', 'ics', 'management-sciences', 'physics',
                'software-engineering', 'telecommunications', 'textile-sciences'
            ],
            'Pre-Medical': [
                # Pre-Medical: Eligible for BS programs + Biomedical Engineering only
                # According to prospectus: NOT eligible for other Engineering, CS, or Management Sciences
                'biomedical-engineering', 'chemistry', 'computational-finance', 'development-studies',
                'economics', 'english-linguistics', 'finance', 'physics'
            ],
            'ICom (Commerce)': [
                # Commerce: Eligible for Management Sciences, Economics & Finance, English Linguistics, Development Studies
                # According to prospectus: NOT eligible for Engineering, CS, Computational Finance, or Physics
                'development-studies', 'economics', 'english-linguistics', 'finance', 'management-sciences'
            ],
            'IA (Arts)': [
                # Arts: Eligible for Management Sciences, Economics & Finance, English Linguistics, Development Studies
                # According to prospectus: NOT eligible for Engineering, CS, Computational Finance, or Physics
                'development-studies', 'economics', 'english-linguistics', 'finance', 'management-sciences'
            ]
        }
        
        # Get allowed interests based on HSC group
        allowed_interests = subject_restrictions.get(hsc_group, [])
        
        # Filter interests to only include allowed ones
        filtered_interests = [interest for interest in interests if interest in allowed_interests]
        
        # If no interests match the student's background, use a broader approach
        if not filtered_interests and hsc_group in subject_restrictions:
            # Allow some flexibility based on group
            if hsc_group == 'Pre-Engineering':
                filtered_interests = ['computer-science', 'engineering', 'Technology']
            elif hsc_group == 'Pre-Medical':
                filtered_interests = ['Medicine', 'Health Sciences']
            elif hsc_group == 'ICS (Computer Science)':
                filtered_interests = ['computer-science', 'Technology']
            elif hsc_group == 'ICom (Commerce)':
                filtered_interests = ['Business', 'Commerce']
            elif hsc_group == 'IA (Arts)':
                filtered_interests = ['Arts', 'Humanities']
        
        # Build the complex query for program matching
        query = text("""
            SELECT DISTINCT 
                po.id as offering_id,
                p.id as program_id, p.name as program_name, p.discipline, p.code,
                u.id as university_id, u.name as university_name, u.sector,
                c.city, po.min_score_pct, po.min_score_type, po.annual_fee, po.hostel_available,
                COUNT(po.id) OVER (PARTITION BY p.id) as offering_count,
                STRING_AGG(DISTINCT t.name, ', ') as tags,
                STRING_AGG(DISTINCT pog.subject_group, ', ') as required_groups,
                STRING_AGG(DISTINCT pob.board, ', ') as accepted_boards
            FROM program_offerings po
            JOIN programs p ON po.program_id = p.id
            JOIN campuses c ON po.campus_id = c.id
            JOIN universities u ON c.university_id = u.id
            LEFT JOIN program_offering_tags pot ON po.id = pot.offering_id
            LEFT JOIN tags t ON pot.tag_id = t.id
            LEFT JOIN program_offering_groups pog ON po.id = pog.offering_id
            LEFT JOIN program_offering_boards pob ON po.id = pob.offering_id
            WHERE po.min_score_pct <= :max_score
            AND po.annual_fee <= :max_fee
            GROUP BY po.id, p.id, p.name, p.discipline, p.code, u.id, u.name, u.sector, c.city, po.min_score_pct, po.min_score_type, po.annual_fee, po.hostel_available
            ORDER BY po.min_score_pct ASC, po.annual_fee ASC
        """)
        
        # Execute query with parameters
        result = db.session.execute(query, {
            'max_score': max(ssc_percentage, hsc_percentage),
            'max_fee': budget
        })
        
        matched_offerings = []
        
        for row in result:
            # Calculate match score
            score = 0
            explanations = []
            
            # Academic requirements check
            if max(ssc_percentage, hsc_percentage) >= row.min_score_pct:
                score += 30
                explanations.append(f"✅ Academic score ({max(ssc_percentage, hsc_percentage)}%) meets requirement ({row.min_score_pct}%)")
            else:
                explanations.append(f"❌ Academic score ({max(ssc_percentage, hsc_percentage)}%) below requirement ({row.min_score_pct}%)")
            
            # Subject group compatibility check (CRITICAL)
            is_compatible = False  # Initialize is_compatible variable
            
            if row.required_groups and hsc_group:
                if hsc_group in row.required_groups:
                    score += 35  # Higher weight for subject compatibility
                    explanations.append(f"✅ HSC group ({hsc_group}) matches program requirement ({row.required_groups})")
                    is_compatible = True
                else:
                    # Check if student's group is compatible with program
                    
                    # Clear compatibility rules based on user requirements
                    if hsc_group == 'Pre-Medical':
                        # Biology students can do ANY field (broadest background)
                        is_compatible = True
                    elif hsc_group == 'Pre-Engineering':
                        # Pre-Engineering students can do everything EXCEPT medical/bio programs
                        if any(med_field in row.tags.lower() if row.tags else '' for med_field in ['medicine', 'mbbs', 'dentistry', 'pharmacy', 'nursing', 'physiotherapy', 'medical technology', 'biotechnology', 'biochemistry', 'microbiology', 'public health', 'nutrition']):
                            is_compatible = False
                        else:
                            is_compatible = True
                    elif hsc_group == 'ICS (Computer Science)':
                        # CS students CANNOT do bio OR engineering programs
                        if any(med_field in row.tags.lower() if row.tags else '' for med_field in ['medicine', 'mbbs', 'dentistry', 'pharmacy', 'nursing', 'physiotherapy', 'medical technology', 'biotechnology', 'biochemistry', 'microbiology', 'public health', 'nutrition']):
                            is_compatible = False
                        elif any(eng_field in row.tags.lower() if row.tags else '' for eng_field in ['engineering', 'civil', 'electrical', 'mechanical', 'chemical', 'industrial', 'textile', 'petroleum', 'architecture']):
                            is_compatible = False
                        else:
                            # CS students can do CS, business, arts, etc.
                            is_compatible = True
                    elif hsc_group == 'ICom (Commerce)':
                        # Commerce students can only do business, arts, and some CS
                        if any(com_field in row.tags.lower() if row.tags else '' for com_field in ['business', 'commerce', 'economics', 'finance', 'accounting', 'marketing', 'management', 'banking', 'insurance', 'taxation']):
                            is_compatible = True
                        elif any(arts_field in row.tags.lower() if row.tags else '' for arts_field in ['arts', 'humanities', 'literature', 'history', 'philosophy', 'psychology', 'sociology', 'political science', 'international relations', 'media studies', 'journalism', 'education']):
                            is_compatible = True
                        elif any(cs_field in row.tags.lower() if row.tags else '' for cs_field in ['computer', 'software', 'information technology', 'web development', 'game development', 'mobile development']):
                            is_compatible = True
                        else:
                            is_compatible = False
                    elif hsc_group == 'IA (Arts)':
                        # Arts students can only do business, arts, and some CS
                        if any(arts_field in row.tags.lower() if row.tags else '' for arts_field in ['arts', 'humanities', 'literature', 'history', 'philosophy', 'psychology', 'sociology', 'political science', 'international relations', 'media studies', 'journalism', 'education']):
                            is_compatible = True
                        elif any(com_field in row.tags.lower() if row.tags else '' for com_field in ['business', 'commerce', 'economics', 'finance', 'accounting', 'marketing', 'management']):
                            is_compatible = True
                        else:
                            is_compatible = False
                    
                    if is_compatible:
                        score += 25
                        explanations.append(f"✅ HSC group ({hsc_group}) is compatible with program field")
                    else:
                        score -= 20  # Penalty for incompatible subjects
                        explanations.append(f"❌ HSC group ({hsc_group}) may not be suitable for this program")
            
            # Determine subject compatibility for frontend display
            subject_compatible = False
            if hsc_group in (row.required_groups.split(', ') if row.required_groups else []):
                subject_compatible = True
            elif is_compatible:
                subject_compatible = True
            
            # Budget check
            if budget >= row.annual_fee:
                score += 20
                explanations.append(f"✅ Budget (PKR {budget:,}) covers annual fees (PKR {row.annual_fee:,})")
            else:
                explanations.append(f"❌ Budget (PKR {budget:,}) below annual fees (PKR {row.annual_fee:,})")
            
            # Location preference
            if preferred_location and preferred_location.lower() in row.city.lower():
                score += 10
                explanations.append(f"✅ Location preference ({preferred_location}) matches campus city ({row.city})")
            
            # Interest matching (only with filtered interests)
            if row.tags and filtered_interests:
                program_tags = [tag.strip().lower() for tag in row.tags.split(',')]
                student_interests = [interest.lower() for interest in filtered_interests]
                
                interest_matches = set(program_tags) & set(student_interests)
                if interest_matches:
                    score += 25  # Increased weight for interest matching
                    explanations.append(f"✅ Interest match: {', '.join(interest_matches)}")
                else:
                    explanations.append(f"ℹ️ No direct interest match, but program may still be suitable")
            
            # Only include offerings with at least 50% match (increased threshold)
            if score >= 50:
                matched_offerings.append({
                    'offering_id': row.offering_id,
                    'program_id': row.program_id,
                    'program_name': row.program_name,
                    'discipline': row.discipline,
                    'program_code': row.code,
                    'university': {
                        'id': row.university_id,
                        'name': row.university_name,
                        'sector': row.sector
                    },
                    'campus': {
                        'city': row.city
                    },
                    'min_score_pct': row.min_score_pct,
                    'min_score_type': row.min_score_type,
                    'annual_fee': row.annual_fee,
                    'hostel_available': row.hostel_available,
                    'offering_count': row.offering_count,
                    'tags': row.tags.split(', ') if row.tags else [],
                    'required_groups': row.required_groups.split(', ') if row.required_groups else [],
                    'accepted_boards': row.accepted_boards.split(', ') if row.accepted_boards else [],
                    'match_score': score,
                    'match_explanation': explanations,
                    'subject_compatibility': subject_compatible
                })
        
        # Sort by match score (highest first), but prioritize programs with higher requirements when student is eligible
        # AND prioritize programs that match student's interests based on priority ranking
        def sort_key(offering):
            # Get student's academic score
            student_score = max(ssc_percentage, hsc_percentage)
            
            # Calculate priority-weighted interest match with SPECIFIC matching
            priority_score = 0
            if offering['tags'] and filtered_interests:
                program_tags = [tag.lower() for tag in offering['tags']]
                
                # Check if we have priority data from the frontend
                if 'interestPriorities' in data:
                    # Use priority-based scoring with SPECIFIC matching
                    highest_priority_score = 0
                    for priority_item in data['interestPriorities']:
                        interest = priority_item['interest'].lower()
                        priority = priority_item['priority']
                        
                        # CATEGORIZED INTEREST MATCHING LOGIC
                        matched = False
                        
                        # Define interest categories with their core and exclusion tags
                        interest_categories = {
                            'medicine': {
                                'core_tags': ['mbbs', 'doctor'],
                                'general_tags': ['medicine', 'medical'],
                                'exclusion_tags': ['nursing', 'pharmacy', 'allied-health'],
                                'boost_tags': ['mbbs', 'doctor']
                            },
                            'nursing': {
                                'core_tags': ['nursing'],
                                'general_tags': [],
                                'exclusion_tags': [],
                                'boost_tags': ['nursing']
                            },
                            'pharmacy': {
                                'core_tags': ['pharmacy'],
                                'general_tags': [],
                                'exclusion_tags': [],
                                'boost_tags': ['pharmacy']
                            },
                            'dentistry': {
                                'core_tags': ['dentistry', 'dental'],
                                'general_tags': [],
                                'exclusion_tags': [],
                                'boost_tags': ['dentistry', 'dental']
                            },
                            'engineering': {
                                'core_tags': ['civil', 'electrical', 'mechanical', 'chemical', 'aerospace', 'industrial', 'computer engineering', 'civil-engineering', 'electrical-engineering', 'mechanical-engineering', 'chemical-engineering', 'engineering'],
                                'general_tags': ['engineering', 'computer'],
                                'exclusion_tags': ['technology', 'information technology', 'it'],
                                'boost_tags': ['civil', 'electrical', 'mechanical', 'chemical', 'computer engineering', 'civil-engineering', 'electrical-engineering', 'mechanical-engineering', 'chemical-engineering', 'engineering']
                            },
                            'computer science': {
                                'core_tags': ['computer science', 'computer-science', 'software engineering', 'software-engineering', 'programming', 'software'],
                                'general_tags': ['software', 'programming', 'computer-science'],
                                'exclusion_tags': ['information technology', 'information-technology', 'it', 'information systems'],
                                'boost_tags': ['computer science', 'computer-science', 'software engineering', 'software-engineering']
                            },
                            'business': {
                                'core_tags': ['business administration', 'finance', 'accounting', 'marketing', 'economics'],
                                'general_tags': ['business'],
                                'exclusion_tags': ['management', 'administration'],
                                'boost_tags': ['business administration', 'finance', 'accounting']
                            },
                            'commerce': {
                                'core_tags': ['commerce', 'business administration'],
                                'general_tags': ['business', 'economics', 'finance', 'accounting'],
                                'exclusion_tags': [],
                                'boost_tags': ['commerce', 'business administration']
                            },
                            'economics': {
                                'core_tags': ['economics'],
                                'general_tags': ['economy'],
                                'exclusion_tags': [],
                                'boost_tags': ['economics']
                            },
                            'finance': {
                                'core_tags': ['finance', 'financial'],
                                'general_tags': ['banking'],
                                'exclusion_tags': [],
                                'boost_tags': ['finance', 'financial']
                            },
                            'accounting': {
                                'core_tags': ['accounting', 'accountancy'],
                                'general_tags': [],
                                'exclusion_tags': [],
                                'boost_tags': ['accounting', 'accountancy']
                            },
                            'marketing': {
                                'core_tags': ['marketing', 'advertising'],
                                'general_tags': ['branding'],
                                'exclusion_tags': [],
                                'boost_tags': ['marketing', 'advertising']
                            },
                            'arts': {
                                'core_tags': ['fine arts', 'visual arts', 'performing arts', 'design', 'creative'],
                                'general_tags': ['arts'],
                                'exclusion_tags': ['humanities', 'liberal arts'],
                                'boost_tags': ['fine arts', 'visual arts', 'performing arts']
                            },
                            'humanities': {
                                'core_tags': ['humanities', 'liberal arts'],
                                'general_tags': ['philosophy', 'history', 'literature'],
                                'exclusion_tags': [],
                                'boost_tags': ['humanities', 'liberal arts']
                            },
                            'literature': {
                                'core_tags': ['literature', 'english'],
                                'general_tags': ['linguistics'],
                                'exclusion_tags': [],
                                'boost_tags': ['literature', 'english']
                            },
                            'history': {
                                'core_tags': ['history'],
                                'general_tags': ['historical'],
                                'exclusion_tags': [],
                                'boost_tags': ['history']
                            },
                            'philosophy': {
                                'core_tags': ['philosophy'],
                                'general_tags': ['philosophical'],
                                'exclusion_tags': [],
                                'boost_tags': ['philosophy']
                            },
                            'psychology': {
                                'core_tags': ['psychology'],
                                'general_tags': ['psychological', 'mental health'],
                                'exclusion_tags': [],
                                'boost_tags': ['psychology']
                            },
                            'sociology': {
                                'core_tags': ['sociology'],
                                'general_tags': ['social', 'social sciences'],
                                'exclusion_tags': [],
                                'boost_tags': ['sociology']
                            },
                            'political science': {
                                'core_tags': ['political science', 'politics'],
                                'general_tags': ['international relations'],
                                'exclusion_tags': [],
                                'boost_tags': ['political science', 'politics']
                            },
                            'international relations': {
                                'core_tags': ['international relations'],
                                'general_tags': ['diplomacy', 'foreign policy'],
                                'exclusion_tags': [],
                                'boost_tags': ['international relations']
                            },
                            'media studies': {
                                'core_tags': ['media studies', 'media'],
                                'general_tags': ['communication', 'journalism'],
                                'exclusion_tags': [],
                                'boost_tags': ['media studies', 'media']
                            },
                            'journalism': {
                                'core_tags': ['journalism'],
                                'general_tags': ['media', 'communication'],
                                'exclusion_tags': [],
                                'boost_tags': ['journalism']
                            },
                            'education': {
                                'core_tags': ['education', 'teaching'],
                                'general_tags': ['pedagogy'],
                                'exclusion_tags': [],
                                'boost_tags': ['education', 'teaching']
                            },
                            'law': {
                                'core_tags': ['law', 'legal', 'jurisprudence'],
                                'general_tags': ['law'],
                                'exclusion_tags': ['legal studies', 'criminal justice'],
                                'boost_tags': ['law', 'legal']
                            },
                            'information technology': {
                                'core_tags': ['information technology', 'it'],
                                'general_tags': ['information systems'],
                                'exclusion_tags': [],
                                'boost_tags': ['information technology', 'it']
                            },
                            'data science': {
                                'core_tags': ['data science', 'data analytics', 'data-science'],
                                'general_tags': ['machine learning'],
                                'exclusion_tags': [],
                                'boost_tags': ['data science', 'data analytics', 'data-science']
                            },
                            'web development': {
                                'core_tags': ['web development', 'web'],
                                'general_tags': ['frontend', 'backend'],
                                'exclusion_tags': [],
                                'boost_tags': ['web development', 'web']
                            },
                            'game development': {
                                'core_tags': ['game development', 'gaming'],
                                'general_tags': ['game design'],
                                'exclusion_tags': [],
                                'boost_tags': ['game development', 'gaming']
                            },
                            'mobile development': {
                                'core_tags': ['mobile development', 'mobile'],
                                'general_tags': ['app development'],
                                'exclusion_tags': [],
                                'boost_tags': ['mobile development', 'mobile']
                            },
                            'banking': {
                                'core_tags': ['banking'],
                                'general_tags': ['finance', 'financial'],
                                'exclusion_tags': [],
                                'boost_tags': ['banking', 'finance']
                            },
                            'insurance': {
                                'core_tags': ['insurance'],
                                'general_tags': ['risk management'],
                                'exclusion_tags': [],
                                'boost_tags': ['insurance']
                            },
                            'taxation': {
                                'core_tags': ['taxation', 'tax'],
                                'general_tags': ['tax law'],
                                'exclusion_tags': [],
                                'boost_tags': ['taxation', 'tax']
                            },
                            'architecture': {
                                'core_tags': ['architecture'],
                                'general_tags': ['design', 'urban planning'],
                                'exclusion_tags': [],
                                'boost_tags': ['architecture']
                            },
                            'computational finance': {
                                'core_tags': ['computational-finance'],
                                'general_tags': ['finance', 'computational'],
                                'exclusion_tags': [],
                                'boost_tags': ['computational-finance']
                            },
                            'cyber security': {
                                'core_tags': ['cyber-security'],
                                'general_tags': ['security', 'cybersecurity'],
                                'exclusion_tags': [],
                                'boost_tags': ['cyber-security']
                            },
                            'ics': {
                                'core_tags': ['ics'],
                                'general_tags': ['computer', 'information'],
                                'exclusion_tags': [],
                                'boost_tags': ['ics']
                            },
                            'software engineering': {
                                'core_tags': ['software-engineering'],
                                'general_tags': ['software', 'programming'],
                                'exclusion_tags': [],
                                'boost_tags': ['software-engineering']
                            },
                            'civil engineering': {
                                'core_tags': ['civil-engineering'],
                                'general_tags': ['civil', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['civil-engineering']
                            },
                            'electrical engineering': {
                                'core_tags': ['electrical-engineering'],
                                'general_tags': ['electrical', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['electrical-engineering']
                            },
                            'mechanical engineering': {
                                'core_tags': ['mechanical-engineering'],
                                'general_tags': ['mechanical', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['mechanical-engineering']
                            },
                            'chemical engineering': {
                                'core_tags': ['chemical-engineering'],
                                'general_tags': ['chemical', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['chemical-engineering']
                            },
                            # Updated tags based on user requirements
                            'architecture': {
                                'core_tags': ['architecture'],
                                'general_tags': ['design', 'urban planning'],
                                'exclusion_tags': [],
                                'boost_tags': ['architecture']
                            },
                            'artificial-intelligence': {
                                'core_tags': ['artificial-intelligence'],
                                'general_tags': ['ai', 'machine learning'],
                                'exclusion_tags': [],
                                'boost_tags': ['artificial-intelligence']
                            },
                            'biomedical-engineering': {
                                'core_tags': ['biomedical-engineering'],
                                'general_tags': ['biomedical', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['biomedical-engineering']
                            },
                            'chemical-engineering': {
                                'core_tags': ['chemical-engineering'],
                                'general_tags': ['chemical', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['chemical-engineering']
                            },
                            'chemistry': {
                                'core_tags': ['chemistry'],
                                'general_tags': ['chemical', 'science'],
                                'exclusion_tags': [],
                                'boost_tags': ['chemistry']
                            },
                            'civil-engineering': {
                                'core_tags': ['civil-engineering'],
                                'general_tags': ['civil', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['civil-engineering']
                            },
                            'computational-finance': {
                                'core_tags': ['computational-finance'],
                                'general_tags': ['finance', 'computational'],
                                'exclusion_tags': [],
                                'boost_tags': ['computational-finance']
                            },
                            'computer-science': {
                                'core_tags': ['computer-science'],
                                'general_tags': ['programming', 'computing'],
                                'exclusion_tags': [],
                                'boost_tags': ['computer-science']
                            },
                            'computer-systems': {
                                'core_tags': ['computer-systems'],
                                'general_tags': ['systems', 'computing'],
                                'exclusion_tags': [],
                                'boost_tags': ['computer-systems']
                            },
                            'cyber-security': {
                                'core_tags': ['cyber-security'],
                                'general_tags': ['security', 'computing'],
                                'exclusion_tags': [],
                                'boost_tags': ['cyber-security']
                            },
                            'data-science': {
                                'core_tags': ['data-science'],
                                'general_tags': ['data', 'analytics'],
                                'exclusion_tags': [],
                                'boost_tags': ['data-science']
                            },
                            'development-studies': {
                                'core_tags': ['development-studies'],
                                'general_tags': ['development', 'social sciences'],
                                'exclusion_tags': [],
                                'boost_tags': ['development-studies']
                            },
                            'economics': {
                                'core_tags': ['economics'],
                                'general_tags': ['economy', 'social sciences'],
                                'exclusion_tags': [],
                                'boost_tags': ['economics']
                            },
                            'electrical-engineering': {
                                'core_tags': ['electrical-engineering'],
                                'general_tags': ['electrical', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['electrical-engineering']
                            
                            },
                            'electronic-engineering': {
                                'core_tags': ['electronic-engineering'],
                                'general_tags': ['electronic', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['electronic-engineering']
                            },
                            'engineering': {
                                'core_tags': ['engineering'],
                                'general_tags': ['engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['engineering']
                            },
                            'english-linguistics': {
                                'core_tags': ['english-linguistics'],
                                'general_tags': ['english', 'linguistics'],
                                'exclusion_tags': [],
                                'boost_tags': ['english-linguistics']
                            },
                            'finance': {
                                'core_tags': ['finance'],
                                'general_tags': ['financial', 'business'],
                                'exclusion_tags': [],
                                'boost_tags': ['finance']
                            },
                            'food-engineering': {
                                'core_tags': ['food-engineering'],
                                'general_tags': ['food', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['food-engineering']
                            },
                            'gaming-animation': {
                                'core_tags': ['gaming-animation'],
                                'general_tags': ['gaming', 'animation'],
                                'exclusion_tags': [],
                                'boost_tags': ['gaming-animation']
                            },
                            'industrial-manufacturing': {
                                'core_tags': ['industrial-manufacturing'],
                                'general_tags': ['industrial', 'manufacturing'],
                                'exclusion_tags': [],
                                'boost_tags': ['industrial-manufacturing']
                            },
                            'management-sciences': {
                                'core_tags': ['management-sciences'],
                                'general_tags': ['management', 'business'],
                                'exclusion_tags': [],
                                'boost_tags': ['management-sciences']
                            },
                            'materials-engineering': {
                                'core_tags': ['materials-engineering'],
                                'general_tags': ['materials', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['materials-engineering']
                            },
                            'mechanical-engineering': {
                                'core_tags': ['mechanical-engineering'],
                                'general_tags': ['mechanical', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['mechanical-engineering']
                            },
                            'metallurgical-engineering': {
                                'core_tags': ['metallurgical-engineering'],
                                'general_tags': ['metallurgical', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['metallurgical-engineering']
                            },
                            'petrochemical-engineering': {
                                'core_tags': ['petrochemical-engineering'],
                                'general_tags': ['petrochemical', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['petrochemical-engineering']
                            },
                            'petroleum-engineering': {
                                'core_tags': ['petroleum-engineering'],
                                'general_tags': ['petroleum', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['petroleum-engineering']
                            },
                            'physics': {
                                'core_tags': ['physics'],
                                'general_tags': ['physical sciences'],
                                'exclusion_tags': [],
                                'boost_tags': ['physics']
                            },
                            'polymer-engineering': {
                                'core_tags': ['polymer-engineering'],
                                'general_tags': ['polymer', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['polymer-engineering']
                            },
                            'software-engineering': {
                                'core_tags': ['software-engineering'],
                                'general_tags': ['software', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['software-engineering']
                            },
                            'telecommunications': {
                                'core_tags': ['telecommunications'],
                                'general_tags': ['telecom', 'communication'],
                                'exclusion_tags': [],
                                'boost_tags': ['telecommunications']
                            },
                            'textile-sciences': {
                                'core_tags': ['textile-sciences'],
                                'general_tags': ['textile', 'sciences'],
                                'exclusion_tags': [],
                                'boost_tags': ['textile-sciences']
                            },
                            'aerospace-engineering': {
                                'core_tags': ['aerospace-engineering'],
                                'general_tags': ['aerospace', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['aerospace-engineering']
                            },
                            'metallurgy': {
                                'core_tags': ['metallurgy'],
                                'general_tags': ['metals', 'materials'],
                                'exclusion_tags': [],
                                'boost_tags': ['metallurgy']
                            },
                            'environmental-engineering': {
                                'core_tags': ['environmental-engineering'],
                                'general_tags': ['environmental', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['environmental-engineering']
                            },
                            'geoinformatics': {
                                'core_tags': ['geoinformatics'],
                                'general_tags': ['geo', 'informatics'],
                                'exclusion_tags': [],
                                'boost_tags': ['geoinformatics']
                            },
                            'computer-engineering': {
                                'core_tags': ['computer-engineering'],
                                'general_tags': ['computer', 'engineering'],
                                'exclusion_tags': [],
                                'boost_tags': ['computer-engineering']
                            },
                            'mechatronics': {
                                'core_tags': ['mechatronics'],
                                'general_tags': ['mechanical', 'electronics'],
                                'exclusion_tags': [],
                                'boost_tags': ['mechatronics']
                            },
                            'information-security': {
                                'core_tags': ['information-security'],
                                'general_tags': ['security', 'information'],
                                'exclusion_tags': [],
                                'boost_tags': ['information-security']
                            },
                            'avionics': {
                                'core_tags': ['avionics'],
                                'general_tags': ['aviation', 'electronics'],
                                'exclusion_tags': [],
                                'boost_tags': ['avionics']
                            },
                            'naval-architecture': {
                                'core_tags': ['naval-architecture'],
                                'general_tags': ['naval', 'architecture'],
                                'exclusion_tags': [],
                                'boost_tags': ['naval-architecture']
                            },
                            'bioinformatics': {
                                'core_tags': ['bioinformatics'],
                                'general_tags': ['bio', 'informatics'],
                                'exclusion_tags': [],
                                'boost_tags': ['bioinformatics']
                            },
                            'business': {
                                'core_tags': ['business'],
                                'general_tags': ['management', 'commerce'],
                                'exclusion_tags': [],
                                'boost_tags': ['business']
                            },
                            'bba': {
                                'core_tags': ['bba'],
                                'general_tags': ['business', 'administration'],
                                'exclusion_tags': [],
                                'boost_tags': ['bba']
                            },
                            'accounting': {
                                'core_tags': ['accounting'],
                                'general_tags': ['finance', 'business'],
                                'exclusion_tags': [],
                                'boost_tags': ['accounting']
                            },
                            'tourism': {
                                'core_tags': ['tourism'],
                                'general_tags': ['hospitality', 'travel'],
                                'exclusion_tags': [],
                                'boost_tags': ['tourism']
                            },
                            'hospitality-management': {
                                'core_tags': ['hospitality-management'],
                                'general_tags': ['hospitality', 'management'],
                                'exclusion_tags': [],
                                'boost_tags': ['hospitality-management']
                            },
                            'social-sciences': {
                                'core_tags': ['social-sciences'],
                                'general_tags': ['social', 'sciences'],
                                'exclusion_tags': [],
                                'boost_tags': ['social-sciences']
                            },
                            'mass-communication': {
                                'core_tags': ['mass-communication'],
                                'general_tags': ['media', 'communication'],
                                'exclusion_tags': [],
                                'boost_tags': ['mass-communication']
                            },
                            'public-administration': {
                                'core_tags': ['public-administration'],
                                'general_tags': ['public', 'administration'],
                                'exclusion_tags': [],
                                'boost_tags': ['public-administration']
                            },
                            'psychology': {
                                'core_tags': ['psychology'],
                                'general_tags': ['behavioral', 'mental'],
                                'exclusion_tags': [],
                                'boost_tags': ['psychology']
                            },
                            'humanities': {
                                'core_tags': ['humanities'],
                                'general_tags': ['arts', 'culture'],
                                'exclusion_tags': [],
                                'boost_tags': ['humanities']
                            },
                            'english-literature': {
                                'core_tags': ['english-literature'],
                                'general_tags': ['english', 'literature'],
                                'exclusion_tags': [],
                                'boost_tags': ['english-literature']
                            },
                            'industrial-design': {
                                'core_tags': ['industrial-design'],
                                'general_tags': ['industrial', 'design'],
                                'exclusion_tags': [],
                                'boost_tags': ['industrial-design']
                            },
                            'natural-sciences': {
                                'core_tags': ['natural-sciences'],
                                'general_tags': ['natural', 'sciences'],
                                'exclusion_tags': [],
                                'boost_tags': ['natural-sciences']
                            },
                            'mathematics': {
                                'core_tags': ['mathematics'],
                                'general_tags': ['math', 'computation'],
                                'exclusion_tags': [],
                                'boost_tags': ['mathematics']
                            },
                            'environmental-science': {
                                'core_tags': ['environmental-science'],
                                'general_tags': ['environmental', 'science'],
                                'exclusion_tags': [],
                                'boost_tags': ['environmental-science']
                            },
                            'biotechnology': {
                                'core_tags': ['biotechnology'],
                                'general_tags': ['bio', 'technology'],
                                'exclusion_tags': [],
                                'boost_tags': ['biotechnology']
                            },
                            'food-science': {
                                'core_tags': ['food-science'],
                                'general_tags': ['food', 'science'],
                                'exclusion_tags': [],
                                'boost_tags': ['food-science']
                            },
                            'agriculture': {
                                'core_tags': ['agriculture'],
                                'general_tags': ['farming', 'crops'],
                                'exclusion_tags': [],
                                'boost_tags': ['agriculture']
                            },
                            'law': {
                                'core_tags': ['law'],
                                'general_tags': ['legal', 'justice'],
                                'exclusion_tags': [],
                                'boost_tags': ['law']
                            },
                            'llb': {
                                'core_tags': ['llb'],
                                'general_tags': ['law', 'legal'],
                                'exclusion_tags': [],
                                'boost_tags': ['llb']
                            },
                            'medicine': {
                                'core_tags': ['medicine'],
                                'general_tags': ['medical', 'healthcare'],
                                'exclusion_tags': [],
                                'boost_tags': ['medicine']
                            },
                            'mbbs': {
                                'core_tags': ['mbbs'],
                                'general_tags': ['medicine', 'medical'],
                                'exclusion_tags': [],
                                'boost_tags': ['mbbs']
                            },
                            'health-sciences': {
                                'core_tags': ['health-sciences'],
                                'general_tags': ['health', 'sciences'],
                                'exclusion_tags': [],
                                'boost_tags': ['health-sciences']
                            },
                            'nutrition': {
                                'core_tags': ['nutrition'],
                                'general_tags': ['diet', 'health'],
                                'exclusion_tags': [],
                                'boost_tags': ['nutrition']
                            },
                            'dietetics': {
                                'core_tags': ['dietetics'],
                                'general_tags': ['diet', 'nutrition'],
                                'exclusion_tags': [],
                                'boost_tags': ['dietetics']
                            }
                        }
                        
                        # UNIVERSAL MATCHING LOGIC
                        if interest.lower() in interest_categories:
                            category = interest_categories[interest.lower()]
                            
                            # Check for core tags
                            has_core = any(tag in category['core_tags'] for tag in program_tags)
                            
                            # Check for exclusion tags
                            has_exclusion = any(tag in category['exclusion_tags'] for tag in program_tags)
                            
                            # Check for general tags (only if no exclusions)
                            has_general = any(tag in category['general_tags'] for tag in program_tags) if not has_exclusion else False
                            
                            # Match if core tags found OR (general tags found AND no exclusions)
                            if has_core or has_general:
                                matched = True
                        else:
                            # Fallback for uncategorized interests
                            if interest.lower() in [tag.lower() for tag in program_tags]:
                                matched = True
                        
                        if matched:
                            # Higher priority (lower number) gets higher score
                            # Priority 1 gets 1000 points, Priority 2 gets 900 points, etc.
                            # Much higher weight to ensure interest matches rank first
                            current_score = (11 - priority) * 100
                            
                            # UNIVERSAL BOOST LOGIC using categories
                            if interest.lower() in interest_categories:
                                category = interest_categories[interest.lower()]
                                boost_tags = category.get('boost_tags', [])
                                
                                # Check if program has boost tags
                                has_boost = any(tag in boost_tags for tag in program_tags)
                                
                                if has_boost:
                                    # Medicine gets extra boost, others get standard boost
                                    boost_amount = 500 if interest.lower() == 'medicine' else 400
                                    current_score += boost_amount
                            
                            if current_score > highest_priority_score:
                                highest_priority_score = current_score
                    
                    priority_score = highest_priority_score
                else:
                    # Fallback to simple interest matching
                    student_interests = [interest.lower() for interest in filtered_interests]
                    interest_matches = set(program_tags) & set(student_interests)
                    priority_score = len(interest_matches) * 100
            
            # CRITICAL: Priority score is the ONLY primary sorting criterion
            # This ensures interest matches ALWAYS rank first, regardless of other factors
            if priority_score > 0:
                # Programs with interest matches get top priority
                return (priority_score, 0, 0)  # Only priority score matters
            else:
                # Programs without interest matches go to the bottom
                return (0, offering['match_score'], 0)
        
        matched_offerings.sort(key=sort_key, reverse=True)
        
        return jsonify({
            'success': True,
            'matched_offerings': matched_offerings,
            'total_matches': len(matched_offerings),
            'subject_restrictions': {
                'hsc_group': hsc_group,
                'allowed_interests': allowed_interests,
                'filtered_interests': filtered_interests
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/debug-match', methods=['POST'])
def debug_match():
    """Debug endpoint to analyze matching logic"""
    try:
        data = request.get_json()
        
        # Extract student data
        ssc_percentage = float(data.get('sscPercentage', 0))
        hsc_percentage = float(data.get('hscPercentage', 0))
        hsc_group = data.get('hscGroup', '')
        interests = data.get('interests', [])
        budget = int(data.get('budget', 0))
        preferred_location = data.get('preferredLocation', '')
        
        # Get a few sample programs to analyze
        query = text("""
            SELECT DISTINCT 
                po.id as offering_id,
                p.id as program_id, p.name as program_name, p.discipline, p.code,
                u.id as university_id, u.name as university_name, u.sector,
                c.city, po.min_score_pct, po.min_score_type, po.annual_fee, po.hostel_available,
                STRING_AGG(DISTINCT t.name, ', ') as tags,
                STRING_AGG(DISTINCT pog.subject_group, ', ') as required_groups
            FROM program_offerings po
            JOIN programs p ON po.program_id = p.id
            JOIN campuses c ON po.campus_id = c.id
            JOIN universities u ON c.university_id = u.id
            LEFT JOIN program_offering_tags pot ON po.id = pot.offering_id
            LEFT JOIN tags t ON pot.tag_id = t.id
            LEFT JOIN program_offering_groups pog ON po.id = pog.offering_id
            WHERE po.annual_fee <= :max_fee
            GROUP BY po.id, p.id, p.name, p.discipline, p.code, u.id, u.name, u.sector, c.city, 
                     po.min_score_pct, po.min_score_type, po.annual_fee, po.hostel_available
            LIMIT 10
        """)
        
        result = db.session.execute(query, {
            'max_fee': budget
        })
        
        debug_info = []
        
        for row in result:
            program_tags = [tag.strip().lower() for tag in row.tags.split(',')] if row.tags else []
            
            # Analyze interest matching
            interest_analysis = []
            for interest in interests:
                interest_lower = interest.lower()
                
                # Check specific matching
                if interest_lower == 'medicine':
                    medicine_matches = [tag for tag in program_tags if tag in ['medicine', 'mbbs', 'doctor']]
                    nursing_matches = [tag for tag in program_tags if tag in ['nursing']]
                    pharmacy_matches = [tag for tag in program_tags if tag in ['pharmacy']]
                    
                    interest_analysis.append({
                        'interest': interest,
                        'program_tags': program_tags,
                        'medicine_matches': medicine_matches,
                        'nursing_matches': nursing_matches,
                        'pharmacy_matches': pharmacy_matches,
                        'would_match_medicine': len(medicine_matches) > 0,
                        'would_match_nursing': len(nursing_matches) > 0,
                        'would_match_pharmacy': len(pharmacy_matches) > 0
                    })
            
            debug_info.append({
                'program_name': row.program_name,
                'university': row.university_name,
                'tags': program_tags,
                'interest_analysis': interest_analysis
            })
        
        return jsonify({
            'success': True,
            'student_data': {
                'ssc_percentage': ssc_percentage,
                'hsc_percentage': hsc_percentage,
                'hsc_group': hsc_group,
                'interests': interests,
                'budget': budget
            },
            'debug_info': debug_info
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/universities')
def get_universities():
    """Get all universities with statistics"""
    try:
        # Use raw SQL for complex statistics
        query = text("""
            SELECT u.id, u.name, u.sector, 
                   COUNT(DISTINCT c.id) as campus_count,
                   COUNT(DISTINCT po.id) as program_count
            FROM universities u
            LEFT JOIN campuses c ON u.id = c.university_id
            LEFT JOIN program_offerings po ON c.id = po.campus_id
            GROUP BY u.id, u.name, u.sector
            ORDER BY u.name
        """)
        
        result = db.session.execute(query)
        
        universities = []
        for row in result:
            universities.append({
                'id': row.id,
                'name': row.name,
                'sector': row.sector,
                'campus_count': row.campus_count,
                'program_count': row.program_count
            })
        
        return jsonify({
            'success': True,
            'universities': universities
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/programs')
def get_programs():
    """Get all programs with offering counts"""
    try:
        # Use raw SQL for program statistics
        query = text("""
            SELECT p.id, p.name, p.discipline, p.code,
                   COUNT(DISTINCT po.id) as offering_count,
                   MIN(po.annual_fee) as min_fee,
                   MAX(po.annual_fee) as max_fee,
                   AVG(po.min_score_pct) as avg_score
            FROM programs p
            LEFT JOIN program_offerings po ON p.id = po.program_id
            GROUP BY p.id, p.name, p.discipline, p.code
            ORDER BY p.name
        """)
        
        result = db.session.execute(query)
        
        programs = []
        for row in result:
            programs.append({
                'id': row.id,
                'name': row.name,
                'discipline': row.discipline,
                'code': row.code,
                'offering_count': row.offering_count,
                'min_fee': row.min_fee,
                'max_fee': row.max_fee,
                'avg_score': round(row.avg_score, 1) if row.avg_score else None
            })
        
        return jsonify({
            'success': True,
            'programs': programs
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/campuses')
def get_campuses():
    """Get all campuses with university info"""
    try:
        campuses = Campus.query.join(University).all()
        return jsonify({
            'success': True,
            'campuses': [{
                'id': campus.id,
                'city': campus.city,
                'university': {
                    'id': campus.university.id,
                    'name': campus.university.name,
                    'sector': campus.university.sector
                }
            } for campus in campuses]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/program-offerings')
def get_program_offerings():
    """Get all program offerings with details"""
    try:
        # Use raw SQL for complex join
        query = text("""
            SELECT po.id, po.min_score_pct, po.min_score_type, po.annual_fee, po.hostel_available,
                   p.id as program_id, p.name as program_name, p.discipline, p.code,
                   u.id as university_id, u.name as university_name, u.sector,
                   c.city,
                   STRING_AGG(DISTINCT t.name, ', ') as tags,
                   STRING_AGG(DISTINCT pog.subject_group, ', ') as required_groups
            FROM program_offerings po
            JOIN programs p ON po.program_id = p.id
            JOIN campuses c ON po.campus_id = c.id
            JOIN universities u ON c.university_id = u.id
            LEFT JOIN program_offering_tags pot ON po.id = pot.offering_id
            LEFT JOIN tags t ON pot.tag_id = t.id
            LEFT JOIN program_offering_groups pog ON po.id = pog.offering_id
            GROUP BY po.id, po.min_score_pct, po.min_score_type, po.annual_fee, po.hostel_available,
                     p.id, p.name, p.discipline, p.code, u.id, u.name, u.sector, c.city
            ORDER BY p.name, c.city
        """)
        
        result = db.session.execute(query)
        
        offerings = []
        for row in result:
            offerings.append({
                'id': row.id,
                'program': {
                    'id': row.program_id,
                    'name': row.program_name,
                    'discipline': row.discipline,
                    'code': row.code
                },
                'university': {
                    'id': row.university_id,
                    'name': row.university_name,
                    'sector': row.sector
                },
                'campus': {
                    'city': row.city
                },
                'min_score_pct': row.min_score_pct,
                'min_score_type': row.min_score_type,
                'annual_fee': row.annual_fee,
                'hostel_available': row.hostel_available,
                'tags': row.tags.split(', ') if row.tags else [],
                'required_groups': row.required_groups.split(', ') if row.required_groups else []
            })
        
        return jsonify({
            'success': True,
            'offerings': offerings
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/program/<int:program_id>')
def get_program_detail(program_id):
    """Get detailed program information with all offerings"""
    try:
        program = Program.query.get_or_404(program_id)
        
        # Get all offerings for this program
        offerings_query = text("""
            SELECT po.id, po.min_score_pct, po.min_score_type, po.annual_fee, po.hostel_available,
                   u.id as university_id, u.name as university_name, u.sector,
                   c.city,
                   STRING_AGG(DISTINCT t.name, ', ') as tags,
                   STRING_AGG(DISTINCT pog.subject_group, ', ') as required_groups,
                   STRING_AGG(DISTINCT pob.board, ', ') as accepted_boards
            FROM program_offerings po
            JOIN campuses c ON po.campus_id = c.id
            JOIN universities u ON c.university_id = u.id
            LEFT JOIN program_offering_tags pot ON po.id = pot.offering_id
            LEFT JOIN tags t ON pot.tag_id = t.id
            LEFT JOIN program_offering_groups pog ON po.id = pog.offering_id
            LEFT JOIN program_offering_boards pob ON po.id = pob.offering_id
            WHERE po.program_id = :program_id
            GROUP BY po.id, po.min_score_pct, po.min_score_type, po.annual_fee, po.hostel_available,
                     u.id, u.name, u.sector, c.city
        """)
        
        result = db.session.execute(offerings_query, {'program_id': program_id})
        
        offerings = []
        for row in result:
            offerings.append({
                'id': row.id,
                'university': {
                    'id': row.university_id,
                    'name': row.university_name,
                    'sector': row.sector
                },
                'campus': {
                    'city': row.city
                },
                'min_score_pct': row.min_score_pct,
                'min_score_type': row.min_score_type,
                'annual_fee': row.annual_fee,
                'hostel_available': row.hostel_available,
                'tags': row.tags.split(', ') if row.tags else [],
                'required_groups': row.required_groups.split(', ') if row.required_groups else [],
                'accepted_boards': row.accepted_boards.split(', ') if row.accepted_boards else []
            })
        
        return jsonify({
            'success': True,
            'program': {
                'id': program.id,
                'name': program.name,
                'discipline': program.discipline,
                'code': program.code,
                'offerings': offerings
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/university/<int:university_id>')
def get_university_detail(university_id):
    """Get detailed university information with campuses and offerings"""
    try:
        university = University.query.get_or_404(university_id)
        campuses = Campus.query.filter_by(university_id=university_id).all()
        
        # Get offerings for this university
        offerings_query = text("""
            SELECT po.id, po.min_score_pct, po.min_score_type, po.annual_fee, po.hostel_available,
                   p.id as program_id, p.name as program_name, p.discipline, p.code,
                   c.city,
                   STRING_AGG(DISTINCT t.name, ', ') as tags
            FROM program_offerings po
            JOIN programs p ON po.program_id = p.id
            JOIN campuses c ON po.campus_id = c.id
            LEFT JOIN program_offering_tags pot ON po.id = pot.offering_id
            LEFT JOIN tags t ON pot.tag_id = t.id
            WHERE c.university_id = :university_id
            GROUP BY po.id, po.min_score_pct, po.min_score_type, po.annual_fee, po.hostel_available,
                     p.id, p.name, p.discipline, p.code, c.city
        """)
        
        result = db.session.execute(offerings_query, {'university_id': university_id})
        
        offerings = []
        for row in result:
            offerings.append({
                'id': row.id,
                'program': {
                    'id': row.program_id,
                    'name': row.program_name,
                    'discipline': row.discipline,
                    'code': row.code
                },
                'campus': {
                    'city': row.city
                },
                'min_score_pct': row.min_score_pct,
                'min_score_type': row.min_score_type,
                'annual_fee': row.annual_fee,
                'hostel_available': row.hostel_available,
                'tags': row.tags.split(', ') if row.tags else []
            })
        
        return jsonify({
            'success': True,
            'university': {
                'id': university.id,
                'name': university.name,
                'sector': university.sector,
                'campuses': [{'id': c.id, 'city': c.city} for c in campuses],
                'offerings': offerings
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/search-programs')
def search_programs():
    """Search programs by name or discipline"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'success': False, 'error': 'Query parameter required'}), 400
        
        # Use raw SQL for search
        search_query = text("""
            SELECT DISTINCT p.id, p.name, p.discipline, p.code,
                   COUNT(DISTINCT po.id) as offering_count,
                   MIN(po.annual_fee) as min_fee,
                   MAX(po.annual_fee) as max_fee
            FROM programs p
            LEFT JOIN program_offerings po ON p.id = po.program_id
            WHERE p.name ILIKE :search_term OR p.discipline ILIKE :search_term
            GROUP BY p.id, p.name, p.discipline, p.code
            ORDER BY p.name
        """)
        
        result = db.session.execute(search_query, {'search_term': f'%{query}%'})
        
        programs = []
        for row in result:
            programs.append({
                'id': row.id,
                'name': row.name,
                'discipline': row.discipline,
                'code': row.code,
                'offering_count': row.offering_count,
                'min_fee': row.min_fee,
                'max_fee': row.max_fee
            })
        
        return jsonify({
            'success': True,
            'programs': programs,
            'query': query
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats')
def get_stats():
    """Get database statistics"""
    try:
        # Get counts using raw SQL
        stats_query = text("""
            SELECT 
                (SELECT COUNT(*) FROM universities) as university_count,
                (SELECT COUNT(*) FROM campuses) as campus_count,
                (SELECT COUNT(*) FROM programs) as program_count,
                (SELECT COUNT(*) FROM program_offerings) as offering_count,
                (SELECT COUNT(*) FROM tags) as tag_count
        """)
        
        result = db.session.execute(stats_query).fetchone()
        
        return jsonify({
            'success': True,
            'stats': {
                'universities': result.university_count,
                'campuses': result.campus_count,
                'programs': result.program_count,
                'offerings': result.offering_count,
                'tags': result.tag_count
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(DIST_DIR, path)):
        return send_from_directory(DIST_DIR, path)
    return send_from_directory(DIST_DIR, "index.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)

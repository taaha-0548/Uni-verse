from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, University, Program, ProgramTag
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:npg_tEDGZj0hFuQ6@ep-hidden-art-a12ljjgh-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&options=endpoint%3Dep-hidden-art-a12ljjgh'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
            "program_detail": "/api/program/<id>",
            "university_detail": "/api/university/<id>"
        }
    })

@app.route('/api/match-programs', methods=['POST'])
def match_programs():
    """Match student profile with available programs"""
    try:
        data = request.get_json()
        
        # Extract student data
        ssc_percentage = float(data.get('sscPercentage', 0))
        hsc_percentage = float(data.get('hscPercentage', 0))
        hsc_group = data.get('hscGroup', '')
        interests = data.get('interests', [])
        budget = int(data.get('budget', 0))
        preferred_location = data.get('preferredLocation', '')
        
        # Query programs that match basic criteria
        programs = Program.query.join(University).all()
        
        matched_programs = []
        
        for program in programs:
            # Calculate match score
            score = 0
            explanations = []
            
            # Academic requirements check
            if ssc_percentage >= program.min_ssc_pct:
                score += 20
                explanations.append(f"✅ SSC percentage ({ssc_percentage}%) meets requirement ({program.min_ssc_pct}%)")
            else:
                explanations.append(f"❌ SSC percentage ({ssc_percentage}%) below requirement ({program.min_ssc_pct}%)")
            
            if hsc_percentage >= program.min_hsc_pct:
                score += 20
                explanations.append(f"✅ HSC percentage ({hsc_percentage}%) meets requirement ({program.min_hsc_pct}%)")
            else:
                explanations.append(f"❌ HSC percentage ({hsc_percentage}%) below requirement ({program.min_hsc_pct}%)")
            
            # Group requirement check
            if hsc_group == program.required_group:
                score += 25
                explanations.append(f"✅ HSC group ({hsc_group}) matches requirement ({program.required_group})")
            else:
                explanations.append(f"❌ HSC group ({hsc_group}) doesn't match requirement ({program.required_group})")
            
            # Budget check
            if budget >= program.annual_fees:
                score += 20
                explanations.append(f"✅ Budget (PKR {budget:,}) covers annual fees (PKR {program.annual_fees:,})")
            else:
                explanations.append(f"❌ Budget (PKR {budget:,}) below annual fees (PKR {program.annual_fees:,})")
            
            # Location preference
            if preferred_location and preferred_location.lower() in program.university.city.lower():
                score += 10
                explanations.append(f"✅ Location preference ({preferred_location}) matches university city ({program.university.city})")
            
            # Interest matching
            program_tags = [tag.tag.lower() for tag in program.tags]
            student_interests = [interest.lower() for interest in interests]
            
            interest_matches = set(program_tags) & set(student_interests)
            if interest_matches:
                score += 5
                explanations.append(f"✅ Interest match: {', '.join(interest_matches)}")
            
            # Only include programs with at least 40% match
            if score >= 40:
                matched_programs.append({
                    'id': program.id,
                    'name': program.name,
                    'university': {
                        'id': program.university.id,
                        'name': program.university.name,
                        'city': program.university.city,
                        'province': program.university.province,
                        'university_type': program.university.university_type
                    },
                    'degree_type': program.degree_type,
                    'duration_years': program.duration_years,
                    'annual_fees': program.annual_fees,
                    'seats_available': program.seats_available,
                    'admission_test': program.admission_test,
                    'merit_based': program.merit_based,
                    'application_deadline': program.application_deadline.isoformat() if program.application_deadline else None,
                    'classes_start': program.classes_start.isoformat() if program.classes_start else None,
                    'match_score': score,
                    'match_explanation': explanations
                })
        
        # Sort by match score (highest first)
        matched_programs.sort(key=lambda x: x['match_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'matched_programs': matched_programs,
            'total_matches': len(matched_programs)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/universities')
def get_universities():
    """Get all universities"""
    try:
        universities = University.query.all()
        return jsonify({
            'success': True,
            'universities': [{
                'id': uni.id,
                'name': uni.name,
                'city': uni.city,
                'province': uni.province,
                'university_type': uni.university_type,
                'annual_fees': uni.annual_fees,
                'website_url': uni.website_url,
                'contact_email': uni.contact_email,
                'contact_phone': uni.contact_phone
            } for uni in universities]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/programs')
def get_programs():
    """Get all programs"""
    try:
        programs = Program.query.join(University).all()
        return jsonify({
            'success': True,
            'programs': [{
                'id': program.id,
                'name': program.name,
                'university': {
                    'id': program.university.id,
                    'name': program.university.name,
                    'city': program.university.city
                },
                'degree_type': program.degree_type,
                'duration_years': program.duration_years,
                'min_ssc_pct': program.min_ssc_pct,
                'min_hsc_pct': program.min_hsc_pct,
                'required_group': program.required_group,
                'annual_fees': program.annual_fees,
                'seats_available': program.seats_available,
                'admission_test': program.admission_test,
                'merit_based': program.merit_based,
                'application_deadline': program.application_deadline.isoformat() if program.application_deadline else None,
                'classes_start': program.classes_start.isoformat() if program.classes_start else None
            } for program in programs]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/program/<int:program_id>')
def get_program_detail(program_id):
    """Get detailed program information"""
    try:
        program = Program.query.get_or_404(program_id)
        return jsonify({
            'success': True,
            'program': {
                'id': program.id,
                'name': program.name,
                'university': {
                    'id': program.university.id,
                    'name': program.university.name,
                    'city': program.university.city,
                    'province': program.university.province,
                    'university_type': program.university.university_type,
                    'website_url': program.university.website_url,
                    'contact_email': program.university.contact_email,
                    'contact_phone': program.university.contact_phone
                },
                'degree_type': program.degree_type,
                'duration_years': program.duration_years,
                'min_ssc_pct': program.min_ssc_pct,
                'min_hsc_pct': program.min_hsc_pct,
                'required_group': program.required_group,
                'annual_fees': program.annual_fees,
                'seats_available': program.seats_available,
                'admission_test': program.admission_test,
                'merit_based': program.merit_based,
                'application_deadline': program.application_deadline.isoformat() if program.application_deadline else None,
                'classes_start': program.classes_start.isoformat() if program.classes_start else None,
                'tags': [tag.tag for tag in program.tags]
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/university/<int:university_id>')
def get_university_detail(university_id):
    """Get detailed university information"""
    try:
        university = University.query.get_or_404(university_id)
        programs = Program.query.filter_by(uni_id=university_id).all()
        
        return jsonify({
            'success': True,
            'university': {
                'id': university.id,
                'name': university.name,
                'city': university.city,
                'province': university.province,
                'university_type': university.university_type,
                'annual_fees': university.annual_fees,
                'website_url': university.website_url,
                'contact_email': university.contact_email,
                'contact_phone': university.contact_phone,
                'programs': [{
                    'id': program.id,
                    'name': program.name,
                    'degree_type': program.degree_type,
                    'duration_years': program.duration_years,
                    'annual_fees': program.annual_fees,
                    'seats_available': program.seats_available
                } for program in programs]
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000) 
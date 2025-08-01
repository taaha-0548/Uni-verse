from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class University(db.Model):
    __tablename__ = 'universities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    university_type = db.Column(db.String(50))  # Public, Private
    annual_fees = db.Column(db.Integer, nullable=False)  # in PKR
    website_url = db.Column(db.String(500))
    contact_email = db.Column(db.String(200))
    contact_phone = db.Column(db.String(50))
    
    # Relationship
    programs = db.relationship('Program', backref='university', lazy=True)
    
    def __repr__(self):
        return f'<University {self.name}>'

class Program(db.Model):
    __tablename__ = 'programs'
    
    id = db.Column(db.Integer, primary_key=True)
    uni_id = db.Column(db.Integer, db.ForeignKey('universities.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    degree_type = db.Column(db.String(50))  # BS, MS, PhD
    duration_years = db.Column(db.Integer, default=4)
    min_ssc_pct = db.Column(db.Float, nullable=False)
    min_hsc_pct = db.Column(db.Float, nullable=False)
    required_group = db.Column(db.String(50), nullable=False)  # Pre-Engineering, Pre-Medical, etc.
    annual_fees = db.Column(db.Integer, nullable=False)  # in PKR
    seats_available = db.Column(db.Integer)
    admission_test = db.Column(db.String(200))
    merit_based = db.Column(db.Boolean, default=True)
    application_deadline = db.Column(db.Date)
    classes_start = db.Column(db.Date)
    
    # Relationship
    tags = db.relationship('ProgramTag', backref='program', lazy=True)
    
    def __repr__(self):
        return f'<Program {self.name}>'

class ProgramTag(db.Model):
    __tablename__ = 'program_tags'
    
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    tag = db.Column(db.String(100), nullable=False)  # programming, management, etc.
    
    def __repr__(self):
        return f'<ProgramTag {self.tag}>' 
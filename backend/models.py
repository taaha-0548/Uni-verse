from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint

db = SQLAlchemy()

class University(db.Model):
    __tablename__ = 'universities'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(500), nullable=False, unique=True)
    sector = db.Column(db.String(50), nullable=False)
    
    # Check constraint for sector validation
    __table_args__ = (
        CheckConstraint("sector IN ('public', 'private', 'semi-government')", name='valid_sector'),
    )
    
    # Relationships
    campuses = db.relationship('Campus', backref='university', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<University {self.name}>'

class Campus(db.Model):
    __tablename__ = 'campuses'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id', ondelete='CASCADE'), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    
    # Unique constraint for university_id + city
    __table_args__ = (
        UniqueConstraint('university_id', 'city', name='unique_university_city'),
    )
    
    # Relationships
    program_offerings = db.relationship('ProgramOffering', backref='campus', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Campus {self.city} - {self.university.name}>'

class Program(db.Model):
    __tablename__ = 'programs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(500), nullable=False, unique=True)
    discipline = db.Column(db.String(100))
    code = db.Column(db.String(50), unique=True)
    
    # Relationships
    program_offerings = db.relationship('ProgramOffering', backref='program', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Program {self.name}>'

class ProgramOffering(db.Model):
    __tablename__ = 'program_offerings'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id', ondelete='CASCADE'), nullable=False)
    campus_id = db.Column(db.Integer, db.ForeignKey('campuses.id', ondelete='CASCADE'), nullable=False)
    min_score_pct = db.Column(db.Float, nullable=False)
    min_score_type = db.Column(db.String(20), nullable=False)
    annual_fee = db.Column(db.Integer, nullable=False)
    hostel_available = db.Column(db.Boolean, nullable=False, default=False)
    
    # Check constraints
    __table_args__ = (
        CheckConstraint("min_score_pct BETWEEN 0 AND 100", name='valid_score_percentage'),
        CheckConstraint("min_score_type IN ('ssc_hsc', 'ibcc')", name='valid_score_type'),
        CheckConstraint("annual_fee >= 0", name='valid_fee'),
    )
    
    # Relationships
    boards = db.relationship('ProgramOfferingBoard', backref='offering', lazy=True, cascade='all, delete-orphan')
    groups = db.relationship('ProgramOfferingGroup', backref='offering', lazy=True, cascade='all, delete-orphan')
    tests = db.relationship('ProgramOfferingTest', backref='offering', lazy=True, cascade='all, delete-orphan')
    tags = db.relationship('ProgramOfferingTag', backref='offering', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ProgramOffering {self.program.name} at {self.campus.city}>'

class ProgramOfferingBoard(db.Model):
    __tablename__ = 'program_offering_boards'
    
    offering_id = db.Column(db.Integer, db.ForeignKey('program_offerings.id', ondelete='CASCADE'), primary_key=True)
    board = db.Column(db.String(100), primary_key=True)
    
    def __repr__(self):
        return f'<ProgramOfferingBoard {self.board}>'

class ProgramOfferingGroup(db.Model):
    __tablename__ = 'program_offering_groups'
    
    offering_id = db.Column(db.Integer, db.ForeignKey('program_offerings.id', ondelete='CASCADE'), primary_key=True)
    subject_group = db.Column(db.String(100), primary_key=True)
    
    def __repr__(self):
        return f'<ProgramOfferingGroup {self.subject_group}>'

class EntranceTestType(db.Model):
    __tablename__ = 'entrance_test_types'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    # Relationships
    program_offering_tests = db.relationship('ProgramOfferingTest', backref='test_type', lazy=True)
    
    def __repr__(self):
        return f'<EntranceTestType {self.name}>'

class ProgramOfferingTest(db.Model):
    __tablename__ = 'program_offering_tests'
    
    offering_id = db.Column(db.Integer, db.ForeignKey('program_offerings.id', ondelete='CASCADE'), primary_key=True)
    test_type_id = db.Column(db.Integer, db.ForeignKey('entrance_test_types.id'), primary_key=True)
    min_score = db.Column(db.Float, nullable=False)
    
    __table_args__ = (
        CheckConstraint("min_score >= 0", name='valid_test_score'),
    )
    
    def __repr__(self):
        return f'<ProgramOfferingTest {self.test_type.name}>'

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    # Relationships
    program_offering_tags = db.relationship('ProgramOfferingTag', backref='tag', lazy=True)
    
    def __repr__(self):
        return f'<Tag {self.name}>'

class ProgramOfferingTag(db.Model):
    __tablename__ = 'program_offering_tags'
    
    offering_id = db.Column(db.Integer, db.ForeignKey('program_offerings.id', ondelete='CASCADE'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
    
    def __repr__(self):
        return f'<ProgramOfferingTag {self.tag.name}>' 
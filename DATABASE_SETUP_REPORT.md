# Uni-verse Database Setup Report

## Table of Contents
1. [Overview](#overview)
2. [Database Technology Stack](#database-technology-stack)
3. [Database Architecture](#database-architecture)
4. [Database Models](#database-models)
5. [Database Configuration](#database-configuration)
6. [Database Relationships](#database-relationships)
7. [Database Constraints](#database-constraints)
8. [API Integration](#api-integration)
9. [Database Statistics](#database-statistics)
10. [Setup Instructions](#setup-instructions)
11. [Security Considerations](#security-considerations)
12. [Performance Optimizations](#performance-optimizations)

## Overview

The Uni-verse platform uses a PostgreSQL database with SQLAlchemy ORM for managing university and program data. The database is designed to support a comprehensive university discovery platform that helps Pakistani students find suitable undergraduate programs.

**Current Database Statistics:**
- Universities: 72
- Campuses: 107
- Programs: 109
- Program Offerings: 2,541

## Database Technology Stack

### Core Technologies
- **Database Engine**: PostgreSQL (Neon DB for production)
- **ORM**: SQLAlchemy 2.0.21
- **Flask Integration**: Flask-SQLAlchemy 3.0.5
- **Database Driver**: psycopg2-binary 2.9.7
- **Migration Tool**: Alembic 1.12.0

### Development Dependencies
```
Flask==2.3.3
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.0.5
psycopg2-binary==2.9.7
python-dotenv==1.0.0
SQLAlchemy==2.0.21
alembic==1.12.0
pydantic==2.4.2
python-multipart==0.0.6
```

## Database Architecture

### Database Structure
The database follows a normalized relational design with the following hierarchy:

```
Universities (1) → (N) Campuses (1) → (N) Program Offerings (N) ← (1) Programs
```

### Core Entities
1. **Universities** - Main educational institutions
2. **Campuses** - Physical locations of universities
3. **Programs** - Academic programs/degrees offered
4. **Program Offerings** - Specific program offerings at specific campuses
5. **Supporting Entities** - Boards, Groups, Tests, Tags

## Database Models

### 1. University Model
```python
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
```

**Fields:**
- `id`: Primary key (auto-incrementing integer)
- `name`: University name (unique, max 500 characters)
- `sector`: University sector (public/private/semi-government)

### 2. Campus Model
```python
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
```

**Fields:**
- `id`: Primary key (auto-incrementing integer)
- `university_id`: Foreign key to universities table
- `city`: Campus city (max 100 characters)

### 3. Program Model
```python
class Program(db.Model):
    __tablename__ = 'programs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(500), nullable=False, unique=True)
    discipline = db.Column(db.String(100))
    code = db.Column(db.String(50), unique=True)
    
    # Relationships
    program_offerings = db.relationship('ProgramOffering', backref='program', lazy=True, cascade='all, delete-orphan')
```

**Fields:**
- `id`: Primary key (auto-incrementing integer)
- `name`: Program name (unique, max 500 characters)
- `discipline`: Academic discipline (max 100 characters)
- `code`: Program code (unique, max 50 characters)

### 4. ProgramOffering Model (Core Junction Table)
```python
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
```

**Fields:**
- `id`: Primary key (auto-incrementing integer)
- `program_id`: Foreign key to programs table
- `campus_id`: Foreign key to campuses table
- `min_score_pct`: Minimum required score percentage (0-100)
- `min_score_type`: Score type (ssc_hsc/ibcc)
- `annual_fee`: Annual tuition fee (non-negative integer)
- `hostel_available`: Boolean flag for hostel availability

### 5. Supporting Models

#### ProgramOfferingBoard
```python
class ProgramOfferingBoard(db.Model):
    __tablename__ = 'program_offering_boards'
    
    offering_id = db.Column(db.Integer, db.ForeignKey('program_offerings.id', ondelete='CASCADE'), primary_key=True)
    board = db.Column(db.String(100), primary_key=True)
```

#### ProgramOfferingGroup
```python
class ProgramOfferingGroup(db.Model):
    __tablename__ = 'program_offering_groups'
    
    offering_id = db.Column(db.Integer, db.ForeignKey('program_offerings.id', ondelete='CASCADE'), primary_key=True)
    subject_group = db.Column(db.String(100), primary_key=True)
```

#### EntranceTestType
```python
class EntranceTestType(db.Model):
    __tablename__ = 'entrance_test_types'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
```

#### ProgramOfferingTest
```python
class ProgramOfferingTest(db.Model):
    __tablename__ = 'program_offering_tests'
    
    offering_id = db.Column(db.Integer, db.ForeignKey('program_offerings.id', ondelete='CASCADE'), primary_key=True)
    test_type_id = db.Column(db.Integer, db.ForeignKey('entrance_test_types.id'), primary_key=True)
    min_score = db.Column(db.Float, nullable=False)
    
    __table_args__ = (
        CheckConstraint("min_score >= 0", name='valid_test_score'),
    )
```

#### Tag System
```python
class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class ProgramOfferingTag(db.Model):
    __tablename__ = 'program_offering_tags'
    
    offering_id = db.Column(db.Integer, db.ForeignKey('program_offerings.id', ondelete='CASCADE'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
```

## Database Configuration

### Environment Configuration
The database configuration is managed through environment variables:

```python
# Database configuration from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required. Please check your .env file.")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

### Environment File Structure
```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/universe_db

# For development (SQLite)
# DATABASE_URL=sqlite:///universe.db

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# CORS Origins
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### PostgreSQL Optimizations
```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_size': 10,
    'max_overflow': 20
}
```

## Database Relationships

### Primary Relationships
1. **University → Campus**: One-to-Many
   - One university can have multiple campuses
   - Cascade delete: When university is deleted, all campuses are deleted

2. **Campus → ProgramOffering**: One-to-Many
   - One campus can offer multiple programs
   - Cascade delete: When campus is deleted, all program offerings are deleted

3. **Program → ProgramOffering**: One-to-Many
   - One program can be offered at multiple campuses
   - Cascade delete: When program is deleted, all program offerings are deleted

### Junction Table Relationships
4. **ProgramOffering ↔ Supporting Entities**: Many-to-Many
   - Boards, Groups, Tests, Tags are linked to program offerings
   - Cascade delete: When program offering is deleted, all related records are deleted

## Database Constraints

### Check Constraints
1. **University Sector Validation**
   ```sql
   CONSTRAINT valid_sector CHECK (sector IN ('public', 'private', 'semi-government'))
   ```

2. **Score Percentage Validation**
   ```sql
   CONSTRAINT valid_score_percentage CHECK (min_score_pct BETWEEN 0 AND 100)
   ```

3. **Score Type Validation**
   ```sql
   CONSTRAINT valid_score_type CHECK (min_score_type IN ('ssc_hsc', 'ibcc'))
   ```

4. **Fee Validation**
   ```sql
   CONSTRAINT valid_fee CHECK (annual_fee >= 0)
   ```

5. **Test Score Validation**
   ```sql
   CONSTRAINT valid_test_score CHECK (min_score >= 0)
   ```

### Unique Constraints
1. **University Name**: Each university name must be unique
2. **Program Name**: Each program name must be unique
3. **Program Code**: Each program code must be unique
4. **University-City Combination**: Each university-city combination must be unique
5. **Tag Name**: Each tag name must be unique
6. **Test Type Name**: Each test type name must be unique

### Foreign Key Constraints
- All foreign keys use `ON DELETE CASCADE` for referential integrity
- Ensures data consistency when parent records are deleted

## API Integration

### Database Queries in API
The application uses raw SQL queries for complex operations:

1. **University List with Statistics**
   ```sql
   SELECT u.id, u.name, u.sector, 
          COUNT(DISTINCT c.id) as campus_count,
          COUNT(DISTINCT po.id) as program_count
   FROM universities u
   LEFT JOIN campuses c ON u.id = c.university_id
   LEFT JOIN program_offerings po ON c.id = po.campus_id
   GROUP BY u.id, u.name, u.sector
   ORDER BY u.name
   ```

2. **Program Matching Algorithm**
   ```sql
   SELECT DISTINCT 
       p.id as program_id, p.name as program_name, p.discipline,
       u.id as university_id, u.name as university_name, u.sector,
       c.city, po.min_score_pct, po.annual_fee, po.hostel_available,
       COUNT(po.id) OVER (PARTITION BY p.id) as offering_count
   FROM program_offerings po
   JOIN programs p ON po.program_id = p.id
   JOIN campuses c ON po.campus_id = c.id
   JOIN universities u ON c.university_id = u.id
   WHERE po.min_score_pct <= :max_score
   AND po.annual_fee <= :max_fee
   ```

### API Endpoints Using Database
1. `/api/universities` - List all universities with statistics
2. `/api/programs` - List all programs with offering counts
3. `/api/campuses` - List all campuses with university info
4. `/api/program-offerings` - List program offerings with details
5. `/api/program/<id>` - Get specific program details
6. `/api/university/<id>` - Get specific university details
7. `/api/search-programs` - Search programs by name/discipline
8. `/api/match-programs` - Match programs based on student criteria
9. `/api/stats` - Get database statistics

## Database Statistics

### Current Data Volume
- **Universities**: 72 institutions
- **Campuses**: 107 physical locations
- **Programs**: 109 unique academic programs
- **Program Offerings**: 2,541 specific program-campus combinations

### Data Distribution
- Average programs per university: ~35
- Average campuses per university: ~1.5
- Average offerings per program: ~23

## Setup Instructions

### 1. Environment Setup
```bash
# Copy environment template
cp backend/env.example backend/.env

# Edit .env file with your database credentials
# DATABASE_URL=postgresql://username:password@localhost:5432/universe_db
```

### 2. Database Creation
```bash
# Create PostgreSQL database
createdb universe_db

# Or for development (SQLite)
# The database will be created automatically in backend/instance/
```

### 3. Dependencies Installation
```bash
cd backend
pip install -r requirements.txt
```

### 4. Database Initialization
```bash
# The database tables are created automatically when the Flask app starts
# No manual migration commands are currently implemented
```

### 5. Application Startup
```bash
# Development startup
python start_dev.py

# Or individual components
python backend/run.py  # Backend only
```

## Security Considerations

### 1. Environment Variables
- Database credentials are stored in `.env` file
- `.env` file is excluded from version control
- Never commit sensitive credentials to repository

### 2. Database Security
- Use strong passwords for database access
- Implement proper user permissions
- Consider using connection pooling for production

### 3. API Security
- CORS is configured for specific origins
- Input validation is implemented at model level
- SQL injection protection through parameterized queries

## Performance Optimizations

### 1. Connection Pooling
```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_size': 10,
    'max_overflow': 20
}
```

### 2. Query Optimization
- Complex queries use raw SQL for better performance
- Indexes are created automatically on primary and foreign keys
- Lazy loading is used for relationships

### 3. Caching Strategy
- No explicit caching implemented
- Consider implementing Redis for frequently accessed data

### 4. Database Indexes
- Primary keys are automatically indexed
- Foreign keys are automatically indexed
- Unique constraints create indexes
- Consider adding indexes on frequently queried columns

## Future Enhancements

### 1. Migration System
- Implement Alembic migrations for schema changes
- Version control for database schema
- Rollback capabilities

### 2. Backup Strategy
- Implement automated database backups
- Point-in-time recovery capabilities
- Data retention policies

### 3. Monitoring
- Database performance monitoring
- Query performance analysis
- Error tracking and alerting

### 4. Scaling Considerations
- Read replicas for heavy read workloads
- Horizontal partitioning for large datasets
- Microservices architecture for complex queries

---

**Report Generated**: $(date)
**Database Version**: Current
**Last Updated**: $(date) 
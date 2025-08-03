#!/usr/bin/env python3
"""
Server Setup Test Script
Tests various aspects of the Flask server to identify timeout issues
"""

import requests
import time
import json
from app import app, db

def test_server_startup():
    """Test if server can start without issues"""
    print("="*60)
    print("TESTING SERVER STARTUP")
    print("="*60)
    
    try:
        # Test basic app import
        print("✅ App imported successfully")
        
        # Test database connection
        with app.app_context():
            result = db.session.execute("SELECT 1").fetchone()
            print("✅ Database connection successful")
        
        # Test basic route
        with app.test_client() as client:
            response = client.get('/')
            print(f"✅ Home route responds: {response.status_code}")
            
        return True
    except Exception as e:
        print(f"❌ Server startup test failed: {e}")
        return False

def test_database_performance():
    """Test database query performance"""
    print("\n" + "="*60)
    print("TESTING DATABASE PERFORMANCE")
    print("="*60)
    
    try:
        with app.app_context():
            # Test simple query
            start_time = time.time()
            result = db.session.execute("SELECT COUNT(*) FROM program_offerings").fetchone()
            simple_time = time.time() - start_time
            print(f"✅ Simple count query: {simple_time:.3f}s")
            
            # Test the actual query from match-programs
            start_time = time.time()
            query = """
                SELECT 
                    po.id as offering_id,
                    p.id as program_id, p.name as program_name, p.discipline, p.code,
                    u.id as university_id, u.name as university_name, u.sector,
                    c.city, po.min_score_pct, po.min_score_type, po.annual_fee, po.hostel_available
                FROM program_offerings po
                JOIN programs p ON po.program_id = p.id
                JOIN campuses c ON po.campus_id = c.id
                JOIN universities u ON c.university_id = u.id
                WHERE po.min_score_pct <= 80
                AND po.annual_fee <= 500000
                ORDER BY po.min_score_pct ASC, po.annual_fee ASC
                LIMIT 100
            """
            result = db.session.execute(query)
            rows = result.fetchall()
            query_time = time.time() - start_time
            print(f"✅ Match query (100 rows): {query_time:.3f}s ({len(rows)} results)")
            
            # Test with larger limit
            start_time = time.time()
            query_large = query.replace("LIMIT 100", "LIMIT 500")
            result = db.session.execute(query_large)
            rows = result.fetchall()
            large_time = time.time() - start_time
            print(f"✅ Match query (500 rows): {large_time:.3f}s ({len(rows)} results)")
            
            return True
    except Exception as e:
        print(f"❌ Database performance test failed: {e}")
        return False

def test_endpoint_performance():
    """Test endpoint performance with different timeouts"""
    print("\n" + "="*60)
    print("TESTING ENDPOINT PERFORMANCE")
    print("="*60)
    
    test_data = {
        "sscPercentage": 75,
        "hscPercentage": 80,
        "hscGroup": "Pre-Engineering",
        "interests": ["Computer Science", "Engineering"],
        "budget": 500000,
        "preferredLocation": "Karachi"
    }
    
    timeouts = [5, 10, 30, 60]
    
    for timeout in timeouts:
        try:
            print(f"\nTesting with {timeout}s timeout...")
            start_time = time.time()
            
            response = requests.post(
                'http://localhost:5000/api/match-programs',
                json=test_data,
                headers={'Content-Type': 'application/json'},
                timeout=timeout
            )
            
            elapsed = time.time() - start_time
            print(f"✅ Request completed in {elapsed:.3f}s")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Matches found: {data.get('total_matches', 0)}")
                return True
            else:
                print(f"   Error: {response.text}")
                
        except requests.exceptions.Timeout:
            print(f"❌ Request timed out after {timeout}s")
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    return False

def test_server_configuration():
    """Test server configuration settings"""
    print("\n" + "="*60)
    print("TESTING SERVER CONFIGURATION")
    print("="*60)
    
    try:
        # Check Flask configuration
        print(f"Debug mode: {app.debug}")
        print(f"Testing mode: {app.testing}")
        print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
        print(f"Engine options: {app.config['SQLALCHEMY_ENGINE_OPTIONS']}")
        
        # Check if we can create a test client
        with app.test_client() as client:
            print("✅ Test client created successfully")
            
            # Test a simple endpoint
            response = client.get('/api/stats')
            print(f"✅ Stats endpoint: {response.status_code}")
            
        return True
    except Exception as e:
        print(f"❌ Server configuration test failed: {e}")
        return False

def test_alternative_approach():
    """Test alternative approach to the match-programs endpoint"""
    print("\n" + "="*60)
    print("TESTING ALTERNATIVE APPROACH")
    print("="*60)
    
    try:
        with app.test_client() as client:
            test_data = {
                "sscPercentage": 75,
                "hscPercentage": 80,
                "hscGroup": "Pre-Engineering",
                "interests": ["Computer Science"],
                "budget": 500000,
                "preferredLocation": ""
            }
            
            print("Testing with test client (no network overhead)...")
            start_time = time.time()
            
            response = client.post(
                '/api/match-programs',
                json=test_data,
                content_type='application/json'
            )
            
            elapsed = time.time() - start_time
            print(f"✅ Test client request: {elapsed:.3f}s")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"   Matches found: {data.get('total_matches', 0)}")
                return True
            else:
                print(f"   Error: {response.get_data(as_text=True)}")
                
    except Exception as e:
        print(f"❌ Alternative approach failed: {e}")
    
    return False

def main():
    """Run all tests"""
    print("SERVER SETUP DIAGNOSTIC TESTS")
    print("="*60)
    
    tests = [
        ("Server Startup", test_server_startup),
        ("Database Performance", test_database_performance),
        ("Server Configuration", test_server_configuration),
        ("Alternative Approach", test_alternative_approach),
        ("Endpoint Performance", test_endpoint_performance)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    # Recommendations
    print("\n" + "="*60)
    print("RECOMMENDATIONS")
    print("="*60)
    
    if not results.get("Database Performance", True):
        print("• Database queries are slow - consider adding indexes")
        print("• Consider reducing query complexity")
    
    if not results.get("Endpoint Performance", True):
        print("• Network requests are timing out - check server load")
        print("• Consider increasing timeout settings")
    
    if results.get("Alternative Approach", False):
        print("• Test client works - issue may be with network/HTTP layer")
    
    if all(results.values()):
        print("• All tests passed - issue may be intermittent or environment-specific")

if __name__ == "__main__":
    main() 
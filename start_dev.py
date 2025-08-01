#!/usr/bin/env python3
"""
Uni-verse Development Server Starter
Automatically starts both backend and frontend servers
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

# Project directories
PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"

# Colors for output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

def print_status(message, color=Colors.BLUE):
    """Print a status message with color"""
    print(f"{color}[INFO]{Colors.END} {message}")

def print_error(message):
    """Print an error message"""
    print(f"{Colors.RED}[ERROR]{Colors.END} {message}")

def print_success(message):
    """Print a success message"""
    print(f"{Colors.GREEN}[SUCCESS]{Colors.END} {message}")

def check_python_dependencies():
    """Check if Python dependencies are installed"""
    print_status("Checking Python dependencies...")
    
    try:
        import flask
        import flask_cors
        import flask_sqlalchemy
        import psycopg2
        print_success("Python dependencies are installed!")
        return True
    except ImportError as e:
        print_error(f"Missing Python dependency: {e}")
        print_status("Installing Python dependencies...")
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(BACKEND_DIR / "requirements.txt")], 
                         check=True, cwd=BACKEND_DIR)
            print_success("Python dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print_error(f"Failed to install Python dependencies: {e}")
            return False

def check_node_installation():
    """Check if Node.js is installed"""
    print_status("Checking Node.js installation...")
    
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"Node.js found: {result.stdout.strip()}")
            return True
        else:
            print_error("Node.js not found")
            return False
    except FileNotFoundError:
        print_error("Node.js not installed")
        return False


def setup_backend():
    """Setup and start the backend server"""
    print_status("Setting up backend...")
    
    if not check_python_dependencies():
        return None
    
    
    print_status("Starting backend server...")
    
    try:
        # Start Flask server
        process = subprocess.Popen(
            [sys.executable, "app.py"],
            cwd=BACKEND_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for server to start
        time.sleep(3)
        
        if process.poll() is None:
            print_success("Backend server started on http://localhost:5000")
            return process
        else:
            stdout, stderr = process.communicate()
            print_error(f"Backend failed to start: {stderr}")
            return None
            
    except Exception as e:
        print_error(f"Failed to start backend: {e}")
        return None

def setup_frontend():
    """Setup and start the frontend server"""
    print_status("Setting up frontend...")
    
    if not check_node_installation():
        print_error("Node.js not found. Frontend cannot be started.")
        print_status("You can still test the backend API at http://localhost:5000")
        print_status("To install Node.js, visit: https://nodejs.org/")
        return None
    
    # Check if node_modules exists
    if not (FRONTEND_DIR / "node_modules").exists():
        print_status("Installing frontend dependencies...")
        try:
            # Try to find npm in common locations
            npm_paths = ["npm", "C:\\Program Files\\nodejs\\npm.cmd", "C:\\Program Files\\nodejs\\npm.ps1"]
            npm_found = False
            
            for npm_path in npm_paths:
                try:
                    subprocess.run([npm_path, "install"], cwd=FRONTEND_DIR, check=True)
                    print_success("Frontend dependencies installed!")
                    npm_found = True
                    break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            
            if not npm_found:
                print_error("npm not found in common locations")
                return None
                
        except Exception as e:
            print_error(f"Failed to install frontend dependencies: {e}")
            return None
    
    print_status("Starting frontend server...")
    
    try:
        # Start Vite dev server
        npm_paths = ["npm", "C:\\Program Files\\nodejs\\npm.cmd", "C:\\Program Files\\nodejs\\npm.ps1"]
        npm_found = False
        
        for npm_path in npm_paths:
            try:
                process = subprocess.Popen(
                    [npm_path, "run", "dev"],
                    cwd=FRONTEND_DIR,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                npm_found = True
                break
            except FileNotFoundError:
                continue
        
        if not npm_found:
            print_error("npm not found for running dev server")
            return None
        
        # Wait a moment for server to start
        time.sleep(5)
        
        if process.poll() is None:
            print_success("Frontend server started on http://localhost:5173")
            return process
        else:
            stdout, stderr = process.communicate()
            print_error(f"Frontend failed to start: {stderr}")
            return None
            
    except Exception as e:
        print_error(f"Failed to start frontend: {e}")
        return None

def create_simple_frontend():
    """Create a simple HTML frontend for testing"""
    print_status("Creating simple HTML frontend...")
    
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Uni-verse Platform</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2563eb; text-align: center; margin-bottom: 30px; }
        .api-test { background: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .endpoint { background: #e2e8f0; padding: 10px; border-radius: 5px; margin: 10px 0; }
        button { background: #2563eb; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 5px; }
        button:hover { background: #1d4ed8; }
        .result { background: #f1f5f9; padding: 15px; border-radius: 5px; margin: 10px 0; white-space: pre-wrap; }
        .success { color: #059669; }
        .error { color: #dc2626; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Uni-verse Platform</h1>
        <p>Welcome to the Uni-verse platform! This is a simple test interface for the backend API.</p>
        
        <div class="api-test">
            <h2>Backend API Testing</h2>
            <p>Test the backend API endpoints:</p>
            
            <div class="endpoint">
                <strong>GET /</strong> - API Info
                <button onclick="testHome()">Test</button>
                <div id="home-result" class="result"></div>
            </div>
            
            <div class="endpoint">
                <strong>GET /api/universities</strong> - List Universities
                <button onclick="testUniversities()">Test</button>
                <div id="universities-result" class="result"></div>
            </div>
            
            <div class="endpoint">
                <strong>GET /api/programs</strong> - List Programs
                <button onclick="testPrograms()">Test</button>
                <div id="programs-result" class="result"></div>
            </div>
            
            <div class="endpoint">
                <strong>POST /api/match-programs</strong> - Match Programs
                <button onclick="testMatchPrograms()">Test</button>
                <div id="match-result" class="result"></div>
            </div>
        </div>
        
        <div class="api-test">
            <h2>Quick Test Data</h2>
            <p>Test with this sample student profile:</p>
            <ul>
                <li>SSC: 75%</li>
                <li>HSC: 80%</li>
                <li>Group: Pre-Engineering</li>
                <li>Interests: programming, technology</li>
                <li>Budget: 300,000 PKR</li>
                <li>Location: Lahore</li>
            </ul>
        </div>
    </div>

    <script>
        const API_BASE = 'http://localhost:5000';
        
        async function testHome() {
            try {
                const response = await fetch(API_BASE + '/');
                const data = await response.json();
                document.getElementById('home-result').innerHTML = 
                    '<span class="success">✅ Success!</span>\\n' + JSON.stringify(data, null, 2);
            } catch (error) {
                document.getElementById('home-result').innerHTML = 
                    '<span class="error">❌ Error: ' + error.message + '</span>';
            }
        }
        
        async function testUniversities() {
            try {
                const response = await fetch(API_BASE + '/api/universities');
                const data = await response.json();
                document.getElementById('universities-result').innerHTML = 
                    '<span class="success">✅ Success!</span>\\n' + JSON.stringify(data, null, 2);
            } catch (error) {
                document.getElementById('universities-result').innerHTML = 
                    '<span class="error">❌ Error: ' + error.message + '</span>';
            }
        }
        
        async function testPrograms() {
            try {
                const response = await fetch(API_BASE + '/api/programs');
                const data = await response.json();
                document.getElementById('programs-result').innerHTML = 
                    '<span class="success">✅ Success!</span>\\n' + JSON.stringify(data, null, 2);
            } catch (error) {
                document.getElementById('programs-result').innerHTML = 
                    '<span class="error">❌ Error: ' + error.message + '</span>';
            }
        }
        
        async function testMatchPrograms() {
            try {
                const response = await fetch(API_BASE + '/api/match-programs', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        sscPercentage: 75.0,
                        hscPercentage: 80.0,
                        hscGroup: "Pre-Engineering",
                        interests: ["programming", "technology"],
                        budget: 300000,
                        preferredLocation: "Lahore"
                    })
                });
                const data = await response.json();
                document.getElementById('match-result').innerHTML = 
                    '<span class="success">✅ Success!</span>\\n' + JSON.stringify(data, null, 2);
            } catch (error) {
                document.getElementById('match-result').innerHTML = 
                    '<span class="error">❌ Error: ' + error.message + '</span>';
            }
        }
    </script>
</body>
</html>
    """
    
    with open("simple_test.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print_success("Simple HTML frontend created: simple_test.html")
    return "simple_test.html"

def main():
    """Main function to start both servers"""
    print_status("🚀 Starting Uni-verse Development Environment")
    print_status("=" * 50)
    
    # Store processes for cleanup
    processes = []
    
    try:
        # Start backend
        backend_process = setup_backend()
        if backend_process:
            processes.append(backend_process)
        else:
            print_error("Backend failed to start. Exiting.")
            return
        
        # Try to start frontend
        frontend_process = setup_frontend()
        if frontend_process:
            processes.append(frontend_process)
        else:
            # Create simple HTML frontend as fallback
            simple_frontend = create_simple_frontend()
            print_status(f"Open {simple_frontend} in your browser to test the platform")
        
        print_status("=" * 50)
        print_success("🎉 Uni-verse platform is ready!")
        print_status("Backend API: http://localhost:5000")
        if frontend_process:
            print_status("Frontend: http://localhost:5173")
        else:
            print_status("Simple Test: Open simple_test.html in your browser")
        
        print_status("Press Ctrl+C to stop all servers")
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print_status("\n🛑 Stopping servers...")
        
        # Stop all processes
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        
        print_success("All servers stopped!")

if __name__ == "__main__":
    main() 
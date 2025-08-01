# Uni-verse Platform

A modern web platform designed to help Pakistani students discover and match with the perfect undergraduate programs. Uni-verse uses intelligent algorithms to analyze student profiles, academic qualifications, and preferences to recommend the most suitable university programs across Pakistan.

## What is Uni-verse?

Uni-verse is a comprehensive university discovery platform that bridges the gap between students and educational opportunities. Instead of manually searching through hundreds of university websites, students can input their academic profile once and receive personalized program recommendations based on:

- **Academic Performance**: SSC/HSC scores or O/A Levels grades
- **Subject Group**: Pre-Engineering, Pre-Medical, ICS, ICom, or A-Level subjects
- **Budget Constraints**: Annual fees and financial considerations
- **Location Preferences**: Preferred cities and provinces
- **Career Interests**: Program-specific requirements and specializations

The platform features a clean, modern interface with a personal dashboard where students can track their interested universities and programs, making the university selection process efficient and data-driven.

## 🚀 Quick Start

Simply run:
```bash
python start_dev.py
```

This will:
- ✅ Start the backend API server (http://localhost:5000)
- ✅ Start the frontend development server (http://localhost:5173)
- ✅ Set up all dependencies automatically

## 📁 Project Structure

```
Uni-verse/
├── backend/                 # Flask API server
│   ├── app.py              # Main Flask application
│   ├── models.py           # Database models
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.jsx         # Main React app
│   │   └── main.jsx        # Entry point
│   └── package.json        # Node.js dependencies
└── start_dev.py            # Development startup script
```

## 🎯 Features

- **Smart Program Matching**: AI-powered algorithm matches student profiles with programs
- **University Discovery**: Browse universities and their programs
- **Personal Dashboard**: Track interested universities and programs
- **Responsive Design**: Works on desktop and mobile

## 🔧 Technology Stack

- **Backend**: Python, Flask, PostgreSQL (Neon DB)
- **Frontend**: React, Vite, Tailwind CSS
- **Database**: PostgreSQL with SQLAlchemy ORM

## 📝 Usage

1. **Start the platform**: `python start_dev.py`
2. **Access the application**: http://localhost:5173
3. **Find programs**: Use the search form to get personalized recommendations
4. **View dashboard**: Track your interested universities and programs

## 🛠️ Development

The platform is designed to be simple and focused on program discovery, not application management. All unnecessary files have been removed to keep the codebase clean and maintainable. 
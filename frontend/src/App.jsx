import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import LandingPage from './components/LandingPage';
import StudentForm from './components/StudentForm';
import ResultsPage from './components/ResultsPage';
import ProgramDetail from './components/ProgramDetail';
import UniversityDetail from './components/UniversityDetail';
import Dashboard from './components/Dashboard';
import './index.css';
const API_BASE_URL = import.meta.env.VITE_API_URL;


function App() {
  const [studentData, setStudentData] = useState(null);
  const [matchedOfferings, setMatchedOfferings] = useState([]);

  const handleFormSubmit = async (formData) => {
    setStudentData(formData);
    
    try {
      const response = await fetch('${API_BASE_URL}/api/match-programs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      if (response.ok) {
        const data = await response.json();
        setMatchedOfferings(data.matched_offerings);
      } else {
        console.error('Failed to match programs');
      }
    } catch (error) {
      console.error('Error matching programs:', error);
    }
  };

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="flex-1">
          <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/form" element={<StudentForm onSubmit={handleFormSubmit} />} />
          <Route path="/results" element={<ResultsPage matchedOfferings={matchedOfferings} studentData={studentData} />} />
          <Route path="/program/:id" element={<ProgramDetail />} />
          <Route path="/university/:id" element={<UniversityDetail />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import LandingPage from './components/LandingPage';
import StudentForm from './components/StudentForm';
import ResultsPage from './components/ResultsPage';
import ProgramDetail from './components/ProgramDetail';
import UniversityDetail from './components/UniversityDetail';
import Dashboard from './components/Dashboard';
import './index.css';

const STORAGE_STUDENT = 'studentData_v1';
const STORAGE_MATCHED = 'matchedOfferings_v1';

const API_BASE_URL = import.meta.env.VITE_API_URL;

function App() {
  const [studentData, setStudentData] = useState(null);
  const [matchedOfferings, setMatchedOfferings] = useState([]);

  const fetchMatches = async (formData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/match-programs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        console.error('Failed to fetch matches, status:', response.status);
        return [];
      }

      const data = await response.json();
      return data.matched_offerings || [];
    } catch (err) {
      console.error('Error fetching matched programs:', err);
      return [];
    }
  };

  const handleFormSubmit = async (formData) => {
    setStudentData(formData);
    localStorage.setItem(STORAGE_STUDENT, JSON.stringify(formData));

    const offerings = await fetchMatches(formData);
    setMatchedOfferings(offerings);
    localStorage.setItem(STORAGE_MATCHED, JSON.stringify(offerings));
  };

  useEffect(() => {
    let cancelled = false;

    try {
      const rawStudent = localStorage.getItem(STORAGE_STUDENT);
      const rawMatched = localStorage.getItem(STORAGE_MATCHED);

      if (rawStudent) {
        const parsedStudent = JSON.parse(rawStudent);
        if (!cancelled) setStudentData(parsedStudent);
      }

      if (rawMatched) {
        const parsedMatched = JSON.parse(rawMatched);
        if (Array.isArray(parsedMatched) && !cancelled) {
          setMatchedOfferings(parsedMatched);
        }
      }

      if (rawStudent && !rawMatched) {
        (async () => {
          const parsedStudent = JSON.parse(rawStudent);
          const offerings = await fetchMatches(parsedStudent);
          if (!cancelled) {
            setMatchedOfferings(offerings);
            localStorage.setItem(STORAGE_MATCHED, JSON.stringify(offerings));
          }
        })();
      }
    } catch (err) {
      console.warn('Failed to rehydrate app state from localStorage', err);
    }

    return () => { cancelled = true; };
  }, []);

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
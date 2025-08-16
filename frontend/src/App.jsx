import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import Header from './components/Header';
import LandingPage from './components/LandingPage';
import StudentForm from './components/StudentForm';
import ResultsPage from './components/ResultsPage';
import ProgramDetail from './components/ProgramDetail';
import UniversityDetail from './components/UniversityDetail';
import Dashboard from './components/Dashboard';
import './index.css';

// Constants
const STORAGE_KEYS = {
  STUDENT: 'studentData_v1',
  MATCHED: 'matchedOfferings_v1',
};

const API_BASE_URL = import.meta.env.VITE_API_URL;

// Separate component to use useNavigate hook
function AppContent() {
  const navigate = useNavigate();
  const [studentData, setStudentData] = useState(null);
  const [matchedOfferings, setMatchedOfferings] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Enhanced API call with better error handling
  const fetchMatches = async (formData) => {
    try {
      setError(null);
      
      const response = await fetch(`${API_BASE_URL}/api/match-programs`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          // Add other headers if needed (auth, etc.)
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorText || 'Failed to fetch matches'}`);
      }

      const data = await response.json();
      
      // Validate response structure
      if (!data || typeof data !== 'object') {
        throw new Error('Invalid response format from server');
      }

      return Array.isArray(data.matched_offerings) ? data.matched_offerings : [];
      
    } catch (err) {
      console.error('Error fetching matched programs:', err);
      
      // Set user-friendly error message
      if (err.message.includes('Failed to fetch')) {
        setError('Network error. Please check your connection and try again.');
      } else if (err.message.includes('HTTP 404')) {
        setError('Service temporarily unavailable. Please try again later.');
      } else if (err.message.includes('HTTP 500')) {
        setError('Server error. Please try again in a few minutes.');
      } else {
        setError('Something went wrong. Please try again.');
      }
      
      return [];
    }
  };

  // Enhanced form submission with loading states and navigation
  const handleFormSubmit = async (formData) => {
    try {
      setIsLoading(true);
      setError(null);
      
      // Validate form data
      if (!formData || typeof formData !== 'object') {
        throw new Error('Invalid form data');
      }

      setStudentData(formData);
      
      // Save to localStorage with error handling
      try {
        localStorage.setItem(STORAGE_KEYS.STUDENT, JSON.stringify(formData));
      } catch (storageErr) {
        console.warn('Failed to save student data to localStorage:', storageErr);
      }

      const offerings = await fetchMatches(formData);
      
      setMatchedOfferings(offerings);
      
      // Save matches to localStorage
      try {
        localStorage.setItem(STORAGE_KEYS.MATCHED, JSON.stringify(offerings));
      } catch (storageErr) {
        console.warn('Failed to save matches to localStorage:', storageErr);
      }

      // Navigate to results page only if we have data
      if (offerings.length > 0 || formData) {
        navigate('/results');
      }
      
    } catch (err) {
      console.error('Error in form submission:', err);
      setError('Failed to process your application. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Enhanced localStorage rehydration with better error handling
  useEffect(() => {
    let isCancelled = false;

    const rehydrateFromStorage = async () => {
      try {
        const rawStudent = localStorage.getItem(STORAGE_KEYS.STUDENT);
        const rawMatched = localStorage.getItem(STORAGE_KEYS.MATCHED);

        if (rawStudent && !isCancelled) {
          try {
            const parsedStudent = JSON.parse(rawStudent);
            setStudentData(parsedStudent);

            // If we have student data but no matches, refetch
            if (!rawMatched) {
              setIsLoading(true);
              const offerings = await fetchMatches(parsedStudent);
              if (!isCancelled) {
                setMatchedOfferings(offerings);
                try {
                  localStorage.setItem(STORAGE_KEYS.MATCHED, JSON.stringify(offerings));
                } catch (storageErr) {
                  console.warn('Failed to save refetched matches:', storageErr);
                }
              }
              setIsLoading(false);
            }
          } catch (parseErr) {
            console.warn('Failed to parse student data from localStorage:', parseErr);
            localStorage.removeItem(STORAGE_KEYS.STUDENT);
          }
        }

        if (rawMatched && !isCancelled) {
          try {
            const parsedMatched = JSON.parse(rawMatched);
            if (Array.isArray(parsedMatched)) {
              setMatchedOfferings(parsedMatched);
            }
          } catch (parseErr) {
            console.warn('Failed to parse matched data from localStorage:', parseErr);
            localStorage.removeItem(STORAGE_KEYS.MATCHED);
          }
        }

      } catch (err) {
        console.warn('Failed to rehydrate app state from localStorage:', err);
      }
    };

    rehydrateFromStorage();

    return () => {
      isCancelled = true;
    };
  }, []);

  // Clear error when navigating
  useEffect(() => {
    setError(null);
  }, [window.location.pathname]);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      {/* Global loading indicator */}
      {isLoading && (
        <div className="fixed top-0 left-0 right-0 z-50 bg-blue-500 text-white text-center py-2">
          <div className="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
          Processing your request...
        </div>
      )}
      
      {/* Global error message */}
      {error && (
        <div className="fixed top-0 left-0 right-0 z-50 bg-red-500 text-white p-4 flex justify-between items-center">
          <span>{error}</span>
          <button 
            onClick={() => setError(null)} 
            className="ml-4 text-white hover:text-gray-200 text-xl font-bold"
          >
            ×
          </button>
        </div>
      )}

      <main className="flex-1">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route 
            path="/form" 
            element={
              <StudentForm 
                onSubmit={handleFormSubmit} 
                isLoading={isLoading}
                error={error}
              />
            } 
          />
          <Route 
            path="/results" 
            element={
              <ResultsPage 
                matchedOfferings={matchedOfferings} 
                studentData={studentData}
                isLoading={isLoading}
              />
            } 
          />
          <Route path="/program/:id" element={<ProgramDetail />} />
          <Route path="/university/:id" element={<UniversityDetail />} />
          <Route path="/dashboard" element={<Dashboard />} />
          
          {/* 404 page */}
          <Route 
            path="*" 
            element={
              <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                  <h1 className="text-4xl font-bold text-gray-900 mb-4">404</h1>
                  <p className="text-gray-600 mb-4">Page not found.</p>
                  <button 
                    onClick={() => navigate('/')}
                    className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                  >
                    Go Home
                  </button>
                </div>
              </div>
            } 
          />
        </Routes>
      </main>
    </div>
  );
}

// Main App component with Router wrapper
function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;

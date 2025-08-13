import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, MapPin, Phone, Mail, Globe, Users, Calendar, Award, Building, Wifi, Car, BookOpen, Instagram, Facebook, Twitter, Linkedin } from 'lucide-react';
const API_BASE_URL = import.meta.env.VITE_API_URL;

const UniversityDetail = () => {
  const { id } = useParams();
  const [university, setUniversity] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUniversityData = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/api/university/${id}`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch university data');
        }
        
        const data = await response.json();
        if (data.success) {
          setUniversity(data.university);
        } else {
          throw new Error(data.error || 'Failed to load university');
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUniversityData();
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Error Loading University</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <Link to="/results" className="text-blue-600 hover:text-blue-700 font-medium">
            Back to Results
          </Link>
        </div>
      </div>
    );
  }

  if (!university) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">University Not Found</h2>
          <p className="text-gray-600 mb-4">The university you're looking for doesn't exist.</p>
          <Link to="/results" className="text-blue-600 hover:text-blue-700 font-medium">
            Back to Results
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <Link to="/results" className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Results
          </Link>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{university.name}</h1>
          <div className="flex items-center text-gray-600">
            <MapPin className="w-4 h-4 mr-2" />
            <span>{university.campuses.map(c => c.city).join(', ')}</span>
          </div>
          <p className="text-lg text-gray-500 capitalize">{university.sector} University</p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* University Overview */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">University Overview</h2>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="flex items-center">
                  <Building className="w-5 h-5 text-blue-600 mr-3" />
                  <div>
                    <p className="text-sm text-gray-600">University Name</p>
                    <p className="font-medium">{university.name}</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <Award className="w-5 h-5 text-blue-600 mr-3" />
                  <div>
                    <p className="text-sm text-gray-600">Sector</p>
                    <p className="font-medium capitalize">{university.sector}</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <MapPin className="w-5 h-5 text-blue-600 mr-3" />
                  <div>
                    <p className="text-sm text-gray-600">Campuses</p>
                    <p className="font-medium">{university.campuses.length} locations</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <BookOpen className="w-5 h-5 text-blue-600 mr-3" />
                  <div>
                    <p className="text-sm text-gray-600">Program Offerings</p>
                    <p className="font-medium">{university.offerings.length} programs</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Campuses */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Campuses</h2>
              <div className="space-y-4">
                {university.campuses.map((campus, index) => (
                  <div key={campus.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">Campus {index + 1}</h3>
                        <p className="text-gray-600">{campus.city}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-600">
                          {university.offerings.filter(o => o.campus.city === campus.city).length} programs
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Program Offerings */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Program Offerings</h2>
              <div className="space-y-4">
                {university.offerings.map((offering, index) => (
                  <div key={offering.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">{offering.program.name}</h3>
                        {offering.program.discipline && (
                          <p className="text-gray-600">{offering.program.discipline}</p>
                        )}
                        <p className="text-sm text-gray-500">{offering.campus.city} Campus</p>
                      </div>
                      <div className="text-right">
                        <p className="text-lg font-bold text-blue-600">PKR {offering.annual_fee.toLocaleString()}</p>
                        <p className="text-sm text-gray-600">per year</p>
                      </div>
                    </div>

                    <div className="grid md:grid-cols-2 gap-4 mb-4">
                      <div className="flex items-center text-sm text-gray-600">
                        <BookOpen className="w-4 h-4 mr-2" />
                        Min Score: {offering.min_score_pct}% ({offering.min_score_type})
                      </div>
                      <div className="flex items-center text-sm text-gray-600">
                        <Building className="w-4 h-4 mr-2" />
                        Hostel: {offering.hostel_available ? 'Available' : 'Not Available'}
                      </div>
                    </div>

                    {offering.tags && offering.tags.length > 0 && (
                      <div className="mb-3">
                        <p className="text-sm font-medium text-gray-700 mb-2">Tags:</p>
                        <div className="flex flex-wrap gap-2">
                          {offering.tags.map(tag => (
                            <span key={tag} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                              {tag}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    <div className="flex space-x-2">
                      <Link
                        to={`/program/${offering.program.id}`}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                      >
                        View Program
                      </Link>
                      <button className="border border-blue-600 text-blue-600 hover:bg-blue-50 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                        Apply Now
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Info */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Info</h3>
              <div className="space-y-3">
                <div className="flex items-center">
                  <MapPin className="w-4 h-4 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-700">{university.campuses.map(c => c.city).join(', ')}</span>
                </div>
                <div className="flex items-center">
                  <Building className="w-4 h-4 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-700 capitalize">{university.sector} University</span>
                </div>
                <div className="flex items-center">
                  <Users className="w-4 h-4 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-700">{university.campuses.length} campuses</span>
                </div>
                <div className="flex items-center">
                  <BookOpen className="w-4 h-4 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-700">{university.offerings.length} program offerings</span>
                </div>
              </div>
            </div>

            {/* Fee Range */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Fee Range</h3>
              <div className="space-y-3">
                <div className="flex items-center">
                  <Globe className="w-4 h-4 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-700">
                    PKR {Math.min(...university.offerings.map(o => o.annual_fee)).toLocaleString()} - {Math.max(...university.offerings.map(o => o.annual_fee)).toLocaleString()}/year
                  </span>
                </div>
                <div className="flex items-center">
                  <BookOpen className="w-4 h-4 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-700">
                    Min Score: {Math.min(...university.offerings.map(o => o.min_score_pct))}% - {Math.max(...university.offerings.map(o => o.min_score_pct))}%
                  </span>
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="space-y-3">
                <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-lg font-medium transition-colors">
                  View All Programs
                </button>
                <button className="w-full border border-blue-600 text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors">
                  Save University
                </button>
                <Link
                  to="/results"
                  className="w-full border border-gray-300 text-gray-700 hover:bg-gray-50 py-3 px-4 rounded-lg font-medium transition-colors inline-block text-center"
                >
                  Back to Results
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UniversityDetail; 

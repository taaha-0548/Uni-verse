import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, MapPin, DollarSign, Calendar, Phone, Mail, Globe, Clock, Users, BookOpen, Building } from 'lucide-react';

const ProgramDetail = () => {
  const { id } = useParams();
  const [program, setProgram] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProgramData = async () => {
      try {
        setLoading(true);
        const response = await fetch(`http://localhost:5000/api/program/${id}`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch program data');
        }
        
        const data = await response.json();
        if (data.success) {
          setProgram(data.program);
        } else {
          throw new Error(data.error || 'Failed to load program');
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProgramData();
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
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Error Loading Program</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <Link to="/results" className="text-blue-600 hover:text-blue-700 font-medium">
            Back to Results
          </Link>
        </div>
      </div>
    );
  }

  if (!program) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Program Not Found</h2>
          <p className="text-gray-600 mb-4">The program you're looking for doesn't exist.</p>
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
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{program.name}</h1>
          {program.discipline && (
            <p className="text-xl text-gray-600 mb-2">{program.discipline}</p>
          )}
          {program.code && (
            <p className="text-lg text-gray-500">Program Code: {program.code}</p>
          )}
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Program Overview */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Program Overview</h2>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="flex items-center">
                  <BookOpen className="w-5 h-5 text-blue-600 mr-3" />
                  <div>
                    <p className="text-sm text-gray-600">Program Name</p>
                    <p className="font-medium">{program.name}</p>
                  </div>
                </div>
                {program.discipline && (
                  <div className="flex items-center">
                    <BookOpen className="w-5 h-5 text-blue-600 mr-3" />
                    <div>
                      <p className="text-sm text-gray-600">Discipline</p>
                      <p className="font-medium">{program.discipline}</p>
                    </div>
                  </div>
                )}
                {program.code && (
                  <div className="flex items-center">
                    <BookOpen className="w-5 h-5 text-blue-600 mr-3" />
                    <div>
                      <p className="text-sm text-gray-600">Program Code</p>
                      <p className="font-medium">{program.code}</p>
                    </div>
                  </div>
                )}
                <div className="flex items-center">
                  <Users className="w-5 h-5 text-blue-600 mr-3" />
                  <div>
                    <p className="text-sm text-gray-600">Total Offerings</p>
                    <p className="font-medium">{program.offerings.length} campuses</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Program Offerings */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Available at Campuses</h2>
              <div className="space-y-4">
                {program.offerings.map((offering, index) => (
                  <div key={offering.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">{offering.university.name}</h3>
                        <p className="text-gray-600">{offering.campus.city}</p>
                        <p className="text-sm text-gray-500">{offering.university.sector} University</p>
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

                    {offering.required_groups && offering.required_groups.length > 0 && (
                      <div className="mb-3">
                        <p className="text-sm font-medium text-gray-700 mb-2">Required Groups:</p>
                        <div className="flex flex-wrap gap-2">
                          {offering.required_groups.map(group => (
                            <span key={group} className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full">
                              {group}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {offering.accepted_boards && offering.accepted_boards.length > 0 && (
                      <div className="mb-3">
                        <p className="text-sm font-medium text-gray-700 mb-2">Accepted Boards:</p>
                        <div className="flex flex-wrap gap-2">
                          {offering.accepted_boards.map(board => (
                            <span key={board} className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                              {board}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

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
                        to={`/university/${offering.university.id}`}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                      >
                        View University
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
                  <Users className="w-4 h-4 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-700">{program.offerings.length} campus offerings</span>
                </div>
                <div className="flex items-center">
                  <DollarSign className="w-4 h-4 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-700">
                    PKR {Math.min(...program.offerings.map(o => o.annual_fee)).toLocaleString()} - {Math.max(...program.offerings.map(o => o.annual_fee)).toLocaleString()}/year
                  </span>
                </div>
                <div className="flex items-center">
                  <BookOpen className="w-4 h-4 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-700">
                    Min Score: {Math.min(...program.offerings.map(o => o.min_score_pct))}% - {Math.max(...program.offerings.map(o => o.min_score_pct))}%
                  </span>
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="space-y-3">
                <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-lg font-medium transition-colors">
                  Compare All Offerings
                </button>
                <button className="w-full border border-blue-600 text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors">
                  Save Program
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

export default ProgramDetail; 
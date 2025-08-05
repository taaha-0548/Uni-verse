import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { MapPin, DollarSign, Star, Filter, SortAsc, SortDesc, AlertCircle, CheckCircle } from 'lucide-react';

const ResultsPage = ({ matchedOfferings, studentData }) => {
  const [filters, setFilters] = useState({
    location: '',
    programType: '',
    maxFees: 1000000,
    minMatch: 0,
    subjectCompatible: 'all', // 'all', 'compatible', 'incompatible'
    eligibility: 'all' // 'all', 'eligible', 'ineligible'
  });

  // Apply user's preferred location when component mounts or studentData changes
  useEffect(() => {
    if (studentData && studentData.preferredLocation) {
      setFilters(prev => ({
        ...prev,
        location: studentData.preferredLocation
      }));
    }
  }, [studentData]);
  const [sortBy, setSortBy] = useState('priority');
  const [sortOrder, setSortOrder] = useState('desc');

  const handleFilterChange = (filter, value) => {
    setFilters(prev => ({
      ...prev,
      [filter]: value
    }));
  };

  const handleSort = (field) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(field);
      setSortOrder('desc');
    }
  };

  const filteredAndSortedOfferings = matchedOfferings
    .filter(offering => {
      if (filters.location && offering.campus.city !== filters.location) return false;
      if (filters.programType && !offering.program_name.toLowerCase().includes(filters.programType.toLowerCase())) return false;
      if (offering.annual_fee > filters.maxFees) return false;
      if (offering.match_score < filters.minMatch) return false;
      
      // Filter by subject compatibility
      if (filters.subjectCompatible === 'compatible' && !offering.subject_compatibility) return false;
      if (filters.subjectCompatible === 'incompatible' && offering.subject_compatibility) return false;
      
      // Filter by eligibility
      if (studentData && filters.eligibility !== 'all') {
        const studentScore = Math.max(studentData.sscPercentage || 0, studentData.hscPercentage || 0);
        const isEligible = studentScore >= offering.min_score_pct;
        
        if (filters.eligibility === 'eligible' && !isEligible) return false;
        if (filters.eligibility === 'ineligible' && isEligible) return false;
      }
      
      return true;
    })
    .sort((a, b) => {
      let aValue, bValue;
      
      switch (sortBy) {
        case 'relevance':
          aValue = a.match_score;
          bValue = b.match_score;
          break;
        case 'fees':
          aValue = a.annual_fee;
          bValue = b.annual_fee;
          break;
        case 'match':
          aValue = a.match_score;
          bValue = b.match_score;
          break;
        case 'minScore':
          // Get student's academic score
          const studentScore = Math.max(studentData?.sscPercentage || 0, studentData?.hscPercentage || 0);
          
          // Calculate eligibility score (higher score = more eligible)
          // If student meets requirement, give higher score
          const aEligible = studentScore >= a.min_score_pct;
          const bEligible = studentScore >= b.min_score_pct;
          
          if (aEligible && !bEligible) return -1;
          if (!aEligible && bEligible) return 1;
          
          // If both eligible, prioritize programs with higher requirements (more prestigious)
          if (aEligible && bEligible) {
            // Higher requirements should appear first (descending order)
            aValue = a.min_score_pct;
            bValue = b.min_score_pct;
          } else {
            // If both ineligible, sort by minimum score requirement
            aValue = a.min_score_pct;
            bValue = b.min_score_pct;
          }
          break;
        case 'priority':
          // Use backend's ranking - programs are already sorted by priority
          // Just maintain the order as received from backend
          return 0; // Keep original order from backend
          break;
        case 'backend':
          // Respect the backend's original ranking order
          return 0; // Keep original order from backend
          break;
        default:
          return 0;
      }
      
      return sortOrder === 'asc' ? aValue - bValue : bValue - aValue;
    });

  const locations = [...new Set(matchedOfferings.map(o => o.campus.city))];
  const programTypes = ['Computer Science', 'Engineering', 'Medicine', 'Business', 'Arts', 'Law'];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Matched Programs</h1>
          <p className="text-gray-600">
            Found {filteredAndSortedOfferings.length} program offerings matching your criteria
          </p>
          
          {/* Student Profile Summary */}
          {studentData && (
            <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h3 className="text-sm font-medium text-blue-900 mb-2">Your Profile</h3>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-sm">
                <div>
                  <span className="text-blue-700">HSC Group:</span>
                  <span className="ml-2 font-medium">{studentData.hscGroup}</span>
                </div>
                <div>
                  <span className="text-blue-700">Academic Score:</span>
                  <span className="ml-2 font-medium">{Math.max(studentData.sscPercentage, studentData.hscPercentage)}%</span>
                </div>
                <div>
                  <span className="text-blue-700">Budget:</span>
                  <span className="ml-2 font-medium">PKR {parseInt(studentData.budget).toLocaleString()}</span>
                </div>
                {studentData.preferredLocation && (
                  <div>
                    <span className="text-blue-700">Preferred Location:</span>
                    <span className="ml-2 font-medium">{studentData.preferredLocation}</span>
                  </div>
                )}
                <div>
                  <span className="text-blue-700">Interests:</span>
                  <span className="ml-2 font-medium">
                    {studentData.interestPriorities ? 
                      studentData.interestPriorities.map(item => item.interest).join(' → ') :
                      studentData.interests.join(', ')
                    }
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Filter Sidebar */}
          <div className="lg:w-1/4">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-6">
                <Filter className="w-5 h-5 text-gray-600 mr-2" />
                <h2 className="text-lg font-semibold text-gray-900">Filters</h2>
              </div>

              {/* Subject Compatibility Filter */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">Subject Compatibility</label>
                <select
                  value={filters.subjectCompatible}
                  onChange={(e) => handleFilterChange('subjectCompatible', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="all">All Programs</option>
                  <option value="compatible">Subject Compatible</option>
                  <option value="incompatible">May Need Additional Prep</option>
                </select>
              </div>

              {/* Eligibility Filter */}
              {studentData && (
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Academic Eligibility</label>
                  <select
                    value={filters.eligibility}
                    onChange={(e) => handleFilterChange('eligibility', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="all">All Programs</option>
                    <option value="eligible">Eligible Programs</option>
                    <option value="ineligible">Programs Requiring Higher Scores</option>
                  </select>
                </div>
              )}

              {/* Location Filter */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
                <select
                  value={filters.location}
                  onChange={(e) => handleFilterChange('location', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">All Locations</option>
                  {locations.map(location => (
                    <option key={location} value={location}>{location}</option>
                  ))}
                </select>
              </div>

              {/* Program Type Filter */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">Program Type</label>
                <select
                  value={filters.programType}
                  onChange={(e) => handleFilterChange('programType', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">All Types</option>
                  {programTypes.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>

              {/* Max Fees Filter */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Max Annual Fees: PKR {filters.maxFees.toLocaleString()}
                </label>
                <input
                  type="range"
                  min="0"
                  max="1000000"
                  step="50000"
                  value={filters.maxFees}
                  onChange={(e) => handleFilterChange('maxFees', parseInt(e.target.value))}
                  className="w-full"
                />
              </div>

              {/* Min Match Percentage Filter */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Min Match Percentage: {filters.minMatch}%
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  step="5"
                  value={filters.minMatch}
                  onChange={(e) => handleFilterChange('minMatch', parseInt(e.target.value))}
                  className="w-full"
                />
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:w-3/4">
            {/* Sort Options */}
            <div className="bg-white rounded-lg shadow-md p-4 mb-6">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">
                  {filteredAndSortedOfferings.length} offerings found
                </span>
                <div className="flex items-center space-x-4">
                  <span className="text-sm text-gray-600">Sort by:</span>
                  <button
                    onClick={() => handleSort('relevance')}
                    className={`flex items-center space-x-1 px-3 py-1 rounded ${
                      sortBy === 'relevance' ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <span>Relevance</span>
                    {sortBy === 'relevance' && (
                      sortOrder === 'asc' ? <SortAsc className="w-4 h-4" /> : <SortDesc className="w-4 h-4" />
                    )}
                  </button>
                  <button
                    onClick={() => handleSort('fees')}
                    className={`flex items-center space-x-1 px-3 py-1 rounded ${
                      sortBy === 'fees' ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <span>Fees</span>
                    {sortBy === 'fees' && (
                      sortOrder === 'asc' ? <SortAsc className="w-4 h-4" /> : <SortDesc className="w-4 h-4" />
                    )}
                  </button>
                  <button
                    onClick={() => handleSort('match')}
                    className={`flex items-center space-x-1 px-3 py-1 rounded ${
                      sortBy === 'match' ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <span>Match %</span>
                    {sortBy === 'match' && (
                      sortOrder === 'asc' ? <SortAsc className="w-4 h-4" /> : <SortDesc className="w-4 h-4" />
                    )}
                  </button>
                                     <button
                     onClick={() => handleSort('minScore')}
                     className={`flex items-center space-x-1 px-3 py-1 rounded ${
                       sortBy === 'minScore' ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
                     }`}
                   >
                     <span>Min Score</span>
                     {sortBy === 'minScore' && (
                       sortOrder === 'asc' ? <SortAsc className="w-4 h-4" /> : <SortDesc className="w-4 h-4" />
                     )}
                   </button>
                                       <button
                      onClick={() => handleSort('priority')}
                      className={`flex items-center space-x-1 px-3 py-1 rounded ${
                        sortBy === 'priority' ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
                      }`}
                    >
                      <span>Interest Priority</span>
                      {sortBy === 'priority' && (
                        sortOrder === 'asc' ? <SortAsc className="w-4 h-4" /> : <SortDesc className="w-4 h-4" />
                      )}
                    </button>
                </div>
              </div>
            </div>

            {/* Program Offering Cards */}
            <div className="space-y-4">
              {filteredAndSortedOfferings.map((offering, index) => (
                <div key={offering.offering_id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                  <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
                    <div className="flex-1">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h3 className="text-xl font-semibold text-gray-900 mb-1">
                            {offering.program_name}
                          </h3>
                          <p className="text-gray-600 mb-2">{offering.university.name}</p>
                          {offering.discipline && (
                            <p className="text-sm text-gray-500 mb-1">{offering.discipline}</p>
                          )}
                        </div>
                        <div className="flex items-center space-x-2">
                          <div className="flex items-center">
                            <Star className="w-4 h-4 text-yellow-400 fill-current" />
                            <span className="ml-1 text-sm font-medium text-gray-700">
                              {offering.match_score}% Match
                            </span>
                          </div>
                          {/* Eligibility indicator */}
                          {studentData && (
                            <div className="flex items-center">
                              {(() => {
                                const studentScore = Math.max(studentData.sscPercentage || 0, studentData.hscPercentage || 0);
                                const isEligible = studentScore >= offering.min_score_pct;
                                return (
                                  <div className={`flex items-center text-xs px-2 py-1 rounded-full ${
                                    isEligible 
                                      ? 'bg-green-100 text-green-700' 
                                      : 'bg-red-100 text-red-700'
                                  }`}>
                                    {isEligible ? (
                                      <>
                                        <CheckCircle className="w-3 h-3 mr-1" />
                                        Eligible
                                      </>
                                    ) : (
                                      <>
                                        <AlertCircle className="w-3 h-3 mr-1" />
                                        Need {offering.min_score_pct - studentScore}% more
                                      </>
                                    )}
                                  </div>
                                );
                              })()}
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Subject Compatibility Indicator */}
                      <div className="mb-3">
                        {offering.subject_compatibility ? (
                          <div className="flex items-center text-green-600 text-sm">
                            <CheckCircle className="w-4 h-4 mr-2" />
                            <span>Subject compatible with your background</span>
                          </div>
                        ) : (
                          <div className="flex items-center text-orange-600 text-sm">
                            <AlertCircle className="w-4 h-4 mr-2" />
                            <span>May require additional preparation</span>
                          </div>
                        )}
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                        <div className="flex items-center text-sm text-gray-600">
                          <MapPin className="w-4 h-4 mr-2" />
                          {offering.campus.city}
                        </div>
                        <div className="flex items-center text-sm text-gray-600">
                          <DollarSign className="w-4 h-4 mr-2" />
                          PKR {offering.annual_fee.toLocaleString()}/year
                        </div>
                        <div className="text-sm text-gray-600">
                          Min Score: {offering.min_score_pct}% ({offering.min_score_type})
                        </div>
                      </div>

                      {offering.tags && offering.tags.length > 0 && (
                        <div className="flex flex-wrap gap-2 mb-4">
                          {offering.tags.map(tag => (
                            <span key={tag} className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                              {tag}
                            </span>
                          ))}
                        </div>
                      )}

                      {offering.required_groups && offering.required_groups.length > 0 && (
                        <div className="flex flex-wrap gap-2 mb-4">
                          <span className="text-sm text-gray-600">Required Groups:</span>
                          {offering.required_groups.map(group => (
                            <span key={group} className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full">
                              {group}
                            </span>
                          ))}
                        </div>
                      )}

                      {offering.match_explanation && (
                        <div className="text-sm text-gray-600 mb-4">
                          {offering.match_explanation.map((explanation, idx) => (
                            <div key={idx} className="mb-1">{explanation}</div>
                          ))}
                        </div>
                      )}
                    </div>

                    <div className="flex flex-col space-y-2 lg:ml-6">
                      <Link
                        to={`/program/${offering.program_id}`}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                      >
                        View Details
                      </Link>
                      <Link
                        to={`/university/${offering.university.id}`}
                        className="border border-gray-300 text-gray-700 hover:bg-gray-50 px-4 py-2 rounded-lg text-sm font-medium transition-colors text-center"
                      >
                        View University
                      </Link>
                      <button className="border border-blue-600 text-blue-600 hover:bg-blue-50 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                        Save Program
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {filteredAndSortedOfferings.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-500 text-lg">No program offerings match your current filters.</p>
                <button
                  onClick={() => setFilters({
                    location: '',
                    programType: '',
                    maxFees: 1000000,
                    minMatch: 0,
                    subjectCompatible: 'all',
                    eligibility: 'all'
                  })}
                  className="mt-4 text-blue-600 hover:text-blue-700 font-medium"
                >
                  Clear all filters
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage; 
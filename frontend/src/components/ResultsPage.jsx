import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { MapPin, DollarSign, Star, Filter, SortAsc, SortDesc } from 'lucide-react';

const ResultsPage = ({ matchedPrograms, studentData }) => {
  const [filters, setFilters] = useState({
    location: '',
    programType: '',
    maxFees: 1000000,
    minMatch: 0
  });
  const [sortBy, setSortBy] = useState('relevance');
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

  const filteredAndSortedPrograms = matchedPrograms
    .filter(program => {
      if (filters.location && program.university.city !== filters.location) return false;
      if (filters.programType && !program.name.toLowerCase().includes(filters.programType.toLowerCase())) return false;
      if (program.annual_fees > filters.maxFees) return false;
      if (program.match_score < filters.minMatch) return false;
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
          aValue = a.annual_fees;
          bValue = b.annual_fees;
          break;
        case 'match':
          aValue = a.match_score;
          bValue = b.match_score;
          break;
        default:
          return 0;
      }
      
      return sortOrder === 'asc' ? aValue - bValue : bValue - aValue;
    });

  const locations = [...new Set(matchedPrograms.map(p => p.university.city))];
  const programTypes = ['Computer Science', 'Engineering', 'Medicine', 'Business', 'Arts', 'Law'];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Matched Programs</h1>
          <p className="text-gray-600">
            Found {filteredAndSortedPrograms.length} programs matching your criteria
          </p>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Filter Sidebar */}
          <div className="lg:w-1/4">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-6">
                <Filter className="w-5 h-5 text-gray-600 mr-2" />
                <h2 className="text-lg font-semibold text-gray-900">Filters</h2>
              </div>

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
                  {filteredAndSortedPrograms.length} programs found
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
                </div>
              </div>
            </div>

            {/* Program Cards */}
            <div className="space-y-4">
              {filteredAndSortedPrograms.map((program, index) => (
                <div key={program.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                  <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
                    <div className="flex-1">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h3 className="text-xl font-semibold text-gray-900 mb-1">
                            {program.name}
                          </h3>
                          <p className="text-gray-600 mb-2">{program.university.name}</p>
                        </div>
                        <div className="flex items-center space-x-2">
                          <div className="flex items-center">
                            <Star className="w-4 h-4 text-yellow-400 fill-current" />
                            <span className="ml-1 text-sm font-medium text-gray-700">
                              {program.match_score}% Match
                            </span>
                          </div>
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                        <div className="flex items-center text-sm text-gray-600">
                          <MapPin className="w-4 h-4 mr-2" />
                          {program.university.city}
                        </div>
                        <div className="flex items-center text-sm text-gray-600">
                          <DollarSign className="w-4 h-4 mr-2" />
                          PKR {program.annual_fees.toLocaleString()}/year
                        </div>
                        <div className="text-sm text-gray-600">
                          Min SSC: {program.min_ssc_pct}% | Min HSC: {program.min_hsc_pct}%
                        </div>
                      </div>

                      {program.tags && program.tags.length > 0 && (
                        <div className="flex flex-wrap gap-2 mb-4">
                          {program.tags.map(tag => (
                            <span key={tag} className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                              {tag}
                            </span>
                          ))}
                        </div>
                      )}

                      {program.match_explanation && (
                        <p className="text-sm text-gray-600 mb-4">
                          {program.match_explanation}
                        </p>
                      )}
                    </div>

                    <div className="flex flex-col space-y-2 lg:ml-6">
                      <Link
                        to={`/program/${program.id}`}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                      >
                        View Details
                      </Link>
                      <button className="border border-blue-600 text-blue-600 hover:bg-blue-50 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                        Save Program
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {filteredAndSortedPrograms.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-500 text-lg">No programs match your current filters.</p>
                <button
                  onClick={() => setFilters({
                    location: '',
                    programType: '',
                    maxFees: 1000000,
                    minMatch: 0
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
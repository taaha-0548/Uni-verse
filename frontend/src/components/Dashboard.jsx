import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  Home, 
  Search, 
  Bookmark, 
  FileText, 
  Calendar, 
  Bell, 
  Settings, 
  User, 
  Plus,
  Clock,
  CheckCircle,
  AlertCircle,
  Star,
  MapPin,
  DollarSign,
  Eye,
  Heart,
  Building,
  GraduationCap,
  Users,
  Globe
} from 'lucide-react';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');

  // Mock data for interested universities and programs
  const interestedUniversities = [
    {
      id: 1,
      name: "LUMS (Lahore University of Management Sciences)",
      city: "Lahore",
      province: "Punjab",
      type: "Private",
      annualFees: 850000,
      website: "https://lums.edu.pk",
      contactEmail: "admissions@lums.edu.pk",
      contactPhone: "+92-42-35608000",
      programs: [
        { name: "BS Computer Science", matchScore: 95, savedDate: "2024-01-15" },
        { name: "BS Electrical Engineering", matchScore: 88, savedDate: "2024-01-10" },
        { name: "BS Business Administration", matchScore: 82, savedDate: "2024-01-08" }
      ],
      lastVisited: "2024-01-20"
    },
    {
      id: 2,
      name: "NUST (National University of Sciences and Technology)",
      city: "Islamabad",
      province: "Federal",
      type: "Public",
      annualFees: 750000,
      website: "https://nust.edu.pk",
      contactEmail: "admissions@nust.edu.pk",
      contactPhone: "+92-51-90851111",
      programs: [
        { name: "BS Computer Science", matchScore: 92, savedDate: "2024-01-12" },
        { name: "BS Software Engineering", matchScore: 89, savedDate: "2024-01-14" }
      ],
      lastVisited: "2024-01-18"
    },
    {
      id: 3,
      name: "IBA (Institute of Business Administration)",
      city: "Karachi",
      province: "Sindh",
      type: "Public",
      annualFees: 650000,
      website: "https://iba.edu.pk",
      contactEmail: "admissions@iba.edu.pk",
      contactPhone: "+92-21-38104700",
      programs: [
        { name: "BS Business Administration", matchScore: 85, savedDate: "2024-01-16" },
        { name: "BS Computer Science", matchScore: 78, savedDate: "2024-01-09" }
      ],
      lastVisited: "2024-01-15"
    }
  ];

  const savedPrograms = [
    {
      id: 1,
      name: "BS Computer Science",
      university: "LUMS",
      city: "Lahore",
      fees: 850000,
      matchScore: 95,
      savedDate: "2024-01-15",
      requirements: {
        ssc: 70,
        hsc: 75,
        group: "Pre-Engineering",
        test: "LUMS Admission Test"
      },
      deadline: "2024-03-15",
      seats: 50
    },
    {
      id: 2,
      name: "BS Electrical Engineering",
      university: "NUST",
      city: "Islamabad",
      fees: 750000,
      matchScore: 88,
      savedDate: "2024-01-10",
      requirements: {
        ssc: 65,
        hsc: 70,
        group: "Pre-Engineering",
        test: "NET"
      },
      deadline: "2024-02-28",
      seats: 80
    }
  ];

  const recentSearches = [
    { query: "Computer Science in Lahore", date: "2024-01-20" },
    { query: "Engineering programs Islamabad", date: "2024-01-18" },
    { query: "Business Administration Karachi", date: "2024-01-15" },
    { query: "Software Engineering", date: "2024-01-12" }
  ];

  return (
    <div className="flex h-[calc(100vh-4rem)] bg-gray-50">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-md">
        <div className="p-6">
          <h1 className="text-xl font-bold text-gray-900 mb-8">My Uni-verse</h1>
          
          <nav className="space-y-2">
            <button
              onClick={() => setActiveTab('overview')}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                activeTab === 'overview' ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Home className="w-5 h-5" />
              <span>Overview</span>
            </button>
            
            <button
              onClick={() => setActiveTab('universities')}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                activeTab === 'universities' ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Building className="w-5 h-5" />
              <span>Interested Universities</span>
            </button>
            
            <button
              onClick={() => setActiveTab('programs')}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                activeTab === 'programs' ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <GraduationCap className="w-5 h-5" />
              <span>Saved Programs</span>
            </button>
            
            <button
              onClick={() => setActiveTab('searches')}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                activeTab === 'searches' ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Search className="w-5 h-5" />
              <span>Recent Searches</span>
            </button>
          </nav>
          
          <div className="mt-8 pt-8 border-t border-gray-200">
            <button className="w-full flex items-center space-x-3 px-4 py-3 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
              <Settings className="w-5 h-5" />
              <span>Settings</span>
            </button>
            
            <button className="w-full flex items-center space-x-3 px-4 py-3 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
              <User className="w-5 h-5" />
              <span>Profile</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-8 overflow-y-auto">
        {activeTab === 'overview' && (
          <div className="space-y-8">
            {/* Header */}
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">Welcome to Uni-verse!</h2>
                <p className="text-gray-600">Track your interested universities and programs</p>
              </div>
              <div className="flex space-x-3">
                <Link
                  to="/form"
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center space-x-2"
                >
                  <Search className="w-4 h-4" />
                  <span>Find Programs</span>
                </Link>
              </div>
            </div>

            {/* Stats Cards */}
            <div className="grid md:grid-cols-4 gap-6">
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center">
                  <div className="p-3 bg-blue-100 rounded-lg">
                    <Building className="w-6 h-6 text-blue-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Universities</p>
                    <p className="text-2xl font-bold text-gray-900">{interestedUniversities.length}</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center">
                  <div className="p-3 bg-green-100 rounded-lg">
                    <GraduationCap className="w-6 h-6 text-green-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Programs</p>
                    <p className="text-2xl font-bold text-gray-900">{savedPrograms.length}</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center">
                  <div className="p-3 bg-purple-100 rounded-lg">
                    <Search className="w-6 h-6 text-purple-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Searches</p>
                    <p className="text-2xl font-bold text-gray-900">{recentSearches.length}</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center">
                  <div className="p-3 bg-yellow-100 rounded-lg">
                    <Star className="w-6 h-6 text-yellow-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Avg Match</p>
                    <p className="text-2xl font-bold text-gray-900">89%</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="grid lg:grid-cols-2 gap-8">
              {/* Top Universities */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Universities</h3>
                <div className="space-y-4">
                  {interestedUniversities.slice(0, 3).map((uni) => (
                    <div key={uni.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <Building className="w-5 h-5 text-blue-600" />
                        <div>
                          <p className="font-medium text-gray-900">{uni.name}</p>
                          <p className="text-sm text-gray-600">{uni.city}, {uni.province}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-medium text-gray-900">{uni.programs.length} programs</p>
                        <p className="text-xs text-gray-600">Last visited: {new Date(uni.lastVisited).toLocaleDateString()}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recent Searches */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Searches</h3>
                <div className="space-y-4">
                  {recentSearches.slice(0, 3).map((search, index) => (
                    <div key={index} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <Search className="w-5 h-5 text-gray-600" />
                        <div>
                          <p className="font-medium text-gray-900">{search.query}</p>
                          <p className="text-sm text-gray-600">{new Date(search.date).toLocaleDateString()}</p>
                        </div>
                      </div>
                      <button className="text-blue-600 hover:text-blue-800 text-sm">
                        Search Again
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'universities' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">Interested Universities</h2>
              <Link
                to="/form"
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
              >
                Find More Universities
              </Link>
            </div>
            
            <div className="grid lg:grid-cols-2 gap-6">
              {interestedUniversities.map((uni) => (
                <div key={uni.id} className="bg-white rounded-lg shadow-md p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-1">{uni.name}</h3>
                      <div className="flex items-center space-x-4 text-sm text-gray-600">
                        <span className="flex items-center">
                          <MapPin className="w-4 h-4 mr-1" />
                          {uni.city}, {uni.province}
                        </span>
                        <span className="flex items-center">
                          <Building className="w-4 h-4 mr-1" />
                          {uni.type}
                        </span>
                      </div>
                    </div>
                    <button className="text-gray-400 hover:text-red-500">
                      <Heart className="w-5 h-5 fill-current" />
                    </button>
                  </div>
                  
                  <div className="space-y-3 mb-4">
                    <div className="flex items-center text-sm text-gray-600">
                      <DollarSign className="w-4 h-4 mr-2" />
                      PKR {uni.annualFees.toLocaleString()}/year
                    </div>
                    <div className="flex items-center text-sm text-gray-600">
                      <GraduationCap className="w-4 h-4 mr-2" />
                      {uni.programs.length} programs of interest
                    </div>
                    <div className="flex items-center text-sm text-gray-600">
                      <Globe className="w-4 h-4 mr-2" />
                      <a href={uni.website} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                        Visit Website
                      </a>
                    </div>
                  </div>
                  
                  <div className="border-t pt-4">
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Programs of Interest:</h4>
                    <div className="space-y-2">
                      {uni.programs.map((program, index) => (
                        <div key={index} className="flex items-center justify-between text-sm">
                          <span className="text-gray-700">{program.name}</span>
                          <span className="text-green-600 font-medium">{program.matchScore}% match</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div className="flex space-x-2 mt-4">
                    <button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg text-sm font-medium transition-colors">
                      View Details
                    </button>
                    <button className="flex-1 border border-blue-600 text-blue-600 hover:bg-blue-50 py-2 px-4 rounded-lg text-sm font-medium transition-colors">
                      Contact
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'programs' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">Saved Programs</h2>
              <Link
                to="/form"
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
              >
                Find More Programs
              </Link>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {savedPrograms.map((program) => (
                <div key={program.id} className="bg-white rounded-lg shadow-md p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center">
                      <Star className="w-5 h-5 text-yellow-400 fill-current" />
                      <span className="ml-2 text-sm font-medium text-gray-700">{program.matchScore}% Match</span>
                    </div>
                    <button className="text-gray-400 hover:text-red-500">
                      <Bookmark className="w-5 h-5 fill-current" />
                    </button>
                  </div>
                  
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{program.name}</h3>
                  <p className="text-gray-600 mb-4">{program.university}</p>
                  
                  <div className="space-y-2 mb-4">
                    <div className="flex items-center text-sm text-gray-600">
                      <MapPin className="w-4 h-4 mr-2" />
                      {program.city}
                    </div>
                    <div className="flex items-center text-sm text-gray-600">
                      <DollarSign className="w-4 h-4 mr-2" />
                      PKR {program.fees.toLocaleString()}/year
                    </div>
                    <div className="flex items-center text-sm text-gray-600">
                      <Users className="w-4 h-4 mr-2" />
                      {program.seats} seats available
                    </div>
                    <div className="flex items-center text-sm text-gray-600">
                      <Calendar className="w-4 h-4 mr-2" />
                      Deadline: {new Date(program.deadline).toLocaleDateString()}
                    </div>
                  </div>
                  
                  <div className="border-t pt-4 mb-4">
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Requirements:</h4>
                    <div className="space-y-1 text-sm text-gray-600">
                      <div>SSC: {program.requirements.ssc}%</div>
                      <div>HSC: {program.requirements.hsc}%</div>
                      <div>Group: {program.requirements.group}</div>
                      <div>Test: {program.requirements.test}</div>
                    </div>
                  </div>
                  
                  <div className="flex space-x-2">
                    <Link
                      to={`/program/${program.id}`}
                      className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg text-sm font-medium transition-colors text-center"
                    >
                      View Details
                    </Link>
                    <button className="flex-1 border border-blue-600 text-blue-600 hover:bg-blue-50 py-2 px-4 rounded-lg text-sm font-medium transition-colors">
                      Contact
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'searches' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900">Recent Searches</h2>
            
            <div className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Search Query</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Results</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {recentSearches.map((search, index) => (
                      <tr key={index}>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900">{search.query}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {new Date(search.date).toLocaleDateString()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-600">
                            12 programs found
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <button className="text-blue-600 hover:text-blue-900 mr-3">Search Again</button>
                          <button className="text-gray-600 hover:text-gray-900">View Results</button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard; 
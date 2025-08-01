import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, MapPin, DollarSign, Calendar, Phone, Mail, Globe, Clock, Users, BookOpen } from 'lucide-react';

const ProgramDetail = () => {
  const { id } = useParams();
  const [program, setProgram] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate fetching program data
    setTimeout(() => {
      setProgram({
        id: id,
        name: "Bachelor of Science in Computer Science",
        university: {
          id: 1,
          name: "Lahore University of Management Sciences (LUMS)",
          city: "Lahore"
        },
        overview: "This program provides a comprehensive foundation in computer science, covering programming, algorithms, data structures, software engineering, and computer systems. Students develop strong problem-solving skills and gain hands-on experience through projects and internships.",
        degree_type: "BS",
        duration_years: 4,
        seats_available: 120,
        admission_test: "LUMS Admission Test",
        merit_based: true,
        career_prospects: "Graduates can pursue careers in software development, data science, artificial intelligence, cybersecurity, and IT consulting. Many alumni work at top tech companies globally.",
        min_ssc_pct: 70,
        min_hsc_pct: 75,
        required_group: "Pre-Engineering",
        annual_fees: 850000,
        application_deadline: "2024-03-15",
        classes_start: "2024-09-01",
        contact_email: "admissions@lums.edu.pk",
        contact_phone: "+92-42-35608000",
        website_url: "https://lums.edu.pk",
        courses: [
          { code: "CS101", name: "Introduction to Programming", credits: 3, semester: 1 },
          { code: "CS102", name: "Data Structures", credits: 3, semester: 2 },
          { code: "CS201", name: "Algorithms", credits: 3, semester: 3 },
          { code: "CS202", name: "Database Systems", credits: 3, semester: 4 },
          { code: "CS301", name: "Software Engineering", credits: 3, semester: 5 },
          { code: "CS302", name: "Computer Networks", credits: 3, semester: 6 },
          { code: "CS401", name: "Artificial Intelligence", credits: 3, semester: 7 },
          { code: "CS402", name: "Final Year Project", credits: 6, semester: 8 }
        ],
        fee_structure: [
          { component: "Tuition Fee", amount: 650000, frequency: "Annual" },
          { component: "Registration Fee", amount: 25000, frequency: "One-time" },
          { component: "Laboratory Fee", amount: 50000, frequency: "Annual" },
          { component: "Library Fee", amount: 15000, frequency: "Annual" },
          { component: "Student Activity Fee", amount: 10000, frequency: "Annual" },
          { component: "Hostel Fee", amount: 120000, frequency: "Annual" }
        ]
      });
      setLoading(false);
    }, 1000);
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
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
          <p className="text-xl text-gray-600">{program.university.name}</p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Overview */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Overview</h2>
              <p className="text-gray-700 leading-relaxed">{program.overview}</p>
            </div>

            {/* Eligibility */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Eligibility</h2>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="flex items-center">
                  <BookOpen className="w-5 h-5 text-blue-600 mr-3" />
                  <div>
                    <p className="text-sm text-gray-600">Minimum SSC Score</p>
                    <p className="font-medium">{program.min_ssc_pct}%</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <BookOpen className="w-5 h-5 text-blue-600 mr-3" />
                  <div>
                    <p className="text-sm text-gray-600">Minimum HSC Score</p>
                    <p className="font-medium">{program.min_hsc_pct}%</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <Users className="w-5 h-5 text-blue-600 mr-3" />
                  <div>
                    <p className="text-sm text-gray-600">Required Group</p>
                    <p className="font-medium">{program.required_group}</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <Clock className="w-5 h-5 text-blue-600 mr-3" />
                  <div>
                    <p className="text-sm text-gray-600">Duration</p>
                    <p className="font-medium">{program.duration_years} Years</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Courses */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Courses</h2>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-3 px-4 font-medium text-gray-900">Code</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900">Course Name</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900">Credits</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900">Semester</th>
                    </tr>
                  </thead>
                  <tbody>
                    {program.courses.map((course, index) => (
                      <tr key={index} className="border-b border-gray-100">
                        <td className="py-3 px-4 text-sm font-medium text-gray-900">{course.code}</td>
                        <td className="py-3 px-4 text-sm text-gray-700">{course.name}</td>
                        <td className="py-3 px-4 text-sm text-gray-700">{course.credits}</td>
                        <td className="py-3 px-4 text-sm text-gray-700">{course.semester}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Fee Structure */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Fee Structure</h2>
              <div className="space-y-3">
                {program.fee_structure.map((fee, index) => (
                  <div key={index} className="flex justify-between items-center py-2 border-b border-gray-100">
                    <div>
                      <p className="font-medium text-gray-900">{fee.component}</p>
                      <p className="text-sm text-gray-600">{fee.frequency}</p>
                    </div>
                    <p className="font-semibold text-gray-900">PKR {fee.amount.toLocaleString()}</p>
                  </div>
                ))}
                <div className="flex justify-between items-center py-3 border-t-2 border-gray-200">
                  <p className="font-bold text-lg text-gray-900">Total Annual Cost</p>
                  <p className="font-bold text-lg text-blue-600">PKR {program.annual_fees.toLocaleString()}</p>
                </div>
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
                  <span className="text-sm text-gray-700">{program.university.city}</span>
                </div>
                <div className="flex items-center">
                  <DollarSign className="w-4 h-4 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-700">PKR {program.annual_fees.toLocaleString()}/year</span>
                </div>
                <div className="flex items-center">
                  <Users className="w-4 h-4 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-700">{program.seats_available} seats available</span>
                </div>
                <div className="flex items-center">
                  <Clock className="w-4 h-4 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-700">{program.duration_years} years duration</span>
                </div>
              </div>
            </div>

            {/* Application Deadlines */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Application Deadlines</h3>
              <div className="space-y-3">
                <div className="flex items-center">
                  <Calendar className="w-4 h-4 text-red-500 mr-3" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Application Deadline</p>
                    <p className="text-sm text-gray-600">{new Date(program.application_deadline).toLocaleDateString()}</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <Calendar className="w-4 h-4 text-green-500 mr-3" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Classes Start</p>
                    <p className="text-sm text-gray-600">{new Date(program.classes_start).toLocaleDateString()}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Contact Information */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Contact Information</h3>
              <div className="space-y-3">
                <div className="flex items-center">
                  <Phone className="w-4 h-4 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-700">{program.contact_phone}</span>
                </div>
                <div className="flex items-center">
                  <Mail className="w-4 h-4 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-700">{program.contact_email}</span>
                </div>
                <div className="flex items-center">
                  <Globe className="w-4 h-4 text-gray-400 mr-3" />
                  <a href={program.website_url} target="_blank" rel="noopener noreferrer" className="text-sm text-blue-600 hover:text-blue-700">
                    Visit Website
                  </a>
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="space-y-3">
                <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-lg font-medium transition-colors">
                  Apply Now
                </button>
                <button className="w-full border border-blue-600 text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors">
                  Save Program
                </button>
                <Link
                  to={`/university/${program.university.id}`}
                  className="w-full border border-gray-300 text-gray-700 hover:bg-gray-50 py-3 px-4 rounded-lg font-medium transition-colors inline-block text-center"
                >
                  View University
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
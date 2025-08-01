import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, MapPin, Phone, Mail, Globe, Users, Calendar, Award, Building, Wifi, Car, BookOpen, Instagram, Facebook, Twitter, Linkedin } from 'lucide-react';

const UniversityDetail = () => {
  const { id } = useParams();
  const [university, setUniversity] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate fetching university data
    setTimeout(() => {
      setUniversity({
        id: id,
        name: "Lahore University of Management Sciences (LUMS)",
        city: "Lahore",
        province: "Punjab",
        established_year: 1985,
        university_type: "Private",
        hec_recognized: true,
        about: "LUMS is Pakistan's premier university, known for its academic excellence and research contributions. Founded in 1985, it has consistently ranked among the top universities in Pakistan and South Asia. The university offers undergraduate, graduate, and doctoral programs across various disciplines.",
        campus_life: "LUMS provides a vibrant campus life with over 50 student organizations, cultural events, sports facilities, and leadership opportunities. Students enjoy a diverse community with international students from various countries.",
        facilities: [
          "Modern Library with 500,000+ books",
          "State-of-the-art Computer Labs",
          "Sports Complex with Indoor/Outdoor facilities",
          "Student Center with Cafeteria",
          "Medical Center",
          "Banking Services",
          "Transportation Services",
          "WiFi across campus"
        ],
        notable_alumni: [
          { name: "Dr. Ayesha Khan", position: "CEO, TechCorp", year: "2010" },
          { name: "Ahmed Hassan", position: "Senior Engineer, Google", year: "2012" },
          { name: "Fatima Ali", position: "Investment Banker, JP Morgan", year: "2015" },
          { name: "Usman Malik", position: "Founder, StartupXYZ", year: "2018" }
        ],
        contact_email: "info@lums.edu.pk",
        contact_phone: "+92-42-35608000",
        website_url: "https://lums.edu.pk",
        address: "DHA, Lahore Cantt, Lahore, Punjab 54792",
        social_media: {
          facebook: "https://facebook.com/lums",
          twitter: "https://twitter.com/lums",
          instagram: "https://instagram.com/lums",
          linkedin: "https://linkedin.com/company/lums"
        },
        programs: [
          { id: 1, name: "BS Computer Science", duration: "4 years", fees: 850000 },
          { id: 2, name: "BS Electrical Engineering", duration: "4 years", fees: 800000 },
          { id: 3, name: "BS Business Administration", duration: "4 years", fees: 750000 },
          { id: 4, name: "BS Economics", duration: "4 years", fees: 700000 }
        ],
        gallery: [
          "https://via.placeholder.com/400x300/4F46E5/FFFFFF?text=Main+Campus",
          "https://via.placeholder.com/400x300/7C3AED/FFFFFF?text=Library",
          "https://via.placeholder.com/400x300/059669/FFFFFF?text=Sports+Complex",
          "https://via.placeholder.com/400x300/DC2626/FFFFFF?text=Student+Center"
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
            <span>{university.city}, {university.province}</span>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* About */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">About</h2>
              <p className="text-gray-700 leading-relaxed mb-4">{university.about}</p>
              <div className="grid md:grid-cols-3 gap-4 text-sm">
                <div className="flex items-center">
                  <Calendar className="w-4 h-4 text-blue-600 mr-2" />
                  <span className="text-gray-600">Established: {university.established_year}</span>
                </div>
                <div className="flex items-center">
                  <Building className="w-4 h-4 text-blue-600 mr-2" />
                  <span className="text-gray-600">Type: {university.university_type}</span>
                </div>
                <div className="flex items-center">
                  <Award className="w-4 h-4 text-blue-600 mr-2" />
                  <span className="text-gray-600">HEC Recognized: {university.hec_recognized ? 'Yes' : 'No'}</span>
                </div>
              </div>
            </div>

            {/* Campus Life */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Campus Life</h2>
              <p className="text-gray-700 leading-relaxed">{university.campus_life}</p>
            </div>

            {/* Facilities */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Facilities</h2>
              <div className="grid md:grid-cols-2 gap-4">
                {university.facilities.map((facility, index) => (
                  <div key={index} className="flex items-center">
                    <div className="w-2 h-2 bg-blue-600 rounded-full mr-3"></div>
                    <span className="text-gray-700">{facility}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Notable Alumni */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Notable Alumni</h2>
              <div className="grid md:grid-cols-2 gap-4">
                {university.notable_alumni.map((alumni, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <h3 className="font-semibold text-gray-900">{alumni.name}</h3>
                    <p className="text-gray-600 text-sm">{alumni.position}</p>
                    <p className="text-gray-500 text-xs">Class of {alumni.year}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Programs */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Programs Offered</h2>
              <div className="space-y-3">
                {university.programs.map((program) => (
                  <div key={program.id} className="flex justify-between items-center p-3 border border-gray-200 rounded-lg">
                    <div>
                      <h3 className="font-medium text-gray-900">{program.name}</h3>
                      <p className="text-sm text-gray-600">{program.duration}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-medium text-gray-900">PKR {program.fees.toLocaleString()}</p>
                      <p className="text-sm text-gray-600">per year</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Gallery */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Gallery</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {university.gallery.map((image, index) => (
                  <div key={index} className="aspect-w-4 aspect-h-3">
                    <img 
                      src={image} 
                      alt={`Campus ${index + 1}`}
                      className="w-full h-32 object-cover rounded-lg"
                    />
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
                  <span className="text-sm text-gray-700">{university.address}</span>
                </div>
                <div className="flex items-center">
                  <Phone className="w-4 h-4 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-700">{university.contact_phone}</span>
                </div>
                <div className="flex items-center">
                  <Mail className="w-4 h-4 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-700">{university.contact_email}</span>
                </div>
                <div className="flex items-center">
                  <Globe className="w-4 h-4 text-gray-400 mr-3" />
                  <a href={university.website_url} target="_blank" rel="noopener noreferrer" className="text-sm text-blue-600 hover:text-blue-700">
                    Visit Website
                  </a>
                </div>
              </div>
            </div>

            {/* Social Media */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Follow Us</h3>
              <div className="space-y-3">
                <a href={university.social_media.facebook} target="_blank" rel="noopener noreferrer" className="flex items-center text-blue-600 hover:text-blue-700">
                  <Facebook className="w-4 h-4 mr-3" />
                  <span className="text-sm">Facebook</span>
                </a>
                <a href={university.social_media.twitter} target="_blank" rel="noopener noreferrer" className="flex items-center text-blue-400 hover:text-blue-500">
                  <Twitter className="w-4 h-4 mr-3" />
                  <span className="text-sm">Twitter</span>
                </a>
                <a href={university.social_media.instagram} target="_blank" rel="noopener noreferrer" className="flex items-center text-pink-600 hover:text-pink-700">
                  <Instagram className="w-4 h-4 mr-3" />
                  <span className="text-sm">Instagram</span>
                </a>
                <a href={university.social_media.linkedin} target="_blank" rel="noopener noreferrer" className="flex items-center text-blue-700 hover:text-blue-800">
                  <Linkedin className="w-4 h-4 mr-3" />
                  <span className="text-sm">LinkedIn</span>
                </a>
              </div>
            </div>

            {/* Location */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Location</h3>
              <div className="bg-gray-200 rounded-lg h-48 flex items-center justify-center">
                <div className="text-center text-gray-500">
                  <MapPin className="w-8 h-8 mx-auto mb-2" />
                  <p className="text-sm">Map View</p>
                </div>
              </div>
              <p className="text-sm text-gray-600 mt-3">{university.address}</p>
            </div>

            {/* Actions */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="space-y-3">
                <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-lg font-medium transition-colors">
                  Apply Now
                </button>
                <button className="w-full border border-blue-600 text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors">
                  Save University
                </button>
                <a href={university.website_url} target="_blank" rel="noopener noreferrer" className="w-full border border-gray-300 text-gray-700 hover:bg-gray-50 py-3 px-4 rounded-lg font-medium transition-colors inline-block text-center">
                  Visit Website
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UniversityDetail; 
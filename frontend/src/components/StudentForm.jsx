import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, Check, AlertCircle, Move, Trash2 } from 'lucide-react';

const StudentForm = ({ onSubmit }) => {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    sscPercentage: '',
    hscPercentage: '',
    qualificationType: '',
    hscGroup: '',
    interestPriorities: [], // Changed from interests to interestPriorities
    budget: '',
    preferredLocation: ''
  });

  const qualificationTypes = [
    'SSC/O-Level',
    'HSC/A-Level',
    'IB Diploma',
    'Other'
  ];

  const hscGroups = [
    'Pre-Engineering',
    'Pre-Medical',
    'ICS (Computer Science)',
    'ICom (Commerce)',
    'IA (Arts)',
    'Other'
  ];

  // Define subject-based interest restrictions based on official NED prospectus criteria
  const subjectRestrictions = {
    'Pre-Engineering': [
      // Pre-Engineering: Eligible for ALL programs (most versatile group)
      // According to prospectus: Eligible for all disciplines available within their academic group
      'accounting', 'aerospace-engineering', 'agriculture', 'architecture', 'artificial-intelligence', 'avionics',
      'bba', 'bioinformatics', 'biomedical-engineering', 'biotechnology', 'business',
      'chemical-engineering', 'chemistry', 'civil-engineering', 'computational-finance', 'computer-engineering',
      'computer-science', 'computer-systems', 'cyber-security', 'data-science', 'development-studies', 'dietetics',
      'economics', 'electrical-engineering', 'electronic-engineering', 'engineering', 'english-linguistics',
      'english-literature', 'environmental-engineering', 'environmental-science', 'finance', 'food-engineering',
      'food-science', 'gaming-animation', 'geoinformatics', 'health-sciences', 'hospitality-management', 'humanities',
      'industrial-design', 'industrial-manufacturing', 'information-security', 'law', 'llb', 'management-sciences',
      'mass-communication', 'materials-engineering', 'mathematics', 'mbbs', 'mechanical-engineering', 'mechatronics',
      'medicine', 'metallurgical-engineering', 'metallurgy', 'natural-sciences', 'naval-architecture', 'nutrition',
      'petrochemical-engineering', 'petroleum-engineering', 'physics', 'polymer-engineering', 'psychology',
      'public-administration', 'social-sciences', 'software-engineering', 'telecommunications', 'textile-sciences', 'tourism'
    ],
    'ICS (Computer Science)': [
      // ICS: Eligible for BS programs + Computer Science + Architecture (NO Engineering)
      // According to prospectus: NOT eligible for Engineering programs
      'accounting', 'architecture', 'artificial-intelligence', 'bba', 'bioinformatics', 'biotechnology', 'business',
      'chemistry', 'computational-finance', 'computer-science', 'computer-systems', 'cyber-security', 'data-science',
      'development-studies', 'dietetics', 'economics', 'english-linguistics', 'english-literature', 'environmental-science',
      'finance', 'food-science', 'gaming-animation', 'health-sciences', 'hospitality-management', 'humanities',
      'industrial-design', 'information-security', 'law', 'llb', 'management-sciences', 'mass-communication',
      'mathematics', 'mbbs', 'medicine', 'natural-sciences', 'nutrition', 'physics', 'psychology',
      'public-administration', 'social-sciences', 'software-engineering', 'telecommunications', 'tourism'
    ],
    'Pre-Medical': [
      // Pre-Medical: Eligible for BS programs + Biomedical Engineering only
      // According to prospectus: NOT eligible for other Engineering, CS, or Management Sciences
      'biomedical-engineering', 'biotechnology', 'chemistry', 'computational-finance', 'development-studies',
      'dietetics', 'economics', 'english-linguistics', 'english-literature', 'environmental-science',
      'finance', 'food-science', 'health-sciences', 'humanities', 'law', 'llb', 'mass-communication',
      'mathematics', 'mbbs', 'medicine', 'natural-sciences', 'nutrition', 'physics', 'psychology',
      'public-administration', 'social-sciences'
    ],
    'ICom (Commerce)': [
      // Commerce: Eligible for Management Sciences, Economics & Finance, English Linguistics, Development Studies
      // According to prospectus: NOT eligible for Engineering, CS, Computational Finance, or Physics
      'accounting', 'bba', 'business', 'development-studies', 'economics', 'english-linguistics', 'english-literature',
      'finance', 'hospitality-management', 'humanities', 'law', 'llb', 'management-sciences', 'mass-communication',
      'psychology', 'public-administration', 'social-sciences', 'tourism'
    ],
    'IA (Arts)': [
      // Arts: Eligible for Management Sciences, Economics & Finance, English Linguistics, Development Studies
      // According to prospectus: NOT eligible for Engineering, CS, Computational Finance, or Physics
      'accounting', 'bba', 'business', 'development-studies', 'economics', 'english-linguistics', 'english-literature',
      'finance', 'hospitality-management', 'humanities', 'law', 'llb', 'management-sciences', 'mass-communication',
      'psychology', 'public-administration', 'social-sciences', 'tourism'
    ],
    'Other': [
      // Default interests for students with unspecified HSC group
      'accounting', 'aerospace-engineering', 'agriculture', 'architecture', 'artificial-intelligence', 'avionics',
      'bba', 'bioinformatics', 'biomedical-engineering', 'biotechnology', 'business',
      'chemical-engineering', 'chemistry', 'civil-engineering', 'computational-finance', 'computer-engineering',
      'computer-science', 'computer-systems', 'cyber-security', 'data-science', 'development-studies', 'dietetics',
      'economics', 'electrical-engineering', 'electronic-engineering', 'engineering', 'english-linguistics',
      'english-literature', 'environmental-engineering', 'environmental-science', 'finance', 'food-engineering',
      'food-science', 'gaming-animation', 'geoinformatics', 'health-sciences', 'hospitality-management', 'humanities',
      'industrial-design', 'industrial-manufacturing', 'information-security', 'law', 'llb', 'management-sciences',
      'mass-communication', 'materials-engineering', 'mathematics', 'mbbs', 'mechanical-engineering', 'mechatronics',
      'medicine', 'metallurgical-engineering', 'metallurgy', 'natural-sciences', 'naval-architecture', 'nutrition',
      'petrochemical-engineering', 'petroleum-engineering', 'physics', 'polymer-engineering', 'psychology',
      'public-administration', 'social-sciences', 'software-engineering', 'telecommunications', 'textile-sciences', 'tourism'
    ]
  };

  const locations = [
    'Karachi',
    'Lahore',
    'Islamabad',
    'Rawalpindi',
    'Faisalabad',
    'Multan',
    'Peshawar',
    'Quetta',
    'Hyderabad',
    'Other'
  ];

  // Get available interests based on selected HSC group
  const getAvailableInterests = () => {
    return subjectRestrictions[formData.hscGroup] || subjectRestrictions['Other'];
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));

    // Clear interests when HSC group changes
    if (field === 'hscGroup') {
      setFormData(prev => ({
        ...prev,
        [field]: value,
        interestPriorities: [] // Clear interests when HSC group changes
      }));
    }
  };

  const handleInterestToggle = (interest) => {
    setFormData(prev => {
      const existingIndex = prev.interestPriorities.findIndex(item => item.interest === interest);
      
      if (existingIndex !== -1) {
        // Remove if already selected
        return {
          ...prev,
          interestPriorities: prev.interestPriorities.filter(item => item.interest !== interest)
        };
      } else {
        // Add with next priority number
        const newPriority = prev.interestPriorities.length + 1;
        return {
          ...prev,
          interestPriorities: [...prev.interestPriorities, { interest, priority: newPriority }]
        };
      }
    });
  };

  const moveInterest = (index, direction) => {
    setFormData(prev => {
      const newPriorities = [...prev.interestPriorities];
      const newIndex = direction === 'up' ? index - 1 : index + 1;
      
      if (newIndex >= 0 && newIndex < newPriorities.length) {
        // Swap priorities
        [newPriorities[index].priority, newPriorities[newIndex].priority] = 
        [newPriorities[newIndex].priority, newPriorities[index].priority];
        
        // Sort by priority
        newPriorities.sort((a, b) => a.priority - b.priority);
      }
      
      return {
        ...prev,
        interestPriorities: newPriorities
      };
    });
  };

  const removeInterest = (interest) => {
    setFormData(prev => {
      const newPriorities = prev.interestPriorities.filter(item => item.interest !== interest);
      // Reorder priorities
      newPriorities.forEach((item, index) => {
        item.priority = index + 1;
      });
      
      return {
        ...prev,
        interestPriorities: newPriorities
      };
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Convert qualification type to match database schema
    const processedData = {
      ...formData,
      // Map qualification types to database score types
      scoreType: formData.qualificationType === 'IB Diploma' ? 'ibcc' : 'ssc_hsc',
      // Extract just the interest names for backward compatibility
      interests: formData.interestPriorities.map(item => item.interest)
    };
    
    onSubmit(processedData);
    navigate('/results');
  };

  const isStepValid = () => {
    switch (currentStep) {
      case 1:
        return formData.sscPercentage && formData.hscPercentage && formData.qualificationType;
      case 2:
        return formData.hscGroup;
      case 3:
        return formData.interestPriorities.length > 0;
      case 4:
        return formData.budget && formData.preferredLocation;
      default:
        return false;
    }
  };

  const nextStep = () => {
    if (isStepValid() && currentStep < 4) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-2xl">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            {[1, 2, 3, 4].map((step) => (
              <div key={step} className="flex items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  step <= currentStep ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-600'
                }`}>
                  {step < currentStep ? <Check className="w-4 h-4" /> : step}
                </div>
                {step < 4 && (
                  <div className={`w-16 h-1 mx-2 ${
                    step < currentStep ? 'bg-blue-600' : 'bg-gray-200'
                  }`} />
                )}
              </div>
            ))}
          </div>
          <div className="text-center text-sm text-gray-600">
            Step {currentStep} of 4
          </div>
        </div>

        {/* Form */}
        <div className="bg-white rounded-lg shadow-md p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Academic Qualifications</h2>
          
          <form onSubmit={handleSubmit}>
            {/* Step 1: Basic Academic Info */}
            {currentStep === 1 && (
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    SSC/O-Level Percentage
                  </label>
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={formData.sscPercentage}
                    onChange={(e) => handleInputChange('sscPercentage', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter your SSC/O-Level percentage"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    HSC/A-Level/IB Percentage
                  </label>
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={formData.hscPercentage}
                    onChange={(e) => handleInputChange('hscPercentage', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter your HSC/A-Level/IB percentage"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Qualification Type
                  </label>
                  <select
                    value={formData.qualificationType}
                    onChange={(e) => handleInputChange('qualificationType', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Select qualification type</option>
                    {qualificationTypes.map(type => (
                      <option key={type} value={type}>{type}</option>
                    ))}
                  </select>
                </div>
              </div>
            )}

            {/* Step 2: HSC Group */}
            {currentStep === 2 && (
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    HSC Group/Subject Combination
                  </label>
                  <select
                    value={formData.hscGroup}
                    onChange={(e) => handleInputChange('hscGroup', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Select your HSC group</option>
                    {hscGroups.map(group => (
                      <option key={group} value={group}>{group}</option>
                    ))}
                  </select>
                </div>

                {formData.hscGroup && (
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <div className="flex items-start">
                      <AlertCircle className="w-5 h-5 text-blue-600 mr-2 mt-0.5" />
                      <div>
                        <h4 className="text-sm font-medium text-blue-900 mb-1">
                          Subject Compatibility
                        </h4>
                        <p className="text-sm text-blue-700">
                          Based on your {formData.hscGroup} background, you'll be able to select from relevant fields in the next step.
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Step 3: Interests */}
            {currentStep === 3 && (
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-4">
                    Select and Rank Your Interests by Priority
                  </label>
                  
                  {formData.hscGroup && (
                    <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                      <p className="text-sm text-green-700">
                        <strong>Available fields for {formData.hscGroup}:</strong> 
                        {getAvailableInterests().join(', ')}
                      </p>
                    </div>
                  )}
                  
                  {/* Available Interests */}
                  <div className="mb-6">
                    <h4 className="text-sm font-medium text-gray-700 mb-3">Available Interests</h4>
                    <div className="grid grid-cols-2 gap-3">
                      {getAvailableInterests().map(interest => (
                        <label key={interest} className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50">
                          <input
                            type="checkbox"
                            checked={formData.interestPriorities.some(item => item.interest === interest)}
                            onChange={() => handleInterestToggle(interest)}
                            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                          />
                          <span className="text-sm text-gray-700">{interest}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                  
                  {/* Priority Ranking */}
                  {formData.interestPriorities.length > 0 && (
                    <div className="mt-6">
                      <h4 className="text-sm font-medium text-gray-700 mb-3">Your Priority Ranking</h4>
                      <div className="space-y-2">
                        {formData.interestPriorities.map((item, index) => (
                          <div key={item.interest} className="flex items-center justify-between p-3 bg-blue-50 border border-blue-200 rounded-lg">
                            <div className="flex items-center space-x-3">
                              <span className="w-6 h-6 bg-blue-600 text-white text-xs rounded-full flex items-center justify-center font-medium">
                                {item.priority}
                              </span>
                              <span className="text-sm font-medium text-gray-700">{item.interest}</span>
                            </div>
                            <div className="flex items-center space-x-2">
                              <button
                                type="button"
                                onClick={() => moveInterest(index, 'up')}
                                disabled={index === 0}
                                className={`p-1 rounded ${index === 0 ? 'text-gray-300' : 'text-gray-600 hover:text-blue-600'}`}
                              >
                                ↑
                              </button>
                              <button
                                type="button"
                                onClick={() => moveInterest(index, 'down')}
                                disabled={index === formData.interestPriorities.length - 1}
                                className={`p-1 rounded ${index === formData.interestPriorities.length - 1 ? 'text-gray-300' : 'text-gray-600 hover:text-blue-600'}`}
                              >
                                ↓
                              </button>
                              <button
                                type="button"
                                onClick={() => removeInterest(item.interest)}
                                className="p-1 text-red-600 hover:text-red-700 rounded"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                            </div>
                          </div>
                        ))}
                      </div>
                      <div className="mt-3 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                        <p className="text-sm text-blue-700">
                          <strong>Priority order:</strong> {formData.interestPriorities.map(item => item.interest).join(' → ')}
                        </p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Step 4: Budget and Location */}
            {currentStep === 4 && (
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Annual Budget (PKR)
                  </label>
                  <input
                    type="number"
                    min="0"
                    value={formData.budget}
                    onChange={(e) => handleInputChange('budget', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter your annual budget in PKR"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Preferred Location
                  </label>
                  <select
                    value={formData.preferredLocation}
                    onChange={(e) => handleInputChange('preferredLocation', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Select preferred location</option>
                    {locations.map(location => (
                      <option key={location} value={location}>{location}</option>
                    ))}
                  </select>
                </div>
              </div>
            )}

            {/* Navigation Buttons */}
            <div className="flex justify-between mt-8">
              {currentStep > 1 && (
                <button
                  type="button"
                  onClick={prevStep}
                  className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Previous
                </button>
              )}
              
              <div className="ml-auto">
                {currentStep < 4 ? (
                  <button
                    type="button"
                    onClick={nextStep}
                    disabled={!isStepValid()}
                    className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
                  >
                    Next
                    <ArrowRight className="w-4 h-4" />
                  </button>
                ) : (
                  <button
                    type="submit"
                    disabled={!isStepValid()}
                    className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
                  >
                    Find Programs
                    <ArrowRight className="w-4 h-4" />
                  </button>
                )}
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default StudentForm;
import React, { useState } from 'react';
import formSchema from './form-schema.json';
import './UdyamForm.css';

function UdyamForm() {
  const [formData, setFormData] = useState({});
  const [errors, setErrors] = useState({});
  const [currentStep, setCurrentStep] = useState(1);

  const validateField = (name, value) => {
    switch (name) {
      case 'ctl00$ContentPlaceHolder1$txtadharno':
        if (value.length > 0 && value.length !== 12) {
          return 'Aadhaar Number must be 12 digits.';
        }
        break;
      case 'ctl00$ContentPlaceHolder1$txtownername':
        if (!value) { // Check if the value is empty
          return 'Name is required.';
        }
        break;
      case 'pincode':
        if (value.length > 0 && value.length !== 6) {
            return 'PIN Code must be 6 digits.';
        }
        break;
      default:
        break;
    }
    return ''; // Return an empty string if there's no error
  };

  const handlePinCodeChange = async (pinCode) => {
    if (pinCode.length === 6) {
      try {
        const response = await fetch(`https://api.postalpincode.in/pincode/${pinCode}`);
        const data = await response.json();

        if (data && data[0].Status === 'Success') {
          const postOffice = data[0].PostOffice[0];
          setFormData(prevData => ({
            ...prevData,
            city: postOffice.District,
            state: postOffice.State,
          }));
        } else {
          setFormData(prevData => ({ ...prevData, city: '', state: '' }));
        }
      } catch (error) {
        console.error("Failed to fetch PIN code data:", error);
      }
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    
    setFormData(prevData => ({ ...prevData, [name]: value }));

    const errorMessage = validateField(name, value);
    setErrors(prevErrors => ({ ...prevErrors, [name]: errorMessage }));

    if (name === 'pincode') {
      handlePinCodeChange(value);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/submit/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          aadhaar_number: formData['ctl00$ContentPlaceHolder1$txtadharno'],
          owner_name: formData['ctl00$ContentPlaceHolder1$txtownername'],
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`HTTP error! status: ${response.status} - ${JSON.stringify(errorData)}`);
      }

      const result = await response.json();
      console.log("Success:", result);
      
      setCurrentStep(2); // Move to the next step
    } catch (error) {
      console.error("Error submitting form:", error);
      alert(`Failed to submit form: ${error.message}`);
    }
  };

  const handleStartOver = () => {
    setFormData({});
    setErrors({});
    setCurrentStep(1);
  };

  return (
    <div className="form-container">
      <div className="progress-tracker">
        <div className={`step ${currentStep > 1 ? 'completed' : ''} ${currentStep >= 1 ? 'active' : ''}`}>
          <div className="step-number">1</div>
          <div className="step-label">Aadhaar Validation</div>
        </div>
        <div className="step-connector"></div>
        <div className={`step ${currentStep >= 2 ? 'active' : ''}`}>
          <div className="step-number">2</div>
          <div className="step-label">PAN Validation</div>
        </div>
      </div>

      {currentStep === 1 ? (
        <form onSubmit={handleSubmit}>
          <h2>Udyam Registration Form</h2>
          {formSchema.map((field) => (
            <div className="form-group" key={field.id}>
              <label htmlFor={field.id}>{field.label}</label>
              <input
                type={field.type}
                id={field.id}
                name={field.name}
                placeholder={field.placeholder}
                onChange={handleInputChange}
                value={formData[field.name] || ''}
                readOnly={field.name === 'city' || field.name === 'state'}
                maxLength={field.validation.maxLength}
                required={field.validation.required}
              />
              {errors[field.name] && <span className="error-message">{errors[field.name]}</span>}
            </div>
          ))}
          <button type="submit">Validate & Generate OTP</button>
        </form>
      ) : (
        <div className="success-message">
          <h2>✅ Submission Successful!</h2>
          <p>You have completed Step 1. The next step would be PAN Validation.</p>
          <button onClick={handleStartOver}>Start Over</button>
        </div>
      )}
    </div>
  );
}

export default UdyamForm;
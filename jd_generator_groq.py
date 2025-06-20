#!/usr/bin/env python3
"""
Medical Job Description Generator - Generate professional medical job descriptions using Groq AI
Specialized for medical staffing and healthcare roles in India
"""

import os
import json
from datetime import datetime

# Try to import Streamlit for secrets (when deployed)
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

# Try to import Groq dependencies
try:
    from langchain_groq import ChatGroq
    from langchain.schema import HumanMessage, SystemMessage
    GROQ_AVAILABLE = True
    print("✅ Groq dependencies available")
except ImportError as e:
    print(f"⚠️ Groq dependencies not available: {e}")
    GROQ_AVAILABLE = False

# Initialize Groq AI
def initialize_groq():
    """Initialize Groq with API key"""
    try:
        if not GROQ_AVAILABLE:
            return False, None
            
        # Try to get API key from Streamlit secrets (when deployed)
        api_key = None
        if STREAMLIT_AVAILABLE and hasattr(st, 'secrets'):
            try:
                if hasattr(st.secrets, 'GROQ_API_KEY'):
                    api_key = st.secrets.GROQ_API_KEY
                    print("✅ Groq API key loaded from Streamlit secrets")
            except Exception as e:
                print(f"⚠️ Streamlit secrets loading failed: {e}")
        
        # Fallback: try environment variable
        if not api_key:
            api_key = os.getenv('GROQ_API_KEY')
            if api_key:
                print("✅ Groq API key loaded from environment variable")
        
        # Last resort: use the provided key
        if not api_key:
            api_key = "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"
            print("✅ Using provided Groq API key")
        
        if api_key:
            # Test the connection
            llm = ChatGroq(
                model="llama-3.1-8b-instant",
                temperature=0,
                max_tokens=100,
                timeout=10,
                max_retries=1,
                groq_api_key=api_key
            )
            
            # Quick test
            test_message = [HumanMessage(content="Hello")]
            response = llm.invoke(test_message)
            print("✅ Groq AI initialized successfully")
            return True, api_key
        else:
            print("❌ No Groq API key found")
            return False, None
            
    except Exception as e:
        print(f"❌ Groq initialization failed: {e}")
        return False, None

# Initialize Groq
GROQ_INITIALIZED, GROQ_API_KEY = initialize_groq()

class MedicalJobDescriptionGenerator:
    def __init__(self):
        """Initialize the medical job description generator for India"""
        self.groq_available = GROQ_AVAILABLE and GROQ_INITIALIZED
        
        if self.groq_available:
            try:
                self.setup_agent()
                print("✅ Medical Job Description Generator (India) initialized with Groq AI")
            except Exception as e:
                print(f"❌ Groq setup failed: {e}")
                self.groq_available = False
                error_msg = f"❌ Groq setup failed: {str(e)}"
                if "api_key" in str(e).lower():
                    error_msg += "\n💡 Check your Groq API key in Streamlit secrets"
                elif "model" in str(e).lower():
                    error_msg += "\n💡 Check if the model name is correct"
                raise Exception(error_msg)
        else:
            error_msg = "❌ Groq AI not available"
            if not GROQ_AVAILABLE:
                error_msg += "\n💡 Groq libraries not installed properly"
            elif not GROQ_INITIALIZED:
                error_msg += "\n💡 Groq initialization failed - check API key"
            raise Exception(error_msg)
    
    def setup_agent(self):
        """Setup the medical job description agent using Groq"""
        try:
            # Initialize Groq LLM
            self.llm = ChatGroq(
                model="llama-3.1-8b-instant",
                temperature=0.28,
                max_tokens=15000,  # Optimized for speed
                timeout=30,  # 30 second timeout
                max_retries=1,  # Only 1 retry for speed
                groq_api_key=GROQ_API_KEY
            )
            
            print("✅ Groq LLM initialized successfully")
            
        except Exception as e:
            print(f"❌ Error setting up Groq agent: {e}")
            raise

    def generate_medical_job_description(self, job_requirements):
        """Generate a comprehensive medical job description using Groq AI for Indian healthcare"""
        try:
            # Check if this is an enhanced prompt (from simple app)
            enhanced_prompt = job_requirements.get('enhanced_prompt', '')
            
            print(f"🏥 Generating medical job description with Groq AI...")
            
            # Create comprehensive medical job description prompt for India
            if enhanced_prompt:
                # Use the enhanced prompt from simple app
                medical_job_prompt = enhanced_prompt
            else:
                # Create detailed prompt for India-specific medical job description
                medical_job_prompt = f"""You are a specialized medical staffing professional and healthcare HR expert in India. Create a comprehensive, compliant, and attractive job description for a medical/healthcare position in the Indian healthcare system.

MEDICAL JOB REQUIREMENTS (INDIA):
- Job Title: {job_requirements.get('job_title', '')}
- Healthcare Facility: {job_requirements.get('facility_name', '')}
- Facility Type: {job_requirements.get('facility_type', '')} (Hospital, Clinic, Nursing Home, Diagnostic Center, etc.)
- Department/Unit: {job_requirements.get('department', '')}
- Location: {job_requirements.get('location', '')}
- Shift Pattern: {job_requirements.get('shift_pattern', '')}
- Employment Type: {job_requirements.get('employment_type', 'Full-time')}
- Contract Type: {job_requirements.get('contract_type', '')}
- Salary/Rate Range: {job_requirements.get('salary_range', '')}
- Experience Level: {job_requirements.get('experience_level', '')}

INDIA-SPECIFIC MEDICAL REQUIREMENTS:
- Required Licenses: {', '.join(job_requirements.get('required_licenses', [])) if job_requirements.get('required_licenses') else 'Valid Indian medical registration'}
- Required Certifications: {', '.join(job_requirements.get('required_certifications', [])) if job_requirements.get('required_certifications') else 'As per Indian medical standards'}
- Specialty Requirements: {', '.join(job_requirements.get('specialty_requirements', [])) if job_requirements.get('specialty_requirements') else 'As per role requirements'}
- Patient Population: {job_requirements.get('patient_population', '')}
- EMR/EHR Systems: {', '.join(job_requirements.get('emr_systems', [])) if job_requirements.get('emr_systems') else 'Hospital management systems'}
- Compliance Requirements: {', '.join(job_requirements.get('compliance_requirements', [])) if job_requirements.get('compliance_requirements') else 'Indian healthcare regulations'}

KEY RESPONSIBILITIES: {', '.join(job_requirements.get('key_responsibilities', [])) if job_requirements.get('key_responsibilities') else 'Standard for role in Indian healthcare'}
QUALIFICATIONS: {', '.join(job_requirements.get('qualifications', [])) if job_requirements.get('qualifications') else 'As per Indian medical education standards'}
PREFERRED QUALIFICATIONS: {', '.join(job_requirements.get('preferred_qualifications', [])) if job_requirements.get('preferred_qualifications') else 'Additional relevant experience'}
BENEFITS: {', '.join(job_requirements.get('benefits', [])) if job_requirements.get('benefits') else 'Competitive benefits as per Indian standards'}

REQUIREMENTS FOR INDIAN MEDICAL JOB DESCRIPTION:
1. **PROFESSIONAL MEDICAL TONE**: Use appropriate medical terminology and professional language suitable for Indian healthcare
2. **COMPLIANCE-FOCUSED**: Emphasize licensing from State Medical Council/National Medical Commission (NMC), and regulatory requirements
3. **PATIENT-CENTERED**: Highlight patient care and safety priorities in Indian healthcare context
4. **CLEAR MEDICAL STRUCTURE**: Follow Indian healthcare industry standards for job descriptions
5. **SPECIALTY-SPECIFIC**: Tailor content to the specific medical role and specialty in Indian context
6. **REGULATORY AWARENESS**: Include relevant Indian healthcare regulations and standards
7. **ATTRACTIVE TO INDIAN MEDICAL PROFESSIONALS**: Appeal to healthcare workers' motivations in India

INDIAN MEDICAL JOB DESCRIPTION STRUCTURE:
- Position Title and Healthcare Facility Overview
- Mission and Values (patient care focus in Indian context)
- Position Summary (role impact on patient care in Indian healthcare system)
- Essential Functions/Clinical Responsibilities
- Required Licensure and Certifications (Indian medical registration)
- Education and Experience Requirements (Indian medical education)
- Preferred Qualifications and Specializations
- Physical and Mental Requirements
- Schedule and Work Environment
- Compensation and Benefits Package (Indian benefits structure)
- Professional Development Opportunities
- Application Process and Requirements

INDIA-SPECIFIC MEDICAL CONSIDERATIONS:
- Include patient safety and quality care emphasis for Indian healthcare
- Mention interdisciplinary collaboration in Indian hospital settings
- Address continuing medical education requirements as per NMC guidelines
- Include physical demands typical for Indian healthcare roles
- Emphasize compliance with Indian healthcare regulations (Clinical Establishments Act, Bio-Medical Waste Rules, etc.)
- Mention hospital management systems and EMR proficiency
- Include infection control and safety protocols as per Indian standards
- Use Indian Rupees (₹) for salary ranges
- Include Indian employment benefits (PF, ESI, Gratuity, Medical Insurance)
- Mention Indian working hours and shift patterns
- Include Indian medical council registration requirements

INDIAN EMPLOYMENT BENEFITS TO CONSIDER:
- Provident Fund (PF)
- Employee State Insurance (ESI)
- Gratuity
- Medical Insurance for employee and family
- Annual Leave as per Indian labor laws
- Festival bonuses
- Professional development and CME support
- Accommodation (if provided)
- Transportation allowance
- Meal facilities

OUTPUT FORMAT:
Create a professional, compliant medical job description that would attract qualified healthcare professionals in India and follows Indian medical education and registration standards."""

            print("🤖 Generating medical job description with Groq AI...")
            
            # Create messages for Groq
            messages = [
                SystemMessage(content="You are a specialized medical staffing professional and healthcare HR expert in India. Create comprehensive, compliant, and attractive job descriptions for medical/healthcare positions in the Indian healthcare system."),
                HumanMessage(content=medical_job_prompt)
            ]
            
            # Generate response using Groq
            response = self.llm.invoke(messages)
            
            if response and response.content:
                # Extract the generated job description
                job_description = response.content.strip()
                
                # Create structured response
                result = {
                    'job_description': job_description,
                    'generated_at': datetime.now().isoformat(),
                    'model_used': 'llama-3.1-8b-instant (Groq)',
                    'generation_time': 'Fast (Groq optimized)',
                    'compliance': 'Indian healthcare standards',
                    'format': 'Professional medical job description'
                }
                
                print("✅ Medical job description generated successfully with Groq AI")
                return result
            else:
                print("❌ Groq AI returned empty response")
                return None
                
        except Exception as e:
            print(f"❌ Error generating medical job description: {e}")
            raise Exception(f"❌ Failed to generate job description: {str(e)}")

    def extract_json_from_response(self, response_text):
        """Extract JSON from response text if present"""
        try:
            # Look for JSON in the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return None
        except Exception as e:
            print(f"⚠️ Could not extract JSON: {e}")
            return None

    def save_medical_job_description(self, job_data, output_dir="medical_job_descriptions"):
        """Save the generated job description to a file"""
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"medical_jd_{timestamp}.json"
            filepath = os.path.join(output_dir, filename)
            
            # Save to JSON file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(job_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Job description saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Error saving job description: {e}")
            return None

    def get_medical_role_templates(self):
        """Get common medical role templates for India"""
        return {
            "Staff Nurse": {
                "education": "B.Sc Nursing / GNM",
                "licenses": ["State Nursing Council Registration"],
                "experience": "1-5 years",
                "specialties": ["ICU", "Emergency", "OT", "Ward", "Pediatrics"]
            },
            "Medical Officer": {
                "education": "MBBS",
                "licenses": ["State Medical Council Registration"],
                "experience": "0-3 years",
                "specialties": ["General Medicine", "Emergency", "Rural Health"]
            },
            "Physiotherapist": {
                "education": "BPT / MPT",
                "licenses": ["State Physiotherapy Council Registration"],
                "experience": "1-3 years",
                "specialties": ["Orthopedic", "Neurological", "Sports", "Cardiopulmonary"]
            },
            "Radiologist": {
                "education": "MBBS + MD/DNB Radiology",
                "licenses": ["State Medical Council Registration"],
                "experience": "3-8 years",
                "specialties": ["Diagnostic Radiology", "Interventional Radiology"]
            }
        }

def main():
    """Test the medical job description generator"""
    try:
        generator = MedicalJobDescriptionGenerator()
        
        # Test with a sample job requirement
        test_requirements = {
            'job_title': 'Staff Nurse ICU',
            'facility_name': 'Apollo Hospital',
            'location': 'Bangalore',
            'experience_level': '3 years',
            'enhanced_prompt': 'Create a job description for Staff Nurse ICU position at Apollo Hospital Bangalore with 3 years experience in critical care, B.Sc Nursing degree, salary range 4 to 6 lakhs per annum with PF ESI benefits.'
        }
        
        result = generator.generate_medical_job_description(test_requirements)
        
        if result:
            print("✅ Test successful!")
            print(f"Generated job description length: {len(result['job_description'])} characters")
        else:
            print("❌ Test failed")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    main()

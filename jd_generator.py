#!/usr/bin/env python3
"""
Medical Job Description Generator - Generate professional medical job descriptions using Google Cloud AI
Specialized for medical staffing and healthcare roles in India
"""

import os
import json
from datetime import datetime

# Try to import Google Cloud dependencies with fallbacks
try:
    import vertexai
    from vertexai import agent_engines
    from langchain_google_vertexai import HarmBlockThreshold, HarmCategory
    GOOGLE_CLOUD_AVAILABLE = True
    print("✅ Google Cloud dependencies available")
except ImportError as e:
    print(f"⚠️ Google Cloud dependencies not available: {e}")
    GOOGLE_CLOUD_AVAILABLE = False

# Try specific Vertex AI imports
try:
    if GOOGLE_CLOUD_AVAILABLE:
        vertexai.init(
            project="theta-outrider-460308-k8",  # Replace with your project ID
            location="us-central1",
        )
        print("✅ Vertex AI initialized")
    VERTEX_AI_INITIALIZED = True
except Exception as e:
    print(f"⚠️ Vertex AI initialization failed: {e}")
    VERTEX_AI_INITIALIZED = False

class MedicalJobDescriptionGenerator:
    def __init__(self):
        """Initialize the medical job description generator for India"""
        self.google_cloud_available = GOOGLE_CLOUD_AVAILABLE and VERTEX_AI_INITIALIZED
        
        if self.google_cloud_available:
            try:
                self.setup_agent()
                print("✅ Medical Job Description Generator (India) initialized with Google Cloud AI")
            except Exception as e:
                print(f"❌ Google Cloud setup failed: {e}")
                self.google_cloud_available = False
                raise Exception("❌ Cannot proceed without Google Cloud AI")
        else:
            raise Exception("❌ Google Cloud AI not available - cannot generate AI responses")
    
    def setup_agent(self):
        """Setup the medical job description agent using LangchainAgent"""
        try:
            # Model configuration
            model = "gemini-2.0-flash"
            
            # Safety settings
            safety_settings = {
                HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            }
            
            # Model parameters - optimized for speed
            model_kwargs = {
                "temperature": 0.28,
                "max_output_tokens": 4000,  # Reduced for faster generation
                "top_p": 0.95,
                "top_k": None,
                "safety_settings": safety_settings,
            }
            
            # Initialize LangchainAgent
            self.agent = agent_engines.LangchainAgent(
                model=model,
                model_kwargs=model_kwargs,
            )
            
            print("✅ LangchainAgent initialized successfully")
            
        except Exception as e:
            print(f"❌ Error setting up AI agent: {e}")
            raise

    def generate_medical_job_description(self, job_requirements):
        """Generate a comprehensive medical job description using AI for Indian healthcare"""
        try:
            job_title = job_requirements.get('job_title', '')
            facility_name = job_requirements.get('facility_name', '')
            facility_type = job_requirements.get('facility_type', '')
            department = job_requirements.get('department', '')
            location = job_requirements.get('location', '')
            shift_pattern = job_requirements.get('shift_pattern', '')
            employment_type = job_requirements.get('employment_type', 'Full-time')
            contract_type = job_requirements.get('contract_type', '')
            salary_range = job_requirements.get('salary_range', '')
            experience_level = job_requirements.get('experience_level', '')
            
            # Medical-specific fields for India
            required_licenses = job_requirements.get('required_licenses', [])
            required_certifications = job_requirements.get('required_certifications', [])
            specialty_requirements = job_requirements.get('specialty_requirements', [])
            patient_population = job_requirements.get('patient_population', '')
            emr_systems = job_requirements.get('emr_systems', [])
            compliance_requirements = job_requirements.get('compliance_requirements', [])
            
            key_responsibilities = job_requirements.get('key_responsibilities', [])
            qualifications = job_requirements.get('qualifications', [])
            preferred_qualifications = job_requirements.get('preferred_qualifications', [])
            benefits = job_requirements.get('benefits', [])
            
            # Check if this is an enhanced prompt (from simple app)
            enhanced_prompt = job_requirements.get('enhanced_prompt', '')
            
            print(f"🏥 Generating medical job description for: '{job_title}' at {facility_name}")
            
            # Create comprehensive medical job description prompt for India
            if enhanced_prompt:
                # Use the enhanced prompt from simple app
                medical_job_prompt = enhanced_prompt
            else:
                # Create detailed prompt for India-specific medical job description
                medical_job_prompt = f"""You are a specialized medical staffing professional and healthcare HR expert in India. Create a comprehensive, compliant, and attractive job description for a medical/healthcare position in the Indian healthcare system.

MEDICAL JOB REQUIREMENTS (INDIA):
- Job Title: {job_title}
- Healthcare Facility: {facility_name}
- Facility Type: {facility_type} (Hospital, Clinic, Nursing Home, Diagnostic Center, etc.)
- Department/Unit: {department}
- Location: {location}
- Shift Pattern: {shift_pattern}
- Employment Type: {employment_type}
- Contract Type: {contract_type}
- Salary/Rate Range: {salary_range}
- Experience Level: {experience_level}

INDIA-SPECIFIC MEDICAL REQUIREMENTS:
- Required Licenses: {', '.join(required_licenses) if required_licenses else 'Valid Indian medical registration'}
- Required Certifications: {', '.join(required_certifications) if required_certifications else 'As per Indian medical standards'}
- Specialty Requirements: {', '.join(specialty_requirements) if specialty_requirements else 'As per role requirements'}
- Patient Population: {patient_population}
- EMR/EHR Systems: {', '.join(emr_systems) if emr_systems else 'Hospital management systems'}
- Compliance Requirements: {', '.join(compliance_requirements) if compliance_requirements else 'Indian healthcare regulations'}

KEY RESPONSIBILITIES: {', '.join(key_responsibilities) if key_responsibilities else 'Standard for role in Indian healthcare'}
QUALIFICATIONS: {', '.join(qualifications) if qualifications else 'As per Indian medical education standards'}
PREFERRED QUALIFICATIONS: {', '.join(preferred_qualifications) if preferred_qualifications else 'Additional relevant experience'}
BENEFITS: {', '.join(benefits) if benefits else 'Competitive benefits as per Indian standards'}

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
Generate a JSON object with the following structure:
{{
    "job_title": "{job_title}",
    "facility_name": "{facility_name}",
    "facility_type": "{facility_type}",
    "job_description": "Complete formatted medical job description with all sections for Indian healthcare",
    "summary": "Brief 2-3 sentence summary highlighting the medical role's impact in Indian healthcare",
    "required_credentials": ["Indian medical registration", "certification1", "qualification1"],
    "key_medical_keywords": ["medical_term1", "specialty1", "skill1", "system1", "compliance1"],
    "patient_care_focus": "Brief description of patient care responsibilities in Indian context",
    "compliance_highlights": ["Indian_regulation1", "standard1", "requirement1"]
}}

Generate a compelling medical job description for the Indian healthcare system that will attract qualified healthcare professionals while ensuring regulatory compliance with Indian medical standards:"""

            print("🤖 Generating medical job description with AI...")
            
            response = self.agent.query(input=medical_job_prompt)
            
            if not response or not response.get('output'):
                raise Exception("❌ AI agent returned empty response")
            
            ai_response = response['output']
            
            # Extract JSON from response
            job_description_data = self.extract_json_from_response(ai_response)
            
            if not job_description_data:
                # Fallback: create structured data from raw response
                job_description_data = {
                    "job_title": job_title,
                    "facility_name": facility_name,
                    "facility_type": facility_type,
                    "job_description": ai_response,
                    "summary": f"Healthcare opportunity: {job_title} at {facility_name}",
                    "required_credentials": required_licenses + required_certifications,
                    "key_medical_keywords": specialty_requirements[:5] if specialty_requirements else [],
                    "patient_care_focus": f"Providing quality care to {patient_population}" if patient_population else "Patient-centered care",
                    "compliance_highlights": compliance_requirements[:3] if compliance_requirements else ["Clinical Establishments Act", "Bio-Medical Waste Rules", "NMC Guidelines"]
                }
            
            print(f"✅ Medical job description generated: {len(job_description_data.get('job_description', ''))} characters")
            
            return job_description_data
            
        except Exception as e:
            print(f"❌ Error generating medical job description: {e}")
            return None

    def extract_json_from_response(self, response_text):
        """Extract JSON object from AI response"""
        try:
            import re
            # Try to find JSON using regex
            json_pattern = r'\{[\s\S]*\}'
            json_match = re.search(json_pattern, response_text)
            
            if json_match:
                return json.loads(json_match.group())
            else:
                return None
        except json.JSONDecodeError as e:
            print(f"⚠️ Error parsing JSON: {e}")
            return None
        except Exception as e:
            print(f"⚠️ Error extracting JSON: {e}")
            return None

    def save_medical_job_description(self, job_data, output_dir="medical_job_descriptions"):
        """Save medical job description to file"""
        try:
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Create filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            job_title_safe = job_data['job_title'].replace(' ', '_').replace('/', '_')
            facility_safe = job_data['facility_name'].replace(' ', '_').replace('/', '_')
            filename = f"medical_jd_{facility_safe}_{job_title_safe}_{timestamp}.json"
            filepath = os.path.join(output_dir, filename)
            
            # Add metadata
            job_data['generated_at'] = datetime.now().isoformat()
            job_data['generator_version'] = '2.0_medical_india'
            job_data['industry'] = 'healthcare'
            job_data['country'] = 'india'
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(job_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Medical job description saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Error saving medical job description: {e}")
            return None

    def get_medical_role_templates(self):
        """Get common medical role templates for India"""
        templates = {
            "registered_nurse": {
                "job_title": "Staff Nurse",
                "required_licenses": ["Valid Nursing Registration", "State Nursing Council Registration"],
                "required_certifications": ["GNM/B.Sc Nursing", "Basic Life Support"],
                "specialty_requirements": ["Medical-Surgical nursing experience"],
                "compliance_requirements": ["Clinical Establishments Act", "Bio-Medical Waste Rules", "Nursing Council guidelines"]
            },
            "medical_officer": {
                "job_title": "Medical Officer",
                "required_licenses": ["Valid Medical Registration", "State Medical Council Registration"],
                "required_certifications": ["MBBS degree", "Permanent/Provisional Registration"],
                "specialty_requirements": ["General medicine experience"],
                "compliance_requirements": ["Clinical Establishments Act", "NMC guidelines", "State medical regulations"]
            },
            "specialist_doctor": {
                "job_title": "Specialist Doctor",
                "required_licenses": ["Valid Medical Registration", "State Medical Council Registration"],
                "required_certifications": ["MBBS + MD/MS/DNB", "Specialty board certification"],
                "specialty_requirements": ["Specialty experience", "Post-graduate qualification"],
                "compliance_requirements": ["Clinical Establishments Act", "NMC guidelines", "Specialty board requirements"]
            },
            "physiotherapist": {
                "job_title": "Physiotherapist",
                "required_licenses": ["Valid Physiotherapy Registration", "State Council Registration"],
                "required_certifications": ["BPT/MPT degree", "Professional registration"],
                "specialty_requirements": ["Orthopedic or general physiotherapy experience"],
                "compliance_requirements": ["Clinical Establishments Act", "Physiotherapy Council guidelines"]
            },
            "pharmacist": {
                "job_title": "Pharmacist",
                "required_licenses": ["Valid Pharmacy Registration", "State Pharmacy Council Registration"],
                "required_certifications": ["D.Pharm/B.Pharm degree", "Professional registration"],
                "specialty_requirements": ["Hospital pharmacy experience"],
                "compliance_requirements": ["Drugs and Cosmetics Act", "Pharmacy Council guidelines"]
            }
        }
        return templates

def main():
    """Example usage of the Medical Job Description Generator for India"""
    print("🏥 Starting Medical Job Description Generator (India)")
    print("=" * 60)
    
    # Initialize generator
    try:
        generator = MedicalJobDescriptionGenerator()
    except Exception as e:
        print(f"❌ Failed to initialize generator: {e}")
        return
    
    # Example medical job requirements - Staff Nurse position in India
    medical_job_requirements = {
        'job_title': 'Staff Nurse - ICU',
        'facility_name': 'Apollo Hospitals',
        'facility_type': 'Multi-specialty Hospital',
        'department': 'Intensive Care Unit',
        'location': 'Bangalore, Karnataka',
        'shift_pattern': '12-hour shifts (Day/Night rotation)',
        'employment_type': 'Full-time',
        'contract_type': 'Permanent Position',
        'salary_range': '₹3,50,000 - ₹5,00,000 per annum',
        'experience_level': '2-4 years ICU experience',
        
        # India-specific medical requirements
        'required_licenses': [
            'Valid Nursing Registration with State Nursing Council',
            'Current Basic Life Support (BLS) certification'
        ],
        'required_certifications': [
            'GNM or B.Sc Nursing degree',
            'Critical Care Nursing certification preferred'
        ],
        'specialty_requirements': [
            'Critical care nursing experience',
            'Ventilator management knowledge',
            'Patient monitoring skills',
            'Emergency response capabilities'
        ],
        'patient_population': 'Adult ICU patients with critical medical conditions',
        'emr_systems': ['Hospital Information System', 'Patient monitoring systems'],
        'compliance_requirements': [
            'Clinical Establishments Act compliance',
            'Bio-Medical Waste Management Rules',
            'Nursing Council of India guidelines',
            'Hospital infection control protocols'
        ],
        
        'key_responsibilities': [
            'Provide comprehensive nursing care to ICU patients',
            'Monitor patient vital signs and conditions',
            'Administer medications as per physician orders',
            'Maintain accurate patient records and documentation',
            'Collaborate with medical team for patient care',
            'Educate patients and families about care plans',
            'Follow infection control and safety protocols'
        ],
        'qualifications': [
            'GNM or B.Sc Nursing from recognized institution',
            'Valid registration with State Nursing Council',
            '2-4 years of acute care nursing experience',
            'Strong clinical assessment and communication skills'
        ],
        'preferred_qualifications': [
            'Critical Care Nursing certification',
            'Experience with ventilated patients',
            'Advanced cardiac life support training',
            'Previous ICU experience in multi-specialty hospital'
        ],
        'benefits': [
            'Competitive salary with annual increments',
            'Provident Fund (PF) and Employee State Insurance (ESI)',
            'Medical insurance for employee and family',
            'Gratuity as per company policy',
            'Annual leave and sick leave',
            'Professional development opportunities',
            'Accommodation facilities (if required)',
            'Transportation allowance'
        ]
    }
    
    # Generate medical job description
    job_data = generator.generate_medical_job_description(medical_job_requirements)
    
    if job_data:
        # Save to file
        filepath = generator.save_medical_job_description(job_data)
        
        # Display summary
        print("\n" + "=" * 60)
        print("✅ MEDICAL JOB DESCRIPTION GENERATED SUCCESSFULLY!")
        print(f"🏥 Position: {job_data.get('job_title', '')}")
        print(f"🏢 Facility: {job_data.get('facility_name', '')}")
        print(f"🏥 Type: {job_data.get('facility_type', '')}")
        print(f"📄 Summary: {job_data.get('summary', '')}")
        print(f"🏥 Patient Care: {job_data.get('patient_care_focus', '')}")
        print(f"📜 Required Credentials: {', '.join(job_data.get('required_credentials', []))}")
        print(f"🔑 Medical Keywords: {', '.join(job_data.get('key_medical_keywords', []))}")
        print(f"⚖️ Compliance: {', '.join(job_data.get('compliance_highlights', []))}")
        print(f"💾 Saved to: {filepath}")
        print("=" * 60)
        
        # Show available templates
        print("\n🩺 Available Medical Role Templates (India):")
        templates = generator.get_medical_role_templates()
        for key, template in templates.items():
            print(f"  • {template['job_title']}")
        
    else:
        print("❌ Failed to generate medical job description")

if __name__ == "__main__":
    main() 
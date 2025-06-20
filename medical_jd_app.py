#!/usr/bin/env python3
"""
Medical Job Description Generator - Simple Streamlit App for Indian Healthcare
With Browser-Based Speech-to-Text Integration
"""

import streamlit as st
import re
from jd_generator import MedicalJobDescriptionGenerator
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Medical Job Description Generator - India",
    page_icon="🏥",
    layout="centered"
)

# Initialize session state
if 'generator' not in st.session_state:
    st.session_state.generator = None
if 'generated_jd' not in st.session_state:
    st.session_state.generated_jd = None
if 'speech_text' not in st.session_state:
    st.session_state.speech_text = ""

def initialize_generator():
    """Initialize the medical job description generator"""
    try:
        if st.session_state.generator is None:
            with st.spinner("🔄 Initializing AI Generator..."):
                st.session_state.generator = MedicalJobDescriptionGenerator()
        return True
    except Exception as e:
        st.error(f"❌ Failed to initialize generator: {str(e)}")
        return False

def create_speech_component():
    """Create browser-based speech recognition component with direct Streamlit integration"""
    # Generate a unique key for this session
    import time
    session_key = int(time.time() * 1000)
    
    speech_html = f"""
    <div style="padding: 20px; border: 2px dashed #ccc; border-radius: 10px; text-align: center;">
        <button id="startBtn" onclick="startSpeechRecognition()" style="
            background-color: #ff4b4b; 
            color: white; 
            border: none; 
            padding: 15px 25px; 
            border-radius: 5px; 
            cursor: pointer; 
            font-size: 16px;
            margin: 5px;">
            🎤 Start Voice Recording
        </button>
        <button id="stopBtn" onclick="stopSpeechRecognition()" style="
            background-color: #666; 
            color: white; 
            border: none; 
            padding: 15px 25px; 
            border-radius: 5px; 
            cursor: pointer; 
            font-size: 16px;
            margin: 5px;" disabled>
            ⏹️ Stop Recording
        </button>
        <button id="clearBtn" onclick="clearAllText()" style="
            background-color: #ffa500; 
            color: white; 
            border: none; 
            padding: 15px 25px; 
            border-radius: 5px; 
            cursor: pointer; 
            font-size: 16px;
            margin: 5px;">
            🗑️ Clear All Text
        </button>
        <div id="status" style="margin-top: 10px; font-weight: bold;"></div>
        <div id="result" style="margin-top: 15px; padding: 10px; background-color: #f0f0f0; border-radius: 5px; min-height: 50px; text-align: left;"></div>
        
        <!-- Hidden form to submit speech text -->
        <form id="speechForm" style="display: none;">
            <input type="text" id="speechInput" name="speech_text" value="">
        </form>
    </div>

    <script>
    let recognition = null;
    let isRecording = false;
    let accumulatedText = "";
    let currentSession = "";
    const sessionKey = {session_key};

    // Simple and direct approach - update URL parameters
    function updateSpeechText(text) {{
        console.log('Updating speech text via URL params:', text);
        
        // Method 1: Update URL parameters
        const url = new URL(parent.window.location);
        url.searchParams.set('speech_text', text);
        url.searchParams.set('speech_timestamp', Date.now());
        parent.window.history.replaceState({{}}, '', url);
        
        // Method 2: Try to find and update any text input
        setTimeout(() => {{
            const inputs = parent.document.querySelectorAll('input[type="text"]');
            console.log('Found', inputs.length, 'text inputs to try');
            
            for (let i = 0; i < inputs.length; i++) {{
                const input = inputs[i];
                if (input.offsetParent !== null) {{ // visible
                    console.log('Updating input', i, 'with speech text');
                    input.value = text;
                    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    // Don't break - update all visible inputs
                }}
            }}
        }}, 100);
        
        // Method 3: Direct session state update (removed forced refresh)
        setTimeout(() => {{
            if (text.trim()) {{
                console.log('Speech text captured, no refresh needed');
                // Let Streamlit handle the state naturally
            }}
        }}, 100);
    }}

    function startSpeechRecognition() {{
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {{
            document.getElementById('status').innerHTML = '❌ Speech recognition not supported in this browser. Try Chrome.';
            return;
        }}

        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-IN'; // Indian English

        recognition.onstart = function() {{
            isRecording = true;
            document.getElementById('startBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;
            document.getElementById('status').innerHTML = '🎤 Listening... Speak now!';
            currentSession = "";
        }};

        recognition.onresult = function(event) {{
            let finalTranscript = '';
            let interimTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {{
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {{
                    finalTranscript += transcript + ' ';
                }} else {{
                    interimTranscript += transcript;
                }}
            }}

            if (finalTranscript) {{
                currentSession += finalTranscript;
                accumulatedText = accumulatedText + finalTranscript;
                
                // Update speech text immediately
                updateSpeechText(accumulatedText.trim());
            }}

            // Display current session + interim
            const displayText = accumulatedText + currentSession + '<span style="color: #666;">' + interimTranscript + '</span>';
            document.getElementById('result').innerHTML = displayText || 'Listening for your voice...';
        }};

        recognition.onerror = function(event) {{
            document.getElementById('status').innerHTML = '❌ Error: ' + event.error;
            stopSpeechRecognition();
        }};

        recognition.onend = function() {{
            if (isRecording) {{
                document.getElementById('status').innerHTML = '✅ Recording stopped. Speech captured!';
            }}
            stopSpeechRecognition();
        }};

        recognition.start();
    }}

    function stopSpeechRecognition() {{
        if (recognition) {{
            recognition.stop();
        }}
        isRecording = false;
        document.getElementById('startBtn').disabled = false;
        document.getElementById('stopBtn').disabled = true;
        
        if (accumulatedText.trim()) {{
            document.getElementById('status').innerHTML = '✅ Voice input captured! Speech will be used for generation.';
            // Final update
            updateSpeechText(accumulatedText.trim());
        }}
    }}

    function clearAllText() {{
        accumulatedText = "";
        currentSession = "";
        document.getElementById('result').innerHTML = 'Voice input cleared. Click Start to begin recording.';
        document.getElementById('status').innerHTML = '';
        
        // Clear speech text
        updateSpeechText('');
    }}

    // Initialize on load
    setTimeout(function() {{
        document.getElementById('status').innerHTML = 'Ready to record! Click Start Voice Recording to begin.';
    }}, 500);
    </script>
    """
    return speech_html

def parse_prompt_for_requirements(prompt):
    """Parse prompt to extract basic job requirements for AI"""
    prompt_lower = prompt.lower()
    
    # Extract basic info that AI can use for Indian healthcare
    job_requirements = {
        'prompt_text': prompt,  # Send full prompt to AI
        'employment_type': 'Full-time',
        'shift_pattern': 'Standard healthcare shifts',
        'required_licenses': ['Valid medical registration with State Council'],
        'compliance_requirements': ['Clinical Establishments Act', 'Bio-Medical Waste Rules', 'NMC Guidelines']
    }
    
    # Try to extract facility name if mentioned (Indian hospitals/clinics)
    facility_patterns = [
        r'at ([A-Z][A-Za-z\s&-]+(?:Hospital|Medical|Healthcare|Clinic|Center|Nursing Home))',
        r'for ([A-Z][A-Za-z\s&-]+(?:Hospital|Medical|Healthcare|Clinic|Center|Nursing Home))',
        r'([A-Z][A-Za-z\s&-]+(?:Hospital|Medical|Healthcare|Clinic|Center|Nursing Home))'
    ]
    
    facility_name = "Healthcare Facility"
    for pattern in facility_patterns:
        match = re.search(pattern, prompt)
        if match:
            facility_name = match.group(1).strip()
            break
    
    job_requirements['facility_name'] = facility_name
    
    return job_requirements

def main():
    # Header
    st.title("🏥 Medical Job Description Generator")
    st.markdown("### Generate professional medical job descriptions for Indian healthcare")
    
    # Initialize generator
    if not initialize_generator():
        st.stop()
    
    # Speech-to-text section
    st.markdown("---")
    st.subheader("🎤 Voice Input")
    st.markdown("**Browser-based speech recognition - works best in Chrome**")
    
    # Create speech recognition component
    speech_html = create_speech_component()
    components.html(speech_html, height=220)
    
    # Check for speech text from URL parameters
    query_params = st.query_params
    if "speech_text" in query_params:
        speech_from_url = query_params["speech_text"]
        if speech_from_url and speech_from_url.strip():
            st.session_state.speech_text = speech_from_url
            st.success(f"✅ Speech captured from URL: {speech_from_url[:50]}...")
            # Clear the query param after capturing
            st.query_params.clear()
    
    # Show current speech text status
    if st.session_state.speech_text.strip():
        st.info(f"🎤 **Current speech text:** {st.session_state.speech_text}")
    else:
        st.info("🎤 **No speech text captured yet** - use voice recording above")
    
    # Debug information
    # st.write(f"**Debug - Session state speech_text:** '{st.session_state.speech_text}'")
    

    
    # Control buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Clear Voice Input", type="secondary"):
            st.session_state.speech_text = ""
            st.rerun()
    
    with col2:
        if st.button("🔄 Refresh Voice Component", type="secondary"):
            st.rerun()
    
    with col3:
        # Show voice input status
        if st.session_state.speech_text.strip():
            st.success("🎤 Voice input ready!")
        else:
            st.info("🎤 No voice input yet")
    
    # Generate button - directly below speech component
    if st.button("🚀 Generate Job Description", type="primary", use_container_width=True):
        if st.session_state.speech_text.strip():
            final_prompt = st.session_state.speech_text.strip()
            st.info(f"🎤 Using voice input: {final_prompt[:100]}..." if len(final_prompt) > 100 else f"🎤 Using voice input: {final_prompt}")
            
            with st.spinner("🤖 AI is creating your medical job description..."):
                try:
                    # Parse prompt for basic requirements
                    job_requirements = parse_prompt_for_requirements(final_prompt)
                    
                    # Enhanced prompt for AI with Indian medical context
                    enhanced_prompt = f"""
                    Based on this medical staffing request for the Indian healthcare system, create a comprehensive medical job description:
                    
                    "{final_prompt}"
                    
                    Please extract and infer all relevant details for Indian healthcare including:
                    - Job title and medical specialty appropriate for India
                    - Hospital/clinic name and type (multi-specialty, super-specialty, etc.)
                    - Location (Indian city/state)
                    - Experience level and qualifications as per Indian standards
                    - Required licenses and certifications (State Medical Council, Nursing Council, etc.)
                    - Salary range in Indian Rupees (₹) - use lakhs/crores format
                    - Shift patterns common in Indian hospitals
                    - Patient population and care setting in Indian context
                    - Key responsibilities following Indian healthcare practices
                    - Indian employment benefits (PF, ESI, Gratuity, Medical Insurance)
                    - Compliance with Indian healthcare regulations (Clinical Establishments Act, Bio-Medical Waste Rules, NMC guidelines)
                    
                    Create a professional, compliant medical job description that would attract qualified healthcare professionals in India and follows Indian medical education and registration standards.
                    """
                    
                    job_requirements['enhanced_prompt'] = enhanced_prompt
                    
                    # Debug information
                    st.info(f"🔧 **Debug:** Sending request to AI generator...")
                    
                    # Generate job description
                    result = st.session_state.generator.generate_medical_job_description(job_requirements)
                    
                    if result:
                        st.session_state.generated_jd = result
                        st.success("✅ Job description generated successfully!")
                    else:
                        st.error("❌ AI generator returned empty result. Check your Google Cloud authentication.")
                        
                except Exception as e:
                    st.error(f"❌ **Error during generation:** {str(e)}")
                    st.info("💡 **Possible solutions:**")
                    st.info("1. Check your Google Cloud credentials")
                    st.info("2. Ensure Vertex AI is enabled in your project")
                    st.info("3. Verify your service account has proper permissions")
                    
                    # Show detailed error for debugging
                    with st.expander("🔍 Show detailed error information"):
                        st.code(str(e))
                        
        else:
            st.warning("⚠️ Please record your job requirements using voice input first.")
    
    # Display generated job description
    if st.session_state.generated_jd:
        st.markdown("---")
        st.subheader("📄 Generated Job Description")
        
        jd_data = st.session_state.generated_jd
        
        # Main job description
        job_desc = jd_data.get('job_description', '')
        if job_desc:
            st.markdown(job_desc)
        else:
            st.error("⚠️ Job description content not available.")
        
        # Reset button
        if st.button("🔄 Create Another Job Description", type="secondary", use_container_width=True):
            st.session_state.generated_jd = None
            st.rerun()

    # Instructions
    st.markdown("---")
    st.markdown("### 📝 **Simple Voice-to-Job Description:**")
    st.markdown("""
    **Super Simple Workflow:**
    1. **🎤 Click "Start Voice Recording"** (works best in Chrome browser)
    2. **🗣️ Speak your job requirements** clearly
    3. **⏹️ Click "Stop Recording"** when done (or continue with more recordings)
    4. **🚀 Click "Generate Job Description"** - that's it!
    
    **What to Say:**
    - **Job title**: "Staff Nurse", "Medical Officer", "Physiotherapist"
    - **Hospital name**: "Apollo Hospital", "Fortis Healthcare", "AIIMS"
    - **Location**: "Bangalore", "Delhi", "Mumbai", "Chennai"
    - **Experience**: "3 years experience", "fresher", "5+ years"
    - **Salary**: "4 to 6 lakhs per annum", "8 lakhs CTC"
    - **Specialization**: "ICU", "Emergency", "Cardiology", "Pediatrics"
    
    **Example Voice Input:**
    *"Generate job description for Staff Nurse ICU position at Apollo Hospital Bangalore. We need someone with 3 years experience in critical care, B.Sc Nursing degree, salary range 4 to 6 lakhs per annum with PF ESI benefits."*
    
    **Features:**
    - ✅ **Voice-only workflow**: No typing required
    - ✅ **Continuous recording**: Add more details across multiple sessions
    - ✅ **Instant generation**: Direct voice-to-job description
    - ✅ **Indian healthcare focus**: Tailored for Indian medical jobs
    """)
    
    # Browser compatibility note
    st.info("""
    🌐 **Browser Compatibility:** 
    - ✅ **Chrome/Edge**: Full speech recognition support (recommended)
    - ⚠️ **Firefox**: Limited support
    - ❌ **Safari**: Not supported
    
    If speech recognition doesn't work, please use the text input area directly.
    """)

if __name__ == "__main__":
    main() 
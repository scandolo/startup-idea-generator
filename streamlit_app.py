import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API URL from environment or use default
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="PitchSlap - AI Startup Idea Generator",
    page_icon="🚀",
    layout="wide",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 0;
        color: #4F8BF9;
    }
    .sub-header {
        font-size: 1.5em;
        color: #8C8C8C;
        margin-bottom: 2em;
    }
    .idea-box {
        background-color: #F0F2F6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .idea-title {
        font-size: 1.5em;
        font-weight: bold;
        color: #4F8BF9;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">PitchSlap</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Generate unique startup ideas with AI</p>', unsafe_allow_html=True)

# Create a form for input
with st.form("pitch_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        industry = st.text_input("Industry", placeholder="Tech, Healthcare, Finance, etc.")
        target_audience = st.text_input("Target Audience", placeholder="Millennials, Small Business Owners, etc.")
    
    with col2:
        problem_to_solve = st.text_area("Problem to Solve", placeholder="Describe the problem your startup should address")
        idea_count = st.slider("Number of Ideas to Generate", min_value=1, max_value=5, value=3)
    
    # Expandable section for additional requirements
    with st.expander("Additional Requirements (Optional)"):
        req1 = st.text_input("Requirement 1", placeholder="e.g., Must be mobile-first")
        req2 = st.text_input("Requirement 2", placeholder="e.g., Include subscription model")
        req3 = st.text_input("Requirement 3", placeholder="e.g., Low initial investment")
    
    submit_button = st.form_submit_button("Generate Ideas! 💡")

# Process form submission
if submit_button:
    if not industry or not target_audience or not problem_to_solve:
        st.error("Please fill in all required fields: Industry, Target Audience, and Problem to Solve.")
    else:
        # Show loading spinner
        with st.spinner("Generating brilliant startup ideas..."):
            # Prepare requirements list (excluding empty ones)
            requirements = [req for req in [req1, req2, req3] if req]
            
            # Prepare request payload
            payload = {
                "industry": industry,
                "target_audience": target_audience,
                "problem_to_solve": problem_to_solve,
                "unique_requirements": requirements,
                "idea_count": idea_count
            }
            
            try:
                # Call API
                response = requests.post(f"{API_URL}/generate", json=payload)
                response.raise_for_status()  # Raise exception for 4XX/5XX responses
                
                data = response.json()
                
                # Display results
                st.success(f"Generated {len(data['ideas'])} startup ideas!")
                
                for i, idea in enumerate(data['ideas']):
                    with st.container():
                        st.markdown(f"""<div class="idea-box">
                                    <p class="idea-title">Idea {i+1}</p>
                                    <p>{idea}</p>
                                    </div>""", unsafe_allow_html=True)
                
                # Add download button for ideas
                idea_text = "\n\n".join([f"Idea {i+1}: {idea}" for i, idea in enumerate(data['ideas'])])
                st.download_button(
                    label="Download Ideas as Text",
                    data=idea_text,
                    file_name="pitchslap_ideas.txt",
                    mime="text/plain"
                )
                
            except requests.exceptions.RequestException as e:
                st.error(f"Error communicating with API: {str(e)}")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by PitchSlap | Using OpenAI GPT-4o") 
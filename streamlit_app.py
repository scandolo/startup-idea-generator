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
st.markdown('<p class="sub-header">Generate startup ideas tailored to your skills and experiences</p>', unsafe_allow_html=True)

# Create a form for input
with st.form("pitch_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        skills = st.text_area("Your Skills", placeholder="Programming languages, design, marketing, communication skills, etc.")
        interests = st.text_area("Your Interests", placeholder="What topics, industries, or activities are you passionate about?")
    
    with col2:
        experience = st.text_area("Your Experience", placeholder="Previous work, projects, or relevant background")
        idea_count = st.slider("Number of Ideas to Generate", min_value=1, max_value=5, value=3)
    
    # Expandable section for additional preferences
    with st.expander("Additional Information (Optional)"):
        preferences = st.text_area("Preferences", placeholder="e.g., Remote-friendly, low startup costs, B2B focus, etc.")
        constraints = st.text_area("Constraints", placeholder="e.g., Limited funding, time constraints, geographic limitations")
    
    submit_button = st.form_submit_button("Generate Personalized Ideas! 💡")

# Process form submission
if submit_button:
    if not skills or not interests or not experience:
        st.error("Please fill in all required fields: Skills, Interests, and Experience.")
    else:
        # Show loading spinner
        with st.spinner("Generating startup ideas tailored to your background..."):
            # Prepare request payload
            payload = {
                "skills": skills,
                "interests": interests,
                "experience": experience,
                "preferences": preferences if preferences else None,
                "constraints": constraints if constraints else None,
                "idea_count": idea_count
            }
            
            try:
                # Call API
                response = requests.post(f"{API_URL}/generate", json=payload)
                response.raise_for_status()  # Raise exception for 4XX/5XX responses
                
                data = response.json()
                
                # Display results
                st.success(f"Generated {len(data['ideas'])} personalized startup ideas!")
                
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
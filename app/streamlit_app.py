import streamlit as st
# from PyPDF2 import PdfReader
# import io
# import asyncio
# from lmnt_streaming_test import generate_audio_response, VOICE_CONFIGS
# import os
# import openai

st.title("Multi-Agent Resume Analyzer")

# Initialize OpenAI client
# client = openai.OpenAI()

# File uploader for PDF
uploaded_file = st.file_uploader("Upload your resume (TXT)", type="txt")

if uploaded_file is not None:
    # Read text file content
    text = uploaded_file.getvalue().decode("utf-8")

    # Define different agent personalities
    agents = {
        "Jargon": "You are a professional recruiter. Analyze the resume in a formal, structured way highlighting key qualifications and experience.",
        "Nervous": "You are a nervous person. Analyze the resume in a casual, unstructured way highlighting key qualifications and experience.",
        "Casual": "You are a casual person. Analyze the resume in a casual, unstructured way highlighting key qualifications and experience.",
        "Industry Expert": "You are a seasoned industry expert. Evaluate the resume from a technical perspective and discuss relevant industry trends.",
    }
    
    st.write(text)

    # Create columns for better layout
    cols = st.columns(len(agents))

    # Track which agent is currently active
    if 'active_agent' not in st.session_state:
        st.session_state.active_agent = None

    # Create widgets for each agent
    for idx, (agent_name, prompt) in enumerate(agents.items()):
        with cols[idx]:
            st.subheader(agent_name)
            
            # Create unique key for each button
            button_key = f"button_{agent_name}"
            
            if st.button("🎬 Play", key=button_key):
                st.session_state.active_agent = agent_name
                
                # Load the pre-generated audio file
                audio_path = '../output/output-jargon-ava.mp3'
                
                try:
                    # Play the audio
                    audio_file = open(audio_path, 'rb')
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format='audio/mp3')
                    audio_file.close()
                except FileNotFoundError:
                    st.error(f"Audio file not found for {agent_name}")

import streamlit as st
import base64

st.markdown("""
<style>
.stButton button {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

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
    
    # st.write(text)

    # Create columns for better layout
    cols = st.columns(len(agents))

    # Track which agent is currently active and playing
    if 'active_agent' not in st.session_state:
        st.session_state.active_agent = None
        st.session_state.is_playing = False

    # Create widgets for each agent
    for idx, (agent_name, prompt) in enumerate(agents.items()):
        with cols[idx]:
            st.subheader(agent_name)
            
            if st.button("🎬 Play", key=f"button_{agent_name}"):
                # If clicking the same button that's currently playing, stop the audio
                if st.session_state.active_agent == agent_name and st.session_state.is_playing:
                    st.session_state.active_agent = None
                    st.session_state.is_playing = False
                    # Insert empty audio to stop current playback
                    st.components.v1.html(
                        """
                        <audio id="audio" style="display: none">
                            <source src="" type="audio/mp3">
                        </audio>
                        """,
                        height=0
                    )
                else:
                    # Play new audio
                    st.session_state.active_agent = agent_name
                    st.session_state.is_playing = True
                    
                    audio_path = "../output/output-jargon-sam-altman.mp3"
                    try:
                        audio_html = f"""
                            <audio autoplay style="display: none">
                                <source src="data:audio/mp3;base64,{base64.b64encode(open(audio_path, 'rb').read()).decode()}" type="audio/mp3">
                            </audio>
                        """
                        st.components.v1.html(audio_html, height=0)
                    except FileNotFoundError:
                        st.error(f"Audio file not found for {agent_name}")

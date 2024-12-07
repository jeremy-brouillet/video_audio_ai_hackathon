import streamlit as st
from PyPDF2 import PdfReader
import io
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

st.title("Multi-Agent Resume Analyzer")

# File uploader for PDF
uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

if uploaded_file is not None:
    # Read PDF content
    pdf_reader = PdfReader(io.BytesIO(uploaded_file.read()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    # Initialize ChatGPT
    chat = ChatOpenAI(temperature=0.7)

    # Define different agent personalities
    agents = {
        "Professional Recruiter": "You are a professional recruiter. Analyze the resume in a formal, structured way highlighting key qualifications and experience.",
        "Career Coach": "You are an enthusiastic career coach. Provide constructive feedback and suggestions for improvement in an encouraging tone.",
        "Industry Expert": "You are a seasoned industry expert. Evaluate the resume from a technical perspective and discuss relevant industry trends.",
        "Creative Director": "You are a creative director. Focus on the unique aspects and creative elements of the candidate's experience.",
    }

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

            # Display response if this agent is active
            if st.session_state.active_agent == agent_name:
                with st.spinner(f"{agent_name} is analyzing..."):
                    messages = [
                        SystemMessage(content=prompt),
                        HumanMessage(content=f"Please analyze this resume:\n\n{text}")
                    ]
                    response = chat.invoke(messages)
                    st.write(response.content)

import streamlit as st
from resume_parser import extract_resume_text
from skill_extractor import load_skills, extract_skills
from ats_score import calculate_ats_score
from resume_generator import generate_resume
from ai_resume_optimizer import optimize_resume

# PAGE CONFIG
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="🤖",
    layout="wide"
)

# CUSTOM CSS
st.markdown("""
<style>

body {
background-color: #f5f7fb;
}

.big-title {
text-align:center;
font-size:50px;
font-weight:bold;
color:#2c3e50;
}

.section {
background-color:white;
padding:25px;
border-radius:15px;
box-shadow:0px 4px 15px rgba(0,0,0,0.1);
margin-bottom:20px;
}

.stButton>button {
background: linear-gradient(90deg,#4facfe,#00f2fe);
color:white;
font-size:18px;
border-radius:10px;
padding:10px 20px;
border:none;
}

.stButton>button:hover {
background: linear-gradient(90deg,#43e97b,#38f9d7);
}

</style>
""", unsafe_allow_html=True)

# TITLE
st.markdown("<div class='big-title'>🤖 AI Resume Screening System</div>", unsafe_allow_html=True)
st.write("")

# SESSION STATE
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None

if "jd_text" not in st.session_state:
    st.session_state.jd_text = None

if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = []

if "missing_skills" not in st.session_state:
    st.session_state.missing_skills = []


# INPUT SECTION
st.markdown("<div class='section'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

with col2:
    jd = st.text_area("📝 Paste Job Description", height=200)

st.markdown("</div>", unsafe_allow_html=True)


# ANALYZE BUTTON
if st.button("🔍 Analyze Resume"):

    if uploaded_file and jd:

        resume_text = extract_resume_text(uploaded_file)

        st.session_state.resume_text = resume_text
        st.session_state.jd_text = jd

        skills_db = load_skills()

        resume_skills = extract_skills(resume_text, skills_db)
        jd_skills = extract_skills(jd, skills_db)

        ats_score = calculate_ats_score(resume_text, jd)

        missing_skills = list(set(jd_skills) - set(resume_skills))

        # Save to session
        st.session_state.resume_skills = resume_skills
        st.session_state.missing_skills = missing_skills

        st.markdown("<div class='section'>", unsafe_allow_html=True)

        st.subheader("📊 ATS Score")
        st.progress(int(ats_score))
        st.success(f"ATS Match Score: {ats_score}%")

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("✅ Resume Skills")
            st.write(resume_skills)

        with col4:
            st.subheader("⚠️ Missing Skills")
            st.write(missing_skills)

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.warning("Please upload a resume and paste a job description.")



# AI OPTIMIZER
if st.session_state.resume_text and st.session_state.jd_text:

    if st.button("✨ Generate AI Optimized Resume"):

        with st.spinner("🤖 Generating optimized resume..."):

            improved_resume = optimize_resume(
                st.session_state.resume_text,
                st.session_state.jd_text
            )

        st.markdown("<div class='section'>", unsafe_allow_html=True)

        st.subheader("🤖 AI Optimized Resume")
        st.write(improved_resume)

        # Generate formatted resume file
        file_path = generate_resume(improved_resume)

        with open(file_path, "rb") as f:
            st.download_button(
                label="⬇ Download AI Optimized Resume",
                data=f,
                file_name="optimized_resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        st.markdown("</div>", unsafe_allow_html=True)
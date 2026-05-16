import streamlit as st
from resume_parser import extract_resume_text
from skill_extractor import load_skills, extract_skills
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
st.markdown(
    "<div class='big-title'>🤖 AI Resume Screening System</div>",
    unsafe_allow_html=True
)

st.write("")

# SESSION STATE
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""

if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = []

if "missing_skills" not in st.session_state:
    st.session_state.missing_skills = []

# INPUT SECTION
st.markdown("<div class='section'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader(
        "📄 Upload Resume (PDF)",
        type=["pdf"]
    )

with col2:
    jd = st.text_area(
        "📝 Paste Job Description",
        height=220
    )

st.markdown("</div>", unsafe_allow_html=True)

# ANALYZE BUTTON
if st.button("🔍 Analyze Resume"):

    if uploaded_file and jd:

        try:

            # EXTRACT TEXT
            resume_text = extract_resume_text(uploaded_file)

            # DEBUG OUTPUT
            st.markdown("<div class='section'>", unsafe_allow_html=True)

            st.subheader("📄 Extracted Resume Text")

            if resume_text.strip() == "":
                st.error("❌ No text extracted from PDF.")
                st.stop()

            st.write(resume_text[:5000])

            st.markdown("</div>", unsafe_allow_html=True)

            # SAVE SESSION
            st.session_state.resume_text = resume_text
            st.session_state.jd_text = jd

            # LOAD SKILLS
            skills_db = load_skills()

            # EXTRACT SKILLS
            resume_skills = extract_skills(
                resume_text,
                skills_db
            )

            jd_skills = extract_skills(
                jd,
                skills_db
            )

            # MATCHED SKILLS
            matched_skills = list(
                set(resume_skills) & set(jd_skills)
            )

            # ATS SCORE
            if len(jd_skills) > 0:

                ats_score = round(
                    (len(matched_skills) / len(jd_skills)) * 100,
                    2
                )

            else:
                ats_score = 0

            # MISSING SKILLS
            missing_skills = list(
                set(jd_skills) - set(resume_skills)
            )

            # SAVE TO SESSION
            st.session_state.resume_skills = resume_skills
            st.session_state.missing_skills = missing_skills

            # RESULT SECTION
            st.markdown("<div class='section'>", unsafe_allow_html=True)

            st.subheader("📊 ATS Match Score")

            st.progress(min(int(ats_score), 100))

            st.success(f"ATS Match Score: {ats_score}%")

            col3, col4 = st.columns(2)

            with col3:

                st.subheader("✅ Resume Skills")

                if resume_skills:
                    st.write(resume_skills)
                else:
                    st.warning("No skills found in resume.")

            with col4:

                st.subheader("⚠️ Missing Skills")

                if missing_skills:
                    st.write(missing_skills)
                else:
                    st.success("No missing skills detected.")

            st.subheader("🎯 Matched Skills")

            if matched_skills:
                st.write(matched_skills)
            else:
                st.warning("No matching skills found.")

            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:

            st.error(f"Error: {str(e)}")

    else:

        st.warning(
            "Please upload a resume and paste a job description."
        )

# AI OPTIMIZER
if (
    st.session_state.resume_text != ""
    and
    st.session_state.jd_text != ""
):

    if st.button("✨ Generate AI Optimized Resume"):

        with st.spinner("🤖 Generating optimized resume..."):

            improved_resume = optimize_resume(
                st.session_state.resume_text,
                st.session_state.jd_text
            )

        st.markdown("<div class='section'>", unsafe_allow_html=True)

        st.subheader("🤖 AI Optimized Resume")

        st.write(improved_resume)

        # GENERATE DOCX
        file_path = generate_resume(improved_resume)

        with open(file_path, "rb") as f:

            st.download_button(
                label="⬇ Download AI Optimized Resume",
                data=f,
                file_name="optimized_resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        st.markdown("</div>", unsafe_allow_html=True)
        #rebuild

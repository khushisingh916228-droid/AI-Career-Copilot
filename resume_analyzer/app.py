import streamlit as st
from main import analyze_resume

st.title("🎯 AI Resume Analyzer")
st.write("Upload your resume and paste the job description — you will get your match score instantly!")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
jd_text = st.text_area("Paste the job description here")

if st.button("Analyze"):
    if uploaded_file and jd_text:
        with open("data/temp_resume.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        score, matched, missing, resume_skills = analyze_resume("data/temp_resume.pdf", jd_text)

        st.subheader(f"Match Score: {score:.1f}%")
        st.progress(score / 100)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ✅ Matched Skills")
            if matched:
                for skill in sorted(matched):
                    st.markdown(f"- {skill.title()}")
            else:
                st.write("No matches found")

        with col2:
            st.markdown("### ❌ Missing Skills")
            if missing:
                for skill in sorted(missing):
                    st.markdown(f"- {skill.title()}")
            else:
                st.write("All skills matched! 🎉")
    else:
        st.warning("Please upload a resume and paste the job description!")
        
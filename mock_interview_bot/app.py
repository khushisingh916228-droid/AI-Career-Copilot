import streamlit as st
from main import generate_interview_question, evaluate_answer

st.title("🎤 AI Mock Interview Bot")
st.write("Practice technical interviews with instant AI feedback!")

# To select the role and difficulty
role = st.text_input("Job Role", placeholder="e.g. Machine Learning Engineer")
difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])

# Session state — so the question is remembered until the page reloads
if "question" not in st.session_state:
    st.session_state.question = None

if st.button("Generate Question"):
    if role:
        st.session_state.question = generate_interview_question(role, difficulty)
    else:
        st.warning("Please enter a role first!")

if st.session_state.question:
    st.subheader("Interview Question:")
    st.write(st.session_state.question)

    answer = st.text_area("Your Answer")

    if st.button("Submit Answer"):
        if answer:
            with st.spinner("Evaluating your answer..."):
                feedback = evaluate_answer(st.session_state.question, answer, role)
            st.subheader("Feedback:")
            st.write(feedback)
        else:
            st.warning("Please write an answer first!")
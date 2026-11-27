import streamlit as st
import importlib.util
import io
import os
import json
import hashlib
from dotenv import load_dotenv

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

st.set_page_config(page_title="AI Career Copilot", page_icon="🎯", layout="wide")

# ---------- LOGIN / SIGNUP (Supabase Auth) ----------
# Each browser session keeps its own Supabase client in st.session_state (never shared),
# so one user's login can never be picked up by another user.
import auth_client

def _start_session(email, client):
    st.session_state.logged_in = True
    st.session_state.sb_client = client
    st.session_state.user_email = email
    st.session_state.username = email.split("@")[0]

def login_gate():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("\U0001F3AF AI Career Copilot")
        st.write("Log in or create a new account.")

        tab1, tab2 = st.tabs(["\U0001F510 Login", "\U0001F195 Sign Up"])

        with tab1:
            login_email = st.text_input("Email", key="login_email")
            login_pass = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login"):
                if not login_email or not login_pass:
                    st.warning("Please enter both email and password.")
                else:
                    ok, msg, client = auth_client.sign_in(login_email.strip(), login_pass)
                    if ok:
                        _start_session(login_email.strip(), client)
                        st.rerun()
                    else:
                        st.error(msg)

        with tab2:
            new_email = st.text_input("Email", key="signup_email")
            new_pass = st.text_input("New password (8+ characters, letters and digits)", type="password", key="signup_pass")
            new_pass2 = st.text_input("Confirm password", type="password", key="signup_pass2")
            if st.button("Sign Up"):
                if not new_email or not new_pass:
                    st.warning("Please enter both email and password.")
                elif new_pass != new_pass2:
                    st.error("The two passwords do not match.")
                else:
                    ok, msg, client = auth_client.sign_up(new_email.strip(), new_pass)
                    if ok:
                        _start_session(new_email.strip(), client)
                        st.rerun()
                    else:
                        st.error(msg)

        st.stop()

login_gate()

ml_main = load_module("ml_main", os.path.join("multilingual_layer", "main.py"))

TRANSLATIONS = {
    "en": {
        "app_title": "🎯 AI Career Copilot",
        "nav_label": "Choose a module:",
        "home": "🏠 Home",
        "resume": "📄 Resume Analyzer",
        "interview": "🎤 Mock Interview Bot",
        "skillgap": "🧠 Skill Gap",
        "career": "📊 Career Insights",
        "welcome": "Welcome to AI Career Copilot 🎯",
        "welcome_sub": "Select any module from the sidebar.",
    },
    "hi": {
        "app_title": "🎯 एआई करियर कोपायलट",
        "nav_label": "मॉड्यूल चुनो:",
        "home": "🏠 होम",
        "resume": "📄 रिज़्यूमे एनालाइज़र",
        "interview": "🎤 मॉक इंटरव्यू बॉट",
        "skillgap": "🧠 स्किल गैप",
        "career": "📊 करियर इनसाइट्स",
        "welcome": "एआई करियर कोपायलट में स्वागत है 🎯",
        "welcome_sub": "साइडबार से कोई भी मॉड्यूल चुनो।",
    },
    "pa": {
        "app_title": "🎯 ਏਆਈ ਕਰੀਅਰ ਕੋਪਾਇਲਟ",
        "nav_label": "ਮੋਡਿਊਲ ਚੁਣੋ:",
        "home": "🏠 ਹੋਮ",
        "resume": "📄 ਰੈਜ਼ਿਊਮੇ ਵਿਸ਼ਲੇਸ਼ਕ",
        "interview": "🎤 ਮੌਕ ਇੰਟਰਵਿਊ ਬੋਟ",
        "skillgap": "🧠 ਸਕਿੱਲ ਗੈਪ",
        "career": "📊 ਕਰੀਅਰ ਇਨਸਾਈਟਸ",
        "welcome": "ਏਆਈ ਕਰੀਅਰ ਕੋਪਾਇਲਟ ਵਿੱਚ ਸੁਆਗਤ ਹੈ 🎯",
        "welcome_sub": "ਸਾਈਡਬਾਰ ਤੋਂ ਕੋਈ ਵੀ ਮੋਡਿਊਲ ਚੁਣੋ।",
    },
}

def t(key):
    lang = st.session_state.get("interface_lang", "en")
    english_text = TRANSLATIONS["en"][key]
    if lang in TRANSLATIONS:
        return TRANSLATIONS[lang][key]
    return tr(english_text, lang)  # other languages use dynamic Google Translate

@st.cache_data(show_spinner=False)
def _tr_cached(text, lang):
    # Raises on failure, so a failed translation is never cached
    return ml_main.translate_text(text, lang, max_retries=2, raise_on_fail=True)

import json as _json
try:
    with open("translations.json", "r", encoding="utf-8") as _f:
        STATIC_TR = _json.load(_f)
except Exception:
    STATIC_TR = {}

def tr(text, lang):
    if not text or lang == "en":
        return text
    hit = STATIC_TR.get(lang, {}).get(text)
    if hit:
        return hit
    try:
        return _tr_cached(text, lang)
    except Exception:
        return text

def get_interview_avg():
    """Average score across all three interview modes (Personalized + Adaptive + Role-Based)"""
    interview_scores = []
    for item in st.session_state.get("queue_answers", []):
        if item.get("score") is not None:
            interview_scores.append(item["score"])
    for item in st.session_state.get("adaptive_history", []):
        if item.get("score") is not None:
            interview_scores.append(item["score"])
    for score in st.session_state.get("rolebased_scores", []):
        if score is not None:
            interview_scores.append(score)
    return (sum(interview_scores) / len(interview_scores)) if interview_scores else None

def _read_and_delete(path):
    """Reads an audio file and deletes it right away (so temp files do not pile up)"""
    try:
        with open(path, "rb") as f:
            return f.read()
    finally:
        try:
            os.remove(path)
        except OSError:
            pass

def speak_button(text, lang, key):
    """Button that plays the translated text as audio"""
    if st.button("🔊 Listen", key=key):
        try:
            with st.spinner("Generating audio..."):
                audio_file = ml_main.text_to_speech(text, lang)
            audio_bytes = _read_and_delete(audio_file)
            st.audio(audio_bytes, format="audio/mp3")
        except Exception:
            st.warning("Audio is not available for this language yet.")

def auto_speak(text, lang, unique_key):
    """
    Speaks automatically like Ira (autoplay), no button click needed.
    Tracks an 'already played' set so the same text/question is not autoplayed again.
    """
    if "auto_played" not in st.session_state:
        st.session_state.auto_played = set()

    if unique_key not in st.session_state.auto_played:
        try:
            audio_file = ml_main.text_to_speech(text, lang)
            if audio_file:
                audio_bytes = _read_and_delete(audio_file)
                st.audio(audio_bytes, format="audio/mp3", autoplay=True)
        except Exception:
            pass
        st.session_state.auto_played.add(unique_key)

def autoplay_once(text, lang):
    """Speaks the text AUTOMATICALLY (no button press), but only once per unique text —
    so reruns do not replay the same audio."""
    if "played_texts" not in st.session_state:
        st.session_state.played_texts = set()

    if text and text not in st.session_state.played_texts:
        try:
            audio_file = ml_main.text_to_speech(text, lang)
            audio_bytes = _read_and_delete(audio_file)
            st.audio(audio_bytes, format="audio/mp3", autoplay=True)
            st.session_state.played_texts.add(text)
        except Exception:
            pass


# Dropdown language -> Google speech recognition language code.
# Bhojpuri has no Google speech code, so it falls back to Hindi.
MIC_LANG = {
    "en": "en-IN", "hi": "hi-IN", "pa": "pa-Guru-IN", "bho": "hi-IN",
    "mr": "mr-IN", "gu": "gu-IN", "bn": "bn-IN", "ta": "ta-IN",
    "te": "te-IN", "kn": "kn-IN", "ml": "ml-IN", "ur": "ur-IN",
}

def mic_text_area(label, key, lang, placeholder=""):
    """Text area where you can type OR speak into the mic. A mic error never crashes the app."""
    if key not in st.session_state:
        st.session_state[key] = ""

    col1, col2 = st.columns([5, 1])
    with col2:
        st.write("")
        st.write("")
        if st.button("🎤 Speak", key=f"{key}_mic_btn"):
            try:
                with st.spinner(tr("Listening... speak now", lang)):
                    spoken = ml_main.speech_to_text(MIC_LANG.get(lang, "en-IN"))

                error_phrases = ["Could not understand", "your internet connection", "Microphone not connected", "problem with the microphone"]
                if spoken and not any(p in spoken for p in error_phrases):
                    st.session_state[key] = spoken
                    st.rerun()
                elif spoken:
                    st.warning(spoken)
            except Exception:
                st.warning(tr("Couldn't understand the mic input. You can type instead.", lang))
    with col1:
        value = st.text_area(label, key=key, placeholder=placeholder)
    return value

# ---------- SIDEBAR ----------
st.sidebar.title(t("app_title"))

lang_display = {
    "English": "en",
    "हिंदी (Hindi)": "hi",
    "ਪੰਜਾਬੀ (Punjabi)": "pa",
}
chosen_lang_label = st.sidebar.selectbox("🌐 Language (applies to all modules)", list(lang_display.keys()))
st.session_state.interface_lang = lang_display[chosen_lang_label]
current_lang = st.session_state.interface_lang

st.sidebar.markdown("---")

# If a button requested navigation, apply it BEFORE the widget is created
if "nav_target" in st.session_state:
    st.session_state["current_page"] = st.session_state.pop("nav_target")

page_ids = ["home", "resume", "interview", "skillgap", "career"]
page = st.sidebar.radio(t("nav_label"), page_ids, format_func=lambda pid: t(pid), key="current_page")

st.sidebar.markdown("---")
st.sidebar.write(f"👤 {st.session_state.username}")
if st.sidebar.button(f"🚪 {tr('Logout', current_lang)}"):
    auth_client.sign_out(st.session_state.get("sb_client"))
    st.session_state.clear()  # remove all of this user's data so the next user cannot see it
    st.rerun()

# ================= PAGES =================

if page == "home":
    st.title(f"{tr('Welcome', current_lang)}, {st.session_state.username}! 🎯")
    st.write(t("welcome_sub"))

    ci_main = load_module("ci_main", os.path.join("career_insights", "main.py"))
    resume_score = st.session_state.get("resume_score")
    skillgap_pct = st.session_state.get("sg_percentage")
    interview_avg = get_interview_avg()

    overall, label = ci_main.compute_readiness(resume_score, skillgap_pct, interview_avg)

    if overall is not None:
        st.markdown("### " + tr("Your Career Readiness", current_lang))
        st.progress(min(overall / 100, 1.0))
        st.markdown(f"#### {tr(label, current_lang)} — {overall:.1f}%")
    else:
        st.info(tr("You haven't used any module yet — get started with one below!", current_lang))

    st.markdown("---")
    st.markdown("### " + tr("Quick Access", current_lang))

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button(t("resume"), use_container_width=True):
            st.session_state["nav_target"] = "resume"
            st.rerun()
    with col2:
        if st.button(t("interview"), use_container_width=True):
            st.session_state["nav_target"] = "interview"
            st.rerun()
    with col3:
        if st.button(t("skillgap"), use_container_width=True):
            st.session_state["nav_target"] = "skillgap"
            st.rerun()
    with col4:
        if st.button(t("career"), use_container_width=True):
            st.session_state["nav_target"] = "career"
            st.rerun()

elif page == "resume":
    st.title(tr("🎯 AI Resume Analyzer", current_lang))
    st.write(tr("Upload your resume and paste the job description — get your match score instantly!", current_lang))

    ra_main = load_module("ra_main", os.path.join("resume_analyzer", "main.py"))

    uploaded_file = st.file_uploader(tr("Upload your resume (PDF)", current_lang), type="pdf")
    jd_text = mic_text_area(tr("Paste the Job Description here", current_lang), "jd_text", current_lang)

    if st.button(tr("Analyze", current_lang)):
        if uploaded_file and jd_text:
            # The resume is never saved to disk (it is read in memory), so users cannot overlap
            resume_file = io.BytesIO(uploaded_file.getvalue())

            score, matched, missing, resume_skills = ra_main.analyze_resume(resume_file, jd_text)

            if not resume_skills and score == 0:
                st.error(tr("Couldn't extract text from the resume. The PDF may be a scanned image or corrupted — try a text-based PDF.", current_lang))
            else:
                st.success(tr("✅ Analysis complete!", current_lang))

            st.session_state.user_skills = resume_skills
            st.session_state.matched_skills = matched
            st.session_state.missing_skills = missing
            st.session_state.resume_score = score
        else:
            st.warning(tr("Please upload a resume and paste the job description!", current_lang))

    # Render the result from session_state so it does not disappear when Listen is pressed
    if "resume_score" in st.session_state:
        score = st.session_state.resume_score
        missing = st.session_state.missing_skills
        matched_display = st.session_state.matched_skills

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric(tr("🎯 Overall Match", current_lang), f"{score:.1f}%")
        with col_b:
            ats_score = min(100, score + (10 if len(matched_display) >= 3 else 0))
            st.metric(tr("📊 ATS-Friendly Score", current_lang), f"{ats_score:.0f}%")

        st.progress(score / 100)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### ✅ {tr('Skills Found', current_lang)}")
            if matched_display:
                for skill in sorted(matched_display):
                    st.markdown(f"- {tr(skill.title(), current_lang)}")
            else:
                st.write(tr("No matches found", current_lang))

        with col2:
            st.markdown(f"### ❌ {tr('Missing Skills', current_lang)}")
            if missing:
                for skill in sorted(missing):
                    st.markdown(f"- {tr(skill.title(), current_lang)}")
            else:
                st.write(tr("All skills matched! 🎉", current_lang))

        st.markdown("---")
        st.markdown(f"### 🤖 {tr('AI Recommendation', current_lang)}")
        recommendation = ra_main.generate_recommendation(score, missing)
        st.info(tr(recommendation, current_lang))

        summary_text = tr(
            f"Match score {score:.1f} percent. Matched skills: {', '.join(matched_display) if matched_display else 'none'}. "
            f"Missing skills: {', '.join(missing) if missing else 'none'}. {recommendation}",
            current_lang
        )
        speak_button(summary_text, current_lang, "speak_resume")

        st.markdown("---")
        col_x, col_y = st.columns(2)
        with col_x:
            if st.button(f"🧠 {tr('Check Skill Gap', current_lang)}", use_container_width=True):
                st.session_state["nav_target"] = "skillgap"
                st.rerun()
        with col_y:
            if st.button(f"📊 {tr('View Career Insights', current_lang)}", use_container_width=True):
                st.session_state["nav_target"] = "career"
                st.rerun()

elif page == "interview":
    st.title(tr("🎤 AI Mock Interview Bot", current_lang))

    load_dotenv(os.path.join("mock_interview_bot", ".env"))
    mib_main = load_module("mib_main", os.path.join("mock_interview_bot", "main.py"))

    interview_mode = st.radio(
        tr("Choose Interview Type:", current_lang),
        [
            tr("🤖 Personalized Interview — Based on your Skill Gap", current_lang),
            tr("🎯 Role-Based Interview — Based on your Target Role", current_lang),
            tr("🧠 AI Adaptive Interview — Difficulty/topic adjusts automatically", current_lang),
        ]
    )

    is_personalized = "Personalized" in interview_mode or "🤖" in interview_mode
    is_adaptive = "Adaptive" in interview_mode or "🧠" in interview_mode

    st.markdown("---")

    # ============ PERSONALIZED MODE (Skill Gap based) ============
    if is_personalized:
        missing = st.session_state.get("sg_missing")

        if not missing:
            st.warning(tr("Check your skills in the 'Skill Gap' module first, so your weak areas can be identified.", current_lang))
        else:
            subject_text = ', '.join(sorted(missing))

            if "interview_queue" not in st.session_state:
                st.session_state.interview_queue = None

            if not st.session_state.interview_queue:
                st.markdown("### 🎓 " + tr("Interview Summary", current_lang))
                st.info(
                    f"**{tr('Mode', current_lang)}:** {tr('Personalized Interview', current_lang)}\n\n"
                    f"**{tr('Subject', current_lang)}:** {subject_text}"
                )
                ira_msg = mib_main.get_ira_greeting("Personalized Interview", subject_text)
                translated_greeting = tr(ira_msg, current_lang)
                st.write("🎙️ " + translated_greeting)
                auto_speak(translated_greeting, current_lang, "greeting_personalized")

            if st.button(tr("Confirm & Start Interview", current_lang)):
                st.session_state.interview_queue = mib_main.build_personalized_queue(missing, total_questions=10)
                st.session_state.queue_index = 0
                st.session_state.queue_answers = []
                st.session_state.p_question = None
                st.session_state.p_feedback = None
                st.rerun()

            if st.session_state.interview_queue:
                idx = st.session_state.queue_index
                total = len(st.session_state.interview_queue)

                if idx < total:
                    current_skill = st.session_state.interview_queue[idx]
                    st.progress((idx) / total)
                    st.caption(f"{tr('Question', current_lang)} {idx + 1} / {total} — {tr('Skill', current_lang)}: {current_skill.title()}")

                    if st.session_state.p_question is None:
                        target_role = st.session_state.get("target_role", "")
                        st.session_state.p_question = mib_main.generate_skill_based_question(current_skill, target_role, mib_main.get_next_difficulty(st.session_state.queue_answers))

                    translated_q = tr(st.session_state.p_question, current_lang)
                    st.subheader(tr("Question:", current_lang))
                    st.write(translated_q)
                    auto_speak(translated_q, current_lang, f"autoq_p_{idx}")
                    speak_button(translated_q, current_lang, f"speak_pq_{idx}")

                    p_answer = mic_text_area(tr("Your Answer", current_lang), f"p_answer_{idx}", current_lang)

                    if st.button(tr("Submit Answer", current_lang), key=f"submit_p_{idx}"):
                        if p_answer:
                            with st.spinner(tr("Evaluating your answer...", current_lang)):
                                target_role = st.session_state.get("target_role", "the role")
                                st.session_state.p_feedback = mib_main.evaluate_answer(st.session_state.p_question, p_answer, target_role)
                        else:
                            st.warning(tr("Please write an answer first!", current_lang))

                    if st.session_state.p_feedback:
                        translated_fb = tr(st.session_state.p_feedback, current_lang)
                        st.subheader("🎙️ " + tr("Ira's Feedback:", current_lang))
                        st.write(translated_fb)
                        speak_button(translated_fb, current_lang, f"speak_pfb_{idx}")

                        if st.button(tr("Next Question ➡️", current_lang), key=f"next_{idx}"):
                            p_score = mib_main.extract_score(st.session_state.p_feedback)
                            st.session_state.queue_answers.append({
                                "skill": current_skill, "question": st.session_state.p_question,
                                "feedback": st.session_state.p_feedback, "score": p_score
                            })
                            st.session_state.queue_index += 1
                            st.session_state.p_question = None
                            st.session_state.p_feedback = None
                            st.rerun()
                else:
                    st.success(tr("🎉 Interview complete! Here's your summary:", current_lang))
                    for i, item in enumerate(st.session_state.queue_answers):
                        st.markdown(f"**{i+1}. {item['skill'].title()}** — {tr(item['question'], current_lang)}")
                        st.write(tr(item['feedback'], current_lang))
                        st.markdown("---")

    # ============ ADAPTIVE MODE (AI adjusts topic/difficulty) ============
    elif is_adaptive:
        role = st.text_input(tr("Job Role", current_lang), placeholder="e.g. Data Analyst", key="adaptive_role")
        num_questions = st.slider(tr("Total Questions", current_lang), 5, 12, 8)

        if "adaptive_history" not in st.session_state:
            st.session_state.adaptive_history = []
            st.session_state.adaptive_question = None
            st.session_state.adaptive_feedback = None
            st.session_state.adaptive_count = 0

        if role and st.session_state.adaptive_count == 0 and not st.session_state.adaptive_question:
            st.markdown("### 🎓 " + tr("Interview Summary", current_lang))
            st.info(
                f"**{tr('Mode', current_lang)}:** {tr('AI Adaptive Interview', current_lang)}\n\n"
                f"**{tr('Subject', current_lang)}:** {role}"
            )
            ira_msg = mib_main.get_ira_greeting("AI Adaptive Interview", role)
            translated_greeting = tr(ira_msg, current_lang)
            st.write("🎙️ " + translated_greeting)
            auto_speak(translated_greeting, current_lang, "greeting_adaptive")

        if st.button(tr("Start Adaptive Interview", current_lang)):
            if role:
                st.session_state.target_role = role
                st.session_state.adaptive_history = []
                st.session_state.adaptive_question = None
                st.session_state.adaptive_feedback = None
                st.session_state.adaptive_count = 0
            else:
                st.warning(tr("Please enter a role first!", current_lang))

        # Interview in progress (while a role is set and count < total)
        if role and st.session_state.adaptive_count < num_questions:
            idx = st.session_state.adaptive_count
            st.progress(idx / num_questions)
            st.caption(f"{tr('Question', current_lang)} {idx + 1} / {num_questions}")

            if st.session_state.adaptive_question is None:
                with st.spinner(tr("Preparing the next question...", current_lang)):
                    st.session_state.adaptive_question = mib_main.generate_adaptive_question(role, st.session_state.adaptive_history)

            translated_q = tr(st.session_state.adaptive_question, current_lang)
            st.subheader(tr("Question:", current_lang))
            st.write(translated_q)
            auto_speak(translated_q, current_lang, f"autoq_a_{idx}")
            speak_button(translated_q, current_lang, f"speak_aq_{idx}")

            a_answer = mic_text_area(tr("Your Answer", current_lang), f"a_answer_{idx}", current_lang)

            if st.button(tr("Submit Answer", current_lang), key=f"submit_a_{idx}"):
                if a_answer:
                    with st.spinner(tr("Evaluating your answer...", current_lang)):
                        st.session_state.adaptive_feedback = mib_main.evaluate_answer(st.session_state.adaptive_question, a_answer, role)
                else:
                    st.warning(tr("Please write an answer first!", current_lang))

            if st.session_state.adaptive_feedback:
                translated_fb = tr(st.session_state.adaptive_feedback, current_lang)
                st.subheader("🎙️ " + tr("Ira's Feedback:", current_lang))
                st.write(translated_fb)
                speak_button(translated_fb, current_lang, f"speak_afb_{idx}")

                score = mib_main.extract_score(st.session_state.adaptive_feedback)

                if st.button(tr("Next Question ➡️", current_lang), key=f"next_a_{idx}"):
                    st.session_state.adaptive_history.append({
                        "question": st.session_state.adaptive_question,
                        "answer": a_answer,
                        "score": score if score is not None else 5
                    })
                    st.session_state.adaptive_count += 1
                    st.session_state.adaptive_question = None
                    st.session_state.adaptive_feedback = None
                    st.rerun()

        elif role and st.session_state.adaptive_count >= num_questions and st.session_state.adaptive_history:
            st.success(tr("🎉 Adaptive interview complete! Here's your summary:", current_lang))
            scores = [h["score"] for h in st.session_state.adaptive_history if h["score"] is not None]
            if scores:
                avg = sum(scores) / len(scores)
                st.metric(tr("Average Score", current_lang), f"{avg:.1f} / 10")
            for i, item in enumerate(st.session_state.adaptive_history):
                st.markdown(f"**{i+1}. {tr(item['question'], current_lang)}**")
                st.write(f"{tr('Score', current_lang)}: {item['score']}/10")
                st.markdown("---")

    # ============ ROLE-BASED MODE (original flow) ============
    else:
        role = st.text_input(tr("Job Role", current_lang), placeholder="e.g. Machine Learning Engineer")
        st.session_state.target_role = role
        difficulty = st.selectbox(tr("Difficulty Level", current_lang), ["Easy", "Medium", "Hard"])

        if "question" not in st.session_state:
            st.session_state.question = None

        if role and not st.session_state.question:
            st.markdown("### 🎓 " + tr("Interview Summary", current_lang))
            st.info(
                f"**{tr('Mode', current_lang)}:** {tr('Role-Based Interview', current_lang)}\n\n"
                f"**{tr('Subject', current_lang)}:** {role} ({difficulty})"
            )
            ira_msg = mib_main.get_ira_greeting("Role-Based Interview", role)
            translated_greeting = tr(ira_msg, current_lang)
            st.write("🎙️ " + translated_greeting)
            auto_speak(translated_greeting, current_lang, "greeting_rolebased")

        if st.button(tr("Generate Question", current_lang)):
            if role:
                st.session_state.question = mib_main.generate_interview_question(role, difficulty)
                st.session_state.feedback = None
            else:
                st.warning(tr("Please enter a role first!", current_lang))

        if st.session_state.question:
            translated_question = tr(st.session_state.question, current_lang)
            st.subheader(tr("Interview Question:", current_lang))
            st.write(translated_question)
            auto_speak(translated_question, current_lang, f"autoq_r_{st.session_state.question[:30]}")
            speak_button(translated_question, current_lang, "speak_question")

            answer = mic_text_area(tr("Your Answer", current_lang), "interview_answer", current_lang)

            if st.button(tr("Submit Answer", current_lang)):
                if answer:
                    with st.spinner(tr("Evaluating your answer...", current_lang)):
                        st.session_state.feedback = mib_main.evaluate_answer(st.session_state.question, answer, role)
                else:
                    st.warning(tr("Please write an answer first!", current_lang))

            if st.session_state.get("feedback"):
                translated_feedback = tr(st.session_state.feedback, current_lang)
                st.subheader("🎙️ " + tr("Ira's Feedback:", current_lang))
                st.write(translated_feedback)
                speak_button(translated_feedback, current_lang, "speak_feedback")

                # Also track the Role-Based interview score for Career Insights
                rb_score = mib_main.extract_score(st.session_state.feedback)
                if rb_score is not None:
                    if "rolebased_scores" not in st.session_state:
                        st.session_state.rolebased_scores = []
                    if "rolebased_logged_questions" not in st.session_state:
                        st.session_state.rolebased_logged_questions = []
                    already_logged = st.session_state.question in st.session_state.rolebased_logged_questions
                    if not already_logged:
                        st.session_state.rolebased_scores.append(rb_score)
                        st.session_state.rolebased_logged_questions.append(st.session_state.question)

elif page == "skillgap":
    st.title(tr("🧠 Skill Gap Analysis", current_lang))
    st.write(tr("Compare your skills with the target role and see what you still need to learn.", current_lang))

    sg_main = load_module("sg_main", os.path.join("skill_gap", "main.py"))

    if "user_skills" not in st.session_state or not st.session_state.user_skills:
        st.warning(tr("Analyze your resume in 'Resume Analyzer' first, so your skills can be used here.", current_lang))
    else:
        st.info(f"{tr('Skills found from resume:', current_lang)} {len(st.session_state.user_skills)}")

        category = st.selectbox(tr("Choose a category:", current_lang), list(sg_main.ROLE_CATEGORIES.keys()))
        roles_in_category = sg_main.ROLE_CATEGORIES[category] + ["✍️ Enter my own role"]
        selected_option = st.selectbox(tr("Choose target role:", current_lang), roles_in_category)

        if selected_option == "✍️ Enter my own role":
            target_role = st.text_input(tr("Type your target role:", current_lang), placeholder="e.g. DevOps Engineer")
        else:
            target_role = selected_option

        if st.button(tr("Check Skill Gap", current_lang)):
            if not target_role:
                st.warning(tr("Please type or select a role first.", current_lang))
            elif target_role not in sg_main.ROLE_SKILLS:
                st.error(f"'{target_role}' {tr('is not in our database yet.', current_lang)}")
            else:
                matched, missing, percentage = sg_main.get_skill_gap(st.session_state.user_skills, target_role)
                st.session_state.sg_matched = matched
                st.session_state.sg_missing = missing
                st.session_state.sg_percentage = percentage
                st.session_state.target_role = target_role

        if "sg_percentage" in st.session_state:
            matched = st.session_state.sg_matched
            missing = st.session_state.sg_missing
            percentage = st.session_state.sg_percentage

            st.subheader(f"{tr('Match', current_lang)}: {percentage:.1f}%")
            st.progress(percentage / 100)

            st.markdown(f"### ✅ {tr('Skills You Have', current_lang)}")
            if matched:
                for skill in sorted(matched):
                    st.markdown(f"- {tr(skill.title(), current_lang)}")
            else:
                st.write(tr("No matches found", current_lang))

            st.markdown("---")
            st.markdown(f"### 📚 {tr('Missing / Weak Skills (By Priority)', current_lang)}")

            if missing:
                high, medium, low = sg_main.get_priority_skills(missing)

                if high:
                    st.markdown(f"#### 🔴 {tr('High Priority', current_lang)}")
                    for skill in high:
                        rec = sg_main.get_skill_recommendation(skill)
                        with st.expander(f"{skill.title()}"):
                            st.write(f"**{tr('Learn', current_lang)}:** {tr(rec['learn'], current_lang)}")
                            st.write(f"**{tr('Practice', current_lang)}:** {tr(rec['practice'], current_lang)}")

                if medium:
                    st.markdown(f"#### 🟠 {tr('Medium Priority', current_lang)}")
                    for skill in medium:
                        rec = sg_main.get_skill_recommendation(skill)
                        with st.expander(f"{skill.title()}"):
                            st.write(f"**{tr('Learn', current_lang)}:** {tr(rec['learn'], current_lang)}")
                            st.write(f"**{tr('Practice', current_lang)}:** {tr(rec['practice'], current_lang)}")

                if low:
                    st.markdown(f"#### 🟢 {tr('Low Priority', current_lang)}")
                    for skill in low:
                        rec = sg_main.get_skill_recommendation(skill)
                        with st.expander(f"{skill.title()}"):
                            st.write(f"**{tr('Learn', current_lang)}:** {tr(rec['learn'], current_lang)}")
                            st.write(f"**{tr('Practice', current_lang)}:** {tr(rec['practice'], current_lang)}")

                st.markdown("---")
                if st.button(f"🎤 {tr('Practice Weak Skills', current_lang)}", use_container_width=True):
                    st.session_state["nav_target"] = "interview"
                    st.rerun()
            else:
                st.write(tr("You already have all the required skills! 🎉", current_lang))

            summary_text = tr(
                f"Match {percentage:.1f} percent. You have: {', '.join(matched) if matched else 'none'}. "
                f"You need to learn: {', '.join(missing) if missing else 'none'}.",
                current_lang
            )
            speak_button(summary_text, current_lang, "speak_skillgap")

elif page == "career":
    st.title(tr("📊 Career Insights", current_lang))
    st.write(tr("A combined summary of all your modules — see how ready you are.", current_lang))

    ci_main = load_module("ci_main", os.path.join("career_insights", "main.py"))

    resume_score = st.session_state.get("resume_score")
    skillgap_pct = st.session_state.get("sg_percentage")
    interview_avg = get_interview_avg()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"### 📄 {tr('Resume Match', current_lang)}")
        if resume_score is not None:
            st.metric(tr("Score", current_lang), f"{resume_score:.1f}%")
        else:
            st.info(tr("You haven't used Resume Analyzer yet.", current_lang))

    with col2:
        st.markdown(f"### 🧠 {tr('Skill Gap Match', current_lang)}")
        if skillgap_pct is not None:
            st.metric(tr("Score", current_lang), f"{skillgap_pct:.1f}%")
        else:
            st.info(tr("You haven't checked Skill Gap yet.", current_lang))

    with col3:
        st.markdown(f"### 🎤 {tr('Interview Average', current_lang)}")
        if interview_avg is not None:
            st.metric(tr("Score", current_lang), f"{interview_avg:.1f} / 10")
        else:
            st.info(tr("You haven't completed any interview yet.", current_lang))

    st.markdown("---")

    overall, label = ci_main.compute_readiness(resume_score, skillgap_pct, interview_avg)

    if overall is not None:
        st.subheader(tr("Overall Career Readiness", current_lang))
        st.progress(min(overall / 100, 1.0))
        st.markdown(f"## {tr(label, current_lang)} — {overall:.1f}%")

        summary_text = tr(f"Your overall career readiness score is {overall:.1f} percent. {label}", current_lang)
        speak_button(summary_text, current_lang, "speak_career")
    else:
        st.warning(tr("Use Resume Analyzer, Skill Gap, or Mock Interview first to see your Career Insights.", current_lang))
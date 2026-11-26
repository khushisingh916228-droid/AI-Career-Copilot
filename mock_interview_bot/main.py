from dotenv import load_dotenv
import os
import re
import sys

# app.py is file ko load_module se kholta hai, isliye apna folder path mein jodna zaroori hai
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llm_client import ask_llm

load_dotenv()

def safe_generate(prompt):
    """AI call ko safely wrap karta hai: pehle Groq, fail ho to Gemini. Crash nahi karta."""
    try:
        return ask_llm(prompt)
    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "quota" in error_str.lower() or "ResourceExhausted" in error_str:
            return "\u26a0\ufe0f Daily API limit khatam ho gaya hai. Thodi der baad (ya kal) dobara try karo."
        return f"\u26a0\ufe0f Kuch error aaya: {error_str[:150]}"

def generate_interview_question(role, difficulty="medium"):
    prompt = f"""Generate ONE technical interview question for a {role}.
Difficulty level: {difficulty}.
Only output the question, nothing else."""

    return safe_generate(prompt)

LEVELS = ["easy", "medium", "hard"]

LEVEL_GUIDES = {
    "easy": "Ask a beginner-friendly question on ONE basic concept (a definition or simple use) that can be answered in 2-4 sentences.",
    "medium": "Ask a practical question on ONE concept, such as how you would use it in a small real task, answerable in 4-6 sentences.",
    "hard": "Ask a short scenario-based question where the candidate must pick an approach and justify it, still on ONE concept and answerable in 5-8 sentences.",
}

def get_next_difficulty(answers):
    """Pichle jawabon ke score se agla level nikalta hai (score 7+ upar, 4 ya kam neeche).
    Question number ka cap bhi lagta hai: Q1-3 easy, Q4-7 tak medium, hard sirf Q8+.
    Score kisi ka na mile to sirf cap (question number) se level milta hai."""
    idx = len(answers)
    cap = 0 if idx < 3 else (1 if idx < 7 else 2)
    level = 0
    scored = False
    for a in answers:
        s = a.get("score")
        if s is None:
            continue
        scored = True
        if s >= 7:
            level += 1
        elif s <= 4:
            level -= 1
        level = max(0, min(2, level))
    if not scored:
        return LEVELS[cap]
    return LEVELS[min(level, cap)]

def generate_skill_based_question(skill, role="", difficulty="medium"):
    """Skill Gap se aayi ek specific skill pe question banata hai"""
    role_context = f" for a {role} position" if role else ""
    level_guide = LEVEL_GUIDES.get(str(difficulty).lower(), LEVEL_GUIDES["easy"])
    prompt = f"""Generate ONE technical interview question that specifically tests a candidate's
knowledge of "{skill}"{role_context}.
The candidate is a fresher (final-year student, 0-1 years of experience). {level_guide}
Difficulty level: {difficulty}.
Only output the question, nothing else."""

    return safe_generate(prompt)

def build_personalized_queue(missing_skills, total_questions=10):
    """
    Missing skills ki list leke, unme total_questions ko proportionally
    distribute karta hai. Har skill ko kam se kam 1 question milta hai.
    """
    skills = sorted(missing_skills)
    n = len(skills)
    if n == 0:
        return []

    base = total_questions // n
    remainder = total_questions % n

    if base == 0:
        skills = skills[:total_questions]
        counts = [1] * len(skills)
    else:
        counts = [base] * n
        for i in range(remainder):
            counts[i] += 1

    queue = []
    for skill, count in zip(skills, counts):
        queue.extend([skill] * count)
    return queue

def generate_adaptive_question(role, history):
    """
    history: list of dicts [{"question":..., "answer":..., "score":...}, ...]
    Pichle performance ke hisaab se agla question ka topic/difficulty decide karta hai.
    """
    history_text = ""
    for h in history[-3:]:
        q = h["question"]
        a = h["answer"]
        s = h["score"]
        history_text += "Q: " + q + "\nA: " + a + "\nScore: " + str(s) + "/10\n\n"

    last_score = history[-1]["score"] if history else None

    if last_score is None:
        difficulty_hint = "Start with an EASY, beginner-level question (a basic definition or simple use of one concept)."
    elif last_score <= 5:
        difficulty_hint = "The candidate struggled with the last question. Ask an EASIER question on the SAME topic to reinforce understanding."
    elif last_score <= 7:
        difficulty_hint = "The candidate did okay. Ask a slightly harder question, either on the same topic or a related one."
    else:
        difficulty_hint = "The candidate did well. Move to a NEW topic and increase the difficulty slightly."

    prompt = f"""You are conducting an adaptive technical interview for a {role} position.

Interview history so far:
{history_text if history_text else "No questions asked yet."}

{difficulty_hint}

The candidate is a fresher (final-year student, 0-1 years of experience). Keep the question focused on ONE concept and answerable in a few sentences. Do not ask system-design or multi-part questions unless the candidate scored 8 or more on recent answers.

Generate ONE technical interview question. Only output the question, nothing else."""

    return safe_generate(prompt)

def get_ira_greeting(mode, subject):
    """Ira (AI interviewer persona) greeting message, shown before the interview starts"""
    return (
        f"Hi, I'm Ira — your AI interviewer for today! 👋 "
        f"We'll be doing a '{mode}', focusing on: {subject}. "
        f"Relax and give it your best shot — I'll give you honest, detailed feedback. Let's get started!"
    )

def extract_score(feedback_text):
    """Feedback text se 'Overall Score: X/10' (ya purana 'Score: X/10') nikal ke number return karta hai"""
    match = re.search(r"Overall Score:\s*(\d+(?:\.\d+)?)\s*/\s*10", feedback_text)
    if match:
        return float(match.group(1))
    # Backward-compatible fallback (purana format)
    match = re.search(r"Score:\s*(\d+(?:\.\d+)?)\s*/\s*10", feedback_text)
    if match:
        return float(match.group(1))
    return None

def evaluate_answer(question, answer, role):
    """Ira ki tarah, multi-criteria grading ke saath detailed feedback deti hai"""
    prompt = f"""You are Ira, a friendly but thorough AI interviewer evaluating a candidate for a {role} position.

Question asked: {question}

Candidate's answer: {answer}

Evaluate this answer carefully across multiple criteria. Give feedback in this EXACT format:

Technical Accuracy: [X/10]
Clarity: [X/10]
Completeness: [X/10]
Overall Score: [X/10]
Strengths: [1-2 lines about what was good]
Improvements: [1-2 lines about what could be better]
"""

    return safe_generate(prompt)

# Testing ke liye
if __name__ == "__main__":
    role = "Machine Learning Engineer"

    question = generate_interview_question(role)
    print("Interview Question:")
    print(question)

    test_answer = "Batch Normalization normalizes across the batch dimension, while Layer Normalization normalizes across features. Layer Norm is preferred in Transformers because it works better with variable sequence lengths and doesn't depend on batch size."

    print("\n--- Evaluation ---")
    feedback = evaluate_answer(question, test_answer, role)
    print(feedback)
    print("\nExtracted score:", extract_score(feedback))

    print("\n--- Personalized Queue Test ---")
    queue = build_personalized_queue({"sql", "power bi", "statistics"}, 10)
    print(queue)

    print("\n--- Ira Greeting Test ---")
    print(get_ira_greeting("Role-Based Interview", "Machine Learning Engineer"))
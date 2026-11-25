# AI Career Copilot

An AI-powered career platform that helps students and freshers check how ready they are for a job. It combines resume analysis, skill gap detection, mock interviews and a combined readiness score, with support for 12 languages and voice.

## Modules

| Module | What it does |
|---|---|
| Resume Analyzer | Upload a PDF resume and paste a job description to get a match score, matched and missing skills, and a rule-based recommendation |
| Skill Gap | Compares your resume skills with a target role and lists missing skills by priority (high, medium, low) with learn and practice suggestions |
| Mock Interview Bot | AI interviewer "Ira" with 3 modes: Personalized (based on your skill gap), Role-Based (by role and difficulty) and Adaptive (topic adjusts to your answers). Gives feedback and a score for each answer |
| Career Insights | Combines resume score, skill gap match and interview average into one overall career readiness score |
| Multilingual Layer | Translation, text-to-speech and speech-to-text across the whole app |

## Features

- Login and signup (passwords are stored as SHA-256 hashes)
- 12 interface languages: English, Hindi, Punjabi, Bhojpuri, Marathi, Gujarati, Bengali, Tamil, Telugu, Kannada, Malayalam, Urdu
- Voice: questions are read aloud automatically, and answers can be spoken using the mic
- Home dashboard with career readiness progress and quick access to every module

## Tech Stack

Python, Streamlit, pdfplumber, Google Gemini API, Google Translate, gTTS, SpeechRecognition

## Project Structure

```
AI-Career-Copilot/
|-- app.py                  # Main Streamlit app (login, navigation, all pages)
|-- requirements.txt
|-- resume_analyzer/        # Resume vs job description matching
|-- skill_gap/              # Role-based skill gap and priorities
|-- mock_interview_bot/     # Gemini-powered interview and feedback
|-- career_insights/        # Overall readiness score
`-- multilingual_layer/     # Translation, TTS, STT
```

## Setup

1. Clone the repo

```
git clone https://github.com/khushisingh916228-droid/AI-Career-Copilot.git
cd AI-Career-Copilot
```

2. Create and activate a virtual environment

```
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Add your Gemini API key. Create a file `mock_interview_bot/.env` with:

```
GEMINI_API_KEY=your_key_here
```

5. Run the app

```
streamlit run app.py
```

## Notes

- `.env`, `users.json` and generated audio files are not committed to the repo.
- The standalone version of the Resume Analyzer is available at https://github.com/khushisingh916228-droid/AI-Resume-Analyzer

## Author

Khushi, B.Tech AI and ML, Khalsa College of Engineering & Technology, Amritsar


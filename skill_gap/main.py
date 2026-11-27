# Roles by category and their required skills

ROLE_SKILLS = {
    # AI / Machine Learning
    "AI Engineer": {"python", "machine learning", "deep learning", "tensorflow", "pytorch", "docker", "api development"},
    "Machine Learning Engineer": {"python", "machine learning", "deep learning", "tensorflow", "pytorch", "sql", "docker"},
    "Deep Learning Engineer": {"python", "deep learning", "tensorflow", "pytorch", "computer vision", "nlp"},
    "NLP Engineer": {"python", "nlp", "machine learning", "deep learning", "pytorch", "tensorflow"},
    "Computer Vision Engineer": {"python", "computer vision", "deep learning", "tensorflow", "pytorch", "opencv"},
    "Generative AI Engineer": {"python", "generative ai", "llm", "prompt engineering", "langchain", "machine learning"},
    "AI Researcher": {"python", "machine learning", "deep learning", "research", "statistics", "generative ai"},
    "MLOps Engineer": {"python", "docker", "kubernetes", "aws", "azure", "mlops", "ci/cd"},
    "Prompt Engineer": {"prompt engineering", "generative ai", "llm", "python", "communication"},
    "AI Product Engineer": {"python", "machine learning", "api development", "product management", "communication"},

    # Data
    "Data Analyst": {"sql", "excel", "python", "data visualization", "tableau", "statistics"},
    "Data Scientist": {"python", "sql", "machine learning", "statistics", "pandas", "numpy", "data visualization"},
    "Business Analyst": {"sql", "excel", "communication", "data visualization", "business analysis"},
    "Data Engineer": {"python", "sql", "etl", "data warehousing", "spark", "aws"},
    "BI Analyst": {"sql", "power bi", "tableau", "excel", "data visualization"},
    "BI Developer": {"sql", "power bi", "data warehousing", "etl", "data visualization"},
    "Machine Learning Data Analyst": {"python", "sql", "machine learning", "statistics", "pandas"},
    "Product Analyst": {"sql", "excel", "data visualization", "communication", "a/b testing"},
    "Marketing Data Analyst": {"sql", "excel", "data visualization", "google analytics", "statistics"},

    # Software / Development
    "Python Developer": {"python", "sql", "git", "api development", "django", "flask"},
    "Software Developer": {"python", "java", "git", "algorithms", "oop"},
    "Backend Developer": {"python", "sql", "api development", "django", "flask", "docker", "git"},
    "Frontend Developer": {"html", "css", "javascript", "react", "git", "responsive design"},
    "Full Stack Developer": {"html", "css", "javascript", "react", "python", "sql", "git", "api development"},
    "Java Developer": {"java", "sql", "git", "oop", "rest api"},
    "Web Developer": {"html", "css", "javascript", "git", "responsive design"},
    "Mobile App Developer": {"java", "kotlin", "flutter", "react native", "git"},
    "Cloud Developer": {"aws", "azure", "docker", "api development", "python"},
    "DevOps Engineer": {"docker", "kubernetes", "aws", "ci/cd", "git", "linux"},

    # Other Technology Roles
    "Cybersecurity Analyst": {"cybersecurity", "network security", "communication", "sql"},
    "Cloud Engineer": {"aws", "azure", "docker", "kubernetes", "linux"},
    "Database Administrator": {"sql", "database management", "excel", "communication"},
    "QA Engineer": {"testing", "automation testing", "selenium", "communication"},
    "Automation Engineer": {"python", "testing", "automation testing", "selenium"},
    "IoT Engineer": {"python", "iot", "embedded systems", "communication"},
    "Blockchain Developer": {"blockchain", "solidity", "python", "git"},
    "Solutions Engineer": {"communication", "api development", "sql", "python"},
    "Technical Support Engineer": {"communication", "sql", "excel", "troubleshooting"},

    # Product / Design
    "UI/UX Designer": {"figma", "wireframing", "prototyping", "user research", "communication"},
    "Product Designer": {"figma", "prototyping", "user research", "communication"},
    "Product Manager": {"product management", "communication", "excel", "agile", "roadmap planning"},
    "Technical Product Manager": {"product management", "sql", "communication", "agile", "api development"},
}

ROLE_CATEGORIES = {
    "🤖 AI / Machine Learning": [
        "AI Engineer", "Machine Learning Engineer", "Deep Learning Engineer", "NLP Engineer",
        "Computer Vision Engineer", "Generative AI Engineer", "AI Researcher", "MLOps Engineer",
        "Prompt Engineer", "AI Product Engineer"
    ],
    "📊 Data": [
        "Data Analyst", "Data Scientist", "Business Analyst", "Data Engineer", "BI Analyst",
        "BI Developer", "Machine Learning Data Analyst", "Product Analyst", "Marketing Data Analyst"
    ],
    "💻 Software / Development": [
        "Python Developer", "Software Developer", "Backend Developer", "Frontend Developer",
        "Full Stack Developer", "Java Developer", "Web Developer", "Mobile App Developer",
        "Cloud Developer", "DevOps Engineer"
    ],
    "🔐 Other Technology Roles": [
        "Cybersecurity Analyst", "Cloud Engineer", "Database Administrator", "QA Engineer",
        "Automation Engineer", "IoT Engineer", "Blockchain Developer", "Solutions Engineer",
        "Technical Support Engineer"
    ],
    "🎨 Product / Design": [
        "UI/UX Designer", "Product Designer", "Product Manager", "Technical Product Manager"
    ],
}

SKILL_RECOMMENDATIONS = {
    "sql": {"learn": "Joins, subqueries, window functions, indexing", "practice": "Write complex queries on a sample database (e.g. Kaggle datasets)"},
    "power bi": {"learn": "Dashboards, DAX formulas, data modeling", "practice": "Build a sales/marketing data dashboard"},
    "tableau": {"learn": "Visualizations, calculated fields, dashboards", "practice": "Build an interactive dashboard using a public dataset"},
    "statistics": {"learn": "Hypothesis testing, distributions, regression basics", "practice": "Apply descriptive + inferential statistics on a dataset"},
    "excel": {"learn": "Pivot tables, VLOOKUP/XLOOKUP, formulas", "practice": "Analyze a real dataset in Excel"},
    "python": {"learn": "Core syntax, pandas, numpy, OOP basics", "practice": "Build small automation scripts or data analysis projects"},
    "machine learning": {"learn": "Supervised/unsupervised algorithms, model evaluation", "practice": "Try a beginner competition on Kaggle"},
    "deep learning": {"learn": "Neural networks, CNNs, RNNs, TensorFlow/PyTorch basics", "practice": "Build an image classification project"},
    "docker": {"learn": "Containers, Dockerfile, docker-compose", "practice": "Containerize any of your existing projects with Docker"},
    "kubernetes": {"learn": "Pods, deployments, services", "practice": "Deploy an app on a local Kubernetes cluster (minikube)"},
    "aws": {"learn": "EC2, S3, Lambda basics", "practice": "Host a small project on AWS free tier"},
    "azure": {"learn": "Azure fundamentals, App Services", "practice": "Deploy an app on Azure free tier"},
    "django": {"learn": "Models, views, templates, REST framework", "practice": "Build a small CRUD web app"},
    "flask": {"learn": "Routes, templates, REST API basics", "practice": "Build a simple API in Flask"},
    "react": {"learn": "Components, hooks, state management", "practice": "Build a to-do app or portfolio site"},
    "javascript": {"learn": "ES6+, DOM manipulation, async/await", "practice": "Build small interactive web projects"},
    "git": {"learn": "Branching, merging, pull requests", "practice": "Properly maintain your existing projects on GitHub"},
    "api development": {"learn": "REST principles, authentication, documentation", "practice": "Build a public API and test it with Postman"},
    "communication": {"learn": "Clear technical writing, presentation skills", "practice": "Practice explaining your projects (like this viva prep!)"},
    "data visualization": {"learn": "Chart types, storytelling with data", "practice": "Build a data story using matplotlib/seaborn"},
    "cybersecurity": {"learn": "Network security basics, common vulnerabilities", "practice": "Try platforms like TryHackMe/HackTheBox"},
    "figma": {"learn": "Wireframing, prototyping, design systems", "practice": "Create a UI mockup for an app"},
    "agile": {"learn": "Scrum framework, sprints, user stories", "practice": "Try sprint-style planning on any project"},
}

def get_skill_gap(user_skills, target_role):
    required = ROLE_SKILLS.get(target_role, set())
    user_skills_lower = set(s.lower() for s in user_skills)
    required_lower = set(s.lower() for s in required)

    matched = user_skills_lower & required_lower
    missing = required_lower - user_skills_lower

    percentage = (len(matched) / len(required_lower) * 100) if required_lower else 0

    return matched, missing, percentage

def get_priority_skills(missing_skills):
    """Divides the missing skills into High/Medium/Low priority."""
    skills = sorted(missing_skills)
    n = len(skills)
    if n == 0:
        return [], [], []

    third = max(1, n // 3)
    high = skills[:third]
    medium = skills[third:third * 2] if n > third else []
    low = skills[third * 2:] if n > third * 2 else []

    return high, medium, low

def get_skill_recommendation(skill):
    """Returns what to learn and how to practice for one skill."""
    key = skill.lower()
    if key in SKILL_RECOMMENDATIONS:
        return SKILL_RECOMMENDATIONS[key]
    return {
        "learn": f"Fundamentals and core concepts of {skill.title()}",
        "practice": f"Learn {skill.title()} from online courses or tutorials, then build a small project"
    }
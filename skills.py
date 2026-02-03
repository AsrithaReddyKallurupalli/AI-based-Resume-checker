import re

# Comprehensive list of technical skills (can be expanded)
SKILLS_DB = [
    # Languages
    "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "HTML", "CSS", "SQL", "Go", "Rust", "Swift", "Kotlin", "PHP", "Ruby",
    # Frameworks/Libraries
    "React", "Angular", "Vue", "Node.js", "Django", "Flask", "FastAPI", "Spring Boot", ".NET", "Pandas", "NumPy", "Scikit-Learn", "TensorFlow", "PyTorch", "Keras", "Hadoop", "Spark",
    # Databases
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle", "SQL Server", "DynamoDB",
    # Cloud & DevOps
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "Git", "GitHub", "GitLab", "Terraform", "Ansible",
    # Concepts/Other
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "Data Science", "Big Data", "REST API", "GraphQL", "Microservices", "Agile", "Scrum"
]

def extract_skills(text):
    text = text.lower()
    found_skills = set()
    for skill in SKILLS_DB:
        # Match whole words only to avoid false positives (e.g. "go" in "google")
        # Escape special chars like C++
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text):
            found_skills.add(skill)
    return found_skills

def match_skills(resume_text, jd_text):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    
    missing_skills = jd_skills - resume_skills
    matching_skills = resume_skills.intersection(jd_skills)
    
    match_percentage = (len(matching_skills) / len(jd_skills) * 100) if jd_skills else 100
    
    return {
        "resume_skills": sorted(list(resume_skills)),
        "jd_skills": sorted(list(jd_skills)),
        "missing_skills": sorted(list(missing_skills)),
        "match_percentage": round(match_percentage, 2)
    }

import ats_checker
import sys

print("Testing ATS Checker...")

try:
    checker = ats_checker.ATSChecker()
    resume_text = "Experienced Python Developer with 5 years experience in AWS and Docker."
    jd_text = "Looking for a Python Developer with AWS and Cloud skills."
    
    skill_analysis = {
        "resume_skills": ["python", "aws"],
        "missing_skills": ["docker"]
    }
    ai_prob = 10.0
    
    result = checker.calculate_score(resume_text, jd_text, skill_analysis, ai_prob)
    print("Success!")
    print(result)
    
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()

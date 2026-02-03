import re

def check_quantification(text):
    """
    Checks if the text contains numbers or percentages, suggesting quantification.
    """
    # Regex for number phrases like "20%", "$50k", "5 users", "increased by 10"
    matches = re.findall(r'\b\d+%|\$\d+|\b\d+\s+(?:users|clients|percent|increase|reduction|years)', text.lower())
    return len(matches) > 0

def get_suggestions(resume_text, missing_skills, ai_analysis):
    """
    Generates actionable additions and improvements for the candidate.
    """
    add_list = []
    improve_list = []
    
    # 1. ADD Suggestions (Skills)
    if missing_skills:
        # Take the top 3-5 missing skills to prioritize
        top_missing = missing_skills[:5]
        add_list.append(f"Add missing high-priority skills to your summary or skills section: {', '.join(top_missing)}.")
        if any(skill.lower() in ['aws', 'azure', 'gcp', 'docker', 'kubernetes'] for skill in missing_skills):
            add_list.append("Include Cloud/DevOps tools if you have used them, as they are highly valued.")

    # 2. ADD Suggestions (Projects)
    if "project" not in resume_text.lower():
        add_list.append("Add a 'Projects' section to showcase hands-on experience with your skills.")

    # 3. IMPROVE Suggestions (Quantification)
    # 3. IMPROVE Suggestions (Quantification)
    quant_count = len(re.findall(r'\b\d+%|\$\d+|\b\d+\s+(?:users|clients|percent|increase|reduction|years)', resume_text.lower()))
    if quant_count < 3:
        improve_list.append("Quantify your impact more aggressively. Use numbers (%, $) to prove your value (e.g., 'Reduced costs by 15%').")

    # 4. IMPROVE Suggestions (AI/Phrasing)
    if ai_analysis and ai_analysis.get('ai_probability', 0) > 30: # Lower threshold to 30
        improve_list.append("Vary your sentence structure. Uniform patterns can trigger AI detection; try mixing short and long sentences.")
        improve_list.append("Replace generic words like 'Utilized' or 'Worked on' with strong action verbs: 'Engineered', 'Spearheaded', 'Optimized'.")

    # 5. NEW: Action Verbs Check
    action_verbs = ['led', 'developed', 'managed', 'created', 'designed', 'implemented', 'optimized', 'engineered', 'launched']
    if not any(verb in resume_text.lower() for verb in action_verbs):
        improve_list.append(f"Use strong action verbs to start your bullet points (e.g., {', '.join(action_verbs[:3])}).")

    # 6. Fallback if empty
    if not add_list and not improve_list:
        improve_list.append("Review your formatting to ensure it is ATS-friendly (simple, single-column layout).")
        add_list.append("Consider adding a 'Key Competencies' section to highlight your top technical strengths at a glance.")
    
    return {
        "add": add_list,
        "improve": improve_list
    }

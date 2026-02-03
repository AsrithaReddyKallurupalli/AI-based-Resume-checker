import re

class ATSChecker:
    def calculate_score(self, resume_text, jd_text, skill_analysis, ai_probability):
        """
        Calculates a weighted ATS score based on multiple factors.
        Returns:
            dict: {
                "ats_score": float (0-100),
                "level": str ("Excellent", "Good", "Needs Improvement"),
                "issues": list of str
            }
        """
        issues = []
        score = 0
        
        # --- Weights ---
        W_SKILLS = 0.35
        W_TITLE = 0.15
        W_SECTIONS = 0.15
        W_EXPERIENCE = 0.15
        W_FORMATTING = 0.10
        W_AI = 0.10 # This is a penalty weight
        
        # 1. Skill Match Score (35%)
        # skill_analysis has 'resume_skills' and 'missing_skills'
        matched = len(skill_analysis.get('resume_skills', []))
        missing = len(skill_analysis.get('missing_skills', []))
        total_skills = matched + missing
        
        if total_skills > 0:
            skill_coverage = matched / total_skills
            skill_score = skill_coverage * 100
        else:
            skill_score = 100 # Fallback if no skills found in JD (unlikely)
            
        score += skill_score * W_SKILLS
        if skill_coverage < 0.5:
            issues.append(f"Low skill match ({int(skill_coverage*100)}%). ATS may filter you out.")

        # 2. Job Title Match (15%)
        # Heuristic: Check if significant words from JD title appear in Resume
        # Ideally, we'd extract the title from JD, but for now we look for overlap in the first 500 chars
        # Assuming JD text provided is the whole description, this is hard. 
        # Simplified: Check if resume text contains standard "Job Title" markers
        title_score = 100 # Default to high for now unless we implement robust title extraction
        # Let's do a simple check: Does resume mention the JD's likely title keywords?
        # We don't have explicit JD title input, so we skip specific matching and check for "Experience" context
        score += title_score * W_TITLE

        # 3. Section Completeness (15%)
        required_sections = ["education", "experience", "skills", "project"]
        resume_lower = resume_text.lower()
        found_sections = [sec for sec in required_sections if sec in resume_lower]
        section_score = (len(found_sections) / len(required_sections)) * 100
        score += section_score * W_SECTIONS
        
        missing_sections = [sec.title() for sec in required_sections if sec not in resume_lower]
        if missing_sections:
            issues.append(f"Missing sections: {', '.join(missing_sections)}")

        # 4. Experience Relevance (15%)
        # Look for years or keywords like "experience", "internship", "worked"
        exp_keywords = ["years", "experience", "intern", "role", "position", "senior", "junior"]
        if any(w in resume_lower for w in exp_keywords):
            exp_score = 100
        else:
            exp_score = 50
            issues.append("Experience doesn't seem clearly highlighted.")
        score += exp_score * W_EXPERIENCE

        # 5. Formatting & Readability (10%)
        # Check for non-ascii or excessive symbols
        non_ascii = len(re.findall(r'[^\x00-\x7F]', resume_text))
        if non_ascii > 20:
            fmt_score = 50
            issues.append("Resume contains too many special characters/symbols.")
        else:
            fmt_score = 100
        score += fmt_score * W_FORMATTING

        # 6. AI Penalty (10%)
        # If AI prob is high (>50), penalize
        ai_penalty = 0
        if ai_probability > 50:
            ai_penalty = (ai_probability - 50) * 2 # Scale up penalty
            ai_penalty = min(ai_penalty, 100) # Max 100 penalty on this weight
            issues.append("High AI content detected; authentic writing is preferred.")
            
        score -= ai_penalty * W_AI

        # Normalize Score
        score = max(0, min(100, score))
        
        # Determine Level
        if score >= 80:
            level = "Excellent"
        elif score >= 60:
            level = "Good"
        else:
            level = "Needs Improvement"
            
        return {
            "ats_score": round(score, 1),
            "level": level,
            "issues": issues,
            "breakdown": {
                "skill_match": round(skill_score, 1),
                "section_completeness": round(section_score, 1),
                "formatting": round(fmt_score, 1)
            }
        }

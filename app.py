import resume_parser
import preprocess
import embeddings
import suggestions
import traceback
import importlib

# Force reload to ensure updates to suggestions.py are picked up
importlib.reload(suggestions)

def process_resume_and_jd(resume_path, jd_text):
    """
    Main pipeline to process resume and job description.
    Differs from the monolithic script by being a reusable function.
    """
    try:
        # 1. Parse Resume
        resume_text = resume_parser.get_resume_text(resume_path)
        if not resume_text:
            return {"error": "Could not extract text from the resume. Please check the file format."}

        # 2. Preprocess Text
        clean_resume = preprocess.clean_text(resume_text)
        clean_jd = preprocess.clean_text(jd_text)
        
        # 3. Generate Embeddings (Semantic Understanding)
        # Reshape for cosine similarity (1 sample, N features)
        resume_emb = embeddings.get_embeddings(clean_resume).reshape(1, -1)
        jd_emb = embeddings.get_embeddings(clean_jd).reshape(1, -1)
        
        # 4. Calculate Similarity
        match_score = similarity.calculate_similarity(resume_emb, jd_emb)
        
        # 5. Skill Analysis (Keyword extraction based)
        skill_analysis = skills.match_skills(resume_text, jd_text)

        # 6. AI Content Detection
        checker = ai_content_checker.AIContentChecker()
        ai_analysis = checker.analyze(resume_text)
        
        # 7. Suggestions Engine
        suggestion_results = suggestions.get_suggestions(
            resume_text, 
            skill_analysis['missing_skills'],
            ai_analysis
        )
        
        return {
            "match_score": round(match_score * 100, 2), # Convert 0-1 to percentage
            "skill_analysis": skill_analysis,
            "ai_analysis": ai_analysis,
            "suggestions": suggestion_results,
            "resume_text_snippet": resume_text[:500] + "..." # Snippet for debugging if needed
        }
        
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

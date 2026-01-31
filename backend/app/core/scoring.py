from typing import List, Dict, Any

def calculate_match_score(resume_data: Dict[str, Any], job_requirements: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate a match score between a parsed resume and structured job requirements.
    
    Returns a score (0-100) and a breakdown.
    """
    score = 0
    breakdown = {
        "skills_score": 0,
        "experience_score": 0,
        "education_score": 0,
        "matched_skills": [],
        "missing_skills": []
    }

    # 1. Skills Match (50%)
    req_skills = set([s.lower() for s in job_requirements.get("required_skills", [])])
    parsed_skills = set([s.lower() for s in resume_data.get("skills", [])])
    
    if req_skills:
        matched = req_skills.intersection(parsed_skills)
        breakdown["matched_skills"] = list(matched)
        breakdown["missing_skills"] = list(req_skills - parsed_skills)
        
        skills_ratio = len(matched) / len(req_skills)
        breakdown["skills_score"] = round(skills_ratio * 50)
    else:
        breakdown["skills_score"] = 50 # Default if no requirements
    
    # 2. Experience Match (30%)
    req_exp = job_requirements.get("experience_years", 0)
    # Estimate resume experience - usually LLM extracts a float or we can sum roles
    resume_exp = resume_data.get("total_experience_years", 0)
    
    if req_exp > 0:
        exp_ratio = min(resume_exp / req_exp, 1.2) # Bonus up to 1.2x
        # If they meet req, they get full 30, else partial
        if resume_exp >= req_exp:
             breakdown["experience_score"] = 30
        else:
             breakdown["experience_score"] = round((resume_exp / req_exp) * 30)
    else:
        breakdown["experience_score"] = 30

    # 3. Education Match (20%)
    # Simple hierarchy: Ph.D > Masters > Bachelors > Associate
    edu_rank = {"phd": 4, "masters": 3, "bachelors": 2, "associate": 1, "": 0}
    req_edu = job_requirements.get("education_level", "").lower()
    resume_edu = resume_data.get("education_level", "").lower()
    
    # Normalize req_edu names (common patterns)
    def normalize_edu(e):
        e = e.lower()
        if "phd" in e or "doctor" in e: return "phd"
        if "master" in e: return "masters"
        if "bachelor" in e or "degree" in e: return "bachelors"
        return ""

    n_req = normalize_edu(req_edu)
    n_res = normalize_edu(resume_edu)
    
    if n_req == "":
        breakdown["education_score"] = 20
    else:
        if edu_rank.get(n_res, 0) >= edu_rank.get(n_req, 0):
            breakdown["education_score"] = 20
        else:
            breakdown["education_score"] = 10 # Partial points for having some degree

    total_score = breakdown["skills_score"] + breakdown["experience_score"] + breakdown["education_score"]
    return {
        "score": min(total_score, 100),
        "breakdown": breakdown
    }

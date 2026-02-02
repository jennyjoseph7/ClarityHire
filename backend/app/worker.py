import fitz  # PyMuPDF
import json
import os
import re
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.celery_app import celery_app
from app.db.session import AsyncSessionLocal
from app.models.resume import Resume, ResumeStatus
from app.models.user import User  # Essential for SQLAlchemy relationship resolution
from app.core.config import settings
from groq import Groq
import asyncio

# Setup logger
logger = logging.getLogger(__name__)

# Synchronous wrapper for database update because Celery runs in a separate thread/process
# Ideally we use async with Celery but for simplicity in this setup we might need a sync DB session adapter
# However, our DB stack is async.
# We will run the DB update part in a sync wrapper or using asyncio.run

async def update_resume_status(resume_id: str, status: ResumeStatus, parsed_data: dict = None, error: str = None):
    async with AsyncSessionLocal() as session:
        import uuid
        resume = await session.get(Resume, uuid.UUID(resume_id))
        if resume:
            resume.status = status
            if parsed_data:
                resume.parsed_json = parsed_data
            if error:
                resume.error_message = error
            await session.commit()
        else:
            logger.error(f"Resume not found for resume_id={resume_id}")
            raise ValueError(f"Resume not found for resume_id={resume_id}")

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


# ====== HELPER FUNCTIONS ======
def normalize_skill(skill: str) -> str:
    """Normalize skill names"""
    skill = skill.strip()
    
    # Common mappings
    mappings = {
        "react.js": "React",
        "reactjs": "React",
        "js": "JavaScript",
        "ts": "TypeScript",
        "py": "Python",
        "ml": "Machine Learning",
        "ai": "Artificial Intelligence",
        "next.js": "Next.js",
        "node.js": "Node.js",
        "nodejs": "Node.js",
        "mysql": "MySQL",
        "postgresql": "PostgreSQL",
        "postgres": "PostgreSQL",
        "mongo": "MongoDB",
        "mongodb": "MongoDB"
    }
    
    lower_skill = skill.lower()
    return mappings.get(lower_skill, skill)


def extract_skills_from_text(text: str) -> list:
    """Extract skill keywords from text"""
    common_skills = [
        "Python", "Java", "JavaScript", "TypeScript", "React", "Node.js",
        "Flask", "Django", "MySQL", "PostgreSQL", "MongoDB", "AWS", 
        "Machine Learning", "Data Analysis", "Git", "Docker", "Kubernetes",
        "Spring Boot", "HTML", "CSS", "TailwindCSS", "FastAPI", "SQL"
    ]
    
    found = []
    text_lower = text.lower()
    for skill in common_skills:
        if skill.lower() in text_lower:
            found.append(skill)
    return found


def calculate_total_experience(experiences: list) -> int:
    """Calculate total work experience in months"""
    total = 0
    for exp in experiences:
        total += calculate_duration_months(exp.get("start_date", ""), exp.get("end_date", ""))
    return total


def calculate_duration_months(start: str, end: str) -> int:
    """Calculate months between two dates"""
    try:
        if not start:
            return 0
        
        # Try to parse various date formats
        # Format: "MMM YYYY" or "Month YYYY"
        patterns = [
            r'(\w+)\s+(\d{4})',  # "Jan 2024" or "January 2024"
            r'(\d{4})',          # Just year "2024"
        ]
        
        start_month = start_year = None
        end_month = end_year = None
        
        # Parse start date
        for pattern in patterns:
            match = re.search(pattern, start)
            if match:
                if len(match.groups()) == 2:
                    month_str, year_str = match.groups()
                    start_year = int(year_str)
                    # Try to parse month
                    try:
                        start_month = datetime.strptime(month_str[:3], "%b").month
                    except:
                        start_month = 1  # Default to January
                else:
                    start_year = int(match.group(1))
                    start_month = 1
                break
        
        # Parse end date
        if end and end.lower() not in ["present", "current", "now"]:
            for pattern in patterns:
                match = re.search(pattern, end)
                if match:
                    if len(match.groups()) == 2:
                        month_str, year_str = match.groups()
                        end_year = int(year_str)
                        try:
                            end_month = datetime.strptime(month_str[:3], "%b").month
                        except:
                            end_month = 12
                    else:
                        end_year = int(match.group(1))
                        end_month = 12
                    break
        else:
            # Present - use current date
            now = datetime.now()
            end_year = now.year
            end_month = now.month
        
        if start_year and end_year:
            months = (end_year - start_year) * 12 + (end_month or 12) - (start_month or 1)
            return max(0, months)
        
        return 0
    except Exception as e:
        print(f"Date parsing error: {e}")
        return 0


def estimate_skill_months(skill: str, evidence: list, raw_data: dict) -> int:
    """Estimate months of experience with a skill"""
    # If used in work, count work duration
    for exp in raw_data.get("experience", []):
        exp_techs = exp.get("technologies", [])
        if isinstance(exp_techs, list):
            if skill in [normalize_skill(str(t)) for t in exp_techs]:
                return calculate_duration_months(exp.get("start_date", ""), exp.get("end_date", ""))
    
    # If used in project, estimate 3-6 months
    if any("project:" in str(e) for e in evidence):
        return 3
    
    # If only certification/course, return 0 (just learned)
    return 0


def determine_proficiency(evidence: list, months: int) -> str:
    """Determine skill proficiency level"""
    evidence_count = len(evidence)
    
    if months >= 12 and evidence_count >= 3:
        return "advanced"
    elif months >= 6 or evidence_count >= 2:
        return "intermediate"
    else:
        return "beginner"


def determine_experience_level(total_months: int, experiences: list) -> str:
    """Determine candidate's overall experience level"""
    # Check if mostly virtual
    virtual_count = sum(1 for exp in experiences if "virtual" in str(exp.get("type", "")).lower() or "intern" in str(exp.get("type", "")).lower())
    total_count = len(experiences)
    
    mostly_virtual = virtual_count > total_count / 2 if total_count > 0 else True
    
    if total_months < 12 or (mostly_virtual and total_months < 24):
        return "fresher"
    elif total_months < 36:
        return "junior"
    elif total_months < 60:
        return "mid"
    else:
        return "senior"


def get_top_skills(skills: list, count: int) -> list:
    """Get top N skills by evidence and experience"""
    sorted_skills = sorted(
        skills,
        key=lambda s: (len(s.get("evidence", [])), s.get("months_experience", 0)),
        reverse=True
    )
    return [s["skill"] for s in sorted_skills[:count]]


def infer_employment_type(exp: dict) -> str:
    """Infer employment type from role/description"""
    role = str(exp.get("role", "")).lower()
    company = str(exp.get("company", "")).lower()
    exp_type = str(exp.get("type", "")).lower()
    
    if "intern" in role or "virtual" in company or "intern" in exp_type:
        return "internship"
    elif "contract" in role or "freelance" in role:
        return "contract"
    else:
        return "full-time"


def extract_year(date_str: str) -> int:
    """Extract year from date string"""
    if not date_str:
        return 0
    match = re.search(r'\d{4}', str(date_str))
    return int(match.group()) if match else 0


# ====== STAGE 2: Local Enrichment ======
def enrich_resume_data(raw_data: dict, original_text: str) -> dict:
    """Transform simple extraction into detailed structure needed for matching"""
    
    contact = raw_data.get("contact", {})
    if not isinstance(contact, dict):
        contact = {}
    
    enriched = {
        "name": contact.get("name", ""),
        "email": contact.get("email", ""),
        "phone": contact.get("phone", ""),
        "linkedin": contact.get("linkedin", ""),
        "location": contact.get("location", ""),
        "summary": raw_data.get("summary", ""),
        "skills": [],
        "projects": [],
        "experience": [],
        "education": [],
        "certifications": [],
        "additional_info": {}
    }
    
    # Build evidence map from projects, experience, certifications
    evidence_map = {}  # skill -> [list of evidence]
    
    # Extract from projects
    for project in raw_data.get("projects", []):
        if not isinstance(project, dict):
            continue
        project_name = project.get("title", "Unknown Project")
        techs = project.get("technologies", [])
        if isinstance(techs, list):
            for tech in techs:
                skill = normalize_skill(str(tech))
                if skill not in evidence_map:
                    evidence_map[skill] = []
                evidence_map[skill].append(f"project:{project_name}")
    
    # Extract from experience
    for exp in raw_data.get("experience", []):
        if not isinstance(exp, dict):
            continue
        company = exp.get("company", "Unknown Company")
        techs = exp.get("technologies", [])
        if isinstance(techs, list):
            for tech in techs:
                skill = normalize_skill(str(tech))
                if skill not in evidence_map:
                    evidence_map[skill] = []
                evidence_map[skill].append(f"work:{company}")
    
    # Extract from certifications
    for cert in raw_data.get("certifications", []):
        if not isinstance(cert, dict):
            continue
        cert_name = cert.get("name", "Unknown Cert")
        # Infer skills from certification name
        skills_in_cert = extract_skills_from_text(cert_name)
        for skill in skills_in_cert:
            skill = normalize_skill(skill)
            if skill not in evidence_map:
                evidence_map[skill] = []
            evidence_map[skill].append(f"certification:{cert_name}")
    
    # Build enriched skills array
    all_skills = set()
    
    # Add explicitly mentioned skills
    raw_skills = raw_data.get("skills", [])
    if isinstance(raw_skills, list):
        for skill in raw_skills:
            all_skills.add(normalize_skill(str(skill)))
    
    # Add skills found in evidence
    all_skills.update(evidence_map.keys())
    
    # Calculate experience months per skill (estimate)
    total_exp_months = calculate_total_experience(raw_data.get("experience", []))
    
    for skill in all_skills:
        evidence = evidence_map.get(skill, ["resume:mentioned"])
        
        # Estimate months based on evidence
        months = estimate_skill_months(skill, evidence, raw_data)
        
        # Determine proficiency
        proficiency = determine_proficiency(evidence, months)
        
        enriched["skills"].append({
            "skill": skill,
            "evidence": evidence,
            "months_experience": months,
            "proficiency": proficiency
        })
    
    # Transform projects
    for project in raw_data.get("projects", []):
        if not isinstance(project, dict):
            continue
        enriched["projects"].append({
            "title": project.get("title", ""),
            "description": project.get("description", ""),
            "technologies": [normalize_skill(str(t)) for t in project.get("technologies", []) if t],
            "duration": project.get("duration", ""),
            "key_achievements": project.get("achievements", project.get("key_achievements", [])),
            "url": project.get("url", "")
        })
    
    # Transform experience
    for exp in raw_data.get("experience", []):
        if not isinstance(exp, dict):
            continue
        enriched["experience"].append({
            "company": exp.get("company", ""),
            "role": exp.get("role", ""),
            "type": infer_employment_type(exp),
            "start_date": exp.get("start_date", ""),
            "end_date": exp.get("end_date", "Present"),
            "duration_months": calculate_duration_months(exp.get("start_date", ""), exp.get("end_date", "")),
            "description": exp.get("description", ""),
            "key_responsibilities": exp.get("responsibilities", exp.get("key_responsibilities", [])),
            "technologies_used": [normalize_skill(str(t)) for t in exp.get("technologies", exp.get("technologies_used", [])) if t]
        })
    
    # Transform education
    for edu in raw_data.get("education", []):
        if not isinstance(edu, dict):
            continue
        enriched["education"].append({
            "institution": edu.get("institution", ""),
            "degree": edu.get("degree", ""),
            "field_of_study": edu.get("field", edu.get("field_of_study", "")),
            "start_date": edu.get("start_date", ""),
            "end_date": edu.get("end_date", ""),
            "year": extract_year(edu.get("end_date", edu.get("year", ""))),
            "gpa": edu.get("gpa", ""),
            "relevant_coursework": edu.get("coursework", edu.get("relevant_coursework", []))
        })
    
    # Transform certifications
    for cert in raw_data.get("certifications", []):
        if not isinstance(cert, dict):
            continue
        enriched["certifications"].append({
            "name": cert.get("name", ""),
            "issuer": cert.get("issuer", ""),
            "date": cert.get("date", ""),
            "technologies": extract_skills_from_text(cert.get("name", ""))
        })
    
    # Calculate additional info
    enriched["additional_info"] = {
        "total_experience_months": total_exp_months,
        "experience_level": determine_experience_level(total_exp_months, enriched["experience"]),
        "strongest_skills": get_top_skills(enriched["skills"], 5),
        "volunteering": raw_data.get("volunteering", []),
        "languages": raw_data.get("languages", [])
    }
    
    return enriched


# ====== STAGE 1: Simplified LLM Extraction ======
def parse_with_llm(text: str) -> dict:
    """Stage 1: Extract raw data with simplified LLM prompt"""
    client = Groq(api_key=settings.GROQ_API_KEY)
    
    prompt = f"""Extract ALL information from this resume and return valid JSON.

Extract:
- contact: name, email, phone, linkedin, location
- summary: brief professional summary if mentioned
- skills: Every technology, framework, tool, methodology mentioned
- projects: title, description, technologies used, duration
- experience: company, role, dates, responsibilities, technologies
- education: institution, degree, field, year
- certifications: name, issuer, date

Resume Text:
{text[:20000]}

Return JSON with these keys: contact, summary, skills, projects, experience, education, certifications
Each key should be an object or array as appropriate.
"""
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"},
        timeout=60.0  # 60 second timeout to prevent worker hanging
    )
    
    raw_data = json.loads(completion.choices[0].message.content)
    
    # STAGE 2: Enrich with evidence and structure
    return enrich_resume_data(raw_data, text)


async def parse_resume_async(resume_id: str, file_path: str):
    print(f"WORKER: Starting task for resume {resume_id}")
    try:
        # 1. Update status to PARSING
        print(f"WORKER: Updating status to PARSING...")
        await update_resume_status(resume_id, ResumeStatus.PARSING)
        
        # 2. Extract Text
        print(f"WORKER: Extracting text from {file_path}...")
        text = extract_text_from_pdf(file_path)
        print(f"WORKER: Extracted {len(text)} chars.")
        
        # 3. LLM Extraction (Sync call wrapped to avoid blocking loop too hard, though logic is simple)
        print(f"WORKER: Calling Groq LLM...")
        parsed_data = parse_with_llm(text)
        print(f"WORKER: LLM Success! Keys: {list(parsed_data.keys())}")
        
        # 4. Save Success
        print(f"WORKER: Saving results...")
        await update_resume_status(resume_id, ResumeStatus.PARSED, parsed_data=parsed_data)
        print(f"WORKER: Task Complete.")
        
    except Exception as e:
        print(f"WORKER ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        try:
            # 5. Handle Failure
            await update_resume_status(resume_id, ResumeStatus.FAILED, error=str(e))
        except Exception as db_err:
             print(f"WORKER CRITICAL: Check failed to update status to FAILED: {db_err}")

@celery_app.task(ack_late=True)
def parse_resume_task(resume_id: str, file_path: str):
    import asyncio
    try:
        asyncio.run(parse_resume_async(resume_id, file_path))
    except Exception as e:
        logger.exception(f"WORKER FATAL LOOP ERROR for resume {resume_id}: {e}")
        raise  # Re-raise so Celery can handle retries/monitoring

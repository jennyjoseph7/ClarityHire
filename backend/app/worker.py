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


# ====== LOCAL ENRICHMENT ======
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
    
    # Build evidence map
    evidence_map = {}
    
    # From projects
    for project in raw_data.get("projects", []):
        if not isinstance(project, dict):
            continue
        project_name = project.get("title", "Project")
        techs = project.get("technologies", [])
        if isinstance(techs, list):
            for tech in techs:
                if not tech:
                    continue
                skill = normalize_skill(str(tech))
                if skill not in evidence_map:
                    evidence_map[skill] = []
                evidence_map[skill].append(f"project:{project_name}")
    
    # From experience
    for exp in raw_data.get("experience", []):
        if not isinstance(exp, dict):
            continue
        company = exp.get("company", "Company")
        role = exp.get("role", "")
        
        # Determine if internship/virtual
        is_internship = "intern" in role.lower() or "virtual" in company.lower()
        exp_type = "internship" if is_internship else "work"
        
        techs = exp.get("technologies", [])
        if isinstance(techs, list):
            for tech in techs:
                if not tech:
                    continue
                skill = normalize_skill(str(tech))
                if skill not in evidence_map:
                    evidence_map[skill] = []
                evidence_map[skill].append(f"{exp_type}:{company}")
    
    # From certifications
    for cert in raw_data.get("certifications", []):
        if not isinstance(cert, dict):
            continue
        cert_name = cert.get("name", "Certification")
        
        # Check if any skill from main list is in cert name
        for skill in raw_data.get("skills", []):
            if skill and skill.lower() in cert_name.lower():
                norm_skill = normalize_skill(str(skill))
                if norm_skill not in evidence_map:
                    evidence_map[norm_skill] = []
                evidence_map[norm_skill].append(f"certification:{cert_name[:40]}")
    
    # Collect all unique skills
    all_skills = set()
    
    # From explicit skills list
    for skill in raw_data.get("skills", []):
        if skill:
            all_skills.add(normalize_skill(str(skill)))
    
    # From evidence map
    all_skills.update(evidence_map.keys())
    
    # Calculate total experience
    total_exp_months = calculate_total_experience(raw_data.get("experience", []))
    
    # Build enriched skills with evidence
    for skill in all_skills:
        evidence = evidence_map.get(skill, ["resume:mentioned"])
        
        # Estimate months based on usage
        months = 0
        
        # If used in work experience, use that duration
        for exp in raw_data.get("experience", []):
            if isinstance(exp, dict):
                exp_techs = exp.get("technologies", [])
                if isinstance(exp_techs, list) and skill in [normalize_skill(str(t)) for t in exp_techs if t]:
                    exp_months = calculate_duration_months(exp.get("start_date", ""), exp.get("end_date", ""))
                    months = max(months, exp_months)
        
        # If used in projects but not work, estimate 3 months
        if months == 0 and any("project:" in str(e) for e in evidence):
            months = 3
        
        # Determine proficiency
        evidence_count = len(evidence)
        if months >= 12 and evidence_count >= 3:
            proficiency = "advanced"
        elif months >= 6 or evidence_count >= 2:
            proficiency = "intermediate"
        else:
            proficiency = "beginner"
        
        enriched["skills"].append({
            "skill": skill,
            "evidence": evidence,
            "months_experience": months,
            "proficiency": proficiency
        })
    
    # Sort skills by evidence count and experience
    enriched["skills"].sort(
        key=lambda s: (len(s.get("evidence", [])), s.get("months_experience", 0)), 
        reverse=True
    )
    
    # Transform projects
    for project in raw_data.get("projects", []):
        if not isinstance(project, dict):
            continue
        
        techs = project.get("technologies", [])
        normalized_techs = []
        if isinstance(techs, list):
            normalized_techs = [normalize_skill(str(t)) for t in techs if t]
        
        enriched["projects"].append({
            "title": project.get("title", ""),
            "description": project.get("description", ""),
            "technologies": normalized_techs,
            "duration": str(project.get("duration", "")),
            "key_achievements": [project.get("description", "")] if project.get("description") else [],
            "url": project.get("url", "")
        })
    
    # Transform experience
    enriched_experience = []
    for exp in raw_data.get("experience", []):
        if not isinstance(exp, dict):
            continue
        
        company = exp.get("company", "")
        role = exp.get("role", "")
        
        # Infer type
        exp_type = "full-time"
        if "intern" in role.lower():
            exp_type = "internship"
        if "virtual" in company.lower() or "virtual" in role.lower():
            exp_type = "virtual"
        
        techs = exp.get("technologies", [])
        normalized_techs = []
        if isinstance(techs, list):
            normalized_techs = [normalize_skill(str(t)) for t in techs if t]
        
        duration_months = calculate_duration_months(exp.get("start_date", ""), exp.get("end_date", ""))
        
        enriched_experience.append({
            "company": company,
            "role": role,
            "type": exp_type,
            "start_date": str(exp.get("start_date", "")),
            "end_date": str(exp.get("end_date", "Present")),
            "duration_months": duration_months,
            "description": exp.get("description", ""),
            "key_responsibilities": [exp.get("description", "")] if exp.get("description") else [],
            "technologies_used": normalized_techs
        })
    
    enriched["experience"] = enriched_experience
    
    # Transform education
    for edu in raw_data.get("education", []):
        if not isinstance(edu, dict):
            continue
        
        end_date = edu.get("end_date", "")
        year = extract_year(end_date) if end_date else 0
        
        enriched["education"].append({
            "institution": edu.get("institution", ""),
            "degree": edu.get("degree", ""),
            "field_of_study": edu.get("field", ""),
            "start_date": str(edu.get("start_date", "")),
            "end_date": str(end_date),
            "year": year,
            "gpa": "",
            "relevant_coursework": []
        })
    
    # Transform certifications
    for cert in raw_data.get("certifications", []):
        if not isinstance(cert, dict):
            continue
        
        enriched["certifications"].append({
            "name": cert.get("name", ""),
            "issuer": cert.get("issuer", ""),
            "date": str(cert.get("date", "")),
            "technologies": []
        })
    
    # Determine experience level
    virtual_count = sum(1 for exp in enriched_experience if exp["type"] in ["internship", "virtual"])
    total_count = len(enriched_experience)
    mostly_virtual = virtual_count > total_count / 2 if total_count > 0 else True
    
    if total_exp_months < 12 or (mostly_virtual and total_exp_months < 24):
        exp_level = "fresher"
    elif total_exp_months < 36:
        exp_level = "junior"
    elif total_exp_months < 60:
        exp_level = "mid"
    else:
        exp_level = "senior"
    
    # Additional info
    enriched["additional_info"] = {
        "total_experience_months": total_exp_months,
        "experience_level": exp_level,
        "strongest_skills": [s["skill"] for s in enriched["skills"][:5]],
        "volunteering": raw_data.get("volunteering", []),
        "languages": []
    }
    
    logger.info(f"Enrichment complete: {len(enriched['skills'])} skills, {len(enriched['projects'])} projects, {len(enriched['experience'])} experiences")
    
    return enriched


# ====== TWO-STAGE PARSING: Simple LLM + Local Enrichment ======
def parse_with_llm(text: str) -> dict:
    """Use LLM to extract basic structured data, then enrich locally"""
    client = Groq(api_key=settings.GROQ_API_KEY)
    
    # SIMPLE extraction prompt - just get the raw data
    prompt = f"""Extract information from this resume as JSON.

Return this structure:
{{
  "contact": {{
    "name": "full name",
    "email": "email",
    "phone": "phone",
    "linkedin": "linkedin url",
    "location": "city, state, country"
  }},
  "skills": ["Python", "React", "JavaScript"],
  "projects": [
    {{
      "title": "project name",
      "description": "description",
      "technologies": ["tech1", "tech2"],
      "duration": "Dec 2025"
    }}
  ],
  "experience": [
    {{
      "company": "company name",
      "role": "job title",
      "start_date": "Nov 2024",
      "end_date": "Jan 2025",
      "description": "what they did",
      "technologies": ["tech1", "tech2"]
    }}
  ],
  "education": [
    {{
      "institution": "university",
      "degree": "degree name",
      "field": "field of study",
      "start_date": "2020",
      "end_date": "2023"
    }}
  ],
  "certifications": [
    {{
      "name": "cert name",
      "issuer": "issuer",
      "date": "Nov 2025"
    }}
  ],
  "volunteering": ["volunteer activities"],
  "summary": "brief summary if present"
}}

Extract ALL skills and technologies mentioned anywhere in the resume.
List ALL projects with their technologies.
List ALL work experience with technologies used.

Resume:
{text[:15000]}

Return only JSON, no explanation."""
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a resume parser. Extract information and return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=4000,
            response_format={"type": "json_object"},
            timeout=60.0
        )
        
        raw_data = json.loads(completion.choices[0].message.content)
        logger.info(f"LLM extracted skills: {len(raw_data.get('skills', []))}, projects: {len(raw_data.get('projects', []))}")
        
        # NOW enrich it locally with all the evidence/proficiency logic
        enriched = enrich_resume_data(raw_data, text)
        logger.info(f"After enrichment: {len(enriched.get('skills', []))} skills with evidence")
        
        return enriched
        
    except Exception as e:
        logger.error(f"LLM parsing failed: {e}")
        raise


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
        # Create a new event loop for this task to avoid conflicts
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(parse_resume_async(resume_id, file_path))
        finally:
            # Clean up the loop
            loop.close()
    except Exception as e:
        logger.exception(f"WORKER FATAL LOOP ERROR for resume {resume_id}: {e}")
        raise  # Re-raise so Celery can handle retries/monitoring


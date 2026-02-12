"""
Test script to verify noise filtering and skill extraction improvements
"""
from app.services.inference_engine import extract_skills_from_text

# Sample JD text from Elitz Info Tech
jd_text = """
ELITZ INFO TECH – PUDUCHERRY
Complete Job Description (JD) & Professional Development Guide (PDG)

Position 1: Junior Python Developer (Entry-Level / Fresher)
Eligibility: B.E / B.Tech / BCA / MCA / B.Sc (CS/IT preferred)

Required Skills:
1. Python fundamentals and OOP concepts
2. Basic SQL and database knowledge
3. Git and version control basics
4. Learn Flask/Django frameworks

Position 2: Junior Machine Learning Engineer
Eligibility: B.E / B.Tech / M.Tech / MCA (AI/ML/DS preferred)

Required Skills:
1. Python, NumPy, Pandas
2. Scikit-learn basics
3. Statistics and linear algebra fundamentals

Location: Puducherry
Apply: HR@elitzinfotech.com
"""

# Sample resume text
resume_text = """
Alex Carter - ML Developer
Python, NumPy, Pandas, scikit-learn, PyTorch, SQL, Git, pytest, Docker, AWS, CI/CD, Jenkins, GitHub
Machine Learning, Data Science, Statistics
"""

print("=" * 70)
print("TESTING IMPROVED SKILL EXTRACTION WITH NOISE FILTERING")
print("=" * 70)

print("\n📄 JD TEXT SKILLS:")
jd_skills = extract_skills_from_text(jd_text)
print(f"All skills found: {jd_skills['all_skills']}")
print(f"Technical skills: {jd_skills['technical_skills']}")
print(f"Total: {len(jd_skills['all_skills'])}")

print("\n📄 RESUME TEXT SKILLS:")
resume_skills = extract_skills_from_text(resume_text)
print(f"All skills found: {resume_skills['all_skills']}")
print(f"Technical skills: {resume_skills['technical_skills']}")
print(f"Total: {len(resume_skills['all_skills'])}")

# Check what should be filtered
print("\n" + "=" * 70)
print("✅ NOISE FILTERING CHECK:")
print("=" * 70)

noise_that_should_be_removed = ['bca', 'mca', 'btech', 'be', 'bsc', 'cs', 'it', 'hr', 'elitz', 'ds']
found_noise = [skill for skill in jd_skills['all_skills'] if skill in noise_that_should_be_removed]

if found_noise:
    print(f"⚠️  NOISE DETECTED (should be filtered): {found_noise}")
else:
    print("✅ All noise terms properly filtered!")

# Check valid skills
valid_skills = ['python', 'sql', 'git', 'flask', 'django', 'numpy', 'pandas', 'scikit-learn', 'statistics', 'machine learning', 'ml', 'ai']
found_valid = [skill for skill in jd_skills['all_skills'] if skill in valid_skills]
print(f"\n✅ Valid technical skills found: {found_valid}")
print(f"   Count: {len(found_valid)} out of {len(valid_skills)} expected")

print("\n" + "=" * 70)

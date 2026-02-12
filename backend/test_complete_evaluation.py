"""
Complete test: Alex Carter applying for Elitz Python/ML position
"""
from app.services.inference_engine import extract_skills_from_text, InferenceEngine

engine = InferenceEngine()

# Elitz JD
jd_text = """
ELITZ INFO TECH – PUDUCHERRY
Position 1: Junior Python Developer
Required Skills:
1. Python fundamentals and OOP concepts
2. Basic SQL and database knowledge
3. Git and version control basics
4. Flask/Django frameworks

Position 2: Junior Machine Learning Engineer
Required Skills:
1. Python, NumPy, Pandas
2. Scikit-learn basics
3. Statistics and linear algebra fundamentals
"""

# Alex Carter Resume
resume_text = """
Alex Carter - ML Developer
Entry-level Python/ML developer with strong foundations in machine learning workflows
TECHNICAL SKILLS:
Languages: Python (primary), SQL (basics)
ML & Data: NumPy, Pandas, scikit-learn, PyTorch (basics), Jupyter Notebook
Testing & QA: pytest, unittest, mocking
Tools & Platforms: Git, GitHub, Docker (basics), CI/CD (GitHub Actions/Jenkins)
Cloud: AWS (basic familiarity)
EXPERIENCE: ML QA Intern, Python Test Automation Intern
Built ML classification models, automated data quality checks
Coursework: Machine Learning, Data Structures, Software Testing
Statistics, Linear Algebra
"""

print("=" * 80)
print("COMPLETE EVALUATION: Alex Carter for Elitz Python/ML Position")
print("=" * 80)

# Extract skills
jd_skills_data = extract_skills_from_text(jd_text)
resume_skills_data = extract_skills_from_text(resume_text)

jd_skills = jd_skills_data['all_skills']
resume_skills = resume_skills_data['all_skills']

print(f"\n📋 JD REQUIRED SKILLS ({len(jd_skills)}):")
print(f"   {jd_skills}")

print(f"\n👤 CANDIDATE SKILLS ({len(resume_skills)}):")
print(f"   {resume_skills}")

# Compute match with inference
result = engine.compute_skill_match(jd_skills, resume_skills)

print("\n" + "=" * 80)
print("📊 MATCHING RESULTS:")
print("=" * 80)
print(f"✅ Match Score: {result['match_score']:.4f} ({result['match_score']*100:.1f}%)")
print(f"✅ Match Percentage: {result['match_percentage']:.1f}%")
print(f"✅ Total Matched: {result['matched_count']} out of {result['total_jd_skills']} required")

print(f"\n✓ Matched Skills ({len(result['matched_skills'])}):")
print(f"  {result['matched_skills']}")

if 'matched_inferred' in result and result['matched_inferred']:
    print(f"\n🧠 Inferred Skills ({len(result['matched_inferred'])}):")
    print(f"  {result['matched_inferred']}")

if result['missing_skills']:
    print(f"\n✗ Missing Skills ({len(result['missing_skills'])}):")
    print(f"  {result['missing_skills']}")

print("\n" + "=" * 80)
print("💡 DECISION PREDICTION:")
print("=" * 80)

if result['match_percentage'] >= 80:
    decision = "Fast-Track ⭐⭐⭐"
elif result['match_percentage'] >= 60:
    decision = "Selected ✅"
elif result['match_percentage'] >= 40:
    decision = "Hire-Pooled 📋"
else:
    decision = "Rejected ❌"

print(f"Expected Decision: {decision}")
print(f"Reason: {result['match_percentage']:.1f}% skill match with inference")

print("\n" + "=" * 80)

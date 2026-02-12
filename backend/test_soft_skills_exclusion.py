"""
Test to verify soft skills are NOT counted in DCS (Domain Competency Score)
"""
from app.services.inference_engine import extract_skills_from_text, InferenceEngine
from app.services.scoring_engine import compute_dcs

engine = InferenceEngine()

# JD with both technical and soft skills
jd_text = """
Junior Python Developer Position
Required Technical Skills:
- Python, Flask, Django, SQL, Git
Required Soft Skills:
- Leadership, Teamwork, Communication, Mentoring
"""

# Resume with only technical skills
resume_text = """
Alex Carter - Python Developer
Technical Skills: Python, Flask, SQL, Git, NumPy, Pandas, Machine Learning
Soft Skills: Problem solving, Analytical thinking
"""

print("=" * 80)
print("TEST: Soft Skills Should NOT Count as Missing in DCS")
print("=" * 80)

# Extract all skills
jd_skills_all = extract_skills_from_text(jd_text)
resume_skills_all = extract_skills_from_text(resume_text)

print(f"\n📋 JD Skills:")
print(f"   Technical: {jd_skills_all['technical_skills']}")
print(f"   Soft: {jd_skills_all['soft_skills']}")
print(f"   All: {jd_skills_all['all_skills']}")

print(f"\n👤 Resume Skills:")
print(f"   Technical: {resume_skills_all['technical_skills']}")
print(f"   Soft: {resume_skills_all['soft_skills']}")
print(f"   All: {resume_skills_all['all_skills']}")

# Compute DCS (should use only technical skills now)
dcs_score, skill_match = compute_dcs(jd_text, resume_text)

print("\n" + "=" * 80)
print("📊 DCS RESULTS (Technical Skills Only):")
print("=" * 80)
print(f"✅ DCS Score: {dcs_score:.4f} ({dcs_score*100:.1f}%)")
print(f"✅ Match Percentage: {skill_match['match_percentage']:.1f}%")
print(f"✅ Total JD Skills (Technical): {skill_match['total_jd_skills']}")
print(f"✅ Matched: {skill_match['matched_count']}")

print(f"\n✓ Matched Technical Skills:")
print(f"  {skill_match['matched_skills']}")

print(f"\n✗ Missing Technical Skills:")
print(f"  {skill_match['missing_skills']}")

# Check that soft skills are NOT in missing skills
soft_skills_in_missing = [s for s in skill_match['missing_skills'] 
                          if s in ['leadership', 'teamwork', 'communication', 'mentoring']]

print("\n" + "=" * 80)
print("✅ VERIFICATION:")
print("=" * 80)

if soft_skills_in_missing:
    print(f"❌ FAILED: Soft skills found in missing: {soft_skills_in_missing}")
else:
    print(f"✅ SUCCESS: No soft skills in missing technical skills!")
    print(f"✅ Only technical skills evaluated for DCS")

print("\n" + "=" * 80)

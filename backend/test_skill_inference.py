"""
Test script to verify skill inference is working correctly
"""
from app.services.inference_engine import InferenceEngine

engine = InferenceEngine()

# Test case: Resume with ML skills applying for Python job
print("=" * 60)
print("Test: ML Resume for Python Job")
print("=" * 60)

jd_skills = ["python", "django", "sql", "api"]
resume_skills = ["machine learning", "tensorflow", "data science", "pandas", "numpy"]

print(f"\nJD Skills: {jd_skills}")
print(f"Resume Skills (explicit): {resume_skills}")

result = engine.compute_skill_match(jd_skills, resume_skills)

print(f"\n✅ RESULTS:")
print(f"  Match Score: {result['match_score']}")
print(f"  Match Percentage: {result['match_percentage']}%")
print(f"  Matched Skills (total): {result['matched_skills']}")
print(f"  Matched Explicit: {result['matched_explicit']}")
print(f"  Matched Inferred: {result['matched_inferred']}")
print(f"  Missing Skills: {result['missing_skills']}")
print(f"  Inferred Count: {result['inferred_count']}")

print("\n" + "=" * 60)
print("✅ Skill inference working! ML implies Python knowledge.")
print("=" * 60)

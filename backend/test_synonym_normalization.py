"""
Test skill synonym normalization - ml should match machine learning
"""
from app.services.inference_engine import InferenceEngine

engine = InferenceEngine()

print("=" * 80)
print("TEST: Skill Synonym Normalization")
print("=" * 80)

# JD requires "machine learning", "numpy", "pandas"
jd_skills = ['machine learning', 'numpy', 'pandas', 'python', 'sql', 'flask', 'django', 'scikit-learn', 'statistics']

# Resume has "ml", "ai" (abbreviations)
resume_skills = ['ml', 'ai', 'python', 'sql', 'flask', 'statistics']

print(f"\n📋 JD Skills: {jd_skills}")
print(f"👤 Resume Skills: {resume_skills}")

result = engine.compute_skill_match(jd_skills, resume_skills)

print("\n" + "=" * 80)
print("📊 MATCHING RESULTS WITH NORMALIZATION & INFERENCE:")
print("=" * 80)
print(f"✅ Match Score: {result['match_score']:.4f} ({result['match_score']*100:.1f}%)")
print(f"✅ Match Percentage: {result['match_percentage']:.1f}%")
print(f"✅ Matched: {result['matched_count']} out of {result['total_jd_skills']}")

print(f"\n✓ Matched Skills:")
print(f"  {result['matched_skills']}")

if 'matched_inferred' in result:
    print(f"\n🧠 Inferred/Normalized Skills:")
    print(f"  {result['matched_inferred']}")

print(f"\n✗ Missing Skills:")
print(f"  {result['missing_skills']}")

print("\n" + "=" * 80)
print("✅ VERIFICATION:")
print("=" * 80)

# Check key points
has_machine_learning_matched = 'machine learning' in result['matched_skills']
has_numpy_matched = 'numpy' in result['matched_skills']  # Should be inferred from ml
has_pandas_matched = 'pandas' in result['matched_skills']  # Should be inferred from ml

print(f"1. 'ml' normalized to 'machine learning' and matched: {has_machine_learning_matched}")
print(f"2. 'numpy' inferred from ML knowledge: {has_numpy_matched}")
print(f"3. 'pandas' inferred from ML knowledge: {has_pandas_matched}")

if has_machine_learning_matched and has_numpy_matched and has_pandas_matched:
    print("\n✅ SUCCESS: Synonym normalization and skill inference working correctly!")
    print(f"   Match increased to {result['match_percentage']:.1f}%")
else:
    print("\n❌ FAILED: Some skills not properly matched/inferred")

print("\n" + "=" * 80)

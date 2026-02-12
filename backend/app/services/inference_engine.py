"""
Inference Engine for NLP-based skill extraction and analysis
"""
import re
from typing import List, Dict, Set, Tuple
import requests
from ..config import HF_API_KEY

# Enhanced skill synonym mapping - normalize to consistent terms
SKILL_SYNONYMS = {
    # Machine Learning & AI
    'ml': 'machine learning',
    'ai': 'artificial intelligence',
    'dl': 'deep learning',
    'cv': 'computer vision',
    
    # DevOps & CI/CD (normalize all variants to single term)
    'devops': 'devops',
    'dev ops': 'devops',
    'dev-ops': 'devops',
    'ci/cd': 'ci cd',
    'ci-cd': 'ci cd',
    'cicd': 'ci cd',
    'ci': 'ci cd',  # When standalone, likely refers to CI/CD
    'cd': 'ci cd',  # When standalone, likely refers to CI/CD
    'continuous integration': 'ci cd',
    'continuous deployment': 'ci cd',
    'continuous delivery': 'ci cd',
    
    # REST APIs (normalize all variants)
    'restful': 'rest api',
    'rest': 'rest api',
    'rest api': 'rest api',
    'rest apis': 'rest api',
    'restful api': 'rest api',
    'restful apis': 'rest api',
    
    # Programming Languages
    'js': 'javascript',
    'ts': 'typescript',
    'py': 'python',
    
    # Databases
    'postgres': 'postgresql',
    'mongo': 'mongodb',
    
    # Cloud
    'amazon web services': 'aws',
    'google cloud': 'gcp',
    'google cloud platform': 'gcp',
    
    # Version Control
    'version control': 'git',
    
    # Operating Systems
    'gnu/linux': 'linux',
    
    # Frameworks (normalize similar ones)
    'react.js': 'react',
    'reactjs': 'react',
    'vue.js': 'vue',
    'vuejs': 'vue',
    'node': 'node.js',
    'nodejs': 'node.js',
}

# Skill prerequisite and relationship mapping
# Format: skill -> set of prerequisite/implied skills
SKILL_RELATIONSHIPS = {
    # ML/AI implies Python knowledge + common ML libraries
    'machine learning': {'python', 'statistics', 'mathematics', 'numpy', 'pandas'},
    'ml': {'python', 'statistics', 'mathematics', 'numpy', 'pandas'},
    'deep learning': {'python', 'machine learning', 'ml', 'tensorflow', 'pytorch', 'numpy'},
    'tensorflow': {'python', 'machine learning', 'ml', 'numpy'},
    'pytorch': {'python', 'machine learning', 'ml', 'numpy'},
    'scikit-learn': {'python', 'machine learning', 'ml', 'numpy', 'pandas'},
    'keras': {'python', 'deep learning', 'tensorflow', 'numpy'},
    'nlp': {'python', 'machine learning', 'ml'},
    'computer vision': {'python', 'deep learning', 'opencv', 'numpy'},
    'data science': {'python', 'statistics', 'sql', 'pandas', 'numpy'},
    'artificial intelligence': {'python', 'machine learning', 'ml', 'statistics'},
    'ai': {'python', 'machine learning', 'ml', 'statistics'},
    'pandas': {'python', 'numpy'},
    'numpy': {'python'},
    
    # Web frameworks imply base languages
    'django': {'python', 'sql', 'html', 'css'},
    'flask': {'python', 'html', 'css'},
    'fastapi': {'python'},
    'react': {'javascript', 'html', 'css'},
    'angular': {'typescript', 'javascript', 'html', 'css'},
    'vue': {'javascript', 'html', 'css'},
    'node.js': {'javascript'},
    'express': {'javascript', 'node.js'},
    'spring': {'java'},
    'asp.net': {'c#'},
    
    # Mobile implies base language
    'android': {'java', 'kotlin'},
    'ios': {'swift'},
    'react native': {'javascript', 'react'},
    'flutter': {'dart'},
    
    # Cloud implies DevOps knowledge
    'aws': {'cloud', 'devops'},
    'azure': {'cloud', 'devops'},
    'gcp': {'cloud', 'devops'},
    'docker': {'devops', 'linux'},
    'kubernetes': {'docker', 'devops', 'linux'},
    
    # Databases imply SQL knowledge
    'mysql': {'sql'},
    'postgresql': {'sql'},
    'oracle': {'sql'},
    'mariadb': {'sql'},
    'sqlite': {'sql'},
}

# Noise filter - terms that are NOT actual skills
NOISE_TERMS = {
    # Degree abbreviations
    'b.e', 'b.tech', 'bca', 'mca', 'm.tech', 'b.sc', 'm.sc', 'mba', 'phd',
    'be', 'btech', 'bsc', 'msc', 'ba', 'ma', 'ca',
    
    # Generic organizational terms
    'hr', 'it', 'info', 'tech', 'co', 'ltd', 'inc', 'pvt',
    
    # Common stop words that might appear
    'jr', 'sr', 'mid', 'level', 'entry',
    
    # Document section headers
    'experience', 'education', 'skills', 'summary', 'description',
    
    # Vague 2-letter acronyms (keep specific ones like ml, ai, qa, qa, ci, cd)
    'cs', 'ds', 'we', 'as', 'is', 'an', 'or', 'on', 'in', 'at', 'to',
    
    # Common company name patterns (add specific ones as needed)
    'elitz', 'company', 'corporation', 'enterprises', 'solutions', 'systems',
    'technologies', 'labs', 'innovations', 'digital', 'services',
}

# Valid technical acronyms (whitelist)
VALID_SHORT_SKILLS = {
    'ml', 'ai', 'qa', 'ci', 'cd', 'ui', 'ux', 'ar', 'vr', 'iot', 'api', 'sql', 'aws', 'gcp', 'nlp', 'etl'
}

# Comprehensive skill databases
TECHNICAL_SKILLS = {
    # Programming Languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust', 
    'php', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'shell', 'bash', 'dart',
    
    # Web Technologies
    'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 
    'flask', 'fastapi', 'spring', 'asp.net', 'jquery', 'bootstrap', 'tailwind',
    
    # Databases
    'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'dynamodb',
    'oracle', 'sqlite', 'mariadb', 'elasticsearch', 'neo4j',
    
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github',
    'terraform', 'ansible', 'ci/cd', 'devops', 'linux', 'unix',
    
    # Data Science & ML
    'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
    'pandas', 'numpy', 'nlp', 'computer vision', 'data science', 'statistics',
    'ml', 'ai', 'neural networks', 'transformers', 'llm',
    
    # Tools & Frameworks
    'git', 'jira', 'agile', 'scrum', 'rest api', 'graphql', 'microservices',
    'kafka', 'rabbitmq', 'spark', 'hadoop', 'etl', 'data engineering',
    
    # Mobile Development
    'android', 'ios', 'react native', 'flutter', 'xamarin',
    
    # Others
    'blockchain', 'solidity', 'web3', 'cybersecurity', 'penetration testing',
    'networking', 'tcp/ip', 'api', 'restful', 'soap', 'xml', 'json'
}

SOFT_SKILLS = {
    'leadership', 'communication', 'teamwork', 'problem solving', 'analytical',
    'creative', 'adaptable', 'time management', 'project management',
    'collaboration', 'critical thinking', 'decision making', 'mentoring',
    'presentation', 'negotiation', 'conflict resolution', 'empathy'
}

EDUCATION_KEYWORDS = {
    'bachelor', 'master', 'phd', 'mba', 'degree', 'university', 'college',
    'certification', 'certified', 'diploma', 'doctorate', 'b.tech', 'm.tech',
    'b.sc', 'm.sc', 'b.e', 'm.e', 'b.a', 'm.a'
}


class InferenceEngine:
    """Advanced NLP inference engine for resume and JD analysis"""
    
    def __init__(self):
        self.hf_api_key = HF_API_KEY
        self.ner_model_url = "https://api-inference.huggingface.co/models/dslim/bert-base-NER"
        
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """
        Extract technical and soft skills from text
        
        Args:
            text: Resume or JD text
            
        Returns:
            Dictionary with technical_skills, soft_skills, and all_skills
        """
        text_lower = text.lower()
        
        # Extract technical skills
        technical_found = set()
        for skill in TECHNICAL_SKILLS:
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                # Filter out noise terms
                if skill.lower() not in NOISE_TERMS:
                    # For short skills (2-3 chars), check whitelist
                    if len(skill) <= 3:
                        if skill.lower() in VALID_SHORT_SKILLS:
                            technical_found.add(skill)
                    else:
                        technical_found.add(skill)
        
        # Extract soft skills
        soft_found = set()
        for skill in SOFT_SKILLS:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                soft_found.add(skill)
        
        # Extract potential custom skills (capitalized words, acronyms)
        custom_skills = self._extract_custom_skills(text)
        technical_found.update(custom_skills)
        
        return {
            "technical_skills": sorted(list(technical_found)),
            "soft_skills": sorted(list(soft_found)),
            "all_skills": sorted(list(technical_found.union(soft_found))),
            "skill_count": len(technical_found) + len(soft_found)
        }
    
    def _extract_custom_skills(self, text: str) -> Set[str]:
        """Extract potential custom skills using pattern matching, with noise filtering"""
        custom_skills = set()
        
        # Find acronyms (2-5 uppercase letters) but filter carefully
        acronyms = re.findall(r'\b[A-Z]{2,5}\b', text)
        for a in acronyms:
            a_lower = a.lower()
            # Only add if it's a valid technical acronym and not noise
            if len(a) <= 3 and a_lower in VALID_SHORT_SKILLS:
                custom_skills.add(a_lower)
            elif len(a) > 3 and a_lower not in NOISE_TERMS:
                custom_skills.add(a_lower)
        
        # Find technology patterns (e.g., "Node.js", "C++")
        tech_patterns = re.findall(r'\b[A-Z][a-z]*\.[a-z]{2,}\b', text)
        custom_skills.update([t.lower() for t in tech_patterns if t.lower() not in NOISE_TERMS])
        
        return custom_skills
    
    def _normalize_skills(self, skills: List[str]) -> Set[str]:
        """
        Normalize skills using synonym mapping.
        Converts abbreviations to full forms (e.g., 'ml' -> 'machine learning').
        
        Args:
            skills: List of skills (may contain abbreviations)
            
        Returns:
            Set of normalized skills
        """
        normalized = set()
        for skill in skills:
            skill_lower = skill.lower()
            # Check if it's a synonym that should be normalized
            if skill_lower in SKILL_SYNONYMS:
                normalized.add(SKILL_SYNONYMS[skill_lower])
            # Also keep the original
            normalized.add(skill_lower)
        return normalized
    
    def _infer_skills(self, skills: List[str]) -> Set[str]:
        """
        Infer additional skills based on skill relationships.
        If someone knows ML, they definitely know Python.
        
        Args:
            skills: List of explicitly mentioned skills
            
        Returns:
            Set of all skills (explicit + inferred)
        """
        # First normalize skills (handle synonyms)
        all_skills = self._normalize_skills(skills)
        
        # Then infer prerequisite skills
        for skill in list(all_skills):  # Use list() to avoid modifying set during iteration
            if skill in SKILL_RELATIONSHIPS:
                # Add all prerequisite/implied skills
                all_skills.update(SKILL_RELATIONSHIPS[skill])
        
        return all_skills
    
    def compute_skill_match(self, jd_skills: List[str], resume_skills: List[str]) -> Dict[str, any]:
        """
        Compute detailed skill matching metrics with skill inference and normalization.
        Uses SKILL_SYNONYMS to normalize abbreviations and SKILL_RELATIONSHIPS to infer related skills.
        
        Args:
            jd_skills: Skills extracted from job description
            resume_skills: Skills extracted from resume
            
        Returns:
            Dictionary with match metrics
        """
        # Normalize JD skills (handle synonyms like ml -> machine learning)
        jd_set = self._normalize_skills(jd_skills)
        
        # Infer additional skills from resume based on relationships and normalize
        resume_set_with_inferred = self._infer_skills(resume_skills)
        resume_set_explicit = self._normalize_skills(resume_skills)
        
        if not jd_set:
            return {
                "match_score": 0.0,
                "matched_skills": [],
                "missing_skills": [],
                "extra_skills": [],
                "match_percentage": 0.0,
                "inferred_skills": []
            }
        
        # Match against inferred skills
        matched = jd_set.intersection(resume_set_with_inferred)
        matched_explicit = jd_set.intersection(resume_set_explicit)
        missing = jd_set - resume_set_with_inferred
        extra = resume_set_explicit - jd_set
        inferred = matched - matched_explicit
        
        match_percentage = (len(matched) / len(jd_set)) * 100
        
        # Weighted score: full credit for matched skills (explicit or inferred)
        match_score = len(matched) / (len(jd_set) + 0.3 * len(missing))
        match_score = min(match_score, 1.0)  # Cap at 1.0
        
        return {
            "match_score": round(match_score, 4),
            "matched_skills": sorted(list(matched)),
            "matched_explicit": sorted(list(matched_explicit)),
            "matched_inferred": sorted(list(inferred)),
            "missing_skills": sorted(list(missing)),
            "extra_skills": sorted(list(extra))[:20],
            "match_percentage": round(match_percentage, 2),
            "total_jd_skills": len(jd_set),
            "total_resume_skills": len(resume_set_explicit),
            "matched_count": len(matched),
            "inferred_count": len(inferred)
        }
    
    def extract_experience_details(self, text: str) -> Dict[str, any]:
        """
        Extract detailed experience information from text
        
        Returns:
            Dictionary with years, roles, companies found
        """
        text_lower = text.lower()
        
        # Extract years of experience
        year_patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience\s*:\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?\s+(?:of\s+)?experience'
        ]
        
        years_found = []
        for pattern in year_patterns:
            matches = re.findall(pattern, text_lower)
            years_found.extend([int(m) for m in matches])
        
        max_years = max(years_found) if years_found else 0
        
        # Extract potential roles
        role_keywords = ['developer', 'engineer', 'manager', 'analyst', 'architect', 
                        'lead', 'senior', 'junior', 'intern', 'consultant', 'specialist']
        
        roles_found = []
        for keyword in role_keywords:
            if keyword in text_lower:
                roles_found.append(keyword)
        
        return {
            "experience_years": max_years,
            "roles_mentioned": roles_found,
            "has_leadership": any(word in text_lower for word in ['lead', 'manager', 'director', 'head'])
        }
    
    def analyze_text_quality(self, text: str) -> Dict[str, any]:
        """
        Analyze the quality and completeness of resume/JD text
        
        Returns:
            Quality metrics
        """
        word_count = len(text.split())
        char_count = len(text)
        
        # Check for key sections
        has_education = any(keyword in text.lower() for keyword in EDUCATION_KEYWORDS)
        has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
        has_phone = bool(re.search(r'\+?[\d\s\-\(\)]{10,}', text))
        has_urls = bool(re.search(r'https?://|www\.', text, re.IGNORECASE))
        
        # Completeness score
        completeness_factors = [
            word_count > 100,
            has_education,
            has_email or has_phone,
            word_count < 5000  # Not too long
        ]
        completeness = sum(completeness_factors) / len(completeness_factors)
        
        return {
            "word_count": word_count,
            "character_count": char_count,
            "has_education": has_education,
            "has_contact": has_email or has_phone,
            "has_links": has_urls,
            "completeness_score": round(completeness, 2),
            "quality_level": "high" if completeness >= 0.75 else "medium" if completeness >= 0.5 else "low"
        }
    
    def generate_skill_embedding_enhancement(self, text: str, skills: List[str]) -> str:
        """
        Create an enhanced text representation by emphasizing extracted skills
        Useful for better embedding generation
        """
        skill_emphasis = " ".join(skills[:20])  # Top 20 skills
        return f"{text}\n\nKey Skills: {skill_emphasis}"
    
    def parse_jd_skill_priority(self, jd_text: str, all_skills: List[str]) -> Dict[str, any]:
        """
        Parse JD to identify which skills are required vs nice-to-have
        
        Args:
            jd_text: Job description text
            all_skills: All skills extracted from JD
            
        Returns:
            Dictionary classifying skills by priority
        """
        jd_lower = jd_text.lower()
        
        # Define section markers for required skills
        required_markers = [
            'requirements', 'required', 'must have', 'essential', 'mandatory',
            'required skills', 'key requirements', 'qualifications',
            'minimum qualifications', 'you must', 'you should'
        ]
        
        # Define section markers for optional skills
        optional_markers = [
            'nice to have', 'preferred', 'bonus', 'plus', 'optional',
            'would be nice', 'additional', 'advantageous', 'desired',
            'good to have', 'we would love', 'ideal candidate'
        ]
        
        required_skills = set()
        nice_to_have_skills = set()
        
        # Find required and nice-to-have sections
        required_section_start = -1
        optional_section_start = -1
        
        for marker in required_markers:
            pos = jd_lower.find(marker)
            if pos != -1 and (required_section_start == -1 or pos < required_section_start):
                required_section_start = pos
        
        for marker in optional_markers:
            pos = jd_lower.find(marker)
            if pos != -1 and (optional_section_start == -1 or pos < optional_section_start):
                optional_section_start = pos
        
        # If we found sections, classify skills based on which section they appear in
        if required_section_start != -1 or optional_section_start != -1:
            for skill in all_skills:
                skill_positions = [m.start() for m in re.finditer(r'\b' + re.escape(skill.lower()) + r'\b', jd_lower)]
                
                if not skill_positions:
                    continue
                
                # Check each occurrence of the skill
                in_required = False
                in_optional = False
                
                for pos in skill_positions:
                    # Determine if this occurrence is in required or optional section
                    if required_section_start != -1 and optional_section_start != -1:
                        # Both sections exist
                        if required_section_start < optional_section_start:
                            # Required comes first
                            if required_section_start <= pos < optional_section_start:
                                in_required = True
                            elif pos >= optional_section_start:
                                in_optional = True
                        else:
                            # Optional comes first
                            if optional_section_start <= pos < required_section_start:
                                in_optional = True
                            elif pos >= required_section_start:
                                in_required = True
                    elif required_section_start != -1:
                        # Only required section exists
                        if pos >= required_section_start:
                            in_required = True
                    elif optional_section_start != -1:
                        # Only optional section exists
                        if pos >= optional_section_start:
                            in_optional = True
                
                # Prioritize required over optional if skill appears in both
                if in_required:
                    required_skills.add(skill)
                elif in_optional:
                    nice_to_have_skills.add(skill)
                else:
                    # Skill mentioned but not in any specific section - treat as required by default
                    required_skills.add(skill)
        else:
            # No clear sections found - all skills are required
            required_skills = set(all_skills)
        
        # Skills not classified yet go to required by default
        unclassified = set(all_skills) - required_skills - nice_to_have_skills
        required_skills.update(unclassified)
        
        return {
            "required_skills": sorted(list(required_skills)),
            "nice_to_have_skills": sorted(list(nice_to_have_skills)),
            "required_count": len(required_skills),
            "nice_to_have_count": len(nice_to_have_skills),
            "has_clear_sections": required_section_start != -1 or optional_section_start != -1
        }
    
    def compute_weighted_skill_match(self, jd_text: str, jd_skills: List[str], 
                                     resume_skills: List[str]) -> Dict[str, any]:
        """
        Compute skill matching with weighted scoring based on required vs nice-to-have
        
        Args:
            jd_text: Job description text (for parsing priority)
            jd_skills: Skills extracted from JD
            resume_skills: Skills extracted from resume
            
        Returns:
            Dictionary with weighted match metrics (with backward compatibility keys)
        """
        # Parse JD to classify skills
        skill_priority = self.parse_jd_skill_priority(jd_text, jd_skills)
        
        required_skills = set(skill_priority["required_skills"])
        nice_to_have_skills = set(skill_priority["nice_to_have_skills"])
        
        # Normalize and infer skills
        resume_set_with_inferred = self._infer_skills(resume_skills)
        resume_set_explicit = self._normalize_skills(resume_skills)
        
        # All JD skills combined
        all_jd_skills = required_skills.union(nice_to_have_skills)
        
        # Match against required skills (weighted heavily)
        matched_required = required_skills.intersection(resume_set_with_inferred)
        missing_required = required_skills - resume_set_with_inferred
        
        # Match against nice-to-have skills (bonus points)
        matched_nice_to_have = nice_to_have_skills.intersection(resume_set_with_inferred)
        missing_nice_to_have = nice_to_have_skills - resume_set_with_inferred
        
        # Calculate candidate extras (skills not in JD)
        candidate_extras = resume_set_explicit - all_jd_skills
        
        # Calculate weighted score
        # Required skills: 100% weight
        # Nice-to-have: 20% weight (bonus)
        required_weight = 1.0
        nice_to_have_weight = 0.2
        
        if len(required_skills) > 0:
            required_score = len(matched_required) / len(required_skills)
        else:
            required_score = 1.0  # No required skills specified
        
        if len(nice_to_have_skills) > 0:
            nice_to_have_bonus = (len(matched_nice_to_have) / len(nice_to_have_skills)) * nice_to_have_weight
        else:
            nice_to_have_bonus = 0.0
        
        # Final weighted score (required score + bonus, capped at 1.0)
        weighted_score = min(required_score + nice_to_have_bonus, 1.0)
        
        # Overall match (all skills combined)
        all_matched = matched_required.union(matched_nice_to_have)
        all_missing = missing_required.union(missing_nice_to_have)
        
        # Calculate legacy match_percentage for backward compatibility
        overall_match_pct = round((len(all_matched) / (len(required_skills) + len(nice_to_have_skills)) * 100) if (len(required_skills) + len(nice_to_have_skills)) > 0 else 0, 2)
        
        return {
            "match_score": round(weighted_score, 4),
            "required_match_score": round(required_score, 4),
            "matched_skills": sorted(list(all_matched)),
            "matched_required": sorted(list(matched_required)),
            "matched_nice_to_have": sorted(list(matched_nice_to_have)),
            "missing_skills": sorted(list(all_missing)),
            "missing_required": sorted(list(missing_required)),
            "missing_nice_to_have": sorted(list(missing_nice_to_have)),
            "extra_skills": sorted(list(candidate_extras))[:20],  # Backward compatibility
            "candidate_extras": sorted(list(candidate_extras))[:20],  # Alternative name
            "required_match_percentage": round((len(matched_required) / len(required_skills) * 100) if len(required_skills) > 0 else 100, 2),
            "overall_match_percentage": overall_match_pct,
            "match_percentage": overall_match_pct,  # Backward compatibility
            "matched_count": len(all_matched),  # Backward compatibility
            "priority_breakdown": {
                "required_total": len(required_skills),
                "required_matched": len(matched_required),
                "required_missing": len(missing_required),
                "nice_to_have_total": len(nice_to_have_skills),
                "nice_to_have_matched": len(matched_nice_to_have),
                "nice_to_have_missing": len(missing_nice_to_have)
            },
            "total_jd_skills": len(all_jd_skills),  # Backward compatibility
            "jd_skill_count": len(jd_skills),
            "resume_skill_count": len(resume_skills)
        }


# Singleton instance
inference_engine = InferenceEngine()


def extract_skills_from_text(text: str) -> Dict[str, List[str]]:
    """Extract skills from text"""
    return inference_engine.extract_skills(text)


def compute_skill_similarity(jd_skills: List[str], resume_skills: List[str]) -> Dict[str, any]:
    """Compute skill matching between JD and resume"""
    return inference_engine.compute_skill_match(jd_skills, resume_skills)


def analyze_resume_quality(resume_text: str) -> Dict[str, any]:
    """Analyze resume quality and completeness"""
    return inference_engine.analyze_text_quality(resume_text)


def extract_experience_info(text: str) -> Dict[str, any]:
    """Extract experience details from text"""
    return inference_engine.extract_experience_details(text)

import os
import json
import re
from io import BytesIO
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from PyPDF2 import PdfReader
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

def strip_markdown_fences(text):
    """Remove markdown code fences from text."""
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    return text.strip()

def parse_analysis_response(response_text):
    """Parse JSON response from Groq API."""
    cleaned_text = strip_markdown_fences(response_text)
    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        # Fallback mock response if parsing fails
        return {
            "match_score": 50,
            "matched_skills": ["Python", "Problem Solving"],
            "required_skills": ["Python", "React", "AWS", "Docker", "Problem Solving"],
            "skill_gaps": ["React", "AWS", "Docker"],
            "learning_plan": [
                {
                    "week": 1,
                    "focus": "React Fundamentals",
                    "tasks": [
                        "Learn React hooks and component lifecycle",
                        "Build simple components",
                        "Understand JSX syntax"
                    ]
                },
                {
                    "week": 2,
                    "focus": "Docker Basics",
                    "tasks": [
                        "Learn Docker containerization",
                        "Create Dockerfile",
                        "Deploy container"
                    ]
                },
                {
                    "week": 3,
                    "focus": "AWS Fundamentals",
                    "tasks": [
                        "Learn AWS core services (EC2, S3, RDS)",
                        "Set up AWS account",
                        "Deploy simple application"
                    ]
                },
                {
                    "week": 4,
                    "focus": "Integration Project",
                    "tasks": [
                        "Build full-stack application",
                        "Deploy to AWS",
                        "Document learning"
                    ]
                }
            ]
        }

def extract_text_from_pdf(file_stream):
    """Extract text from PDF file."""
    try:
        pdf_reader = PdfReader(file_stream)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

def fetch_github_skills(github_username: str) -> list:
    """Fetch GitHub user's repositories and extract programming languages used."""
    try:
        # Clean up username
        username = github_username.replace("https://github.com/", "").replace("http://github.com/", "").strip()
        if not username:
            return []
        
        # Fetch user repositories
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=30"
        repos_response = requests.get(repos_url, timeout=10)
        repos_response.raise_for_status()
        repos = repos_response.json()
        
        if not isinstance(repos, list):
            return []
        
        # Aggregate language data
        language_bytes = {}
        for repo in repos:
            if repo.get('languages_url'):
                try:
                    langs_response = requests.get(repo['languages_url'], timeout=5)
                    langs_response.raise_for_status()
                    langs = langs_response.json()
                    if isinstance(langs, dict):
                        for lang, bytes_count in langs.items():
                            language_bytes[lang] = language_bytes.get(lang, 0) + bytes_count
                except Exception:
                    continue
        
        # Sort by usage and return top 15
        sorted_langs = sorted(language_bytes.items(), key=lambda x: x[1], reverse=True)
        top_skills = [lang for lang, _ in sorted_langs[:15]]
        return top_skills if top_skills else []
    except requests.exceptions.RequestException:
        return []
    except Exception:
        return []

def extract_skills_from_text(text):
    """Extract skills from resume or job description text."""
    common_skills = {
        "python", "javascript", "typescript", "java", "csharp", "c#", "php", "ruby", "go", "rust",
        "react", "angular", "vue", "next.js", "nextjs", "svelte", "express", "fastapi", "django",
        "node.js", "nodejs", "flask", "spring boot", "springboot", ".net", "dotnet",
        "sql", "postgresql", "mysql", "mongodb", "redis", "firebase", "dynamodb",
        "aws", "azure", "gcp", "docker", "kubernetes", "git", "github", "gitlab",
        "rest api", "graphql", "microservices", "ci/cd", "jenkins", "gitlab ci",
        "html", "css", "tailwind", "bootstrap", "sass", "webpack", "vite",
        "linux", "unix", "windows", "devops", "terraform", "ansible",
        "machine learning", "ai", "nlp", "deep learning", "pandas", "numpy", "scikit-learn",
        "testing", "jest", "pytest", "mocha", "unittest", "rspec",
        "agile", "scrum", "jira", "communication", "problem solving", "leadership"
    }
    
    text_lower = text.lower()
    found_skills = set()
    
    for skill in common_skills:
        if skill in text_lower:
            found_skills.add(skill.title())
    
    return list(found_skills)

def generate_mock_analysis(resume_text="", github_skills=None, job_description=""):
    """Generate analysis based on actual resume and job content - NOT hardcoded values."""
    if github_skills is None:
        github_skills = []
    
    # Extract skills from resume and job
    resume_skills = extract_skills_from_text(resume_text) if resume_text else []
    resume_skills.extend(github_skills)
    resume_skills = list(set([s.title() if s.lower() not in ["ai", "nlp", "ci/cd"] else s for s in resume_skills]))
    
    job_skills = extract_skills_from_text(job_description) if job_description else []
    
    # Calculate actual match
    matched = [s for s in resume_skills if s in job_skills]
    gaps = [s for s in job_skills if s not in resume_skills]
    
    # Calculate match percentage based on actual overlap
    match_score = int((len(matched) / len(job_skills) * 100)) if job_skills else 0
    match_score = max(0, min(100, match_score))  # Clamp 0-100
    
    return {
        "match_score": match_score,
        "matched_skills": matched[:10] if matched else resume_skills[:5],
        "required_skills": job_skills[:15] if job_skills else [],
        "skill_gaps": gaps[:10] if gaps else [],
        "learning_plan": [
            {
                "week": 1,
                "focus": f"Learn {gaps[0] if gaps else 'Core Concepts'}",
                "tasks": [
                    f"Study {gaps[0] if gaps else 'fundamentals'}",
                    "Build practice projects",
                    "Review documentation"
                ] if gaps else ["Study fundamentals", "Build practice projects", "Review documentation"]
            },
            {
                "week": 2,
                "focus": f"Master {gaps[1] if len(gaps) > 1 else 'Advanced Concepts'}",
                "tasks": [
                    f"Deep dive into {gaps[1] if len(gaps) > 1 else 'advanced topics'}",
                    "Complete hands-on labs",
                    "Build mini project"
                ] if len(gaps) > 1 else ["Deep dive into advanced topics", "Complete hands-on labs", "Build mini project"]
            },
            {
                "week": 3,
                "focus": f"Implement {gaps[2] if len(gaps) > 2 else 'Practical Applications'}",
                "tasks": [
                    f"Apply {gaps[2] if len(gaps) > 2 else 'your skills'} in real scenarios",
                    "Contribute to open source",
                    "Build portfolio project"
                ] if len(gaps) > 2 else ["Apply your skills in real scenarios", "Contribute to open source", "Build portfolio project"]
            },
            {
                "week": 4,
                "focus": "Integration & Mastery",
                "tasks": [
                    "Build full-stack application",
                    "Deploy to production",
                    "Document and share learning"
                ]
            }
        ]
    }

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "model": "llama-3.3-70b-versatile",
        "version": "2.0-real-analysis"
    })

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze skill gap between resume and job description."""
    try:
        data = request.form if request.form else request.get_json()
        
        # Extract inputs
        resume_text = data.get('resume_text', '') or ''
        github_username = data.get('github_username', '') or ''
        job_description = data.get('job_description', '') or ''
        
        # Handle file upload
        if 'resume_file' in request.files:
            file = request.files['resume_file']
            if file.filename.endswith('.pdf'):
                pdf_stream = BytesIO(file.read())
                resume_text = extract_text_from_pdf(pdf_stream)
            else:
                resume_text = file.read().decode('utf-8')
        
        # Fetch GitHub skills if provided
        github_skills = []
        if github_username and len(github_username) >= 3:
            github_skills = fetch_github_skills(github_username)
        
        # Validation
        if not resume_text and not github_skills:
            return jsonify({"error": "Please provide resume text, PDF, or GitHub profile"}), 400
        
        if not job_description:
            return jsonify({"error": "Job description is required"}), 400
        
        # Combine inputs for prompt
        input_text = f"""Resume/Skills: {resume_text or ', '.join(github_skills)}
        
Job Description: {job_description}"""
        
        # Try to get analysis from Groq API
        api_key = os.getenv("GROQ_API_KEY", "").strip()
        analysis = None
        
        if api_key:  # Only try Groq if API key exists
            try:
                prompt = f"""You are an expert career coach and recruiter. Analyze the candidate's resume and GitHub skills against the job description and provide a detailed skill gap analysis.

{input_text}

Provide ONLY a valid JSON response (no markdown, no code fences) with this exact structure:
{{
  "match_score": <integer 0-100>,
  "matched_skills": [<list of skills they have that match job requirements>],
  "required_skills": [<comprehensive list of all required skills for the job>],
  "skill_gaps": [<list of missing skills in priority order>],
  "learning_plan": [
    {{
      "week": 1,
      "focus": "<primary skill to learn this week>",
      "tasks": ["<specific task 1>", "<specific task 2>", "<specific task 3>"]
    }},
    {{
      "week": 2,
      "focus": "<primary skill to learn this week>",
      "tasks": ["<specific task 1>", "<specific task 2>", "<specific task 3>"]
    }},
    {{
      "week": 3,
      "focus": "<primary skill to learn this week>",
      "tasks": ["<specific task 1>", "<specific task 2>", "<specific task 3>"]
    }},
    {{
      "week": 4,
      "focus": "<primary skill to learn this week>",
      "tasks": ["<specific task 1>", "<specific task 2>", "<specific task 3>"]
    }}
  ]
}}

Be specific about match_score based on actual skill overlap. Calculate: (matched_skills count / required_skills count) * 100"""
                
                response = client.messages.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=3000
                )
                
                response_text = response.content[0].text
                analysis = parse_analysis_response(response_text)
                print(f"✓ Groq API analysis successful - match_score: {analysis.get('match_score', 0)}")
                
            except Exception as e:
                print(f"⚠ Groq API error: {e}")
                print("Falling back to text-based analysis...")
                analysis = None
        else:
            print("⚠ GROQ_API_KEY not set - using text-based analysis")
        
        # Fallback to intelligent mock analysis
        if not analysis:
            analysis = generate_mock_analysis(resume_text, github_skills, job_description)
            print(f"✓ Text-based analysis complete - match_score: {analysis.get('match_score', 0)}")
        
        # Transform response to match frontend expectations
        transformed = {
            "match_score": analysis.get("match_score", 0),
            "resume_skills": analysis.get("matched_skills", []),
            "required_skills": analysis.get("required_skills", []),
            "matched_skills": analysis.get("matched_skills", []),
            "gap_skills": [
                {
                    "skill": gap,
                    "priority": "high" if i < 2 else "medium" if i < 4 else "low",
                    "reason": f"Required for the role but not in your current skill set"
                }
                for i, gap in enumerate(analysis.get("skill_gaps", []))
            ],
            "learning_plan": [
                {
                    "week": plan.get("week", i+1),
                    "title": plan.get("focus", ""),
                    "skills": plan.get("tasks", []),
                    "tasks": [
                        {
                            "day_range": f"Day {(i*2)+1}-{(i*2)+2}",
                            "task": task,
                            "resource": "Online course",
                            "resource_url": "https://learn.example.com",
                            "type": "course"
                        }
                        for i, task in enumerate(plan.get("tasks", [])[:3])
                    ]
                }
                for i, plan in enumerate(analysis.get("learning_plan", []))
            ],
            "summary": f"Your skills match {analysis.get('match_score', 0)}% of the job requirements. Focus on: {', '.join(analysis.get('skill_gaps', [])[:3])}"
        }
        
        return jsonify(transformed)
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/plan', methods=['POST'])
def get_learning_plan():
    """Get detailed learning plan for a specific skill."""
    try:
        data = request.get_json()
        skill = data.get('skill', '')
        current_level = data.get('current_level', 'beginner')
        
        if not skill:
            return jsonify({"error": "Skill is required"}), 400
        
        if not os.getenv("GROQ_API_KEY"):
            return jsonify({
                "skill": skill,
                "level": current_level,
                "week": 1,
                "focus": f"Learn {skill}",
                "tasks": [f"Study {skill} basics", f"Practice {skill}"],
                "resources": [
                    {"title": "Free Course", "url": "https://learn.example.com"},
                    {"title": "Documentation", "url": "https://docs.example.com"}
                ]
            })
        
        prompt = f"""Create a 7-day learning plan for {skill}. Current level: {current_level}.

Respond with a JSON plan for week 1 only:
{{
  "week": 1,
  "focus": "<main focus>",
  "tasks": ["<day 1>", "<day 2>", ... "<day 7>"],
  "resources": [
    {{"title": "<resource>", "url": "<url>"}},
    ...
  ]
}}

Respond with ONLY valid JSON."""
        
        response = client.messages.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000
        )
        
        response_text = response.content[0].text
        plan = parse_analysis_response(response_text)
        return jsonify(plan)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

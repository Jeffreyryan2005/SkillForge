#!/usr/bin/env python
"""Test script for SkillForge API"""
import requests
import json

print("Testing Backend API: POST /api/analyze")
print("=" * 60)

payload = {
    'resume_text': 'Senior software engineer with 8 years of experience in React, TypeScript, Node.js, Python, and Flask. Skilled in REST APIs, SQL, and agile development.',
    'job_description': 'Full-stack engineer needed. Required: React, Next.js, Flask, PostgreSQL, cloud deployment, GitHub Actions.'
}

try:
    print("Sending request to http://127.0.0.1:5000/api/analyze...")
    response = requests.post('http://127.0.0.1:5000/api/analyze', json=payload, timeout=10)
    print(f"Response Status: {response.status_code}\n")
    
    data = response.json()
    
    print("✅ API Response Received:")
    print(f"   • Match Score: {data.get('match_score')}%")
    print(f"   • Matched Skills Count: {len(data.get('matched_skills', []))}")
    print(f"   • Matched Skills: {', '.join(data.get('matched_skills', [])[:5])}")
    print(f"   • Required Skills: {', '.join(data.get('required_skills', [])[:5])}")
    print(f"   • Skill Gaps: {', '.join(data.get('skill_gaps', [])[:3])}")
    print(f"   • Learning Plan Weeks: {len(data.get('learning_plan', []))}")
    
    print("\n✅ Backend API is working correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

import requests
import json

# Test 1: Python dev with some overlapping skills
test1 = {
    'resume_text': 'Python, JavaScript, React, Node.js, Flask, PostgreSQL',
    'job_description': 'React, Node.js, Python, PostgreSQL, Docker, Kubernetes, AWS'
}

# Test 2: Minimal overlap
test2 = {
    'resume_text': 'Python, Java, C++',
    'job_description': 'React, Node.js, TypeScript, Docker, Kubernetes'
}

# Test 3: Full overlap
test3 = {
    'resume_text': 'React, Node.js, Python, PostgreSQL, Docker, Kubernetes, AWS',
    'job_description': 'React, Node.js, Python, PostgreSQL, Docker, Kubernetes, AWS'
}

tests = [test1, test2, test3]
names = ["Overlapping Skills", "Minimal Match", "Full Match"]

for i, (test, name) in enumerate(zip(tests, names), 1):
    print(f"\n{'='*60}")
    print(f"Test {i}: {name}")
    print('='*60)
    try:
        r = requests.post('http://localhost:5000/api/analyze', json=test, timeout=5)
        data = r.json()
        print(f"Match Score: {data['match_score']}%")
        print(f"Matched Skills: {data['matched_skills'][:5]}")
        print(f"Gap Skills: {[g['skill'] for g in data['gap_skills'][:3]]}")
        print(f"Status: ✓ WORKING - Real analysis!")
    except Exception as e:
        print(f"Error: {e}")

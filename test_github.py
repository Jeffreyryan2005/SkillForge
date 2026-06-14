import requests

print("Testing GitHub profile analysis...")
print()

test = {
    'github_username': 'Jeffreyryan2005',
    'job_description': 'Senior Full-stack Engineer: React, Node.js, Python, PostgreSQL, Docker, AWS, Kubernetes'
}

print(f"Request: GitHub user '{test['github_username']}'")

try:
    r = requests.post('http://localhost:5000/api/analyze', json=test, timeout=10)
    print(f"Status: {r.status_code}")
    print()
    
    data = r.json()
    
    if r.status_code == 200:
        print("✓ Analysis successful!")
        print(f"  Match Score: {data['match_score']}%")
        print(f"  Matched Skills: {data['matched_skills'][:5]}")
        print(f"  Gap Skills: {[g['skill'] for g in data['gap_skills'][:3]]}")
        print(f"  Summary: {data['summary']}")
    else:
        print("✗ Error:")
        print(f"  {data.get('error', 'Unknown error')}")
        
except Exception as e:
    print(f"✗ Request failed: {e}")

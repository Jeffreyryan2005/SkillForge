import requests

print("Testing invalid GitHub username detection...\n")

tests = [
    ("fakeuser12345678901234567890", "Invalid username"),
    ("nonexistent___user___xyz", "Invalid username"),
    ("Jeffreyryan2005", "Valid username"),
]

for username, description in tests:
    print(f"Test: {description}")
    print(f"  Username: {username}")
    
    test = {
        'github_username': username,
        'job_description': 'React, Node.js, Python, Docker, AWS'
    }
    
    try:
        r = requests.post('http://localhost:5000/api/analyze', json=test, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            print(f"  Result: ✓ Match Score: {data['match_score']}%")
        else:
            data = r.json()
            print(f"  Result: ✗ Error (Status {r.status_code})")
            print(f"  Message: {data.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"  Result: ✗ Request failed: {e}")
    
    print()

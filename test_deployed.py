import requests
import time

print('Testing deployed backend at: https://skillforge-wngd.onrender.com')
print('Waiting for deployment... (Render can take 2-5 minutes)\n')

test = {
    'resume_text': 'Python, React, Node.js, Flask, PostgreSQL, 8 years experience',
    'job_description': 'Senior Full-stack Engineer: React, Node.js, Python, PostgreSQL, Docker, AWS, Kubernetes'
}

for attempt in range(12):  # Try for 2 minutes
    try:
        r = requests.post('https://skillforge-wngd.onrender.com/api/analyze', json=test, timeout=10)
        if r.status_code == 200:
            data = r.json()
            print('✓ Deployment successful!')
            print(f'  Match Score: {data["match_score"]}%')
            print(f'  Matched Skills: {data["matched_skills"][:5]}')
            print(f'  Gap Skills: {[g["skill"] for g in data["gap_skills"][:3]]}')
            break
        else:
            print(f'  Attempt {attempt+1}: Server responded with {r.status_code}')
    except requests.exceptions.ConnectionError:
        print(f'  Attempt {attempt+1}/12: Waiting for deployment ({attempt*10}s elapsed)...')
    except Exception as e:
        print(f'  Attempt {attempt+1}: {str(e)[:50]}')
    
    if attempt < 11:
        time.sleep(10)
